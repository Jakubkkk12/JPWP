import tkinter as tk
from tkinter import messagebox

from resources.devices.Router import Router
from gui_resources import config
from resources.routing_protocols.Network import Network
from resources.routing_protocols.StaticRoute import StaticRoute


class StaticRouteAddGUI:
    def __init__(self, router: Router, static_routes_gui):
        self.hostname = router.name
        self.int_name = ''
        self.selected_router_iid = None
        self.static_routes_gui = static_routes_gui

        root = tk.Toplevel()
        # ######## WINDOW PARAMETERS ######## #
        # title
        root.title(config.APPNAME + ' ' + config.VERSION + ' ' + self.hostname + ' Add Route')

        # window icon, using conversion to iso, cause tkinter doesn't accept jpg
        icon = tk.PhotoImage(file=config.WINDOW_ICON_PATH)
        root.wm_iconphoto(False, icon)

        # size parameters
        width = 400
        height = 300
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=True, height=True)

        root.minsize(300, 300)

        lblDestination = tk.Label(root, text='Destination:')

        destinationFrame = tk.Frame(root)
        entryIPDestinationFirst = tk.Entry(destinationFrame, width=10)
        entryIPDestinationFirst.pack(side='left')
        labelDot1 = tk.Label(destinationFrame, text='.')
        labelDot1.pack(side='left')

        entryIPDestinationSecond = tk.Entry(destinationFrame, width=10)
        entryIPDestinationSecond.pack(side='left')
        labelDot2 = tk.Label(destinationFrame, text='.')
        labelDot2.pack(side='left')

        entryIPDestinationThird = tk.Entry(destinationFrame, width=10)
        entryIPDestinationThird.pack(side='left')
        labelDot3 = tk.Label(destinationFrame, text='.')
        labelDot3.pack(side='left')

        entryIPDestinationFourth = tk.Entry(destinationFrame, width=10)
        entryIPDestinationFourth.pack(side='left')

        lblMask = tk.Label(root, text='Mask:')
        entryMask = tk.Entry(root, width=5)

        lblNextHop = tk.Label(root, text='Next hop:')

        nexthopFrame = tk.Frame(root)
        entryIPNextHopFirst = tk.Entry(nexthopFrame, width=10)
        entryIPNextHopFirst.pack(side='left')
        labelDot1 = tk.Label(nexthopFrame, text='.')
        labelDot1.pack(side='left')

        entryIPNextHopSecond = tk.Entry(nexthopFrame, width=10)
        entryIPNextHopSecond.pack(side='left')
        labelDot2 = tk.Label(nexthopFrame, text='.')
        labelDot2.pack(side='left')

        entryIPNextHopThird = tk.Entry(nexthopFrame, width=10)
        entryIPNextHopThird.pack(side='left')
        labelDot3 = tk.Label(nexthopFrame, text='.')
        labelDot3.pack(side='left')

        entryIPNextHopFourth = tk.Entry(nexthopFrame, width=10)
        entryIPNextHopFourth.pack(side='left')

        lblDestination.pack()
        destinationFrame.pack()
        lblMask.pack()
        entryMask.pack()
        lblNextHop.pack()
        nexthopFrame.pack()


        interfaceSelectFrame = tk.Frame(root)
        lblInterface = tk.Label(interfaceSelectFrame, text='Interface (optional):')
        lblInterface.pack(side='left')

        interfaceVariable = tk.StringVar(root, '-')
        interfaces = []
        for k, interface in router.interfaces.items():
            interfaces.append(interface.name)
        interfacesMenu = tk.OptionMenu(interfaceSelectFrame, interfaceVariable, *interfaces)
        interfacesMenu.pack(side='right')

        interfaceSelectFrame.pack()

        distanceFrame = tk.Frame(root)
        lblDistance = tk.Label(distanceFrame, text='Distance (optional):')
        lblDistance.pack(side='left')
        entryDistance = tk.Entry(distanceFrame, width=10)
        entryDistance.pack(side='right')
        entryDistance.insert(0, '1')
        distanceFrame.pack()
        def get_destination() -> str:
            return (entryIPDestinationFirst.get() + '.' + entryIPDestinationSecond.get() + '.' +
                    entryIPDestinationThird.get() + '.' + entryIPDestinationFourth.get())

        def get_mask() -> int:
            return int(entryMask.get())

        def get_next_hop() -> str:
            return (entryIPNextHopFirst.get() + '.' + entryIPNextHopSecond.get() + '.' +
                    entryIPNextHopThird.get() + '.' + entryIPNextHopFourth.get())

        def get_distance() -> int:
            return int(entryDistance.get())

        def validate_route() -> bool:
            if interfaceVariable.get() == '-':
                ip_entries = [entryIPDestinationFirst, entryIPDestinationSecond, entryIPDestinationThird,
                              entryIPDestinationFourth,
                              entryIPNextHopFirst, entryIPNextHopSecond, entryIPNextHopThird, entryIPNextHopFourth]
                for entry in ip_entries:
                    value = entry.get()
                    if not value.isdigit() or not (0 <= int(value) <= 255):
                        messagebox.showerror('Error', 'Incorrect IP Format', parent=root)
                        for entry in ip_entries:
                            entry.delete(0, 'end')
                        return False
                try:
                    if int(entryIPDestinationFirst.get()) == 0 or int(entryIPNextHopFirst.get()) == 0:
                        messagebox.showerror('Error', 'Incorrect IP Format', parent=root)
                        for entry in ip_entries:
                            entry.delete(0, 'end')
                        return False
                except ValueError:
                    return False

                mask_value = entryMask.get()
                if not mask_value.isdigit() or not (0 <= int(mask_value) <= 32):
                    messagebox.showerror('Error', 'Incorrect Mask Value', parent=root)
                    entryMask.delete(0, 'end')
                    return False
                if not entryDistance.get().isdigit() or not (1 <= int(entryDistance.get()) <= 255):
                    messagebox.showerror('Error', 'Incorrect distance value', parent=root)
                    entryDistance.delete(0, 'end')
                return True
            else:
                ip_entries = [entryIPDestinationFirst, entryIPDestinationSecond, entryIPDestinationThird,
                              entryIPDestinationFourth]
                for entry in ip_entries:
                    value = entry.get()
                    if not value.isdigit() or not (0 <= int(value) <= 255):
                        messagebox.showerror('Error', 'Incorrect IP Format', parent=root)
                        for entry in ip_entries:
                            entry.delete(0, 'end')
                        return False
                return True

        def clean_entries() -> None:
            ip_entries = [entryIPDestinationFirst, entryIPDestinationSecond, entryIPDestinationThird,
                          entryIPDestinationFourth,
                          entryIPNextHopFirst, entryIPNextHopSecond, entryIPNextHopThird, entryIPNextHopFourth]
            for entry in ip_entries:
                entry.delete(0, 'end')

            entryMask.delete(0, 'end')

        def apply_route():
            if validate_route():
                destination = get_destination()
                mask = get_mask()
                next_hop = get_next_hop()
                int_name = interfaceVariable.get()
                distance = get_distance()

                if int_name == '-':
                    staticroute = StaticRoute(network=Network(network=destination, mask=mask),
                                              next_hop=next_hop,
                                              interface='',
                                              distance=distance)
                    clean_entries()
                    messagebox.showinfo('Route Added', 'Route Added', parent=root)
                    self.static_routes_gui.insert_route(staticroute)
                else:
                    staticroute = StaticRoute(network=Network(network=destination, mask=mask),
                                              next_hop='',
                                              interface=int_name,
                                              distance=distance)
                    clean_entries()
                    messagebox.showinfo('Route Added', 'Route Added', parent=root)
                    self.static_routes_gui.insert_route(staticroute)

        btnApply = tk.Button(root, text='Apply', command=apply_route)
        btnApply.pack(pady=5)
        btnQuit = tk.Button(root, text='Quit', command=root.destroy)
        btnQuit.pack()

        root.mainloop()
