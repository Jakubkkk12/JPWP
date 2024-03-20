import re

from resources.routing_protocols.Network import Network
from resources.routing_protocols.Redistribution import Redistribution
from resources.routing_protocols.StaticRoute import StaticRoute
from resources.routing_protocols.ospf.OSPFArea import OSPFArea
from resources.routing_protocols.ospf.OSPFInformation import OSPFInformation
from resources.routing_protocols.bgp.BGPInformation import BGPInformation
from resources.ssh.SSHInformation import SSHInformation

from resources.connections.configure_connection import *
from resources.cisco.getting_interface_information import *

if __name__ == '__main__':
    devices = {
        'R1': Router(name='R1',
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
                                                               networks={'10.0.0.0 0.0.255.255': Network(network='10.0.0.0',
                                                                                                mask=None,
                                                                                                wildcard='0.0.255.255'
                                                                                                )
                                                                         }
                                                               )
                                                 }
                                          ),
                     )
    }
    user = User(username='admin12', ssh_password='ZAQ!2wsx')



    r1 = Router(name='R1',
                ssh_information=SSHInformation(ip_addresses={'0': '10.250.250.1'}),
                type='cisco_ios',
                enable_password='ZSEDCxzaqwe')

    r2 = Router(name='R2',
                ssh_information=SSHInformation(ip_addresses={'0': '10.250.250.2'}),
                type='cisco_ios',
                enable_password='ZSEDCxzaqwe')
    from resources.cisco.getting_bgp_information import get_bgp_information
    from resources.cisco.getting_ospf_information import get_ospf_information
    for router in [r1, r2]:
        conn = create_connection_to_router(router=router, user=user)

        ospf_information = get_ospf_information(conn)
        close_connection(connection=conn)
        print(ospf_information)

    # for router in [r1, r2]:
    #     conn = create_connection_to_router(router=router, user=user)
    #     int_list = get_interfaces_name(conn)
    #
    #     int_list.sort()
    #     r1.interfaces = {}
    #     for intf in int_list:
    #         r1.interfaces[intf]: RouterInterface = get_base_interface_information(connection=conn, interface_name=intf)
    #         r1.interfaces[intf].ospf = get_interface_ospf_information(connection=conn, interface_name=intf)
    #
    #     close_connection(connection=conn)
    #     print(r1)
    #     v: RouterInterface
    #     for v in r1.interfaces.values():
    #         if v.ospf is not None:
    #             print(v.ospf.network_type, v.ip_address, v.statistics.information.layer1_status, v.statistics.information.duplex)
