import tkinter as tk
import tkinter.ttk
from tkinter import ttk
from python_guis.gui_resources import config
from python_guis.interface.interface_edit_all_gui import EditInterfaceGUI
from python_guis.interface.interface_errors_gui import InterfaceErrorsGUI
from python_guis.interface.interface_statistics_gui import InterfaceStatisticsGUI
from resources.devices.Router import Router
from resources.user.User import User
import platform
from resources.connect_frontend_with_backend.frontend_backend_functions import set_to_default_interface


class InterfacesDetailsGUI:
    def __init__(self, main_gui, router: Router, user: User):
        self.router = router
        self.user = user
        self.main_gui = main_gui
        self.hostname = router.name
        self.int_name = ''
        self.selected_router_iid = None

        root = tk.Toplevel()
        # ######## WINDOW PARAMETERS ######## #
        # title
        root.title(config.APPNAME + ' ' + config.VERSION + ' ' + self.hostname + ' Interfaces Details')

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

        root.minsize(300, 300)

        # Frame containing treeview and scrollbars
        treeFrame = tk.Frame(root)
        treeFrame.configure(bg=config.BG_COLOR)
        treeFrame.pack(fill='both', expand=True)

        verticalScrollbar = ttk.Scrollbar(treeFrame, orient='vertical')
        verticalScrollbar.pack(side='right', fill='y')

        horizontalScrollbar = ttk.Scrollbar(treeFrame, orient='horizontal')
        horizontalScrollbar.pack(side='bottom', fill='x')

        treeColumns = ('No', 'Name', 'IP', 'Subnet', 'Description')
        self.tree = tk.ttk.Treeview(treeFrame, columns=treeColumns, show='headings')
        self.tree.pack(side='top', expand=True, fill='both')
        self.tree.configure(yscrollcommand=verticalScrollbar.set)
        self.tree.configure(xscrollcommand=horizontalScrollbar.set)

        verticalScrollbar.config(command=self.tree.yview)
        horizontalScrollbar.config(command=self.tree.xview)

        # Button is a child of root, not treeFrame
        btnQuit = tk.Button(root, text='Quit', command=root.destroy)
        btnQuit.pack(side='bottom')

        # Data insert
        interfaces = router.interfaces
        i = 1
        for k, interface in interfaces.items():
            values = (i, interface.name, interface.ip_address, interface.subnet, interface.description)
            self.tree.insert('', tk.END, iid=i-1, values=values)
            i += 1

        self.tree.heading(treeColumns[0], text='No', anchor='w')
        self.tree.column(treeColumns[0], width=30, stretch=False)

        self.tree.heading(treeColumns[1], text='Name', anchor='w')
        self.tree.column(treeColumns[1], width=100, stretch=False)

        self.tree.heading(treeColumns[2], text='IP', anchor='w')
        self.tree.column(treeColumns[2], width=100, stretch=False)

        self.tree.heading(treeColumns[3], text='Subnet', anchor='w')
        self.tree.column(treeColumns[3], width=50, stretch=False)

        self.tree.heading(treeColumns[4], text='Description', anchor='w')
        self.tree.column(treeColumns[4], width=100, stretch=False)

        def show_menu_interfaces(event) -> None:
            item = self.tree.identify_row(event.y)
            self.tree.selection_set(item)
            if item:
                try:
                    self.int_name = self.tree.item(item)['values'][1]
                    menu.post(event.x_root, event.y_root)
                    self.selected_router_iid = self.tree.item(item)['values'][0]
                    interface = self.router.interfaces[self.int_name]
                    menu.entryconfigure('Reset', command=lambda: set_to_default_interface(main_gui, self,
                                                                                          self.router, user, interface))
                except IndexError():
                    pass

        # Pop-up menu configuration
        menu = tk.Menu(root, tearoff=False)
        menu.add_command(label='Edit', command=self.edit_interface)

        def reset_interface():
            import threading
            threading.Thread(target=set_to_default_interface, args=(main_gui, self, self.router, user,
                                                                    interface)).start()
        menu.add_command(label='Reset', command=reset_interface)

        sub_details_menu = tk.Menu(menu, tearoff=False)
        sub_details_menu.add_command(label='Statistics', command=self.show_interface_statistics)
        sub_details_menu.add_command(label='Errors', command=self.show_interface_errors)
        menu.add_cascade(label='Details', menu=sub_details_menu)

        if platform.system() == 'Windows':
            self.tree.bind('<Button-3>', show_menu_interfaces)
        if platform.system() == 'Darwin':
            self.tree.bind('<Button-2>', show_menu_interfaces)

    def edit_interface(self) -> None:
        EditInterfaceGUI(self.main_gui, self, self.router, self.user, self.int_name, self.selected_router_iid)
        return None

    def show_interface_statistics(self) -> None:
        InterfaceStatisticsGUI(self.router, self.int_name)
        return None

    def show_interface_errors(self) -> None:
        InterfaceErrorsGUI(self.router, self.int_name)
        return None

    def update_window(self) -> None:
        self.tree.delete(*self.tree.get_children())
        interfaces = self.router.interfaces
        i = 1
        for k, interface in interfaces.items():
            values = (i, interface.name, interface.ip_address, interface.subnet, interface.description)
            self.tree.insert('', tk.END, iid=i-1, values=values)
            i += 1
