import re

from resources.routing_protocols.Network import Network
from resources.routing_protocols.Redistribution import Redistribution
from resources.routing_protocols.StaticRoute import StaticRoute
from resources.routing_protocols.ospf.OSPFArea import OSPFArea
from resources.routing_protocols.ospf.OSPFInformation import OSPFInformation
from resources.routing_protocols.bgp.BGPInformation import BGPInformation
from resources.routing_protocols.bgp.BGPTimers import BGPTimers
from resources.routing_protocols.bgp.BGPNeighbor import BGPNeighbor
from resources.ssh.SSHInformation import SSHInformation
from resources.routing_protocols.rip.RIPInformation import RIPInformation

from resources.connections.configure_connection import *
from resources.cisco.getting_interface import *

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
                                                                   '10.0.0.0 0.0.255.255': Network(network='10.0.0.0',
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
    user = User(username='admin12', ssh_password='ZAQ!2wsx')

    r1 = Router(name='R1',
                ssh_information=SSHInformation(ip_addresses={'0': '10.250.250.1'}),
                type='cisco_ios',
                enable_password='ZSEDCxzaqwe')

    r2 = Router(name='R2',
                ssh_information=SSHInformation(ip_addresses={'0': '10.250.250.2'}),
                type='cisco_ios',
                enable_password='ZSEDCxzaqwe')

    from resources.cisco.execute_commands import update_bgp, get_bgp, update_bgp_neighbor, update_ospf, update_interface_ospf, update_rip, update_ospf_area, update_redistribution, get_ospf, get_static_r, get_rip, get_all_interfaces
    conn = create_connection_to_router(r1, user)
    conn.enable()
    r1.bgp = get_bgp(conn)
    r1.ospf = get_ospf(conn)
    r1.rip = get_rip(conn)
    r1.static_routes = get_static_r(conn)
    r1.interfaces = get_all_interfaces(conn)
    close_connection(conn)
    print(r1.interfaces)
    print(r1.bgp)
    print(r1.ospf)
    print(r1.rip)
    print(r1.static_routes)

    # done, out = update_bgp(r1, user, r1.bgp.router_id, False,
    #                        60, 30, 90)
    # print(done)
    # print(out)
    # done, out = update_bgp_neighbor(r1, user,  '10.0.0.1', remote_as=555, ebgp_multihop=1,
    #                                 next_hop_self=False, shutdown=True, update_source=None, keep_alive=80, hold_on=100)
    # print(done)

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
