import resources.cisco.commands as cisco
from netmiko import BaseConnection
from resources.devices.Router import Router
from resources.user.User import User
from resources.routing_protocols.StaticRoute import StaticRoute
from resources.routing_protocols.rip.RIPInformation import RIPInformation
from resources.routing_protocols.ospf.OSPFInformation import OSPFInformation
from resources.routing_protocols.ospf.OSPFArea import OSPFArea
from resources.routing_protocols.bgp.BGPInformation import BGPInformation
from resources.routing_protocols.Redistribution import Redistribution
from resources.interfaces import RouterInterface


########################################################################################################################
# Section: BGP
def enable_bgp(router: Router, user: User, autonomous_system: int, router_id: str, default_information_originate: bool,
               default_metric_of_redistributed_routes: int, keep_alive: int, hold_on: int,
               network_and_mask: list[list[str, int]]) -> tuple[bool, str | None]:
    if 'cisco_ios' == router.type:
        return cisco.enable_bgp(router, user, autonomous_system, router_id, default_information_originate,
                                default_metric_of_redistributed_routes, keep_alive, hold_on,network_and_mask)

def get_bgp(connection: BaseConnection | None, router: Router, user: User = None) -> BGPInformation | None:
    if 'cisco_ios' == router.type:
        return cisco.get_bgp(connection, router, user)
    return None


def update_bgp(router: Router, user: User, router_id: str, default_information_originate: bool,
               default_metric_of_redistributed_routes: int, keep_alive: int, hold_on: int) -> tuple[bool, str | None]:
    if 'cisco_ios' == router.type:
        return cisco.update_bgp(router, user, router_id, default_information_originate,
                                default_metric_of_redistributed_routes, keep_alive, hold_on)


def add_bgp_networks(router: Router, user: User, network_and_mask: list[list[str, int]]) -> tuple[bool, str | None]:
    if 'cisco_ios' == router.type:
        return cisco.add_bgp_networks(router, user, network_and_mask)


def remove_bgp_networks(router: Router, user: User, network_and_mask: list[list[str, int]]) -> tuple[bool, str | None]:
    if 'cisco_ios' == router.type:
        return cisco.remove_bgp_networks(router, user, network_and_mask)


def update_bgp_neighbor(router: Router, user: User, neighbor_id: str, remote_as: int, ebgp_multihop: int,
                        next_hop_self: bool, shutdown: bool, update_source: str, keep_alive: int,
                        hold_on: int) -> tuple[bool, str | None]:
    if 'cisco_ios' == router.type:
        return cisco.update_bgp_neighbor(router, user, neighbor_id, remote_as, ebgp_multihop, next_hop_self, shutdown,
                                         update_source, keep_alive, hold_on)


def remove_bgp_neighbor(router: Router, user: User, neighbor_id: str):
    if 'cisco_ios' == router.type:
        return cisco.remove_bgp_neighbor(router, user, neighbor_id)


def add_bgp_neighbor(router: Router, user: User, neighbor_id: str, remote_as: int, ebgp_multihop: int,
                     next_hop_self: bool, shutdown: bool, keep_alive: int, hold_on: int) -> tuple[bool, str | None]:
    if 'cisco_ios' == router.type:
        return cisco.add_bgp_neighbor(router, user, neighbor_id, remote_as, ebgp_multihop, next_hop_self, shutdown,
                                      keep_alive, hold_on)


########################################################################################################################
# Section StaticRoutes


def get_static_routes(connection: BaseConnection | None, router: Router, user: User = None) -> list[StaticRoute]:
    if 'cisco_ios' == router.type:
        return cisco.get_static_r(connection, router, user)


def add_static_route(router: Router, user: User, network: str, network_mask: int, route_distance: int = 1,
                     next_hop: str = None, interface_name: str = None) -> tuple[bool, str | None]:
    if 'cisco_ios' == router.type:
        return cisco.add_static_route(router, user, network, network_mask, route_distance, next_hop, interface_name)


def remove_static_route(router: Router, user: User, network: str, network_mask: int) -> tuple[bool, str | None]:
    if 'cisco_ios' == router.type:
        return cisco.remove_static_route(router, user, network, network_mask)


########################################################################################################################
# Section RIP


def enable_rip(router: Router, user: User, auto_summary: bool, default_information_originate: bool,
               default_metric_of_redistributed_routes: int, distance: int, maximum_paths: int, version: int,
               networks: list[str]) -> tuple[
    bool, str | None]:
    if 'cisco_ios' == router.type:
        return cisco.enable_rip(router, user, auto_summary, default_information_originate,
                                default_metric_of_redistributed_routes, distance, maximum_paths, version, networks)


def get_rip(connection: BaseConnection | None, router: Router, user: User = None) -> RIPInformation | None:
    if 'cisco_ios' == router.type:
        return cisco.get_rip(connection, router, user)


def update_rip(router: Router, user: User, auto_summary: bool, default_information_originate: bool,
               default_metric_of_redistributed_routes: int, distance: int, maximum_paths: int, version: int) -> tuple[
    bool, str | None]:
    if 'cisco_ios' == router.type:
        return cisco.update_rip(router, user, auto_summary, default_information_originate,
                                default_metric_of_redistributed_routes, distance, maximum_paths, version)


def add_rip_networks(router: Router, user: User, networks: list[str]) -> tuple[bool, str | None]:
    if 'cisco_ios' == router.type:
        return cisco.add_rip_networks(router, user, networks)


def remove_rip_networks(router: Router, user: User, networks: list[str]) -> tuple[bool, str | None]:
    if 'cisco_ios' == router.type:
        return cisco.remove_rip_networks(router, user, networks)


########################################################################################################################
# Section OSPF


def get_ospf(connection: BaseConnection | None, router: Router, user: User | None) -> OSPFInformation | None:
    if 'cisco_ios' == router.type:
        return cisco.get_ospf(connection, router, user)


def update_ospf(router: Router, user: User, router_id: str, auto_cost_reference_bandwidth: int,
                default_information_originate: bool, default_metric_of_redistributed_routes: int, distance: int,
                maximum_paths: int, passive_interface_default: bool) -> tuple[bool, str | None]:
    if 'cisco_ios' == router.type:
        return cisco.update_ospf(router, user, router_id, auto_cost_reference_bandwidth, default_information_originate,
                                 default_metric_of_redistributed_routes, distance, maximum_paths,
                                 passive_interface_default)


def update_ospf_area(router: Router, user: User, area: OSPFArea, authentication_message_digest: bool, area_type: str) -> \
tuple[bool, str | None]:
    if 'cisco_ios' == router.type:
        return cisco.update_ospf_area(router, user, area, authentication_message_digest, area_type)


def add_ospf_area_networks(router: Router, user: User, area: OSPFArea, network_and_wildcard: list[list[str]]) -> tuple[
    bool, str | None]:
    if 'cisco_ios' == router.type:
        return cisco.add_ospf_area_networks(router, user, area, network_and_wildcard)


def remove_ospf_area_networks(router: Router, user: User, area: OSPFArea, network_and_wildcard: list[list[str]]) -> \
tuple[bool, str | None]:
    if 'cisco_ios' == router.type:
        return cisco.remove_ospf_area_networks(router, user, area, network_and_wildcard)


########################################################################################################################
# Section Redistribution


def get_redistribution(connection: BaseConnection | None, router: Router, user: User | None, routing_protocol: str) -> Redistribution | None:
    if 'cisco_ios' == router.type:
        return cisco.get_redistribution(connection, router, user, routing_protocol)


def update_redistribution(router: Router, user: User, routing_protocol: str, redistribution: Redistribution, ospf: bool,
                          rip: bool, bgp: bool, static: bool, connected: bool, subnets_on: bool) -> tuple[
    bool, str | None]:
    if 'cisco_ios' == router.type:
        return cisco.update_redistribution(router, user, routing_protocol, redistribution, ospf, rip, bgp, static,
                                           connected, subnets_on)


########################################################################################################################
# Section RouterInterface


def get_all_interfaces(connection: BaseConnection | None, router: Router, user: User | None) -> dict[
    str, RouterInterface]:
    if 'cisco_ios' == router.type:
        return cisco.get_all_interfaces(connection, router, user)


def update_interface_basic(router: Router, user: User, router_interface: RouterInterface, description: str,
                           ip_address: str, subnet: int, duplex: str, speed: str, mtu: int) -> tuple[bool, str | None]:
    if 'cisco_ios' == router.type:
        return cisco.update_interface_basic(router, user, router_interface, description, ip_address, subnet, duplex,
                                            speed, mtu)


def update_interface_ospf(router: Router, user: User, router_interface: RouterInterface, network_type: str, cost: int,
                          priority: int, authentication_message_digest: bool, authentication_password: str,
                          hello_timer: int, dead_timer: int, retransmit_timer: int) -> tuple[bool, str | None]:
    if 'cisco_ios' == router.type:
        return cisco.update_interface_ospf(router, user, router_interface, network_type, cost, priority,
                                           authentication_message_digest, authentication_password, hello_timer,
                                           dead_timer, retransmit_timer)
