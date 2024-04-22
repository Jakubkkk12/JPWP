import ipaddress
import threading
import tkinter as tk
from tkinter import messagebox

from python_guis.gui_resources import config
from resources.connect_frontend_with_backend.frontend_backend_functions import enable_rip
from resources.routing_protocols.rip.RIPInformation import RIPInformation
from resources.user.User import User


class RIPAddRouterGUI:
    def __init__(self, main_gui, user: User):
        self.main_gui = main_gui

        root = tk.Toplevel()
        # ######## WINDOW PARAMETERS ######## #
        # title
        root.title(config.APPNAME + ' ' + config.VERSION + ' ' + ' RIP Add router')

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

        root.minsize(300, 400)

        root.columnconfigure(0, weight=1)
        root.columnconfigure(1, weight=1)

        # Components
        devices = main_gui.get_devices()
        ripOptions = []
        for k, router in devices.items():
            if router.rip is None:
                ripOptions.append(router.name)
        if len(ripOptions) == 0:
            messagebox.showerror('Error', 'All routers have RIP configured', parent=root)
            root.destroy()
            return
        lblHostname = tk.Label(root, text='Hostname:')
        lblHostname.grid(row=0, column=0)

        varHostname = tk.StringVar(root)
        optionMenuHostname = tk.OptionMenu(root, varHostname, *ripOptions)
        optionMenuHostname.grid(row=0, column=1)

        lblAutoSummary = tk.Label(root, text='Auto Summary')
        lblAutoSummary.grid(column=0, row=1)
        varAutoSummary = tk.BooleanVar(root)
        chckbtnAutoSummary = tk.Checkbutton(root, variable=varAutoSummary)
        chckbtnAutoSummary.grid(column=1, row=1)

        lblDefaultInformationOriginate = tk.Label(root, text='Default Information Originate')
        lblDefaultInformationOriginate.grid(column=0, row=2)
        varDefaultInformationOriginate = tk.BooleanVar(root)
        chckbtnDefaultInformation = tk.Checkbutton(root, variable=varDefaultInformationOriginate)
        chckbtnDefaultInformation.grid(column=1, row=2)

        lblDefaultMetric = tk.Label(root, text='Default Metric')
        lblDefaultMetric.grid(column=0, row=3)
        entryDefaultMetric = tk.Entry(root)
        entryDefaultMetric.grid(column=1, row=3)

        lblDistance = tk.Label(root, text='Distance')
        lblDistance.grid(column=0, row=4)
        entryDistance = tk.Entry(root)
        entryDistance.grid(column=1, row=4)

        lblMaximumPaths = tk.Label(root, text='Maximum Paths')
        lblMaximumPaths.grid(column=0, row=5)
        entryMaximumPaths = tk.Entry(root)
        entryMaximumPaths.grid(column=1, row=5)

        lblVersion = tk.Label(root, text='Version')
        lblVersion.grid(column=0, row=6)
        versionOptions = ['1', '2']
        varVersion = tk.StringVar(root)
        optionMenuVersion = tk.OptionMenu(root, varVersion, *versionOptions)
        optionMenuVersion.grid(column=1, row=6)

        lblNetwork = tk.Label(root, text='Network:')
        lblNetwork.grid(column=0, row=7)
        frameNetwork = tk.Frame(root)
        frameNetwork.grid(column=1, row=7)
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
        lblMask.grid(column=0, row=8)
        entryMask = tk.Entry(root)
        entryMask.grid(column=1, row=8)

        def get_network() -> str:
            try:
                ip = (entryNetworkFirst.get() + '.' + entryNetworkSecond.get() + '.' + entryNetworkThird.get() + '.' +
                      entryNetworkFourth.get())
                mask = entryMask.get()
                ipaddress.ip_network(ip + '/' + mask)
                return ip
            except ValueError:
                messagebox.showerror('Error', 'Invalid network', parent=root)

        def validate_router() -> bool:
            if not entryDefaultMetric.get().isdigit() or not (0 <= int(entryDefaultMetric.get()) <= 15):
                messagebox.showerror('Error', 'Default metric must be a an integer between 0 and 15', parent=root)
                entryDefaultMetric.delete(0, tk.END)
                return False
            if not entryDistance.get().isdigit() or not (0 <= int(entryDistance.get()) <= 255):
                messagebox.showerror('Error', 'Distance must be a an integer between 0 and 255', parent=root)
                entryDistance.delete(0, tk.END)
                return False
            if not entryMaximumPaths.get().isdigit() or not (1 <= int(entryMaximumPaths.get()) <= 16):
                messagebox.showerror('Error', 'Maximum paths must be a an integer between 1 and 16', parent=root)
                entryMaximumPaths.delete(0, tk.END)
                return False
            if varVersion.get() not in ['1', '2']:
                messagebox.showerror('Error', 'Version must be 1 or 2', parent=root)
                return False
            try:
                ipaddress.ip_network(get_network() + '/' + entryMask.get())
            except ValueError:
                return False
            except TypeError:
                return False
            return True

        def add_router():
            if validate_router():
                router = main_gui.get_router(varHostname.get())
                network: str = get_network()
                threading.Thread(target=enable_rip,
                                 args=(main_gui, router, user, varAutoSummary.get(),
                                       varDefaultInformationOriginate.get(), int(entryDefaultMetric.get()),
                                       int(entryDistance.get()), int(entryMaximumPaths.get()),
                                       int(varVersion.get()), [network])).start()

                root.destroy()

        btnFrame = tk.Frame(root)
        btnAdd = tk.Button(btnFrame, text='Add', command=add_router, width=15)
        btnAdd.pack()
        btnCancel = tk.Button(btnFrame, text='Cancel', command=root.destroy, width=15)
        btnCancel.pack()
        btnFrame.grid(row=9, column=1)

        root.mainloop()
