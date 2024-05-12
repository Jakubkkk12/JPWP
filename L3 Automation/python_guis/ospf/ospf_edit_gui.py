import ipaddress
import threading
import tkinter as tk
from tkinter import messagebox

from python_guis.gui_resources import config
from resources.connect_frontend_with_backend.frontend_backend_functions import update_ospf
from resources.devices.Router import Router
from resources.user.User import User


class OSPFEditGUI:
    def __init__(self, main_gui, router: Router, user: User):
        self.main_gui = main_gui
        self.router = router

        root = tk.Toplevel()
        # ######## WINDOW PARAMETERS ######## #
        # title
        root.title(config.APPNAME + ' ' + config.VERSION + ' ' + ' Edit OSPF')

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

        router_id = router.ospf.router_id.split('.')
        entryRouterIdFirst.insert(0, router_id[0])
        entryRouterIdSecond.insert(0, router_id[1])
        entryRouterIdThird.insert(0, router_id[2])
        entryRouterIdFourth.insert(0, router_id[3])

        lblAutoCostReferenceBandwidth = tk.Label(root, text='Auto-cost reference bandwidth:')
        lblAutoCostReferenceBandwidth.grid(row=2, column=0)
        entryAutoCostReferenceBandwidth = tk.Entry(root)
        entryAutoCostReferenceBandwidth.grid(row=2, column=1)
        entryAutoCostReferenceBandwidth.insert(0, str(router.ospf.auto_cost_reference_bandwidth))

        lblDefaultInformationOriginate = tk.Label(root, text='Default information originate:')
        lblDefaultInformationOriginate.grid(row=3, column=0)
        varDefaultInformationOriginate = tk.BooleanVar()
        varDefaultInformationOriginate.set(router.ospf.default_information_originate)
        checkDefaultInformationOriginate = tk.Checkbutton(root, variable=varDefaultInformationOriginate)
        checkDefaultInformationOriginate.grid(row=3, column=1)

        lblDefaultMetricOfRedistributedRoutes = tk.Label(root, text='Default metric of redistributed routes:')
        lblDefaultMetricOfRedistributedRoutes.grid(row=4, column=0)
        entryDefaultMetricOfRedistributedRoutes = tk.Entry(root)
        entryDefaultMetricOfRedistributedRoutes.grid(row=4, column=1)
        entryDefaultMetricOfRedistributedRoutes.insert(0, str(router.ospf.default_metric_of_redistributed_routes))

        lblDistance = tk.Label(root, text='Distance:')
        lblDistance.grid(row=5, column=0)
        entryDistance = tk.Entry(root)
        entryDistance.grid(row=5, column=1)
        entryDistance.insert(0, str(router.ospf.distance))

        lblMaximumPaths = tk.Label(root, text='Maximum paths:')
        lblMaximumPaths.grid(row=6, column=0)
        entryMaximumPaths = tk.Entry(root)
        entryMaximumPaths.grid(row=6, column=1)
        entryMaximumPaths.insert(0, str(router.ospf.maximum_paths))

        lblPassiveInterface = tk.Label(root, text='Passive interface:')
        lblPassiveInterface.grid(row=7, column=0)
        varPassiveInterface = tk.BooleanVar()
        varPassiveInterface.set(router.ospf.passive_interface_default)
        checkPassiveInterface = tk.Checkbutton(root, variable=varPassiveInterface)
        checkPassiveInterface.grid(row=7, column=1)

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

        def validate_ospf() -> bool:
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
            return True

        def update_router_ospf():
            if validate_ospf():
                router_id = get_router_id()
                auto_cost_reference_bandwidth = int(entryAutoCostReferenceBandwidth.get())
                default_information_originate = varDefaultInformationOriginate.get()
                default_metric_of_redistributed_routes = int(entryDefaultMetricOfRedistributedRoutes.get())
                distance = int(entryDistance.get())
                maximum_paths = int(entryMaximumPaths.get())
                passive_interface_default = varPassiveInterface.get()

                threading.Thread(target=update_ospf, args=(main_gui, router, user, router_id,
                                                           auto_cost_reference_bandwidth, default_information_originate,
                                                           default_metric_of_redistributed_routes, distance,
                                                           maximum_paths, passive_interface_default)).start()

                root.destroy()

        btnFrame = tk.Frame(root)
        btnApply = tk.Button(btnFrame, text='Apply', command=update_router_ospf, width=15)
        btnApply.pack()
        btnCancel = tk.Button(btnFrame, text='Cancel', command=root.destroy, width=15)
        btnCancel.pack()
        btnFrame.grid(row=13, column=1)

        root.mainloop()
