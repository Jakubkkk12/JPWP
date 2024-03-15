import tkinter as tk
from tkinter import ttk

import ssh_password_gui
from gui_resources import config
from login_gui import LoginGUI
from PIL import Image, ImageTk

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

APPNAME = config.APPNAME
VERSION = config.VERSION
BG_COLOR = config.BG_COLOR
WINDOW_ICON_PATH = 'gui_resources/APP_ICON_512.png'
QUIT_ICON_PATH = 'gui_resources/QUIT_512.png'


class MainGUI:
    def __init__(self):
        self.root = tk.Tk()
        # title
        self.root.title(APPNAME + ' ' + VERSION)

        # window icon, using conversion to iso, cause tkinter doesn't accept jpg
        icon = tk.PhotoImage(file=WINDOW_ICON_PATH)
        self.root.wm_iconphoto(False, icon)

        # setting window size
        width = 800
        height = 800
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.root.geometry(alignstr)
        self.root.resizable(width=True, height=True)

        self.root.configure(bg=BG_COLOR)

        self.root.minsize(300, 200)

        self.root.columnconfigure(0, weight=4)
        self.root.columnconfigure(1, weight=4)
        self.root.columnconfigure(2, weight=4)
        self.root.columnconfigure(3, weight=4)
        self.root.columnconfigure(4, weight=1)

        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=4)
        self.root.rowconfigure(2, weight=4)
        self.root.rowconfigure(3, weight=4)

        # Sample data:
        self.devices = {
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
                                                                   )
                                                     }
                                              ),
                         ),
            'R2': Router(name='R2',
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
                                                                   )
                                                     }
                                              ),
                         )
        }

        treeColumns = ('No', 'Name', 'Type', 'SSH IP')
        slc_no: slice = slice(0, 1)
        slc_name: slice = slice(1, 2)
        slc_type: slice = slice(2, 3)
        slc_ssh_ip: slice = slice(4, 3, -1) # need fix

        self.tree = ttk.Treeview(self.root, columns=treeColumns, show='headings')
        self.tree.grid(column=0, row=1, padx=2, pady=2, columnspan=4, rowspan=4, sticky='NSWE')

        max_height = 1
        for i, (router_name, router) in enumerate(self.devices.items(), start=1):
            ssh_ips = self.get_ssh_ip_addresses(router)
            values = (i, router.name, router.type, ssh_ips)
            self.tree.insert('', tk.END, values=values, iid=i)

            if self.get_number_of_ssh_addresses(router) > max_height:
                max_height = self.get_number_of_ssh_addresses(router)

        # Adjust row height
        max_height_px = max_height*15
        s = ttk.Style()
        s.configure('Treeview', rowheight=max_height_px)

        self.tree.heading(treeColumns[slc_no], text='No')
        self.tree.column(treeColumns[slc_no], width=30)

        self.tree.heading(treeColumns[slc_name], text='Hostname')
        self.tree.column(treeColumns[slc_name], width=80)

        self.tree.heading(treeColumns[slc_type], text='Type')
        self.tree.column(treeColumns[slc_type], width=50)

        self.tree.heading(treeColumns[3], text='SSH Address')
        self.tree.column(treeColumns[3], width=50)

        self.tree.bind('<Button-3>', self.show_content_menu)

        # Buttons
        buttonsFrame = tk.Frame(self.root)
        buttonsFrame.grid(column=0, row=0, sticky='EW')
        buttonsFrame.configure(bg=BG_COLOR)

        btnAll = tk.Button(buttonsFrame, text='All', padx=10, command=self.btnAll_command)
        btnAll.grid(column=0, row=1)

        btnRIP = tk.Button(buttonsFrame, text='RIP', padx=10, command=self.btnRIP_command)
        btnRIP.grid(column=1, row=1)

        btnOSPF = tk.Button(buttonsFrame, text='OSPF', padx=10, command=self.btnOSPF_command)
        btnOSPF.grid(column=2, row=1)

        btnBGP = tk.Button(buttonsFrame, text='BGP', padx=10, command=self.btnBGP_command)
        btnBGP.grid(column=3, row=1)

        btnAddRouter = tk.Button(self.root, text='Add Router', command=self.btnAddRouter_command)
        btnAddRouter.grid(column=4, row=2, sticky='EW')

        btnSSHPassword = tk.Button(self.root, text='SSH Password', padx=10, pady=2,
                                   command=ssh_password_gui.SSHPasswordGUI)
        btnSSHPassword.grid(column=4, row=0, pady=10)

        btnLogOut = tk.Button(self.root, text='Log Out', command=self.btnLogOut_command)
        btnLogOut.grid(column=4, row=3, sticky='EWS')

        QUIT_ICON = Image.open(QUIT_ICON_PATH)
        QUIT_ICON = QUIT_ICON.resize((24, 24))
        quit_icon = ImageTk.PhotoImage(QUIT_ICON)
        btnQuit = tk.Button(self.root, text='Quit', image=quit_icon, compound=tk.RIGHT, command=self.root.destroy)
        btnQuit.grid(column=4, row=4, sticky='EWS')

        self.menu = tk.Menu(self.root)
        self.menu.add_command(label='test', command=self.do_test)

        self.root.mainloop()

    def get_ssh_ip_addresses(self, router) -> str:
        ssh_ip = ''
        ip_addresses = list(router.ssh_information.ip_addresses.values())
        for i, ip in enumerate(ip_addresses):
            ssh_ip += ip
            if i != len(ip_addresses) - 1:
                ssh_ip += '\n'
        return ssh_ip

    def get_number_of_ssh_addresses(self, router)-> int:
        number_of_ips = len(router.ssh_information.ip_addresses)
        return number_of_ips

    def show_content_menu(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            self.menu.post(event.x_root, event.y_root)

    def do_test(self):
        selected_item = self.tree.selection()
        if selected_item:
            item_text = self.tree.item(selected_item)['values']
            print(f'do something: {item_text}')

    def btnLogOut_command(self) -> None:
        self.root.destroy()
        LoginGUI()
        return None

    def btnAddRouter_command(self):

        return None

    def btnAll_command(self) -> None:
        self.clear_tree()
        treeColumns = ('No', 'Hostname', 'Type', 'SSH Address')
        self.tree.configure(columns=treeColumns)

        max_height = 1
        for i, (router_name, router) in enumerate(self.devices.items(), start=1):
            ssh_ips = self.get_ssh_ip_addresses(router)
            values = (i, router.name, router.type, ssh_ips)
            self.tree.insert('', tk.END, values=values, iid=i)

            if self.get_number_of_ssh_addresses(router) > max_height:
                max_height = self.get_number_of_ssh_addresses(router)

        self.tree.configure(columns=treeColumns)

        self.tree.heading(treeColumns[0], text='No')
        self.tree.column(treeColumns[0], width=30)

        self.tree.heading(treeColumns[1], text='Hostname')
        self.tree.column(treeColumns[1], width=80)

        self.tree.heading(treeColumns[2], text='Type')
        self.tree.column(treeColumns[2], width=50)

        self.tree.heading(treeColumns[3], text='SSH Address')
        self.tree.column(treeColumns[3], width=50)
        return None

    def btnRIP_command(self) -> None:
        self.clear_tree()

        return None

    def btnBGP_command(self) -> None:
        self.clear_tree()

        return None

    def btnOSPF_command(self) -> None:
        self.clear_tree()

        return None

    def clear_tree(self) -> None:
        for item in self.tree.get_children():
            self.tree.delete(item)

        treeColumns = ()
        self.tree.configure(columns=treeColumns)
        return None


if __name__ == "__main__":
    MainGUI()
