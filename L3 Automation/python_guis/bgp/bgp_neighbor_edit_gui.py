import ipaddress
import threading
import tkinter as tk
from tkinter import messagebox

from resources.devices.Router import Router
from python_guis.gui_resources import config
from resources.user.User import User
from resources.connect_frontend_with_backend.frontend_backend_functions import update_bgp_neighbor
from resources.routing_protocols.bgp.BGPNeighbor import BGPNeighbor


class BGPNeighborEditGUI:
    def __init__(self, main_gui, bgp_neighbors_gui, router: Router, user: User, neighbor: BGPNeighbor):
        self.hostname = router.name
        self.bgp_neighbors_gui = bgp_neighbors_gui

        root = tk.Toplevel()
        # ######## WINDOW PARAMETERS ######## #
        # title
        root.title(config.APPNAME + ' ' + config.VERSION + ' ' + self.hostname + ' Edit BGP Neighbor')

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

        lblIpAddress = tk.Label(root, text='IP address:')
        lblIpAddress.grid(column=0, row=0)

        ip = neighbor.ip_address
        ip = ip.split('.')

        networkFrame = tk.Frame(root)
        entryIPNetworkFirst = tk.Entry(networkFrame, width=10)
        entryIPNetworkFirst.pack(side='left')
        entryIPNetworkFirst.insert(0, ip[0])
        labelDot1 = tk.Label(networkFrame, text='.')
        labelDot1.pack(side='left')

        entryIPNetworkSecond = tk.Entry(networkFrame, width=10)
        entryIPNetworkSecond.pack(side='left')
        entryIPNetworkSecond.insert(0, ip[1])
        labelDot2 = tk.Label(networkFrame, text='.')
        labelDot2.pack(side='left')

        entryIPNetworkThird = tk.Entry(networkFrame, width=10)
        entryIPNetworkThird.pack(side='left')
        entryIPNetworkThird.insert(0, ip[2])
        labelDot3 = tk.Label(networkFrame, text='.')
        labelDot3.pack(side='left')

        entryIPNetworkFourth = tk.Entry(networkFrame, width=10)
        entryIPNetworkFourth.pack(side='left')
        entryIPNetworkFourth.insert(0, ip[3])

        networkFrame.grid(column=1, row=0)

        lblRemoteAS = tk.Label(root, text='Remote AS:')
        lblRemoteAS.grid(column=0, row=1)
        entryRemoteAS = tk.Entry(root, width=5)
        entryRemoteAS.grid(column=1, row=1)
        entryRemoteAS.insert(0, str(neighbor.remote_as))

        lblEBGPMultihop = tk.Label(root, text='EBGP Multihop:')
        lblEBGPMultihop.grid(column=0, row=2)
        entryEBGPMultihop = tk.Entry(root)
        entryEBGPMultihop.grid(column=1, row=2)
        entryEBGPMultihop.insert(0, str(neighbor.ebgp_multihop))

        lblNextHopSelf = tk.Label(root, text='Next hop self:')
        lblNextHopSelf.grid(column=0, row=3)
        varNextHopSelf = tk.BooleanVar(root)
        chckbtnNextHopSelf = tk.Checkbutton(root, variable=varNextHopSelf)
        chckbtnNextHopSelf.grid(column=1, row=3)
        chckbtnNextHopSelf.select() if neighbor.next_hop_self else chckbtnNextHopSelf.deselect()

        lblShutdown = tk.Label(root, text='Shutdown')
        lblShutdown.grid(column=0, row=4)
        varShutdown = tk.BooleanVar(root)
        chckbtnShutdown = tk.Checkbutton(root, variable=varShutdown)
        chckbtnShutdown.grid(column=1, row=4)
        chckbtnShutdown.select() if neighbor.shutdown else chckbtnShutdown.deselect()

        lblKeepAliveTimer = tk.Label(root, text='Keep alive timer:')
        lblKeepAliveTimer.grid(column=0, row=5)
        entryKeepAliveTimer = tk.Entry(root)
        entryKeepAliveTimer.grid(column=1, row=5)
        entryKeepAliveTimer.insert(0, str(neighbor.timers.keep_alive))

        lblHoldTimeTimer = tk.Label(root, text='Hold time timer:')
        lblHoldTimeTimer.grid(column=0, row=6)
        entryHoldTimeTimer = tk.Entry(root)
        entryHoldTimeTimer.grid(column=1, row=6)
        entryHoldTimeTimer.insert(0, str(neighbor.timers.hold_time))

        def get_ip() -> str:
            try:
                return (entryIPNetworkFirst.get() + '.' + entryIPNetworkSecond.get() + '.' +
                        entryIPNetworkThird.get() + '.' + entryIPNetworkFourth.get())
            except ValueError:
                messagebox.showerror('Error', 'Incorrect ip format.', parent=root)

        def clean_entries() -> None:
            ip_entries = [entryIPNetworkFirst, entryIPNetworkSecond, entryIPNetworkThird,
                          entryIPNetworkFourth]
            for entry in ip_entries:
                entry.delete(0, 'end')
            entryRemoteAS.delete(0, 'end')
            entryEBGPMultihop.delete(0, 'end')
            entryKeepAliveTimer.delete(0, 'end')
            entryHoldTimeTimer.delete(0, 'end')

        def validate_neighbor() -> bool:
            ip_entries = [entryIPNetworkFirst, entryIPNetworkSecond, entryIPNetworkThird, entryIPNetworkFourth]
            neighbor_id = ''
            for entry in ip_entries:
                value = entry.get()
                neighbor_id += value + '.'
            neighbor_id = neighbor_id.rstrip('.')
            try:
                ipaddress.ip_address(neighbor_id)
            except ValueError:
                messagebox.showerror('Error', 'Incorrect IP Format', parent=root)
                for entry in ip_entries:
                    entry.delete(0, 'end')
                return False

            value = entryRemoteAS.get()
            if not value.isdigit() or not (0 <= int(value) <= 4294967295):
                messagebox.showerror('Error', 'Incorrect remote AS value.', parent=root)
                entryRemoteAS.delete(0, 'end')
                return False
            value = entryEBGPMultihop.get()
            if not value.isdigit() or not (0 <= int(value) <= 255):
                messagebox.showerror('Error', 'Incorrect EBGP Multihop value.'
                                              'It must be between 0 and 255.', parent=root)
                entryEBGPMultihop.delete(0, 'end')
                return False
            value = entryKeepAliveTimer.get()
            if not value.isdigit() or not (0 <= int(value) <= 65535):
                messagebox.showerror('Error', 'Incorrect Keep Alive Timer.'
                                              ' It must be between 0 and 65535 seconds.', parent=root)
                entryKeepAliveTimer.delete(0, 'end')
                return False
            value = entryHoldTimeTimer.get()
            if not value.isdigit() or not (3 <= int(value) <= 65535):
                messagebox.showerror('Error', 'Incorrect Hold Time Timer.'
                                              ' It must be between 3 and 65535 seconds.', parent=root)
                entryHoldTimeTimer.delete(0, 'end')
                return False
            return True

        def apply_neighbor():
            if validate_neighbor():
                ip = get_ip()
                remote_as = int(entryRemoteAS.get())
                ebgpMultihop = int(entryEBGPMultihop.get())
                nextHopSelf = varNextHopSelf.get()
                shutdown = varShutdown.get()
                keepAliveTimer = int(entryKeepAliveTimer.get())
                holdTimeTimer = int(entryHoldTimeTimer.get())

                threading.Thread(target=update_bgp_neighbor,
                                 args=(main_gui, self.bgp_neighbors_gui, router, user, ip, remote_as, ebgpMultihop,
                                       nextHopSelf, shutdown, keepAliveTimer, holdTimeTimer)).start()
                clean_entries()

        btnFrame = tk.Frame(root)
        btnApply = tk.Button(btnFrame, text='Apply', command=apply_neighbor)
        btnApply.pack(pady=5)
        btnQuit = tk.Button(btnFrame, text='Quit', command=root.destroy)
        btnQuit.pack()
        btnFrame.grid(column=0, row=7, columnspan=2)

        root.mainloop()
