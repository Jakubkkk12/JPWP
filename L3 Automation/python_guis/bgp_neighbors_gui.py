
import tkinter as tk
import tkinter.ttk
from gui_resources import config
from python_guis.bgp_neighbor_add_gui import BGPNeighborAddGUI
from resources.routing_protocols.bgp.BGPNeighbor import BGPNeighbor
from resources.devices.Router import Router


class BGPNeighborsGUI:
    def __init__(self, router: Router):
        root = tk.Toplevel()

        # title
        root.title(config.APPNAME + ' ' + config.VERSION + ' ' + router.name + ' BGP Neighbors')
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
        verticalscrollbar = tk.Scrollbar(treeFrame, orient='vertical')
        verticalscrollbar.pack(side='right', fill='y')
        horizontalscrollbar = tk.Scrollbar(treeFrame, orient='horizontal')
        horizontalscrollbar.pack(side='bottom', fill='x')

        treeColumns = ('No', 'ID', 'Remote AS', 'State', 'EBGP Multihop', 'Next hop self', 'Shutdown',
                       'Keep alive timer', 'Hold time timer')
        self.tree = tk.ttk.Treeview(treeFrame, columns=treeColumns, show='headings')

        self.tree.configure(yscrollcommand=verticalscrollbar.set)
        self.tree.configure(xscrollcommand=horizontalscrollbar.set)

        self.tree.pack(side='left', fill='both', expand=True)

        verticalscrollbar.config(command=self.tree.yview)
        horizontalscrollbar.config(command=self.tree.xview)

        self.tree.heading(treeColumns[0], text='No', anchor='w')
        self.tree.column(treeColumns[0], width=15)

        self.tree.heading(treeColumns[1], text='ID', anchor='w')
        self.tree.column(treeColumns[1], width=30)

        self.tree.heading(treeColumns[2], text='Remote AS', anchor='w')
        self.tree.column(treeColumns[2], width=50)

        self.tree.heading(treeColumns[3], text='State', anchor='w')
        self.tree.column(treeColumns[3], width=50)

        self.tree.heading(treeColumns[4], text='EBGP Multihop', anchor='w')
        self.tree.column(treeColumns[4], width=100)

        self.tree.heading(treeColumns[5], text='Next hop self', anchor='w')
        self.tree.column(treeColumns[5], width=100)

        self.tree.heading(treeColumns[6], text='Shutdown', anchor='w')
        self.tree.column(treeColumns[6], width=50)

        self.tree.heading(treeColumns[7], text='Keep alive timer', anchor='w')
        self.tree.column(treeColumns[7], width=100)

        self.tree.heading(treeColumns[8], text='Hold time timer', anchor='w')
        self.tree.column(treeColumns[8], width=100)

        i = 1
        for k, neighbor in router.bgp.neighbors.items():
            values = (i, neighbor.ip_address, neighbor.remote_as, neighbor.state, neighbor.ebgp_multihop,
                      neighbor.next_hop_self, neighbor.shutdown, neighbor.timers.keep_alive, neighbor.timers.hold_time)
            self.tree.insert('', tk.END, iid=i-1, values=values)
            i += 1

        treeFrame.grid(column=0, row=3, columnspan=2, sticky='NEWS')

        def add_neighbor(router, self):
            BGPNeighborAddGUI(router, self)

        def remove_neighbor() -> None:
            item = self.tree.selection()
            ip = self.tree.item(item)['values'][1]

            del router.bgp.neighbors[ip]
            self.tree.delete(item)

            # Update No
            children = self.tree.get_children()
            for i, child in enumerate(children, start=1):
                self.tree.item(child, values=(i,) + self.tree.item(child, 'values')[1:])

        buttonFrame = tk.Frame(root)
        btnAdd = tk.Button(buttonFrame, text='Add', command=lambda: add_neighbor(router, self))
        btnAdd.pack()
        btnRemove = tk.Button(buttonFrame, text='Remove', command=remove_neighbor)
        btnRemove.pack()
        btnQuit = tk.Button(buttonFrame, text='Quit', command=root.destroy)
        btnQuit.pack()
        buttonFrame.grid(column=0, row=4, columnspan=2)

        root.mainloop()

    def insert_neighbor(self, neighbor: BGPNeighbor):
        last_item = self.tree.get_children()[-1]
        last_index = self.tree.index(last_item)
        no = last_index + 2
        values = (no, neighbor.ip_address, neighbor.remote_as, neighbor.state, neighbor.ebgp_multihop,
                  neighbor.next_hop_self, neighbor.shutdown, neighbor.timers.keep_alive, neighbor.timers.hold_time)
        # Update tree
        self.tree.insert('', tk.END, values=values)
