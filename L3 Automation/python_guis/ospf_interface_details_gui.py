import tkinter as tk
import tkinter.ttk
from tkinter import ttk
from gui_resources import config
from python_guis.edit_interface_all_gui import EditInterfaceGUI
from python_guis.edit_interface_ospf_gui import EditInterfaceOSPFGUI
from python_guis.interface_errors_gui import InterfaceErrorsGUI
from python_guis.interface_statistics_gui import InterfaceStatisticsGUI
from resources.devices.Router import Router


class OSPFInterfaceDetailsGUI:
    def __init__(self, router: Router):
        self.selected_router = router
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

        treeColumns = ('No', 'Name', 'Network type', 'Cost', 'State', 'Passive', 'Priority', 'Hello timer', 'Dead timer',
                       'Wait timer', 'Retransmit timer')
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
            values = (i, interface.name, interface.ospf.network_type, interface.ospf.cost,
                      interface.ospf.state, interface.ospf.passive_interface, interface.ospf.priority,
                      interface.ospf.timers.hello_timer, interface.ospf.timers.dead_timer,
                      interface.ospf.timers.wait_timer,
                      interface.ospf.timers.retransmit_timer)
            self.tree.insert('', tk.END, iid=i-1, values=values)
            i += 1

        self.tree.heading(treeColumns[0], text='No', anchor='w')
        self.tree.column(treeColumns[0], width=30, stretch=False)

        self.tree.heading(treeColumns[1], text='Name', anchor='w')
        self.tree.column(treeColumns[1], width=50, stretch=False)

        self.tree.heading(treeColumns[2], text='Network type', anchor='w')
        self.tree.column(treeColumns[2], width=90, stretch=False)

        self.tree.heading(treeColumns[3], text='Cost', anchor='w')
        self.tree.column(treeColumns[3], width=50, stretch=False)

        self.tree.heading(treeColumns[4], text='State', anchor='w')
        self.tree.column(treeColumns[4], width=50, stretch=False)

        self.tree.heading(treeColumns[5], text='Passive', anchor='w')
        self.tree.column(treeColumns[5], width=50, stretch=False)

        self.tree.heading(treeColumns[6], text='Priority', anchor='w')
        self.tree.column(treeColumns[6], width=50, stretch=False)

        self.tree.heading(treeColumns[7], text='Hello timer', anchor='w')
        self.tree.column(treeColumns[7], width=80, stretch=False)

        self.tree.heading(treeColumns[8], text='Dead timer', anchor='w')
        self.tree.column(treeColumns[8], width=80, stretch=False)

        self.tree.heading(treeColumns[9], text='Wait timer', anchor='w')
        self.tree.column(treeColumns[9], width=80, stretch=False)

        self.tree.heading(treeColumns[10], text='Retransmit timer', anchor='w')
        self.tree.column(treeColumns[10], width=105, stretch=False)

        def show_menu_interfaces(event) -> None:
            item = self.tree.identify_row(event.y)
            self.tree.selection_set(item)
            if item:
                try:
                    self.selected_router_iid = self.tree.item(item)['values'][0]
                    self.int_name = self.tree.item(item)['values'][1]
                    menu.post(event.x_root, event.y_root)
                except IndexError():
                    pass

        # Pop-up menu configuration
        menu = tk.Menu(root, tearoff=False)
        menu.add_command(label='Edit', command=self.edit_interface_ospf)

        self.tree.bind('<Button-3>', show_menu_interfaces)

    def edit_interface_ospf(self) -> None:
        EditInterfaceOSPFGUI(self.selected_router, self.int_name, self.selected_router_iid, self)
        return None

    # IDK how but it works, I love gpt
    def update_interface_details(self, iid, name, network_type, cost, passive_interface,
                                 priority, hello_timer, dead_timer, wait_timer, retransmit_timer) -> None:
        self.tree.item(iid-1, values=(iid, name, network_type, cost, self.tree.item(iid-1, 'values')[2],
                                      passive_interface, priority, hello_timer, dead_timer, wait_timer,
                                      retransmit_timer))
        return None
