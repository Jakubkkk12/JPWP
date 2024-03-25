import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

import ssh_password_gui
from gui_resources import config
from login_gui import LoginGUI
from python_guis.interfaces_details_gui import InterfacesDetails
from python_guis.ospf_interface_details_gui import OSPFInterfaceDetailsGUI
from python_guis.static_routes_gui import StaticRoutesGUI

from resources.devices.Router import Router
from resources.interfaces.InterfaceOSPFInformation import InterfaceOSPFInformation
from resources.interfaces.InterfaceStatistics import InterfaceStatistics, InformationStatistics, ErrorsStatistics
from resources.interfaces.RouterInterface import RouterInterface
from resources.routing_protocols.Network import Network
from resources.routing_protocols.Redistribution import Redistribution
from resources.routing_protocols.StaticRoute import StaticRoute
from resources.routing_protocols.ospf.OSPFArea import OSPFArea
from resources.routing_protocols.ospf.OSPFInformation import OSPFInformation
from resources.routing_protocols.ospf.OSPFTimers import OSPFTimers
from resources.ssh.SSHInformation import SSHInformation


class MainGUI:
    def __init__(self):
        self.root = tk.Tk()

        # title
        self.root.title(config.APPNAME + ' ' + config.VERSION)

        # window icon, using conversion to iso, cause tkinter doesn't accept jpg
        icon = tk.PhotoImage(file=config.WINDOW_ICON_PATH)
        self.root.wm_iconphoto(False, icon)

        # Window properties
        width = config.WIDTH
        height = config.HEIGHT
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.root.geometry(alignstr)
        self.root.resizable(width=True, height=True)

        self.root.configure(bg=config.BG_COLOR)

        self.root.minsize(300, 200)

        self.root.columnconfigure(0, weight=4)
        self.root.columnconfigure(1, weight=4)
        self.root.columnconfigure(2, weight=4)
        self.root.columnconfigure(3, weight=4)
        self.root.columnconfigure(4, weight=1)

        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)
        self.root.rowconfigure(2, weight=4)
        self.root.rowconfigure(3, weight=4)
        self.root.rowconfigure(5, weight=4)

        # Sample data:
        self.devices = {
            'R1': Router(name='R1',
                         ssh_information=SSHInformation(ip_addresses={'0': '10.250.250.1',
                                                                      '1': '10.250.250.2'}),
                         type='cisco',
                         enable_password='ZSEDCxzaqwe',
                         interfaces={'f0/0': RouterInterface(name='f0/0',
                                                             description='test1',
                                                             statistics=InterfaceStatistics(
                                                                 information=InformationStatistics(
                                                                     collision=1,
                                                                     late_collision=12,
                                                                     broadcast=234,
                                                                     packets_input=45,
                                                                     packets_output=76,
                                                                     duplex='full',
                                                                     speed='100 Mb/s',
                                                                     layer1_status='up',
                                                                     layer2_status='up',
                                                                     mtu=1500,
                                                                     encapsulation='XD'
                                                                 ),
                                                                 errors=ErrorsStatistics(
                                                                     input_errors=123,
                                                                     output_errors=45,
                                                                     output_buffer_failures=34,
                                                                     runts=9,
                                                                     giants=0,
                                                                     crc=56,
                                                                     frame=4,
                                                                     throttles=9,
                                                                     overrun=0,
                                                                     ignored=0
                                                                 )
                                                             ),
                                                             ip_address='23.45.67.43',
                                                             subnet=24,
                                                             ospf=InterfaceOSPFInformation(
                                                                 network_type='broadcast',
                                                                 cost=10,
                                                                 state='DR',
                                                                 passive_interface=False,
                                                                 priority=10,
                                                                 timers=OSPFTimers(hello_timer=5,
                                                                                   dead_timer=20,
                                                                                   wait_timer=20,
                                                                                   retransmit_timer=30
                                                                                   )
                                                             )
                                                             )
                                     },
                         static_routes={'192.168.1.0/24': StaticRoute(network=Network(network='192.168.1.0',
                                                                                      mask=24,
                                                                                      wildcard='0.0.0.255'
                                                                                      ),
                                                                      distance=1,
                                                                      next_hop='12.345.32.1',
                                                                      interface='f0/0')
                                        },
                         ospf=OSPFInformation(router_id='1.1.1.1',
                                              auto_cost_reference_bandwidth=1000,
                                              default_information_originate=False,
                                              default_metric_of_redistributed_routes=10,
                                              distance=110,
                                              maximum_paths=2,
                                              passive_interface_default=False,
                                              redistribution=Redistribution(is_redistribute_static=True,
                                                                            is_redistribute_bgp=False,
                                                                            is_redistribute_rip=False,
                                                                            is_redistribute_connected=True
                                                                            ),
                                              areas={'0': OSPFArea(id='0',
                                                                   is_authentication_message_digest=False,
                                                                   type='NSSA',
                                                                   networks={'10.0.0.0/16': Network(network='10.0.0.0',
                                                                                                    mask=16,
                                                                                                    wildcard='0.0.255.255'
                                                                                                    ),
                                                                             '20.0.0.0/16': Network(network='20.0.0.0',
                                                                                                    mask=16,
                                                                                                    wildcard='0.0.255.255'
                                                                                                    )
                                                                             }
                                                                   ),
                                                     '1': OSPFArea(id='1',
                                                                   is_authentication_message_digest=False,
                                                                   type='NSSA',
                                                                   networks={'10.0.0.0/16': Network(network='10.0.0.0',
                                                                                                    mask=16,
                                                                                                    wildcard='0.0.255.255'
                                                                                                    ),
                                                                             '30.0.0.0/16': Network(network='30.0.0.0',
                                                                                                    mask=16,
                                                                                                    wildcard='0.0.255.255'
                                                                                                    )
                                                                             }
                                                                   ),
                                                     }
                                              ),
                         ),
            'R2': Router(name='R2',
                         ssh_information=SSHInformation(ip_addresses={'0': '10.250.250.1'}),
                         type='cisco',
                         enable_password='ZSEDCxzaqwe',
                         interfaces={'f0/0': RouterInterface(name='f0/0',
                                                             description='test',
                                                             statistics=InterfaceStatistics(
                                                                 information=InformationStatistics(
                                                                     collision=1,
                                                                     late_collision=12,
                                                                     broadcast=234,
                                                                     packets_input=45,
                                                                     packets_output=76,
                                                                     duplex='full',
                                                                     speed='100 Mb/s',
                                                                     layer1_status='up',
                                                                     layer2_status='up',
                                                                     mtu=1500,
                                                                     encapsulation='XD'
                                                                 ),
                                                                 errors=ErrorsStatistics(
                                                                     input_errors=123,
                                                                     output_errors=45,
                                                                     output_buffer_failures=34,
                                                                     runts=9,
                                                                     giants=0,
                                                                     crc=56,
                                                                     frame=4,
                                                                     throttles=9,
                                                                     overrun=0,
                                                                     ignored=0
                                                                 )
                                                             ),
                                                             ip_address='23.45.67.43',
                                                             subnet=24,
                                                             ospf=InterfaceOSPFInformation(
                                                                 network_type='broadcast',
                                                                 cost=10,
                                                                 state='DR',
                                                                 passive_interface=False,
                                                                 priority=10,
                                                                 timers=OSPFTimers(hello_timer=5,
                                                                                   dead_timer=20,
                                                                                   wait_timer=20,
                                                                                   retransmit_timer=30
                                                                                   )
                                                             )
                                                             )
                                     },
                         static_routes={'192.168.1.0/24': StaticRoute(network=Network(network='192.168.1.0',
                                                                                      mask=24,
                                                                                      wildcard='0.0.0.255'
                                                                                      ),
                                                                      next_hop='12.345.32.1',
                                                                      interface='f0/0')
                                        },
                         ospf=OSPFInformation(router_id='1.1.1.1',
                                              auto_cost_reference_bandwidth=1000,
                                              default_information_originate=False,
                                              default_metric_of_redistributed_routes=10,
                                              distance=110,
                                              maximum_paths=2,
                                              passive_interface_default=False,
                                              redistribution=Redistribution(is_redistribute_static=True,
                                                                            is_redistribute_bgp=False,
                                                                            is_redistribute_rip=False,
                                                                            is_redistribute_connected=True
                                                                            ),
                                              areas={'0': OSPFArea(id='0',
                                                                   is_authentication_message_digest=False,
                                                                   type='NSSA',
                                                                   networks={'10.0.0.0/16': Network(network='10.0.0.0',
                                                                                                    mask=16,
                                                                                                    wildcard='0.0.255.255'
                                                                                                    )
                                                                             }
                                                                   )
                                                     }
                                              ),
                         )
        }

        treeColumns = ()  # default

        # This frame contains scrollbars and treeview widget
        treeFrame = tk.Frame(self.root)
        treeFrame.grid(column=0, row=0, padx=2, pady=2, columnspan=4, rowspan=5, sticky='NSEW')
        treeFrame.configure(bg=config.BG_COLOR)
        treeFrame.grid_rowconfigure(0, weight=1)
        treeFrame.grid_columnconfigure(0, weight=1)

        verticalScrollbar = tk.Scrollbar(treeFrame, orient='vertical')
        verticalScrollbar.grid(column=1, row=0, sticky='NS')

        horizontalScrollbar = tk.Scrollbar(treeFrame, orient='horizontal')
        horizontalScrollbar.grid(column=0, row=1, sticky='EW')

        self.tree = ttk.Treeview(treeFrame, columns=treeColumns, show='headings',
                                 xscrollcommand=horizontalScrollbar.set, yscrollcommand=verticalScrollbar.set)
        self.tree.grid(column=0, row=0, sticky='NSEW')

        verticalScrollbar.config(command=self.tree.yview)
        horizontalScrollbar.config(command=self.tree.xview)

        # Style configuration, font and fontsize -> changeable in config.py
        style = ttk.Style()
        style.configure('Custom.Treeview', font=(config.FONT, config.FONTSIZE))
        style.configure('Treeview.Heading', font=(config.FONT, config.FONTSIZE))
        self.tree.configure(style='Custom.Treeview')

        # MenuBar configuration
        menubar = tk.Menu(self.root)
        viewmenu = tk.Menu(menubar, tearoff=False)
        viewmenu.add_command(label='All', command=self.show_view_all)
        viewmenu.add_command(label='RIP', command=self.show_view_rip)
        viewmenu.add_command(label='OSPF', command=self.show_view_ospf)
        viewmenu.add_command(label='BGP', command=self.show_view_bgp)
        menubar.add_cascade(label='View', menu=viewmenu)

        self.root.config(menu=menubar)

        # Frame containing SSH Button and Add Router
        btnFrameAddSSH = tk.Frame(self.root)
        btnFrameAddSSH.grid(column=5, row=0, padx=10)

        btnAddRouter = tk.Button(btnFrameAddSSH, text='Add Router', command=self.btnAddRouter_command)
        btnAddRouter.grid(column=0, row=0, sticky='EW')

        btnSSHPassword = tk.Button(btnFrameAddSSH, text='SSH Password', padx=2, pady=2,
                                   command=ssh_password_gui.SSHPasswordGUI)
        btnSSHPassword.grid(column=0, row=1)

        # Frame containing Logout and Quit buttons
        btnFrameLogoutQuit = tk.Frame(self.root)
        btnFrameLogoutQuit.grid(column=5, row=4, sticky='NESW', padx=10)
        btnFrameLogoutQuit.configure(bg=config.BG_COLOR)
        btnLogOut = tk.Button(btnFrameLogoutQuit, text='Log Out', command=self.log_out)
        btnLogOut.grid(column=0, row=0, sticky='EWS')

        QUIT_ICON = Image.open(config.QUIT_ICON_PATH)
        QUIT_ICON = QUIT_ICON.resize((24, 24))
        quit_icon = ImageTk.PhotoImage(QUIT_ICON)
        btnQuit = tk.Button(btnFrameLogoutQuit, text='Quit', image=quit_icon, compound=tk.RIGHT,
                            command=self.root.destroy)
        btnQuit.grid(column=0, row=1, sticky='EWS')

        consoleFrame = tk.Frame(self.root)
        consoleScrollbar = tk.Scrollbar(consoleFrame, orient='vertical')
        consoleScrollbar.pack(side='right', fill='y')

        self.consoleBox = tk.Listbox(consoleFrame)
        self.consoleBox.pack(side='left', fill='both', expand=True)
        self.consoleBox.config(yscrollcommand=consoleScrollbar.set)

        consoleScrollbar.config(command=self.consoleBox.yview)
        consoleFrame.grid(column=0, row=5, sticky='NESW', padx=2, columnspan=4)

        for i in range(1, 100):
            self.console_command('test' + str(i))

        # For first data insert load 'all' view
        self.show_view_all()
        self.root.mainloop()

    # This function exits 'main_gui' view and launches loginGUI
    def log_out(self) -> None:
        self.root.destroy()
        LoginGUI()
        return None

    def btnAddRouter_command(self):
        return None

    # This function inserts data into treeview widget and binds <MB-3> according to 'all' view
    def show_view_all(self) -> None:
        self.clear_tree()

        treeColumns = ('No', 'Hostname', 'Type', 'SSH Address')
        self.tree.configure(columns=treeColumns)

        iid = 0
        for i, (router_name, router) in enumerate(self.devices.items(), start=1):
            ssh_ip = router.ssh_information.ip_addresses['0']
            values = (i, router.name, router.type, ssh_ip)
            self.tree.insert('', tk.END, values=values, iid=iid)

            # inserting as sub values additional ssh ips
            if len(router.ssh_information.ip_addresses) > 1:
                for j, ip in router.ssh_information.ip_addresses.items():
                    if j != '0':
                        ssh_ips = ('', '', '', ip)
                        self.tree.insert(iid, tk.END, values=ssh_ips)  # this need to be fixed so it skips first item
            iid += 1

        self.tree.configure(columns=treeColumns)

        self.tree.heading(treeColumns[0], text='No', anchor='w')
        self.tree.column(treeColumns[0], minwidth=30, width=30, stretch=False)

        self.tree.heading(treeColumns[1], text='Hostname', anchor='w')
        self.tree.column(treeColumns[1], minwidth=70, width=70, stretch=True)

        self.tree.heading(treeColumns[2], text='Type', anchor='w')
        self.tree.column(treeColumns[2], minwidth=50, width=50, stretch=True)

        self.tree.heading(treeColumns[3], text='SSH Addresses', anchor='w')
        self.tree.column(treeColumns[3], minwidth=90, stretch=True)

        # This function defines pop-up menu for 'all' view
        def show_menu_all(event):
            item = self.tree.identify_row(event.y)
            self.tree.selection_set(item)
            if item:
                try:
                    hostname = self.tree.item(item)['values'][1]
                    selected_router = self.devices.get(hostname)
                    menu.post(event.x_root, event.y_root)
                    menu.entryconfigure('Interfaces', command=lambda: show_interfaces_details(selected_router))
                    menu.entryconfigure('Static routes', command=lambda: show_static_routes(selected_router))
                except IndexError():
                    pass

        # This function launches InterfacesDetails window when 'Interfaces' is clicked from menu on <MB-3>
        def show_interfaces_details(selected_router: Router):
            if selected_router:
                InterfacesDetails(selected_router)
            return None

        def show_static_routes(selected_router: Router) -> None:
            if selected_router:
                StaticRoutesGUI(selected_router)
            return None

        menu = tk.Menu(self.root, tearoff=False)
        menu.add_command(label='Interfaces', command=show_interfaces_details)
        menu.add_command(label='Static routes', command=show_static_routes)
        self.tree.bind('<Button-3>', show_menu_all)

        return None

    def show_view_rip(self) -> None:
        self.clear_tree()
        return None

    def show_view_bgp(self) -> None:
        self.clear_tree()
        return None

    # This function inserts data into treeview widget and binds <MB-3> according to 'ospf' view
    def show_view_ospf(self) -> None:
        self.clear_tree()

        treeColumns = ('No', 'Hostname', 'Router ID', 'Areas', 'Networks', 'Redistribution')
        self.tree.configure(columns=treeColumns)

        # Data insert
        for iid, (router_name, router) in enumerate(self.devices.items(), start=1):
            ospf_area = router.ospf.areas['0'].id
            ospf_networks = list(router.ospf.areas[ospf_area].networks.keys())
            ospf_redistributions = self.get_ospf_redistribution(router)

            values = (iid, router.name, router.ospf.router_id, ospf_area, ospf_networks, ospf_redistributions)
            self.tree.insert('', tk.END, values=values, iid=iid)

            if len(router.ospf.areas) > 1:
                for j, area in router.ospf.areas.items():
                    if j != '0':
                        values = ('', '', '', area.id, list(router.ospf.areas[area.id].networks.keys()), '')
                        self.tree.insert(iid, tk.END, values=values)

        self.tree.heading(treeColumns[0], text='No', anchor='w')
        self.tree.column(treeColumns[0], minwidth=30, width=30, stretch=False)

        self.tree.heading(treeColumns[1], text='Hostname', anchor='w')
        self.tree.column(treeColumns[1], minwidth=70, width=70, stretch=False)

        self.tree.heading(treeColumns[2], text='Router ID', anchor='w')
        self.tree.column(treeColumns[2], minwidth=70, width=70, stretch=False)

        self.tree.heading(treeColumns[3], text='Areas', anchor='w')
        self.tree.column(treeColumns[3], minwidth=50, width=50, stretch=False)

        self.tree.heading(treeColumns[4], text='Networks', anchor='w')
        self.tree.column(treeColumns[4], minwidth=50, stretch=False)

        self.tree.heading(treeColumns[5], text='Redistribution', anchor='w')
        self.tree.column(treeColumns[5], minwidth=70, stretch=False)

        # This function shows menu when <MB-3> is clicked with treeview item selected
        def show_menu_ospf(event):
            item = self.tree.identify_row(event.y)
            self.tree.selection_set(item)
            if item:
                try:
                    hostname = self.tree.item(item)['values'][1]
                    selected_router = self.devices.get(hostname)
                    menu.post(event.x_root, event.y_root)
                    menu.entryconfigure('Interfaces', command=lambda: show_interfaces_details(selected_router))
                except IndexError():
                    pass

        def show_interfaces_details(selected_router: Router) -> None:
            if selected_router:
                OSPFInterfaceDetailsGUI(selected_router)
            return None

        menu = tk.Menu(self.root, tearoff=False)
        menu.add_command(label='Interfaces', command=OSPFInterfaceDetailsGUI)
        self.tree.bind('<Button-3>', show_menu_ospf)

        self.console_command('test')

        return None

    def get_ospf_redistribution(self, router) -> str:
        ospf_redistribution = ''
        if router.ospf.redistribution.is_redistribute_static is True:
            ospf_redistribution += 'Static, '
        if router.ospf.redistribution.is_redistribute_connected is True:
            ospf_redistribution += 'Connected, '
        if router.ospf.redistribution.is_redistribute_rip is True:
            ospf_redistribution += 'RIP, '
        if router.ospf.redistribution.is_redistribute_bgp is True:
            ospf_redistribution += 'BGP, '
        ospf_redistribution = ospf_redistribution.rstrip(', ')
        return ospf_redistribution

    # This function clears contents of treeview
    def clear_tree(self) -> None:
        for item in self.tree.get_children():
            self.tree.delete(item)
        treeColumns = ()
        self.tree.configure(columns=treeColumns)
        return None

    def console_command(self, text: str) -> None:
        self.consoleBox.insert(tk.END, text)
        return None


if __name__ == "__main__":
    MainGUI()
