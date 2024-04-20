import threading
import tkinter as tk
import tkinter.ttk
from python_guis.gui_resources import config
from python_guis.static.static_route_add_gui import StaticRouteAddGUI
from resources.connect_frontend_with_backend.frontend_backend_functions import remove_static_route
from resources.devices.Router import Router
from resources.user.User import User


class StaticRoutesGUI:
    def __init__(self, main_gui, router: Router, user: User):
        self.selected_router = router
        self.hostname = router.name
        self.int_name = ''
        self.selected_router_iid = None

        root = tk.Toplevel()
        # ######## WINDOW PARAMETERS ######## #
        # title
        root.title(config.APPNAME + ' ' + config.VERSION + ' ' + self.hostname + ' Static routes')

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

        treeColumns = ('No', 'Destination', 'Mask', 'Next hop', 'Interface', 'Distance')
        self.tree = tk.ttk.Treeview(treeFrame, columns=treeColumns, show='headings')
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side='left', fill='both', expand=True)

        scrollbar.config(command=self.tree.yview)

        treeFrame.pack(side='left', fill='both', expand=True)

        self.tree.heading(treeColumns[0], text='No', anchor='w')
        self.tree.column(treeColumns[0], width=15)

        self.tree.heading(treeColumns[1], text='Destination', anchor='w')
        self.tree.column(treeColumns[1], width=50)

        self.tree.heading(treeColumns[2], text='Mask', anchor='w')
        self.tree.column(treeColumns[2], width=30)

        self.tree.heading(treeColumns[3], text='Next hop', anchor='w')
        self.tree.column(treeColumns[3], width=50)

        self.tree.heading(treeColumns[4], text='Interface', anchor='w')
        self.tree.column(treeColumns[4], width=50)

        self.tree.heading(treeColumns[5], text='Distance', anchor='w')
        self.tree.column(treeColumns[5], width=50)

        try:
            i = 1
            for route in router.static_routes:
                values = (i, route.network.network, route.network.mask, route.next_hop, route.interface, route.distance)
                self.tree.insert('', tk.END, iid=i-1, values=values)
                i += 1
        except AttributeError:
            pass
        except TypeError:
            pass

        def add_route(main_gui, router, user):
            StaticRouteAddGUI(main_gui, self, router, user)

        def remove_route() -> None:
            item = self.tree.selection()
            # todo 18
            network = self.tree.item(item, 'values')[1]
            network_mask = int(self.tree.item(item, 'values')[2])

            threading.Thread(target=remove_static_route,
                             args=(main_gui, self, item, router, user, network, network_mask)).start()

            # Update NoS todo 22
            # children = self.tree.get_children()
            # for i, child in enumerate(children, start=1):
            #     self.tree.item(child, values=(i,) + self.tree.item(child, 'values')[1:])

        buttonFrame = tk.Frame(root)
        btnAdd = tk.Button(buttonFrame, text='Add', command=lambda: add_route(main_gui, router, user))
        btnAdd.pack()
        btnRemove = tk.Button(buttonFrame, text='Remove', command=remove_route)
        btnRemove.pack()
        btnQuit = tk.Button(buttonFrame, text='Quit', command=root.destroy)
        btnQuit.pack()
        buttonFrame.pack(side='right', fill='y', padx=2)

        root.mainloop()

    def insert_route(self, staticroute):
        last_item = self.tree.get_children()[-1]
        last_index = self.tree.index(last_item)
        no = last_index + 2
        values = (no, staticroute.network.network, staticroute.network.mask, staticroute.next_hop, staticroute.interface,
                  staticroute.distance)
        self.tree.insert('', tk.END, values=values)
