import threading
import tkinter as tk
import tkinter.ttk
from python_guis.gui_resources import config
from python_guis.ospf.ospf_network_add_gui import OSPFNetworkAddGUI
from resources.connect_frontend_with_backend.frontend_backend_functions import remove_ospf_area_networks
from resources.devices.Router import Router
from resources.routing_protocols.ospf.OSPFArea import OSPFArea
from resources.routing_protocols.Network import Network
from resources.user.User import User


class OSPFAreaConfigurationGUI:
    def __init__(self, main_gui, router: Router, user: User, area: OSPFArea):
        self.main_gui = main_gui
        self.area = area
        self.router = router
        root = tk.Toplevel()

        # title
        root.title(config.APPNAME + ' ' + config.VERSION + ' ' + router.name + ' Area ' + area.id + ' Configuration')
        # window icon, using conversion to iso, cause tkinter doesn't accept jpg
        icon = tk.PhotoImage(file=config.WINDOW_ICON_PATH)
        root.wm_iconphoto(False, icon)

        # size parameters
        width = 400
        height = 400
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=True, height=True)

        root.minsize(400, 400)

        root.grid_columnconfigure(1, weight=1)
        root.grid_columnconfigure(1, weight=1)

        lblIsAuthMsgDigest = tk.Label(root, text='Is Authentication Message Digest:')
        lblIsAuthMsgDigest.grid(column=0, row=0)
        varIsAuthMsgDigest = tk.BooleanVar(root)
        chckbtnIsAuthMsgDigest = tk.Checkbutton(root, variable=varIsAuthMsgDigest)
        if area.is_authentication_message_digest:
            chckbtnIsAuthMsgDigest.select()
            varIsAuthMsgDigest = True
        else:
            chckbtnIsAuthMsgDigest.deselect()
            varIsAuthMsgDigest = False
        chckbtnIsAuthMsgDigest.grid(column=1, row=0)

        lblType = tk.Label(root, text='Type:')
        lblType.grid(column=0, row=1)

        if area.id == '0':
            typeOption = ['backbone area']
        else:
            typeOption = ['standard area', 'stub area', 'totally stubby area',
                          'NSSA']

        varType = tk.StringVar(root)
        varType.set(area.type)

        optionMenuType = tk.OptionMenu(root, varType, *typeOption)
        optionMenuType.grid(column=1, row=1)

        treeFrame = tk.Frame(root)
        scrollbar = tk.Scrollbar(treeFrame, orient='vertical')
        scrollbar.pack(side='right', fill='y')

        treeColumns = ('No', 'Network', 'Mask', 'Wildcard')
        self.tree = tk.ttk.Treeview(treeFrame, columns=treeColumns, show='headings')
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side='left', fill='both', expand=True)

        scrollbar.config(command=self.tree.yview)

        self.tree.heading(treeColumns[0], text='No', anchor='w')
        self.tree.column(treeColumns[0], width=15)

        self.tree.heading(treeColumns[1], text='Network', anchor='w')
        self.tree.column(treeColumns[1], width=50)

        self.tree.heading(treeColumns[2], text='Mask', anchor='w')
        self.tree.column(treeColumns[2], width=30)

        self.tree.heading(treeColumns[3], text='Wildcard', anchor='w')
        self.tree.column(treeColumns[3], width=50)

        i = 1
        for k, network in area.networks.items():
            values = (i, network.network, network.mask, network.wildcard)
            self.tree.insert('', tk.END, iid=i-1, values=values)
            i += 1

        treeFrame.grid(column=0, row=3, columnspan=2, sticky='NEWS')

        def add_network(router, area):
            OSPFNetworkAddGUI(main_gui, self, router, user, area)

        def remove_network() -> None:
            item = self.tree.selection()
            network = self.tree.item(item)['values'][1]
            wildcard = str(self.tree.item(item)['values'][3])

            network_and_wildcard = [[network, wildcard]]
            threading.Thread(target=remove_ospf_area_networks,
                             args=(main_gui, self, router, user, area, network_and_wildcard)).start()

        buttonFrame = tk.Frame(root)
        btnAdd = tk.Button(buttonFrame, text='Add', command=lambda: add_network(router, area))
        btnAdd.pack()
        btnRemove = tk.Button(buttonFrame, text='Remove', command=remove_network)
        btnRemove.pack()
        btnQuit = tk.Button(buttonFrame, text='Quit', command=root.destroy)
        btnQuit.pack()
        buttonFrame.grid(column=0, row=4, columnspan=2)

        root.mainloop()

    def update_window(self) -> None:
        self.tree.delete(*self.tree.get_children())
        i = 1
        for k, network in self.router.ospf.areas[self.area.id].networks.items():
            values = (i, network.network, network.mask, network.wildcard)
            self.tree.insert('', tk.END, iid=i-1, values=values)
            i += 1
