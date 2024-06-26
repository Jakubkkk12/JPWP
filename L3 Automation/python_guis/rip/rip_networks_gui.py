import threading
import tkinter as tk
import tkinter.ttk
from python_guis.gui_resources import config
from python_guis.rip.rip_network_add_gui import RIPNetworkAddGUI
from resources.connect_frontend_with_backend.frontend_backend_functions import remove_rip_networks
from resources.devices.Router import Router
from resources.routing_protocols.Network import Network
from resources.user.User import User


class RIPNetworksGUI:
    def __init__(self, main_gui, router: Router, user: User):
        self.router = router

        root = tk.Toplevel()

        # title
        root.title(config.APPNAME + ' ' + config.VERSION + ' ' + router.name + ' RIP Networks Configuration')
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

        treeFrame = tk.Frame(root)
        scrollbar = tk.Scrollbar(treeFrame, orient='vertical')
        scrollbar.pack(side='right', fill='y')

        treeColumns = ('No', 'Network', 'Mask')
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

        i = 1
        try:
            for k, network in router.rip.networks.items():
                values = (i, network.network, network.mask)
                self.tree.insert('', tk.END, iid=i-1, values=values)
                i += 1
        except AttributeError:
            pass
        treeFrame.grid(column=0, row=3, columnspan=2, sticky='NEWS')

        def add_network(router):
            RIPNetworkAddGUI(main_gui, self, router, user)

        def remove_network() -> None:
            item = self.tree.selection()
            ip = self.tree.item(item)['values'][1]

            threading.Thread(target=remove_rip_networks,
                             args=(main_gui, self, router, user, [ip])).start()

        buttonFrame = tk.Frame(root)
        btnAdd = tk.Button(buttonFrame, text='Add', command=lambda: add_network(router))
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
        for k, network in self.router.rip.networks.items():
            values = (i, network.network, network.mask)
            self.tree.insert('', tk.END, iid=i - 1, values=values)
            i += 1
