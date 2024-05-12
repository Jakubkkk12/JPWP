import threading
import tkinter as tk
import tkinter.ttk

from python_guis.bgp.bgp_neighbor_edit_gui import BGPNeighborEditGUI
from python_guis.gui_resources import config
from python_guis.bgp.bgp_neighbor_add_gui import BGPNeighborAddGUI
from resources.connect_frontend_with_backend.frontend_backend_functions import remove_bgp_neighbor
from resources.routing_protocols.bgp.BGPNeighbor import BGPNeighbor
from resources.devices.Router import Router
from resources.user.User import User


class BGPNeighborsGUI:
    def __init__(self, main_gui, router: Router, user: User):
        self.main_gui = main_gui
        self.router_name = router.name
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
        self.tree.column(treeColumns[0], width=30)

        self.tree.heading(treeColumns[1], text='ID', anchor='w')
        self.tree.column(treeColumns[1], width=100)

        self.tree.heading(treeColumns[2], text='Remote AS', anchor='w')
        self.tree.column(treeColumns[2], width=100)

        self.tree.heading(treeColumns[3], text='State', anchor='w')
        self.tree.column(treeColumns[3], width=50)

        self.tree.heading(treeColumns[4], text='EBGP Multihop', anchor='w')
        self.tree.column(treeColumns[4], width=100)

        self.tree.heading(treeColumns[5], text='Next hop self', anchor='w')
        self.tree.column(treeColumns[5], width=100)

        self.tree.heading(treeColumns[6], text='Shutdown', anchor='w')
        self.tree.column(treeColumns[6], width=80)

        self.tree.heading(treeColumns[7], text='Keep alive timer', anchor='w')
        self.tree.column(treeColumns[7], width=120)

        self.tree.heading(treeColumns[8], text='Hold time timer', anchor='w')
        self.tree.column(treeColumns[8], width=120)

        i = 1
        try:
            for k, neighbor in router.bgp.neighbors.items():
                values = (i, neighbor.ip_address, neighbor.remote_as, neighbor.state, neighbor.ebgp_multihop,
                          neighbor.next_hop_self, neighbor.shutdown, neighbor.timers.keep_alive,
                          neighbor.timers.hold_time)
                self.tree.insert('', tk.END, iid=i-1, values=values)
                i += 1
        except AttributeError:
            pass

        treeFrame.grid(column=0, row=3, columnspan=2, sticky='NEWS')

        def add_neighbor(main_gui, bgp_neighbors_gui, router, user):
            BGPNeighborAddGUI(main_gui, bgp_neighbors_gui, router, user)

        def remove_neighbor() -> None:
            item = self.tree.selection()
            ip = self.tree.item(item)['values'][1]

            threading.Thread(target=remove_bgp_neighbor,
                             args=(main_gui, self, router, user, ip)).start()

        buttonFrame = tk.Frame(root)
        btnAdd = tk.Button(buttonFrame, text='Add', command=lambda: add_neighbor(main_gui, self, router, user))
        btnAdd.pack()
        btnRemove = tk.Button(buttonFrame, text='Remove', command=remove_neighbor)
        btnRemove.pack()
        btnQuit = tk.Button(buttonFrame, text='Quit', command=root.destroy)
        btnQuit.pack()
        buttonFrame.grid(column=0, row=4, columnspan=2)

        menu = tk.Menu(root, tearoff=0)
        menu.add_command(label='Edit', command=lambda: BGPNeighborEditGUI(main_gui, self, router, user, neighbor))

        def show_menu_all(event):
            item = self.tree.identify_row(event.y)
            self.tree.selection_set(item)
            if item:
                try:
                    hostname = self.tree.item(item)['values'][1]
                    selected_neighbor = router.bgp.neighbors[hostname]
                    menu.post(event.x_root, event.y_root)
                    menu.entryconfigure('Edit', command=lambda: BGPNeighborEditGUI(main_gui, self, router, user,
                                                                                   selected_neighbor))
                except IndexError:
                    pass

        root.bind('<Button-3>', show_menu_all)

        root.mainloop()

    def insert_neighbor(self, neighbor: BGPNeighbor):
        last_item = self.tree.get_children()[-1]
        last_index = self.tree.index(last_item)
        no = last_index + 2
        values = (no, neighbor.ip_address, neighbor.remote_as, neighbor.state, neighbor.ebgp_multihop,
                  neighbor.next_hop_self, neighbor.shutdown, neighbor.timers.keep_alive, neighbor.timers.hold_time)
        # Update tree
        self.tree.insert('', tk.END, values=values)

    def update_window(self):
        self.tree.delete(*self.tree.get_children())
        router = self.main_gui.get_router(self.router_name)
        i = 1
        if router.bgp.neighbors is not None:
            for k, neighbor in router.bgp.neighbors.items():
                values = (i, neighbor.ip_address, neighbor.remote_as, neighbor.state, neighbor.ebgp_multihop,
                          neighbor.next_hop_self, neighbor.shutdown, neighbor.timers.keep_alive,
                          neighbor.timers.hold_time)
                self.tree.insert('', tk.END, iid=i-1, values=values)
                i += 1

