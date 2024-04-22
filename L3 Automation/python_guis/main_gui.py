import platform
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import asksaveasfile, askopenfilename

from PIL import Image, ImageTk

from python_guis.add_router_gui import AddRouterGUI
from python_guis.bgp.bgp_add_router_gui import BGPAddRouterGUI
from python_guis.enable_password_gui import EnablePasswordGUI
from python_guis.ospf.ospf_add_router_gui import OSPFAddRouterGUI
from python_guis.rip.rip_add_router_gui import RIPAddRouterGUI
from python_guis.ssh import ssh_password_gui
from gui_resources import config
from login_gui import LoginGUI
from python_guis.bgp.bgp_edit_gui import BGPEditGUI
from python_guis.bgp.bgp_neighbors_gui import BGPNeighborsGUI
from python_guis.bgp.bgp_redistribution_gui import BGPRedistributionGUI
from python_guis.interface.interfaces_details_gui import InterfacesDetailsGUI
from python_guis.ospf.ospf_area_configuration_gui import OSPFAreaConfigurationGUI
from python_guis.ospf.ospf_interface_details_gui import OSPFInterfaceDetailsGUI
from python_guis.ospf.ospf_redistribution_gui import OSPFRedistributionGUI
from python_guis.rip.rip_edit_gui import RIPEditGUI
from python_guis.rip.rip_network_add_gui import RIPNetworkAddGUI
from python_guis.rip.rip_networks_gui import RIPNetworksGUI
from python_guis.rip.rip_redistribution_gui import RIPRedistributionGUI
from python_guis.ssh.ssh_connections_gui import SSHConnectionsGUI
from python_guis.static.static_routes_gui import StaticRoutesGUI
from python_guis import enable_password_gui
from resources.connect_frontend_with_backend.frontend_backend_functions import get_info_router

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
from resources.Project import Project
from resources.user.User import User


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
        self.project = Project()
        self.project.current_user = User(username='admin12', ssh_password='ZAQ!2wsx')
        # self.project.devices = {
        #     'R1': Router(name='R1',
        #                  ssh_information=SSHInformation(ip_addresses={'0': '10.250.250.1',
        #                                                               '1': '13.13.13.13'},),
        #                  type='cisco',
        #                  enable_password='ZSEDCxzaqwe',
        #                  interfaces={'f0/0': RouterInterface(name='f0/0',
        #                                                      statistics=InterfaceStatistics(
        #                                                          information=InformationStatistics(
        #                                                              collision=1,
        #                                                              late_collision=12,
        #                                                              broadcast=234,
        #                                                              packets_input=45,
        #                                                              packets_output=76,
        #                                                              duplex='full',
        #                                                              speed='100 Mb/s',
        #                                                              layer1_status='up',
        #                                                              layer2_status='up',
        #                                                              mtu=1500,
        #                                                              encapsulation='XD'
        #                                                          ),
        #                                                          errors=ErrorsStatistics(
        #                                                              input_errors=123,
        #                                                              output_errors=45,
        #                                                              output_buffer_failures=34,
        #                                                              runts=9,
        #                                                              giants=0,
        #                                                              crc=56,
        #                                                              frame=4,
        #                                                              throttles=9,
        #                                                              overrun=0,
        #                                                              ignored=0
        #                                                          )
        #                                                      ),
        #                                                      ip_address='23.45.67.43',
        #                                                      subnet=24,
        #                                                      ospf=InterfaceOSPFInformation(
        #                                                          network_type='broadcast',
        #                                                          cost=10,
        #                                                          state='DR',
        #                                                          passive_interface=False,
        #                                                          priority=10,
        #                                                          timers=OSPFTimers(hello_timer=5,
        #                                                                            dead_timer=20,
        #                                                                            wait_timer=20,
        #                                                                            retransmit_timer=30
        #                                                                            )
        #                                                      )
        #                                                      )
        #                              },
        #                  static_routes=[StaticRoute(network=Network(network='192.168.1.0',
        #                                                             mask=24,
        #                                                             wildcard='0.0.0.255'
        #                                                             ),
        #                                             next_hop='12.345.32.1',
        #                                             interface='f0/0')
        #                                 ],
        #                  ospf=OSPFInformation(router_id='1.1.1.1',
        #                                       auto_cost_reference_bandwidth=1000,
        #                                       default_information_originate=False,
        #                                       default_metric_of_redistributed_routes=10,
        #                                       distance=110,
        #                                       maximum_paths=2,
        #                                       passive_interface_default=False,
        #                                       redistribution=Redistribution(is_redistribute_static=True,
        #                                                                     is_redistribute_bgp=False,
        #                                                                     is_redistribute_rip=False,
        #                                                                     is_redistribute_connected=True
        #                                                                     ),
        #                                       areas={'0': OSPFArea(id='0',
        #                                                            is_authentication_message_digest=False,
        #                                                            type='NSSA',
        #                                                            networks={'10.0.0.0/16': Network(network='10.0.0.0',
        #                                                                                             mask=16,
        #                                                                                             wildcard='0.0.255.255'
        #                                                                                             )
        #                                                                      }
        #                                                            )
        #                                              }
        #                                       ),
        #                  ),
        #     'R2': Router(name='R2',
        #                  ssh_information=SSHInformation(ip_addresses={'0': '10.250.250.1'}),
        #                  type='cisco',
        #                  enable_password='ZSEDCxzaqwe',
        #                  interfaces={'f0/0': RouterInterface(name='f0/0',
        #                                                      statistics=InterfaceStatistics(
        #                                                          information=InformationStatistics(
        #                                                              collision=1,
        #                                                              late_collision=12,
        #                                                              broadcast=234,
        #                                                              packets_input=45,
        #                                                              packets_output=76,
        #                                                              duplex='full',
        #                                                              speed='100 Mb/s',
        #                                                              layer1_status='up',
        #                                                              layer2_status='up',
        #                                                              mtu=1500,
        #                                                              encapsulation='XD'
        #                                                          ),
        #                                                          errors=ErrorsStatistics(
        #                                                              input_errors=123,
        #                                                              output_errors=45,
        #                                                              output_buffer_failures=34,
        #                                                              runts=9,
        #                                                              giants=0,
        #                                                              crc=56,
        #                                                              frame=4,
        #                                                              throttles=9,
        #                                                              overrun=0,
        #                                                              ignored=0
        #                                                          )
        #                                                      ),
        #                                                      ip_address='23.45.67.43',
        #                                                      subnet=24,
        #                                                      ospf=InterfaceOSPFInformation(
        #                                                          network_type='broadcast',
        #                                                          cost=10,
        #                                                          state='DR',
        #                                                          passive_interface=False,
        #                                                          priority=10,
        #                                                          timers=OSPFTimers(hello_timer=5,
        #                                                                            dead_timer=20,
        #                                                                            wait_timer=20,
        #                                                                            retransmit_timer=30
        #                                                                            )
        #                                                      )
        #                                                      )
        #                              },
        #                  static_routes=[StaticRoute(network=Network(network='192.168.1.0',
        #                                                             mask=24,
        #                                                             wildcard='0.0.0.255'
        #                                                             ),
        #                                             next_hop='12.345.32.1',
        #                                             interface='f0/0')
        #                                 ],
        #                  ospf=OSPFInformation(router_id='1.1.1.1',
        #                                       auto_cost_reference_bandwidth=1000,
        #                                       default_information_originate=False,
        #                                       default_metric_of_redistributed_routes=10,
        #                                       distance=110,
        #                                       maximum_paths=2,
        #                                       passive_interface_default=False,
        #                                       redistribution=Redistribution(is_redistribute_static=True,
        #                                                                     is_redistribute_bgp=False,
        #                                                                     is_redistribute_rip=False,
        #                                                                     is_redistribute_connected=True
        #                                                                     ),
        #                                       areas={'0': OSPFArea(id='0',
        #                                                            is_authentication_message_digest=False,
        #                                                            type='NSSA',
        #                                                            networks={
        #                                                                '10.0.0.0/16': Network(
        #                                                                    network='10.0.0.0',
        #                                                                    mask=None,
        #                                                                    wildcard='0.0.255.255'
        #                                                                )
        #                                                            }
        #                                                            ),
        #                                              '10': OSPFArea(id='10',
        #                                                             is_authentication_message_digest=True,
        #                                                             type='NSSA',
        #                                                             networks={
        #                                                                 '25.0.0.0/16': Network(
        #                                                                     network='25.0.0.0',
        #                                                                     mask=None,
        #                                                                     wildcard='0.0.255.255'
        #                                                                 )
        #                                                             }
        #                                                             ),
        #                                              '20': OSPFArea(id='20',
        #                                                             is_authentication_message_digest=True,
        #                                                             type='NSSA',
        #                                                             networks={
        #                                                                 '25.0.0.0/16': Network(
        #                                                                     network='25.0.0.0',
        #                                                                     mask=None,
        #                                                                     wildcard='0.0.255.255'
        #                                                                 )
        #                                                             }
        #                                                             )
        #                                              }
        #                                       ),
        #                  rip=RIPInformation(auto_summary=True,
        #                                     default_information_originate=False,
        #                                     default_metric_of_redistributed_routes=14,
        #                                     distance=115,
        #                                     maximum_paths=2,
        #                                     version=2,
        #                                     redistribution=Redistribution(is_redistribute_static=True,
        #                                                                   is_redistribute_bgp=False,
        #                                                                   is_redistribute_ospf=False,
        #                                                                   is_redistribute_connected=True,
        #                                                                   ),
        #                                     networks={'10.1.0.0': Network(network='10.1.0.0', mask=24),
        #                                               '192.168.3.0': Network(network='192.168.3.0', mask=24)}
        #                                     ),
        #                  bgp=BGPInformation(autonomous_system=666,
        #                                     router_id='1.1.1.1',
        #                                     default_information_originate=False,
        #                                     default_metric_of_redistributed_routes=5,
        #                                     timers=BGPTimers(keep_alive=20,
        #                                                      hold_time=60
        #                                                      ),
        #                                     networks={'10.1.0.0 255.255.255.0': Network(network='10.1.0.0', mask=24)},
        #                                     redistribution=Redistribution(is_redistribute_ospf=False,
        #                                                                   is_redistribute_connected=True,
        #                                                                   is_redistribute_static=False,
        #                                                                   is_redistribute_rip=True),
        #                                     neighbors={'10.22.33.2': BGPNeighbor(ip_address='10.22.33.2',
        #                                                                          remote_as=456,
        #                                                                          state='COS',
        #                                                                          ebgp_multihop=3,
        #                                                                          next_hop_self=False,
        #                                                                          shutdown=False,
        #                                                                          timers=BGPTimers(keep_alive=30,
        #                                                                                           hold_time=90))}
        #                                     )
        #                  )
        # }

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

        filemenu = tk.Menu(menubar, tearoff=False)

        def save_as_project():
            # TODO Punkt 14
            files = [('L3 Project Files', '*.jkal')]
            file = asksaveasfile(filetypes=files)
            print(file.name)
            new_project = Project(file_path=file, devices=self.project.devices)
            ## TODO Punkt 7
            aes_key = 'zzzzxxxxccccvvvv'
            new_project.save_project(aes_key=aes_key)

        filemenu.add_command(label='Save project...', command=save_as_project)

        def save_project():
            ## TODO Punkt 8, 9 - zrobić save zwykłe
            # aes_key = ...
            # self.project.save_project(aes_key=aes_key)
            pass

        def open_project():
            files = [('L3 Project Files', '*.jkal')]
            file = askopenfilename(filetypes=files)
            self.project.file_path = file
            ## TODO Punkt 6
            aes_key = 'zzzzxxxxccccvvvv'
            self.project.open_project(aes_key)
            self.show_view_all()
            from resources.connect_frontend_with_backend.universal_router_commands import (get_rip, get_ospf, get_bgp,
                                                                                           get_all_interfaces,
                                                                                           get_static_routes)
            import threading

            for name, device in self.project.devices.items():
                self.project.devices[name].enable_password = 'ZSEDCxzaqwe'
                # print(self.project.devices[name].enable_password)
                # self.project.devices[name].rip = get_rip(None, self.project.devices[name], self.project.current_user)
                # self.project.devices[name].ospf = get_ospf(None, self.project.devices[name], self.project.current_user)
                # self.project.devices[name].bgp = get_bgp(None, self.project.devices[name], self.project.current_user)
                # self.project.devices[name].interfaces = get_all_interfaces(None, self.project.devices[name],
                #                                                            self.project.current_user)
                # self.project.devices[name].static_routes = get_static_routes(None, self.project.devices[name], self.project.current_user)
                # TODO po zrobieniu 25 usunąć tamto i katywować to (konieczna modyfikacja get_info_router
                threading.Thread(target=get_info_router,
                                 args=(self, self.project.devices[name], self.project.current_user)).start()

        filemenu.add_command(label='Open project...', command=open_project)
        menubar.add_cascade(label='File', menu=filemenu)
        self.root.config(menu=menubar)

        # Frame containing buttons
        btnFrameAddSSH = tk.Frame(self.root)
        btnFrameAddSSH.grid(column=5, row=0, padx=10)

        self.btnAddRouter = tk.Button(btnFrameAddSSH, text='Add Router')
        self.btnAddRouter.grid(column=0, row=0, sticky='EW')

        btnSSHPassword = tk.Button(btnFrameAddSSH, text='SSH Password', padx=2, pady=2,
                                   command=ssh_password_gui.SSHPasswordGUI)
        btnSSHPassword.grid(column=0, row=1, sticky='EW')

        btnEnablePassword = tk.Button(btnFrameAddSSH, text='Enable Password', padx=2, pady=2,
                                      command=EnablePasswordGUI)
        btnEnablePassword.grid(column=0, row=2, sticky='EW')

        btnCredentials = tk.Button(btnFrameAddSSH, text='Credentials', padx=2, pady=2,
                                   command=LoginGUI)
        btnCredentials.grid(column=0, row=3, sticky='EW')

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

        # For first data insert load 'all' view
        self.show_view_all()
        self.root.mainloop()

    # This function exits 'main_gui' view and launches loginGUI
    def log_out(self) -> None:
        self.root.destroy()
        LoginGUI()
        return None

    # This function inserts data into treeview widget and binds <MB-3> according to 'all' view
    def show_view_all(self) -> None:
        self.clear_tree()

        treeColumns = ('No', 'Hostname', 'Type', 'RIP', 'OSPF', 'BGP')
        self.tree.configure(columns=treeColumns)

        iid = 0
        for i, (router_name, router) in enumerate(self.project.devices.items(), start=1):

            rip = ''
            if router.rip is not None:
                rip = 'Enabled'
            ospf = ''
            if router.ospf is not None:
                ospf = 'Enabled'
            bgp = ''
            if router.bgp is not None:
                bgp = 'Enabled'

            values = (i, router.name, router.type, rip, ospf, bgp)
            self.tree.insert('', tk.END, values=values, iid=iid)

            iid += 1

        self.tree.configure(columns=treeColumns)

        self.tree.heading(treeColumns[0], text='No', anchor='w')
        self.tree.column(treeColumns[0], minwidth=30, width=30, stretch=False)

        self.tree.heading(treeColumns[1], text='Hostname', anchor='w')
        self.tree.column(treeColumns[1], minwidth=70, width=70, stretch=True)

        self.tree.heading(treeColumns[2], text='Type', anchor='w')
        self.tree.column(treeColumns[2], minwidth=50, width=50, stretch=True)

        self.tree.heading(treeColumns[3], text='RIP', anchor='w')
        self.tree.column(treeColumns[3], minwidth=50, width=50, stretch=True)

        self.tree.heading(treeColumns[4], text='OSPF', anchor='w')
        self.tree.column(treeColumns[4], minwidth=50, width=50, stretch=True)

        self.tree.heading(treeColumns[5], text='BGP', anchor='w')
        self.tree.column(treeColumns[5], minwidth=50, width=50, stretch=True)

        # This function defines pop-up menu for 'all' view
        def show_menu_all(event):
            print('showed')
            item = self.tree.identify_row(event.y)
            self.tree.selection_set(item)
            if item:
                try:
                    hostname = self.tree.item(item)['values'][1]
                    selected_router = self.project.devices.get(hostname)
                    menu.post(event.x_root, event.y_root)
                    menu.entryconfigure('SSH Addresses', command=lambda: SSHConnectionsGUI(selected_router))
                    menu.entryconfigure('Interfaces', command=lambda: show_interfaces_details(selected_router))
                    menu.entryconfigure('Static routes', command=lambda: show_static_routes(self, selected_router,
                                                                                            self.project.current_user))
                except IndexError():
                    pass

        # This function launches InterfacesDetails window when 'Interfaces' is clicked from menu on <MB-3>
        def show_interfaces_details(selected_router: Router):
            if selected_router:
                InterfacesDetailsGUI(self, selected_router, self.project.current_user)
            return None

        def show_static_routes(main_gui, selected_router: Router, user: User) -> None:
            if selected_router:
                StaticRoutesGUI(main_gui, selected_router, user)
            return None

        def show_ssh_addresses(selected_router: Router) -> None:
            if selected_router:
                SSHConnectionsGUI(selected_router)
            return None

        menu = tk.Menu(self.root, tearoff=False)
        menu.add_command(label='SSH Addresses', command=show_ssh_addresses)
        menu.add_command(label='Interfaces', command=show_interfaces_details)
        menu.add_command(label='Static routes', command=show_static_routes)
        if platform.system() == 'Windows':
            self.tree.bind('<Button-3>', show_menu_all)
        if platform.system() == 'Darwin':
            self.tree.bind('<Button-2>', show_menu_all)

        def add_router_all():
            AddRouterGUI(self, self.project.current_user)

        self.btnAddRouter.config(command=add_router_all)

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
        self.tree.column(treeColumns[3], minwidth=100, width=200, stretch=False)

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
        for i, (router_name, router) in enumerate(self.project.devices.items(), start=1):
            if router.rip is not None:
                values = (iid + 1, router.name, router.rip.auto_summary, router.rip.default_information_originate,
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
                    selected_router = self.project.devices.get(hostname)
                    if selected_router.rip is not None:
                        menu.post(event.x_root, event.y_root)
                        menu.entryconfigure('Edit', command=lambda: RIPEditGUI(self, selected_router,
                                                                               self.project.current_user))
                        menu.entryconfigure('Networks', command=lambda: RIPNetworksGUI(self, selected_router,
                                                                                       self.project.current_user))
                        menu.entryconfigure('Redistribution', command=lambda: RIPRedistributionGUI(self,
                                                                                                   selected_router,
                                                                                                   self.project.current_user))
                except IndexError:
                    pass

        menu = tk.Menu(self.root, tearoff=False)
        menu.add_command(label='Edit', command=RIPEditGUI)
        menu.add_command(label='Networks', command=RIPNetworkAddGUI)
        menu.add_command(label='Redistribution', command=RIPRedistributionGUI)
        if platform.system() == 'Windows':
            self.tree.bind('<Button-3>', show_menu_rip)
        if platform.system() == 'Darwin':
            self.tree.bind('<Button-2>', show_menu_rip)

        def add_router_rip():
            RIPAddRouterGUI(self, self.project.current_user)

        self.btnAddRouter.config(command=add_router_rip)

        return None

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
        self.tree.column(treeColumns[4], minwidth=70, width=200, stretch=False)

        self.tree.heading(treeColumns[5], text='Default metric of redistributed routes', anchor='w')
        self.tree.column(treeColumns[5], minwidth=50, width=230, stretch=False)

        self.tree.heading(treeColumns[6], text='Keep alive timer', anchor='w')
        self.tree.column(treeColumns[6], minwidth=50, width=120, stretch=False)

        self.tree.heading(treeColumns[7], text='Hold time timer', anchor='w')
        self.tree.column(treeColumns[7], minwidth=50, width=120, stretch=False)

        # Data insert
        iid = 0
        for i, (router_name, router) in enumerate(self.project.devices.items(), start=1):
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
                    selected_router = self.project.devices.get(hostname)
                    if selected_router.bgp is not None:
                        menu.post(event.x_root, event.y_root)
                        menu.entryconfigure('Edit', command=lambda: BGPEditGUI(self, selected_router,
                                                                               self.project.current_user))
                        menu.entryconfigure('Neighbors', command=lambda: BGPNeighborsGUI(self, selected_router,
                                                                                         self.project.current_user))
                        menu.entryconfigure('Redistribution', command=lambda: BGPRedistributionGUI(self,
                                                                                                   selected_router,
                                                                                                   self.project.current_user))
                except IndexError:
                    pass

        menu = tk.Menu(self.root, tearoff=False)
        menu.add_command(label='Edit', command=BGPEditGUI)
        menu.add_command(label='Neighbors', command=BGPNeighborsGUI)
        menu.add_command(label='Redistribution', command=BGPRedistributionGUI)
        if platform.system() == 'Windows':
            self.tree.bind('<Button-3>', show_menu_all)
        if platform.system() == 'Darwin':
            self.tree.bind('<Button-2>', show_menu_all)

        self.btnAddRouter.config(command=lambda: BGPAddRouterGUI(self, self.project.current_user))

        return None

    # This function inserts ospf data into treeview widget and binds <MB-3> according to 'ospf' view
    def show_view_ospf(self) -> None:
        self.clear_tree()

        treeColumns = ('No', 'Hostname', 'Router ID', 'Areas', 'Auto cost bandwidth', 'Default information originate',
                       'Default metric of redistributed routes', 'Distance', 'Maximum paths')
        self.tree.configure(columns=treeColumns)

        # Data insert
        for iid, (router_name, router) in enumerate(self.project.devices.items(), start=1):
            if router.ospf is not None:
                router_areas = list(router.ospf.areas.keys())
                ospf_area = str(router_areas[0])
                if len(router_areas) > 1:
                    ospf_area += '*'
                values = (iid, router.name, router.ospf.router_id, ospf_area,
                          router.ospf.auto_cost_reference_bandwidth, router.ospf.default_information_originate,
                          router.ospf.default_metric_of_redistributed_routes, router.ospf.distance,
                          router.ospf.maximum_paths)
                self.tree.insert('', tk.END, values=values, iid=iid)

                if len(router_areas) > 1:
                    for area in router_areas[1:]:
                        values = ('', router.name, '', router.ospf.areas[area].id)
                        self.tree.insert(iid, tk.END, values=values)

        self.tree.heading(treeColumns[0], text='No', anchor='w')
        self.tree.column(treeColumns[0], minwidth=30, width=30, stretch=False)

        self.tree.heading(treeColumns[1], text='Hostname', anchor='w')
        self.tree.column(treeColumns[1], minwidth=70, width=70, stretch=False)

        self.tree.heading(treeColumns[2], text='Router ID', anchor='w')
        self.tree.column(treeColumns[2], minwidth=70, width=70, stretch=False)

        self.tree.heading(treeColumns[3], text='Areas', anchor='w')
        self.tree.column(treeColumns[3], minwidth=50, width=50, stretch=False)

        self.tree.heading(treeColumns[4], text='Auto cost reference bandwidth', anchor='w')
        self.tree.column(treeColumns[4], minwidth=50, width=200, stretch=False)

        self.tree.heading(treeColumns[5], text='Default information originate', anchor='w')
        self.tree.column(treeColumns[5], minwidth=50, width=200, stretch=False)

        self.tree.heading(treeColumns[6], text='Default metric of redistributed routes', anchor='w')
        self.tree.column(treeColumns[6], minwidth=50, width=230, stretch=False)

        self.tree.heading(treeColumns[7], text='Distance', anchor='w')
        self.tree.column(treeColumns[7], minwidth=50, width=70, stretch=False)

        self.tree.heading(treeColumns[8], text='Maximum paths', anchor='w')
        self.tree.column(treeColumns[8], minwidth=50, width=100, stretch=False)

        # This function shows menu when <MB-3> is clicked with treeview item selected
        def show_menu_ospf(event):
            item = self.tree.identify_row(event.y)
            self.tree.selection_set(item)
            if item:
                try:
                    hostname = str(self.tree.item(item)['values'][1])
                    selected_router = self.get_router(hostname)
                    if selected_router.ospf is not None:
                        area = self.tree.item(item)['values'][3]
                        if type(area) is str:
                            area = area.replace('*', '')
                        selected_area = selected_router.ospf.areas.get(str(area))

                        menu.post(event.x_root, event.y_root)
                        menu.entryconfigure('Interfaces', command=lambda: show_interfaces_details(selected_router))
                        menu.entryconfigure('Area', command=lambda: run_ospf_area_configuration_gui(selected_router,
                                                                                                    selected_area))
                        menu.entryconfigure('Redistribution', command=lambda: show_redistribution(selected_router))
                except IndexError:
                    pass

        def show_interfaces_details(selected_router: Router) -> None:
            if selected_router:
                OSPFInterfaceDetailsGUI(self, selected_router, self.project.current_user)
            return None

        def run_ospf_area_configuration_gui(selected_router: Router, selected_area: OSPFArea) -> None:
            if selected_area:
                OSPFAreaConfigurationGUI(self, selected_router, self.project.current_user, selected_area)
            return None

        def show_redistribution(selected_router: Router) -> None:
            if selected_router:
                OSPFRedistributionGUI(self, selected_router, self.project.current_user)
            return None

        menu = tk.Menu(self.root, tearoff=False)
        menu.add_command(label='Interfaces', command=OSPFInterfaceDetailsGUI)
        menu.add_command(label='Area', command=OSPFAreaConfigurationGUI)
        menu.add_command(label='Redistribution', command=OSPFRedistributionGUI)
        if platform.system() == 'Windows':
            self.tree.bind('<Button-3>', show_menu_ospf)
        if platform.system() == 'Darwin':
            self.tree.bind('<Button-2>', show_menu_ospf)

        self.btnAddRouter.config(command=lambda: OSPFAddRouterGUI(self, self.project.current_user))

        return None

    # This function clears contents of treeview
    def clear_tree(self) -> None:
        for item in self.tree.get_children():
            self.tree.delete(item)
        treeColumns = ()
        self.tree.configure(columns=treeColumns)
        return None

    def clear_tree_data(self) -> None:
        self.tree.delete(*self.tree.get_children())

    def console_command(self, text: str) -> None:
        self.consoleBox.insert(tk.END, text)
        return None

    def console_commands(self, text: str | list) -> None:
        if isinstance(text, str):
            for command in text.splitlines():
                self.console_command(command)
            return None
        for command in text:
            self.console_command(command)
        return None

    def update_all_tree(self) -> None:
        self.clear_tree_data()
        routers = self.get_devices()
        i = 1
        for k, router in routers.items():
            rip = ''
            ospf = ''
            bgp = ''
            if router.rip is not None:
                rip = 'Enabled'
            if router.ospf is not None:
                ospf = 'Enabled'
            if router.bgp is not None:
                bgp = 'Enabled'
            values = (i, router.name, router.type, rip, ospf, bgp)
            self.tree.insert('', tk.END, values=values)
        return None

    def update_rip_tree(self) -> None:
        self.clear_tree_data()
        routers = self.get_devices()
        i = 1
        for k, router in routers.items():
            if router.rip is not None:
                values = (i, router.name, router.rip.auto_summary, router.rip.default_information_originate,
                          router.rip.default_metric_of_redistributed_routes, router.rip.distance,
                          router.rip.maximum_paths, router.rip.version)
                self.tree.insert('', tk.END, values=values)
                i += 1

    def update_bgp_tree(self) -> None:
        self.clear_tree_data()
        routers = self.get_devices()
        i = 1
        for k, router in routers.items():
            if router.bgp is not None:
                values = (i, router.name, router.bgp.autonomous_system, router.bgp.router_id,
                          router.bgp.default_information_originate, router.bgp.default_metric_of_redistributed_routes,
                          router.bgp.timers.keep_alive, router.bgp.timers.hold_time)
                self.tree.insert('', tk.END, values=values)
                i += 1
        return None

    def update_ospf_tree(self) -> None:
        self.clear_tree_data()
        routers = self.get_devices()
        i = 1
        for k, router in routers.items():
            if router.ospf is not None:
                router_areas = list(router.ospf.areas.keys())
                ospf_area = router_areas[0]

                values = (i, router.name, router.ospf.router_id, ospf_area, router.ospf.auto_cost_reference_bandwidth,
                          router.ospf.default_information_originate, router.ospf.default_metric_of_redistributed_routes,
                          router.ospf.distance, router.ospf.maximum_paths)
                self.tree.insert('', tk.END, values=values)

                if len(router_areas) > 1:
                    for area in router_areas[1:]:
                        values = ('', router.name, '', router.ospf.areas[area].id)
                        self.tree.insert(i, tk.END, values=values)
                i += 1

    def router_exists(self, hostname: str) -> bool:
        for k, router in enumerate(self.project.devices.values(), start=1):
            if router.name == hostname:
                return True
        return False

    def get_router(self, hostname: str) -> Router:
        return self.project.devices.get(hostname)

    def get_devices(self) -> dict:
        return self.project.devices


if __name__ == "__main__":
    MainGUI()
