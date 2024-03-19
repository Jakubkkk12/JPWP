import tkinter as tk
import tkinter.ttk
from tkinter import ttk
from gui_resources import config
from python_guis.edit_interface_gui import EditInterfaceGUI
from python_guis.interface_errors_gui import InterfaceErrorsGUI
from python_guis.interface_statistics_gui import InterfaceStatisticsGUI
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


class InterfacesDetails:
    def __init__(self, hostname):
        self.hostname = hostname
        self.int_name = ''

        devices = {
            'R1': Router(name='R1',
                         ssh_information=SSHInformation(ip_addresses={'0': '10.250.250.1',
                                                                      '1': '10.250.250.2'}),
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
                                                                   ),
                                                     '1': OSPFArea(id='1',
                                                                   is_authentication_message_digest=False,
                                                                   type='NSSA',
                                                                   networks={'10.0.0.0/16': Network(network='10.0.0.0',
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

        root = tk.Toplevel()
        # ######## WINDOW PARAMETERS ######## #
        # title
        root.title(config.APPNAME + ' ' + config.VERSION + ' ' + hostname + ' Interfaces Details')

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

        treeColumns = ('No', 'Name', 'IP', 'Subnet')
        tree = tk.ttk.Treeview(treeFrame, columns=treeColumns, show='headings')
        tree.pack(side='top', expand=True, fill='both')
        tree.configure(yscrollcommand=verticalScrollbar.set)
        tree.configure(xscrollcommand=horizontalScrollbar.set)

        verticalScrollbar.config(command=tree.yview)
        horizontalScrollbar.config(command=tree.xview)

        # Button is a child of root, not treeFrame
        btnQuit = tk.Button(root, text='Quit', command=root.destroy)
        btnQuit.pack(side='bottom')

        # Data insert
        data_router = devices.get(hostname)
        interfaces = data_router.interfaces
        i = 1
        for k, interface in interfaces.items():
            values = (i, interface.name, interface.ip_address, interface.subnet)
            tree.insert('', tk.END, iid=i-1, values=values)
            i += 1

        tree.heading(treeColumns[0], text='No', anchor='w')
        tree.column(treeColumns[0], width=30)

        tree.heading(treeColumns[1], text='Name', anchor='w')
        tree.column(treeColumns[1], width=30)

        tree.heading(treeColumns[2], text='IP', anchor='w')
        tree.column(treeColumns[2], width=30)

        tree.heading(treeColumns[3], text='Subnet', anchor='w')
        tree.column(treeColumns[3], width=30)

        def show_menu_interfaces(event) -> None:
            item = tree.identify_row(event.y)
            tree.selection_set(item)
            if item:
                try:
                    self.int_name = tree.item(item)['values'][1]
                    menu.post(event.x_root, event.y_root)
                except IndexError():
                    pass

        def edit_interface() -> None:
            router_interface = devices.get(self.hostname).interfaces.get(self.int_name)
            EditInterfaceGUI(router_interface)
            return None

        # Pop-up menu configuration
        menu = tk.Menu(root, tearoff=False)
        menu.add_command(label='Edit', command=edit_interface)

        sub_details_menu = tk.Menu(menu, tearoff=False)
        sub_details_menu.add_command(label='Statistics', command=self.show_interface_statistics)
        sub_details_menu.add_command(label='Errors', command=self.show_interface_errors)
        menu.add_cascade(label='Details', menu=sub_details_menu)

        tree.bind('<Button-3>', show_menu_interfaces)

    def show_interface_statistics(self) -> None:
        InterfaceStatisticsGUI(self.hostname, self.int_name)
        return None

    def show_interface_errors(self) -> None:
        InterfaceErrorsGUI(self.hostname, self.int_name)
        return None
