import tkinter as tk
import tkinter.ttk
from gui_resources import config
from python_guis.ssh_address_add_gui import SSHAddressAddGUI
from resources.devices.Router import Router
from resources.ssh.SSHInformation import SSHInformation


class SSHConnectionsGUI:
    def __init__(self, router: Router):
        self.selected_router = router
        self.hostname = router.name

        root = tk.Toplevel()
        # ######## WINDOW PARAMETERS ######## #
        # title
        root.title(config.APPNAME + ' ' + config.VERSION + ' ' + self.hostname + ' SSH Connections')

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

        root.minsize(500, 400)

        # Tree widget
        treeFrame = tk.Frame(root)
        treeFrame.columnconfigure(0, weight=1)
        treeFrame.columnconfigure(1, weight=1)
        treeFrame.rowconfigure(0, weight=1)
        treeFrame.rowconfigure(0, weight=1)

        scrollbar = tk.Scrollbar(treeFrame, orient='vertical')
        scrollbar.pack(side='right', fill='y')

        treeColumns = ('No', 'Address', 'Port')
        self.tree = tk.ttk.Treeview(treeFrame, columns=treeColumns, show='headings')
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side='left', fill='both', expand=True)

        scrollbar.config(command=self.tree.yview)

        treeFrame.pack(side='left', fill='both', expand=True)

        self.tree.heading(treeColumns[0], text='No', anchor='w')
        self.tree.column(treeColumns[0], width=15)

        self.tree.heading(treeColumns[1], text='Address', anchor='w')
        self.tree.column(treeColumns[1], width=50)

        self.tree.heading(treeColumns[2], text='Port', anchor='w')
        self.tree.column(treeColumns[2], width=50)

        i = 1
        for k, address in router.ssh_information.ip_addresses.items():
            values = (i, address, router.ssh_information.port)
            self.tree.insert('', tk.END, iid=i-1, values=values)
            i += 1

        def add_address(router):
            SSHAddressAddGUI(router, self)

        def remove_address() -> None:
            item = self.tree.selection()
            self.tree.delete(item)

            # Update No
            children = self.tree.get_children()
            for i, child in enumerate(children, start=1):
                self.tree.item(child, values=(i,) + self.tree.item(child, 'values')[1:])

        buttonFrame = tk.Frame(root)
        btnAdd = tk.Button(buttonFrame, text='Add', command=lambda: add_address(router))
        btnAdd.pack()
        btnRemove = tk.Button(buttonFrame, text='Remove', command=remove_address)
        btnRemove.pack()
        btnQuit = tk.Button(buttonFrame, text='Quit', command=root.destroy)
        btnQuit.pack()
        buttonFrame.pack(side='right', fill='y', padx=2)

        root.mainloop()

    def insert_address(self, ssh_ip, port):
        last_item = self.tree.get_children()[-1]
        last_index = self.tree.index(last_item)
        no = last_index + 2

        values = (no, ssh_ip, port)
        self.tree.insert('', tk.END, values=values)
