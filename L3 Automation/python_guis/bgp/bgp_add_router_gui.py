import ipaddress
import threading
import tkinter as tk
from tkinter import messagebox

from python_guis.gui_resources import config
from resources.connect_frontend_with_backend.frontend_backend_functions import enable_bgp
from resources.routing_protocols.Network import Network
from resources.routing_protocols.bgp.BGPInformation import BGPInformation
from resources.routing_protocols.bgp.BGPTimers import BGPTimers
from resources.user.User import User


class BGPAddRouterGUI:
    def __init__(self, main_gui, user: User):
        self.main_gui = main_gui

        root = tk.Toplevel()
        # ######## WINDOW PARAMETERS ######## #
        # title
        root.title(config.APPNAME + ' ' + config.VERSION + ' ' + ' BGP Add router')

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

        root.columnconfigure(0, weight=1)
        root.columnconfigure(1, weight=1)

        # Components
        devices = main_gui.get_devices()
        bgpOptions = []
        for k, router in devices.items():
            if router.bgp is None:
                bgpOptions.append(router.name)
        if len(bgpOptions) == 0:
            messagebox.showerror('Error', 'All routers have BGP configured', parent=root)
            root.destroy()
            return
        lblHostname = tk.Label(root, text='Hostname:')
        lblHostname.grid(row=0, column=0)

        varHostname = tk.StringVar(root)
        optionMenuHostname = tk.OptionMenu(root, varHostname, *bgpOptions)
        optionMenuHostname.grid(row=0, column=1)

        lblAS = tk.Label(root, text='AS:')
        lblAS.grid(row=2, column=0)
        entryAS = tk.Entry(root)
        entryAS.grid(row=2, column=1)

        lblRouterId = tk.Label(root, text='Router ID:')
        lblRouterId.grid(row=3, column=0)

        frameRouterId = tk.Frame(root)
        entryRouterIdFirst = tk.Entry(frameRouterId, width=5)
        entryRouterIdFirst.pack(side=tk.LEFT)
        lblDot1 = tk.Label(frameRouterId, text='.')
        lblDot1.pack(side=tk.LEFT)
        entryRouterIdSecond = tk.Entry(frameRouterId, width=5)
        entryRouterIdSecond.pack(side=tk.LEFT)
        lblDot2 = tk.Label(frameRouterId, text='.')
        lblDot2.pack(side=tk.LEFT)
        entryRouterIdThird = tk.Entry(frameRouterId, width=5)
        entryRouterIdThird.pack(side=tk.LEFT)
        lblDot3 = tk.Label(frameRouterId, text='.')
        lblDot3.pack(side=tk.LEFT)
        entryRouterIdFourth = tk.Entry(frameRouterId, width=5)
        entryRouterIdFourth.pack(side=tk.LEFT)
        frameRouterId.grid(row=3, column=1)

        lblDefaultInformationOriginate = tk.Label(root, text='Default information originate:')
        lblDefaultInformationOriginate.grid(row=4, column=0)
        varDefaultInformationOriginate = tk.BooleanVar()
        varDefaultInformationOriginate.set(False)
        checkDefaultInformationOriginate = tk.Checkbutton(root, variable=varDefaultInformationOriginate)
        checkDefaultInformationOriginate.grid(row=4, column=1)

        lblDefaultMetricOfRedistributedRoutes = tk.Label(root, text='Default metric of redistributed routes:')
        lblDefaultMetricOfRedistributedRoutes.grid(row=5, column=0)
        entryDefaultMetricOfRedistributedRoutes = tk.Entry(root)
        entryDefaultMetricOfRedistributedRoutes.grid(row=5, column=1)
        entryDefaultMetricOfRedistributedRoutes.insert(0, '1')

        lblKeepAliveTimer = tk.Label(root, text='Keep alive timer:')
        lblKeepAliveTimer.grid(row=6, column=0)
        entryKeepAliveTimer = tk.Entry(root)
        entryKeepAliveTimer.grid(row=6, column=1)
        entryKeepAliveTimer.insert(0, '60')

        lblHoldTimeTimer = tk.Label(root, text='Hold time timer:')
        lblHoldTimeTimer.grid(row=7, column=0)
        entryHoldTimeTimer = tk.Entry(root)
        entryHoldTimeTimer.grid(row=7, column=1)
        entryHoldTimeTimer.insert(0, '180')

        lblNetwork = tk.Label(root, text='Network:')
        lblNetwork.grid(row=8, column=0)
        frameNetwork = tk.Frame(root)
        frameNetwork.grid(row=8, column=1)
        entryNetworkFirst = tk.Entry(frameNetwork, width=5)
        entryNetworkFirst.pack(side=tk.LEFT)
        lblDot1 = tk.Label(frameNetwork, text='.')
        lblDot1.pack(side=tk.LEFT)
        entryNetworkSecond = tk.Entry(frameNetwork, width=5)
        entryNetworkSecond.pack(side=tk.LEFT)
        lblDot2 = tk.Label(frameNetwork, text='.')
        lblDot2.pack(side=tk.LEFT)
        entryNetworkThird = tk.Entry(frameNetwork, width=5)
        entryNetworkThird.pack(side=tk.LEFT)
        lblDot3 = tk.Label(frameNetwork, text='.')
        lblDot3.pack(side=tk.LEFT)
        entryNetworkFourth = tk.Entry(frameNetwork, width=5)
        entryNetworkFourth.pack(side=tk.LEFT)

        lblMask = tk.Label(root, text='Mask:')
        lblMask.grid(row=9, column=0)
        entryMask = tk.Entry(root)
        entryMask.grid(row=9, column=1)

        def get_router_id() -> str:
            try:
                router_id = (entryRouterIdFirst.get() + '.' + entryRouterIdSecond.get() + '.' + entryRouterIdThird.get()
                             + '.' + entryRouterIdFourth.get())
                ipaddress.ip_address(router_id)
                return router_id
            except ValueError:
                messagebox.showerror('Error', 'Invalid router id', parent=root)
                entryRouterIdFirst.delete(0, tk.END)
                entryRouterIdSecond.delete(0, tk.END)
                entryRouterIdThird.delete(0, tk.END)
                entryRouterIdFourth.delete(0, tk.END)

        def get_network() -> str:
            try:
                network = (entryNetworkFirst.get() + '.' + entryNetworkSecond.get() + '.' + entryNetworkThird.get() +
                           '.' + entryNetworkFourth.get())
                mask = entryMask.get()
                ipaddress.ip_network(network + '/' + mask)
                return network
            except ValueError:
                messagebox.showerror('Error', 'Invalid network', parent=root)
                entryNetworkFirst.delete(0, tk.END)
                entryNetworkSecond.delete(0, tk.END)
                entryNetworkThird.delete(0, tk.END)
                entryNetworkFourth.delete(0, tk.END)
                entryMask.delete(0, tk.END)

        def validate_router() -> bool:
            if varHostname.get() == '':
                messagebox.showerror('Error', 'Hostname is required.', parent=root)
                return False
            if not entryDefaultMetricOfRedistributedRoutes.get().isdigit() or not 0 <= int(
                    entryDefaultMetricOfRedistributedRoutes.get()) <= 16777215:
                messagebox.showerror('Error', 'Invalid default metric of redistributed routes.', parent=root)
                entryDefaultMetricOfRedistributedRoutes.delete(0, tk.END)
                return False
            if not entryKeepAliveTimer.get().isdigit() or not 0 <= int(entryKeepAliveTimer.get()) <= 65535:
                messagebox.showerror('Error', 'Invalid keep alive timer.', parent=root)
                entryKeepAliveTimer.delete(0, tk.END)
                return False
            if not entryHoldTimeTimer.get().isdigit() or not 0 <= int(entryHoldTimeTimer.get()) <= 65535:
                messagebox.showerror('Error', 'Invalid hold time timer.', parent=root)
                entryHoldTimeTimer.delete(0, tk.END)
                return False
            return True

        def add_router():
            if validate_router():
                router = main_gui.get_router(varHostname.get())
                threading.Thread(target=enable_bgp,
                                 args=(main_gui, router, user, int(entryAS.get()), get_router_id(),
                                       varDefaultInformationOriginate.get(),
                                       int(entryDefaultMetricOfRedistributedRoutes.get()),
                                       int(entryKeepAliveTimer.get()), int(entryHoldTimeTimer.get()),
                                       [[get_network(), int(entryMask.get())]])).start()
                root.destroy()

        btnFrame = tk.Frame(root)
        btnAdd = tk.Button(btnFrame, text='Add', command=add_router, width=15)
        btnAdd.pack()
        btnCancel = tk.Button(btnFrame, text='Cancel', command=root.destroy, width=15)
        btnCancel.pack()
        btnFrame.grid(row=13, column=1)

        root.mainloop()
