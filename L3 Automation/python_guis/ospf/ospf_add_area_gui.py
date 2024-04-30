import ipaddress
import threading
import tkinter as tk
from tkinter import messagebox

from python_guis.gui_resources import config
from resources.devices.Router import Router
from resources import constants
from resources.routing_protocols.ospf.OSPFArea import OSPFArea
from resources.user.User import User


class OSPFAddAreaGUI:
    def __init__(self, main_gui, router: Router, user: User):
        self.main_gui = main_gui
        self.router = router

        root = tk.Toplevel()
        # ######## WINDOW PARAMETERS ######## #
        # title
        root.title(config.APPNAME + ' ' + config.VERSION + ' ' + ' OSPF Add Area')

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
        lblAreaID = tk.Label(root, text='Area ID:')
        lblAreaID.grid(row=0, column=0)
        entryAreaID = tk.Entry(root)
        entryAreaID.grid(row=0, column=1)

        lblIsAuthenticationMsgDigest = tk.Label(root, text='Authentication Message Digest')
        lblIsAuthenticationMsgDigest.grid(row=1, column=0)
        varIsAuthenticationMsgDigest = tk.BooleanVar(root)
        chckboxIsAuthenticationMsgDigest = tk.Checkbutton(root, variable=varIsAuthenticationMsgDigest)
        chckboxIsAuthenticationMsgDigest.grid(row=1, column=1)

        lblType = tk.Label(root, text='Type:')
        lblType.grid(row=2, column=0)
        varType = tk.StringVar()
        ospfTypes = ['standard', 'backbone', 'stub', 'nssa']
        varType.set(ospfTypes[0])
        menuType = tk.OptionMenu(root, varType, *ospfTypes)
        menuType.grid(row=2, column=1)

        lblNetwork = tk.Label(root, text='Network:')
        lblNetwork.grid(row=3, column=0)
        frameNetwork = tk.Frame(root)
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
        frameNetwork.grid(row=3, column=1)

        lblMask = tk.Label(root, text='Mask:')
        lblMask.grid(row=4, column=0)
        entryMask = tk.Entry(root)
        entryMask.grid(row=4, column=1)

        def get_network() -> str:
            try:
                ip = (entryNetworkFirst.get() + '.' + entryNetworkSecond.get() + '.' + entryNetworkThird.get() +
                      '.' + entryNetworkFourth.get())
                mask = entryMask.get()
                network = ip + '/' + mask
                ipaddress.ip_network(network)
                return ip
            except ValueError:
                messagebox.showerror('Error', 'Invalid network or mask')

        def validate_area() -> bool:
            area_id = entryAreaID.get()
            if not area_id.isdigit() or not 0 <= int(area_id) <= 4294967295:
                messagebox.showerror('Error', 'Invalid Area ID')
                return False
            if area_id == 0 and varType.get() != 'backbone':
                messagebox.showerror('Error', 'Area ID 0 must be a backbone area')
                return False
            return True

        def add_area():
            if validate_area():
                area_id = entryAreaID.get()
                ip = get_network()
                mask = entryMask.get()
                area_type = varType.get()
                is_authentication_message_digest = varIsAuthenticationMsgDigest.get()

                #  todo: add area to router


        btnFrame = tk.Frame(root)
        btnAdd = tk.Button(btnFrame, text='Add', command=add_area, width=15)
        btnAdd.pack()
        btnCancel = tk.Button(btnFrame, text='Cancel', command=root.destroy, width=15)
        btnCancel.pack()
        btnFrame.grid(row=13, column=1)

        root.mainloop()

