import tkinter as tk
from tkinter import messagebox

from resources.devices.Router import Router
from python_guis.gui_resources import config
from resources.user.User import User
from resources.connect_frontend_with_backend.frontend_backend_functions import redistribution
import threading

class BGPRedistributionGUI:
    def __init__(self, main_gui, router: Router, user: User):
        self.selected_router = router
        self.hostname = router.name

        root = tk.Toplevel()
        # ######## WINDOW PARAMETERS ######## #
        # title
        root.title(config.APPNAME + ' ' + config.VERSION + ' ' + self.hostname + ' Redistribution RIP')

        # window icon, using conversion to iso, cause tkinter doesn't accept jpg
        icon = tk.PhotoImage(file=config.WINDOW_ICON_PATH)
        root.wm_iconphoto(False, icon)

        # size parameters
        width = 200
        height = 200
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=True, height=True)

        root.columnconfigure(0, weight=1)
        root.columnconfigure(1, weight=1)

        lblStatic = tk.Label(root, text='Static')
        lblStatic.grid(column=0, row=0)
        varStatic = tk.BooleanVar(root)
        chckbtnStatic = tk.Checkbutton(root, variable=varStatic)
        chckbtnStatic.grid(column=1, row=0)

        lblConnected = tk.Label(root, text='Connected')
        lblConnected.grid(column=0, row=1)
        varConnected = tk.BooleanVar(root)
        chckbtnConnected = tk.Checkbutton(root, variable=varConnected)
        chckbtnConnected.grid(column=1, row=1)

        lblOSPF = tk.Label(root, text='OSPF')
        lblOSPF.grid(column=0, row=2)
        varOSPF = tk.BooleanVar(root)
        chckbtnOSPF = tk.Checkbutton(root, variable=varOSPF)
        chckbtnOSPF.grid(column=1, row=2)

        lblRIP = tk.Label(root, text='RIP')
        lblRIP.grid(column=0, row=3)
        varRIP = tk.BooleanVar(root)
        chckbtnRIP = tk.Checkbutton(root, variable=varRIP)
        chckbtnRIP.grid(column=1, row=3)

        try:
            if router.bgp.redistribution.is_redistribute_static:
                chckbtnStatic.select()
                varStatic.set(True)
            if router.bgp.redistribution.is_redistribute_connected:
                chckbtnConnected.select()
                varConnected.set(True)
            if router.bgp.redistribution.is_redistribute_ospf:
                chckbtnOSPF.select()
                varOSPF.set(True)
            if router.bgp.redistribution.is_redistribute_rip:
                chckbtnRIP.select()
                varRIP.set(True)
        except AttributeError:
            pass

        def apply_changes():
            static = varStatic.get()
            connected = varConnected.get()
            ospf = varOSPF.get()
            rip = varRIP.get()

            threading.Thread(target=redistribution,
                             args=(main_gui, router, user, 'bgp', router.bgp.redistribution, ospf,
                                   rip, router.bgp.redistribution.is_redistribute_bgp, static,
                                   connected)).start()
            root.destroy()

        btnFrame = tk.Frame(root)
        btnApply = tk.Button(btnFrame, text='Apply', command=apply_changes)
        btnApply.pack()

        btnQuit = tk.Button(btnFrame, text='Quit', command=root.destroy)
        btnQuit.pack()

        btnFrame.grid(column=0, row=4, columnspan=2)

        root.mainloop()
