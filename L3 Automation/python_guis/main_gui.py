import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

import ssh_password_gui
from gui_resources import config
from login_gui import LoginGUI
from python_guis.bgp_neighbors_gui import BGPNeighborsGUI
from python_guis.bgp_redistribution_gui import BGPRedistributionGUI
from python_guis.interfaces_details_gui import InterfacesDetails
from python_guis.ospf_area_configuration_gui import OSPFAreaConfigurationGUI
from python_guis.ospf_interface_details_gui import OSPFInterfaceDetailsGUI
from python_guis.rip_network_add_gui import RIPNetworkAddGUI
from python_guis.rip_networks_gui import RIPNetworksGUI
from python_guis.rip_redistribution_gui import RIPRedistributionGUI
from python_guis.static_routes_gui import StaticRoutesGUI

from resources.devices.Router import Router
from resources.interfaces.InterfaceOSPFInformation import InterfaceOSPFInformation
from resources.interfaces.InterfaceStatistics import InterfaceStatistics, InformationStatistics, ErrorsStatistics
from resources.interfaces.RouterInterface import RouterInterface
from resources.routing_protocols.Network import Network
from resources.routing_protocols.Redistribution import Redistribution
from resources.routing_protocols.StaticRoute import StaticRoute
from resources.routing_protocols.bgp.BGPInformation import BGPInformation
from resources.routing_protocols.bgp.BGPNeighbor import BGPNeighbor
from resources.routing_protocols.bgp.BGPTimers import BGPTimers
from resources.routing_protocols.ospf.OSPFArea import OSPFArea
from resources.routing_protocols.ospf.OSPFInformation import OSPFInformation
from resources.routing_protocols.ospf.OSPFTimers import OSPFTimers
from resources.routing_protocols.rip.RIPInformation import RIPInformation
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
        self.devices = devices = {
            'R1': Router(name='R1',
                         ssh_information=SSHInformation(ip_addresses={'0': '10.250.250.1',
                                                                      '1': '13.13.13.13'}),
                         type='cisco',
                         enable_password='ZSEDCxzaqwe',
                         interfaces={'f0/0': RouterInterface(name='f0/0',
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
                         static_routes=[StaticRoute(network=Network(network='192.168.1.0',
                                                                    mask=24,
                                                                    wildcard='0.0.0.255'
                                                                    ),
                                                    next_hop='12.345.32.1',
                                                    interface='f0/0')
                                        ],
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
                         ),
            'R2': Router(name='R2',
                         ssh_information=SSHInformation(ip_addresses={'0': '10.250.250.1'}),
                         type='cisco',
                         enable_password='ZSEDCxzaqwe',
                         interfaces={'f0/0': RouterInterface(name='f0/0',
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
                         static_routes=[StaticRoute(network=Network(network='192.168.1.0',
                                                                    mask=24,
                                                                    wildcard='0.0.0.255'
                                                                    ),
                                                    next_hop='12.345.32.1',
                                                    interface='f0/0')
                                        ],
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
                                                                   networks={
                                                                       '10.0.0.0/16': Network(
                                                                           network='10.0.0.0',
                                                                           mask=None,
                                                                           wildcard='0.0.255.255'
                                                                           )
                                                                   }
                                                                   ),
                                                     '10': OSPFArea(id='10',
                                                                    is_authentication_message_digest=True,
                                                                    type='NSSA',
                                                                    networks={
                                                                        '25.0.0.0/16': Network(
                                                                            network='25.0.0.0',
                                                                            mask=None,
                                                                            wildcard='0.0.255.255'
                                                                        )
                                                                    }
                                                                    )
                                                     }
                                              ),
                         rip=RIPInformation(auto_summary=True,
                                            default_information_originate=False,
                                            default_metric_of_redistributed_routes=14,
                                            distance=115,
                                            maximum_paths=2,
                                            version=2,
                                            redistribution=Redistribution(is_redistribute_static=True,
                                                                          is_redistribute_bgp=False,
                                                                          is_redistribute_ospf=False,
                                                                          is_redistribute_connected=True,
                                                                          ),
                                            networks={'10.1.0.0': Network(network='10.1.0.0', mask=None),
                                                      '192.168.3.0': Network(network='192.168.3.0', mask=None)}
                                            ),
                         bgp=BGPInformation(autonomous_system=666,
                                            router_id='1.1.1.1',
                                            default_information_originate=False,
                                            default_metric_of_redistributed_routes=5,
                                            timers=BGPTimers(keep_alive=20,
                                                             hold_time=60
                                                             ),
                                            networks={'10.1.0.0 255.255.255.0': Network(network='10.1.0.0', mask=24)},
                                            redistribution=Redistribution(is_redistribute_ospf=False,
                                                                          is_redistribute_connected=True,
                                                                          is_redistribute_static=False,
                                                                          is_redistribute_rip=True),
                                            neighbors={'10.22.33.2': BGPNeighbor(ip_address='10.22.33.2',
                                                                                 remote_as=456,
                                                                                 state='COS',
                                                                                 ebgp_multihop=3,
                                                                                 next_hop_self=False,
                                                                                 shutdown=False,
                                                                                 timers=BGPTimers(keep_alive=30,
                                                                                                  hold_time=90))}
                                            )
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
            ssh_ips = list(router.ssh_information.ip_addresses.values())
            string_ips = ', '.join(ssh_ips)

            values = (i, router.name, router.type, string_ips)
            self.tree.insert('', tk.END, values=values, iid=iid)

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

        treeColumns = ('No', 'Hostname', 'Auto-summary', 'Default information originate', 'Default metric',
                       'Distance', 'Maximum paths', 'Version')
        self.tree.configure(columns=treeColumns)

        self.tree.heading(treeColumns[0], text='No', anchor='w')
        self.tree.column(treeColumns[0], minwidth=30, width=30, stretch=False)

        self.tree.heading(treeColumns[1], text='Hostname', anchor='w')
        self.tree.column(treeColumns[1], minwidth=70, width=70, stretch=False)

        self.tree.heading(treeColumns[2], text='Auto-summary', anchor='w')
        self.tree.column(treeColumns[2], minwidth=50, width=100, stretch=False)

        self.tree.heading(treeColumns[3], text='Default information originate', anchor='w')
        self.tree.column(treeColumns[3], minwidth=100, width=150, stretch=False)

        self.tree.heading(treeColumns[4], text='Default metric', anchor='w')
        self.tree.column(treeColumns[4], minwidth=70, width=100, stretch=False)

        self.tree.heading(treeColumns[5], text='Distance', anchor='w')
        self.tree.column(treeColumns[5], minwidth=50, width=70, stretch=False)

        self.tree.heading(treeColumns[6], text='Maximum paths', anchor='w')
        self.tree.column(treeColumns[6], minwidth=50, width=120, stretch=False)

        self.tree.heading(treeColumns[7], text='Version', anchor='w')
        self.tree.column(treeColumns[7], minwidth=50, width=70, stretch=False)

        # Data insert
        iid = 0
        for i, (router_name, router) in enumerate(self.devices.items(), start=1):
            if router.rip is None:
                values = (iid+1, router.name, 'RIP DISABLED')
                self.tree.insert('', tk.END, iid=iid, values=values)
                iid += 1
            if router.rip is not None:
                values = (iid+1, router.name, router.rip.auto_summary, router.rip.default_information_originate,
                          router.rip.default_metric_of_redistributed_routes, router.rip.distance,
                          router.rip.maximum_paths, router.rip.version)
                self.tree.insert('', tk.END, iid=iid, values=values)
                iid += 1

        # This function shows menu when <MB-3> is clicked with treeview item selected
        def show_menu_rip(event):
            item = self.tree.identify_row(event.y)
            self.tree.selection_set(item)
            if item:
                try:
                    hostname = self.tree.item(item)['values'][1]
                    selected_router = self.devices.get(hostname)
                    if selected_router.rip is not None:
                        menu.post(event.x_root, event.y_root)
                        menu.entryconfigure('Networks', command=lambda: RIPNetworksGUI(selected_router))
                        menu.entryconfigure('Redistribution', command=lambda: RIPRedistributionGUI(selected_router))
                except IndexError:
                    pass

        menu = tk.Menu(self.root, tearoff=False)
        menu.add_command(label='Networks', command=RIPNetworkAddGUI)
        menu.add_command(label='Redistribution', command=RIPRedistributionGUI)
        self.tree.bind('<Button-3>', show_menu_rip)

        return None

    # def insert_rip_network(self, router: Router, network: Network):
    #     print('tutaj')
    #     # self.tree.item
    #     #

    def show_view_bgp(self) -> None:
        self.clear_tree()

        treeColumns = ('No', 'Hostname', 'AS', 'Router ID', 'Default information originate',
                       'Default metric of redistributed routers', 'Keep alive timer', 'Hold time timer')
        self.tree.configure(columns=treeColumns)

        self.tree.heading(treeColumns[0], text='No', anchor='w')
        self.tree.column(treeColumns[0], minwidth=30, width=30, stretch=False)

        self.tree.heading(treeColumns[1], text='Hostname', anchor='w')
        self.tree.column(treeColumns[1], minwidth=70, width=70, stretch=False)

        self.tree.heading(treeColumns[2], text='AS', anchor='w')
        self.tree.column(treeColumns[2], minwidth=50, width=100, stretch=False)

        self.tree.heading(treeColumns[3], text='Router ID', anchor='w')
        self.tree.column(treeColumns[3], minwidth=80, width=80, stretch=False)

        self.tree.heading(treeColumns[4], text='Default information originate', anchor='w')
        self.tree.column(treeColumns[4], minwidth=70, width=120, stretch=False)

        self.tree.heading(treeColumns[5], text='Default metric of redistributed routers', anchor='w')
        self.tree.column(treeColumns[5], minwidth=50, width=120, stretch=False)

        self.tree.heading(treeColumns[6], text='Keep alive timer', anchor='w')
        self.tree.column(treeColumns[6], minwidth=50, width=120, stretch=False)

        self.tree.heading(treeColumns[7], text='Hold time timer', anchor='w')
        self.tree.column(treeColumns[7], minwidth=50, width=120, stretch=False)

        # Data insert
        iid = 0
        for i, (router_name, router) in enumerate(self.devices.items(), start=1):
            if router.bgp is None:
                values = (iid + 1, router.name, 'BGP DISABLED')
                self.tree.insert('', tk.END, iid=iid, values=values)
                iid += 1
            if router.bgp is not None:
                values = (iid + 1, router.name, router.bgp.autonomous_system, router.bgp.router_id,
                          router.bgp.default_information_originate, router.bgp.default_metric_of_redistributed_routes,
                          router.bgp.timers.keep_alive, router.bgp.timers.hold_time)
                self.tree.insert('', tk.END, iid=iid, values=values)
                iid += 1

        def show_menu_bgp(event):
            item = self.tree.identify_row(event.y)
            self.tree.selection_set(item)
            if item:
                try:
                    hostname = self.tree.item(item)['values'][1]
                    selected_router = self.devices.get(hostname)
                    if selected_router.bgp is not None:
                        menu.post(event.x_root, event.y_root)
                        menu.entryconfigure('Neighbors', command=lambda: BGPNeighborsGUI(selected_router))
                        menu.entryconfigure('Redistribution', command=lambda: BGPRedistributionGUI(selected_router))

                except IndexError:
                    pass

        menu = tk.Menu(self.root, tearoff=False)
        menu.add_command(label='Neighbors', command=BGPNeighborsGUI)
        menu.add_command(label='Redistribution', command=BGPRedistributionGUI)
        self.tree.bind('<Button-3>', show_menu_bgp)

        return None

    # This function inserts ospf data into treeview widget and binds <MB-3> according to 'ospf' view
    def show_view_ospf(self) -> None:
        self.clear_tree()

        treeColumns = ('No', 'Hostname', 'Router ID', 'Areas', 'Networks', 'Redistribution')
        self.tree.configure(columns=treeColumns)

        # Data insert
        for iid, (router_name, router) in enumerate(self.devices.items(), start=1):
            if router.ospf is None:
                values = (iid, router.name, 'OSPF DISABLED')
                self.tree.insert('', tk.END, values=values, iid=iid)
            if router.ospf is not None:
                router_areas = list(router.ospf.areas.keys())
                ospf_area = router_areas[0]

                ospf_networks = list(router.ospf.areas[ospf_area].networks.keys())
                ospf_redistributions = self.get_ospf_redistribution(router)

                values = (iid, router.name, router.ospf.router_id, ospf_area, ospf_networks, ospf_redistributions)
                self.tree.insert('', tk.END, values=values, iid=iid)

                if len(router_areas) > 1:
                    for area in router_areas[1:]:
                            values = ('', router.name, '', router.ospf.areas[area].id,
                                      list(router.ospf.areas[area].networks.keys()), '')
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
                    if selected_router.ospf is not None:
                        area = self.tree.item(item)['values'][3]
                        selected_area = selected_router.ospf.areas.get(str(area))

                        menu.post(event.x_root, event.y_root)
                        menu.entryconfigure('Interfaces', command=lambda: show_interfaces_details(selected_router))
                        menu.entryconfigure('Area', command=lambda: run_ospf_area_configuration_gui(selected_router,
                                                                                                    selected_area))
                except IndexError:
                    pass

        def show_interfaces_details(selected_router: Router) -> None:
            if selected_router:
                OSPFInterfaceDetailsGUI(selected_router)
            return None

        def run_ospf_area_configuration_gui(selected_router:Router, selected_area: OSPFArea) -> None:
            if selected_area:
                OSPFAreaConfigurationGUI(selected_router, selected_area, self)
            return None

        menu = tk.Menu(self.root, tearoff=False)
        menu.add_command(label='Interfaces', command=OSPFInterfaceDetailsGUI)
        menu.add_command(label='Area', command=OSPFAreaConfigurationGUI)
        self.tree.bind('<Button-3>', show_menu_ospf)

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

    def update_ospf_networks(self, area: OSPFArea.id, network: Network):
        # todo
        pass


if __name__ == "__main__":
    MainGUI()
