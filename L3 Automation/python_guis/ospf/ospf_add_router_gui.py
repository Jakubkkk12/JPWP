import ipaddress
import threading
import tkinter as tk
from tkinter import messagebox

from python_guis.gui_resources import config
from resources.connect_frontend_with_backend.frontend_backend_functions import enable_ospf
from resources.routing_protocols.Network import Network
from resources.routing_protocols.ospf.OSPFArea import OSPFArea
from resources.routing_protocols.ospf.OSPFInformation import OSPFInformation
from resources import constants
from resources.user.User import User


class OSPFAddRouterGUI:
    def __init__(self, main_gui, user: User):
        self.main_gui = main_gui

        root = tk.Toplevel()
        # ######## WINDOW PARAMETERS ######## #
        # title
        root.title(config.APPNAME + ' ' + config.VERSION + ' ' + ' OSPF Add router')

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

        root.minsize(300, 500)

        root.columnconfigure(0, weight=1)
        root.columnconfigure(1, weight=1)

        # Components
        devices = main_gui.get_devices()
        ospfOptions = []
        for k, router in devices.items():
            if router.ospf is None:
                ospfOptions.append(router.name)
        if len(ospfOptions) == 0:
            messagebox.showerror('Error', 'All routers have OSPF configured', parent=root)
            root.destroy()
            return
        lblHostname = tk.Label(root, text='Hostname:')
        lblHostname.grid(row=0, column=0)

        varHostname = tk.StringVar(root)
        optionMenuHostname = tk.OptionMenu(root, varHostname, *ospfOptions)
        optionMenuHostname.grid(row=0, column=1)

        lblRouterId = tk.Label(root, text='Router ID:')
        lblRouterId.grid(row=1, column=0)

        frameRouterId = tk.Frame(root)
        frameRouterId.grid(row=1, column=1)
        entryRouterIdFirst = tk.Entry(frameRouterId, width=3)
        entryRouterIdFirst.pack(side=tk.LEFT)
        lblDot1 = tk.Label(frameRouterId, text='.')
        lblDot1.pack(side=tk.LEFT)
        entryRouterIdSecond = tk.Entry(frameRouterId, width=3)
        entryRouterIdSecond.pack(side=tk.LEFT)
        lblDot2 = tk.Label(frameRouterId, text='.')
        lblDot2.pack(side=tk.LEFT)
        entryRouterIdThird = tk.Entry(frameRouterId, width=3)
        entryRouterIdThird.pack(side=tk.LEFT)
        lblDot3 = tk.Label(frameRouterId, text='.')
        lblDot3.pack(side=tk.LEFT)
        entryRouterIdFourth = tk.Entry(frameRouterId, width=3)
        entryRouterIdFourth.pack(side=tk.LEFT)

        lblAutoCostReferenceBandwidth = tk.Label(root, text='Auto-cost reference bandwidth:')
        lblAutoCostReferenceBandwidth.grid(row=2, column=0)
        entryAutoCostReferenceBandwidth = tk.Entry(root)
        entryAutoCostReferenceBandwidth.grid(row=2, column=1)
        entryAutoCostReferenceBandwidth.insert(0, '10000')

        lblDefaultInformationOriginate = tk.Label(root, text='Default information originate:')
        lblDefaultInformationOriginate.grid(row=3, column=0)
        varDefaultInformationOriginate = tk.BooleanVar()
        varDefaultInformationOriginate.set(False)
        checkDefaultInformationOriginate = tk.Checkbutton(root, variable=varDefaultInformationOriginate)
        checkDefaultInformationOriginate.grid(row=3, column=1)

        lblDefaultMetricOfRedistributedRoutes = tk.Label(root, text='Default metric of redistributed routes:')
        lblDefaultMetricOfRedistributedRoutes.grid(row=4, column=0)
        entryDefaultMetricOfRedistributedRoutes = tk.Entry(root)
        entryDefaultMetricOfRedistributedRoutes.grid(row=4, column=1)
        entryDefaultMetricOfRedistributedRoutes.insert(0, '1')

        lblDistance = tk.Label(root, text='Distance:')
        lblDistance.grid(row=5, column=0)
        entryDistance = tk.Entry(root)
        entryDistance.grid(row=5, column=1)
        entryDistance.insert(0, '1')

        lblMaximumPaths = tk.Label(root, text='Maximum paths:')
        lblMaximumPaths.grid(row=6, column=0)
        entryMaximumPaths = tk.Entry(root)
        entryMaximumPaths.grid(row=6, column=1)
        entryMaximumPaths.insert(0, '1')

        lblPassiveInterface = tk.Label(root, text='Passive interface:')
        lblPassiveInterface.grid(row=7, column=0)
        varPassiveInterface = tk.BooleanVar()
        varPassiveInterface.set(False)
        checkPassiveInterface = tk.Checkbutton(root, variable=varPassiveInterface)
        checkPassiveInterface.grid(row=7, column=1)

        lblAreaId = tk.Label(root, text='Area ID:')
        lblAreaId.grid(row=8, column=0)
        entryAreaId = tk.Entry(root)
        entryAreaId.grid(row=8, column=1)

        lblNetwork = tk.Label(root, text='Network:')
        lblNetwork.grid(row=9, column=0)
        frameNetwork = tk.Frame(root)
        frameNetwork.grid(row=9, column=1)
        entryNetworkFirst = tk.Entry(frameNetwork, width=3)
        entryNetworkFirst.pack(side=tk.LEFT)
        lblDot1 = tk.Label(frameNetwork, text='.')
        lblDot1.pack(side=tk.LEFT)
        entryNetworkSecond = tk.Entry(frameNetwork, width=3)
        entryNetworkSecond.pack(side=tk.LEFT)
        lblDot2 = tk.Label(frameNetwork, text='.')
        lblDot2.pack(side=tk.LEFT)
        entryNetworkThird = tk.Entry(frameNetwork, width=3)
        entryNetworkThird.pack(side=tk.LEFT)
        lblDot3 = tk.Label(frameNetwork, text='.')
        lblDot3.pack(side=tk.LEFT)
        entryNetworkFourth = tk.Entry(frameNetwork, width=3)
        entryNetworkFourth.pack(side=tk.LEFT)

        lblMask = tk.Label(root, text='Mask:')
        lblMask.grid(row=10, column=0)
        entryMask = tk.Entry(root)
        entryMask.grid(row=10, column=1)

        lblIsAuthenticationMessageDigest = tk.Label(root, text='Is authentication message digest:')
        lblIsAuthenticationMessageDigest.grid(row=11, column=0)
        varIsAuthenticationMessageDigest = tk.BooleanVar()
        varIsAuthenticationMessageDigest.set(False)
        checkIsAuthenticationMessageDigest = tk.Checkbutton(root, variable=varIsAuthenticationMessageDigest)
        checkIsAuthenticationMessageDigest.grid(row=11, column=1)

        lblType = tk.Label(root, text='Type:')
        lblType.grid(row=12, column=0)
        varType = tk.StringVar()
        typeOptions = ['standard', 'stub', 'nssa']
        varType.set(typeOptions[1])
        optionMenuType = tk.OptionMenu(root, varType, *typeOptions)
        optionMenuType.grid(row=12, column=1)

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
            if not entryAutoCostReferenceBandwidth.get().isdigit() or not (
                    1 <= int(entryAutoCostReferenceBandwidth.get()) <= 4294967):
                messagebox.showerror('Error',
                                     'Auto-cost reference bandwidth must be a an integer between 1 and 4294967.',
                                     parent=root)
                entryAutoCostReferenceBandwidth.delete(0, tk.END)
                return False
            if (not entryDefaultMetricOfRedistributedRoutes.get().isdigit() or not
            (1 <= int(entryDefaultMetricOfRedistributedRoutes.get()) <= 16777214)):
                messagebox.showerror('Error', 'Default metric of redistributed routes must be a an '
                                              'integer between 1 and 16777214.', parent=root)
                entryDefaultMetricOfRedistributedRoutes.delete(0, tk.END)
                return False
            if not entryMaximumPaths.get().isdigit() or not (1 <= int(entryMaximumPaths.get()) <= 16):
                messagebox.showerror('Error', 'Maximum paths must be a an integer between 1 and 16.',
                                     parent=root)
                entryMaximumPaths.delete(0, tk.END)
                return False
            if not entryAreaId.get().isdigit() or not (0 <= int(entryAreaId.get()) <= 4294967295):
                messagebox.showerror('Error', 'Area ID must be a an integer between 0 and 4294967295.',
                                     parent=root)
                entryAreaId.delete(0, tk.END)
                return False
            if varType == '':
                messagebox.showerror('Error', 'Type is required.', parent=root)
                return False
            return True

        def add_router():
            if validate_router():
                router = main_gui.get_router(varHostname.get())

                threading.Thread(target=enable_ospf,
                                 args=(main_gui, router, user, get_router_id(),
                                       int(entryAutoCostReferenceBandwidth.get()), varDefaultInformationOriginate.get(),
                                       int(entryDefaultMetricOfRedistributedRoutes.get()), int(entryDistance.get()),
                                       int(entryMaximumPaths.get()), varPassiveInterface.get(), entryAreaId.get(),
                                       [[get_network(), constants.WILDCARD_MASK[int(entryMask.get())]]],
                                       varIsAuthenticationMessageDigest.get(), varType.get(),)).start()

                root.destroy()

        btnFrame = tk.Frame(root)
        btnAdd = tk.Button(btnFrame, text='Add', command=add_router, width=15)
        btnAdd.pack()
        btnCancel = tk.Button(btnFrame, text='Cancel', command=root.destroy, width=15)
        btnCancel.pack()
        btnFrame.grid(row=13, column=1)

        root.mainloop()
