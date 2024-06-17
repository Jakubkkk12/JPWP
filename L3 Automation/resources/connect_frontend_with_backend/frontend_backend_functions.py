from resources.devices.Router import Router
from resources.interfaces.RouterInterface import RouterInterface
from resources.routing_protocols.Redistribution import Redistribution
from resources.routing_protocols.ospf.OSPFArea import OSPFArea
from resources.user.User import User
from resources.connections.configure_connection import create_connection_to_router, close_connection
import resources.connect_frontend_with_backend.universal_router_commands as universal_router_commands
import netmiko


# Info Router
def get_info_router(main_gui, router: Router, user: User) -> None:
    try:
        connection = create_connection_to_router(router, user)
        connection.enable()
        router.interfaces = universal_router_commands.get_all_interfaces(connection, router, user)
        router.static_routes = universal_router_commands.get_static_routes(connection, router, user)
        router.rip = universal_router_commands.get_rip(connection, router, user)
        router.bgp = universal_router_commands.get_bgp(connection, router, user)
        router.ospf = universal_router_commands.get_ospf(connection, router, user)
        close_connection(connection)
    except netmiko.exceptions.NetMikoTimeoutException and netmiko.exceptions.ReadTimeout:
        main_gui.console_commands(f'Cannot connect to {router.name} due to timeout')
        return None
    except netmiko.exceptions.NetMikoAuthenticationException:
        main_gui.console_commands(f'Cannot connect to {router.name} due to authentication error')
        return None

    from python_guis.main_gui import MainGUI
    if main_gui.current_view == MainGUI.ALL:
        main_gui.update_all_tree()
    elif main_gui.current_view == MainGUI.RIP:
        main_gui.update_rip_tree()
    elif main_gui.current_view == MainGUI.BGP:
        main_gui.update_bgp_tree()
    elif main_gui.current_view == MainGUI.OSPF:
        main_gui.update_ospf_tree()

    main_gui.console_commands(f'Data received from {router.name}')
    return None


# Redistribution
def update_redistribution(main_gui, router: Router, user: User, routing_protocol: str,
                          routing_protocol_redistribution: Redistribution, ospf: bool, rip: bool, bgp: bool,
                          static: bool,
                          connected: bool) -> None:
    try:
        if routing_protocol == 'ospf':
            completed, output = universal_router_commands.update_redistribution(router, user, routing_protocol,
                                                                                routing_protocol_redistribution,
                                                                                ospf, rip, bgp, static,
                                                                                connected, subnets_on=True)
        elif routing_protocol == 'rip' or routing_protocol == 'bgp':
            completed, output = universal_router_commands.update_redistribution(router, user, routing_protocol,
                                                                                routing_protocol_redistribution,
                                                                                ospf, rip, bgp, static,
                                                                                connected, subnets_on=False)
        else:
            raise ValueError('Invalid routing protocol')
    except netmiko.exceptions.NetMikoTimeoutException and netmiko.exceptions.ReadTimeout:
        main_gui.console_commands(f'Cannot connect to {router.name} due to timeout')
        return None
    except netmiko.exceptions.NetMikoAuthenticationException:
        main_gui.console_commands(f'Cannot connect to {router.name} due to authentication error')
        return None

    if completed:
        main_gui.console_commands(output)
        if routing_protocol == 'rip':
            router.rip.redistribution = universal_router_commands.get_redistribution(None, router, user,
                                                                                     routing_protocol)
        elif routing_protocol == 'ospf':
            router.ospf.redistribution = universal_router_commands.get_redistribution(None, router, user,
                                                                                      routing_protocol)
        elif routing_protocol == 'bgp':
            router.bgp.redistribution = universal_router_commands.get_redistribution(None, router, user,
                                                                                     routing_protocol)
    return None


# Static Route
def add_static_route(main_gui, static_route_gui, router: Router, user: User, network: str, network_mask: int,
                     route_distance: int,
                     next_hop: str, interface_name: str) -> None:
    try:
        if interface_name == '-':
            completed, output = universal_router_commands.add_static_route(router, user, network, network_mask,
                                                                           route_distance, next_hop)
        else:
            completed, output = universal_router_commands.add_static_route(router, user, network, network_mask,
                                                                           route_distance, next_hop, interface_name)
    except netmiko.exceptions.NetMikoTimeoutException and netmiko.exceptions.ReadTimeout:
        main_gui.console_commands(f'Cannot connect to {router.name} due to timeout')
        return None
    except netmiko.exceptions.NetMikoAuthenticationException:
        main_gui.console_commands(f'Cannot connect to {router.name} due to authentication error')
        return None

    if completed:
        main_gui.console_commands(output)
        router.static_routes = universal_router_commands.get_static_routes(None, router, user)
        static_route_gui.update_window()
    return None


def remove_static_route(main_gui, static_route_gui, router: Router, user: User, network: str,
                        network_mask: int) -> None:
    try:
        completed, output = universal_router_commands.remove_static_route(router, user, network, network_mask)
    except netmiko.exceptions.NetMikoTimeoutException and netmiko.exceptions.ReadTimeout:
        main_gui.console_commands(f'Cannot connect to {router.name} due to timeout')
        return None
    except netmiko.exceptions.NetMikoAuthenticationException:
        main_gui.console_commands(f'Cannot connect to {router.name} due to authentication error')
        return None

    if completed:
        main_gui.console_commands(output)
        router.static_routes = universal_router_commands.get_static_routes(None, router, user)
        static_route_gui.update_window()
    return None


## BGP
def enable_bgp(main_gui, router: Router, user: User, autonomous_system: int, router_id: str,
               default_information_originate: bool,
               default_metric_of_redistributed_routes: int, keep_alive: int, hold_on: int,
               network_and_mask: list[list[str, int]]) -> None:
    try:
        completed, output = universal_router_commands.enable_bgp(router, user, autonomous_system, router_id,
                                                                 default_information_originate,
                                                                 default_metric_of_redistributed_routes, keep_alive,
                                                                 hold_on, network_and_mask)
    except netmiko.exceptions.NetMikoTimeoutException and netmiko.exceptions.ReadTimeout:
        main_gui.console_commands(f'Cannot connect to {router.name} due to timeout')
        return None
    except netmiko.exceptions.NetMikoAuthenticationException:
        main_gui.console_commands(f'Cannot connect to {router.name} due to authentication error')
        return None

    if completed:
        main_gui.console_commands(output)
        router.bgp = universal_router_commands.get_bgp(None, router, user)
        main_gui.update_bgp_tree()
    return None


def update_bgp(main_gui, router: Router, user: User, router_id: str, default_information_originate: bool,
               default_metric_of_redistributed_routes: int, keep_alive: int, hold_on: int) -> None:
    try:
        completed, output = universal_router_commands.update_bgp(router, user, router_id, default_information_originate,
                                                                 default_metric_of_redistributed_routes, keep_alive,
                                                                 hold_on)
    except netmiko.exceptions.NetMikoTimeoutException and netmiko.exceptions.ReadTimeout:
        main_gui.console_commands(f'Cannot connect to {router.name} due to timeout')
        return None
    except netmiko.exceptions.NetMikoAuthenticationException:
        main_gui.console_commands(f'Cannot connect to {router.name} due to authentication error')
        return None

    if completed:
        main_gui.console_commands(output)
        router.bgp = universal_router_commands.get_bgp(None, router, user)
        main_gui.update_bgp_tree()
    return None


def add_bgp_neighbor(main_gui, bgp_neighbors_gui, router: Router, user: User, neighbor_id: str, remote_as: int,
                     ebgp_multihop: int, next_hop_self: bool, shutdown: bool, keep_alive: int, hold_on: int) -> None:
    try:
        completed, output = universal_router_commands.add_bgp_neighbor(router, user, neighbor_id, remote_as,
                                                                       ebgp_multihop, next_hop_self, shutdown,
                                                                       keep_alive, hold_on)
    except netmiko.exceptions.NetMikoTimeoutException and netmiko.exceptions.ReadTimeout:
        main_gui.console_commands(f'Cannot connect to {router.name} due to timeout')
        return None
    except netmiko.exceptions.NetMikoAuthenticationException:
        main_gui.console_commands(f'Cannot connect to {router.name} due to authentication error')
        return None

    if completed:
        main_gui.console_commands(output)
        router.bgp = universal_router_commands.get_bgp(None, router, user)
        bgp_neighbors_gui.update_window()
    return None


def remove_bgp_neighbor(main_gui, bgp_neighbors_gui, router: Router, user: User, neighbor_id: str) -> None:
    try:
        completed, output = universal_router_commands.remove_bgp_neighbor(router, user, neighbor_id)
    except netmiko.exceptions.NetMikoTimeoutException and netmiko.exceptions.ReadTimeout:
        main_gui.console_commands(f'Cannot connect to {router.name} due to timeout')
        return None
    except netmiko.exceptions.NetMikoAuthenticationException:
        main_gui.console_commands(f'Cannot connect to {router.name} due to authentication error')
        return None

    if completed:
        main_gui.console_commands(output)
        router.bgp = universal_router_commands.get_bgp(None, router, user)
        bgp_neighbors_gui.update_window()
    return None


def update_bgp_neighbor(main_gui, bgp_neighbors_gui, router: Router, user: User, neighbor_id: str, remote_as: int,
                        ebgp_multihop: int, next_hop_self: bool, shutdown: bool, keep_alive: int, hold_on: int) -> None:
    try:
        completed, output = universal_router_commands.update_bgp_neighbor(router, user, neighbor_id, remote_as,
                                                                          ebgp_multihop, next_hop_self, shutdown,
                                                                          None, keep_alive, hold_on)
    except netmiko.exceptions.NetMikoTimeoutException and netmiko.exceptions.ReadTimeout:
        main_gui.console_commands(f'Cannot connect to {router.name} due to timeout')
        return None
    except netmiko.exceptions.NetMikoAuthenticationException:
        main_gui.console_commands(f'Cannot connect to {router.name} due to authentication error')
        return None

    if completed:
        main_gui.console_commands(output)
        router.bgp = universal_router_commands.get_bgp(None, router, user)
        bgp_neighbors_gui.update_window()
    return None


def add_bgp_networks(main_gui, bgp_networks_gui, router: Router, user: User, network_and_mask: list[list[str, int]]) -> None:
    try:
        completed, output = universal_router_commands.add_bgp_networks(router, user, network_and_mask)
    except netmiko.exceptions.NetMikoTimeoutException and netmiko.exceptions.ReadTimeout:
        main_gui.console_commands(f'Cannot connect to {router.name} due to timeout')
        return None
    except netmiko.exceptions.NetMikoAuthenticationException:
        main_gui.console_commands(f'Cannot connect to {router.name} due to authentication error')
        return None

    if completed:
        main_gui.console_commands(output)
        router.bgp = universal_router_commands.get_bgp(None, router, user)
        bgp_networks_gui.update_window()
    return None


def remove_bgp_networks(main_gui, bgp_networks_gui, router: Router, user: User,
                        network_and_mask: list[list[str, int]]) -> None:
    try:
        completed, output = universal_router_commands.remove_bgp_networks(router, user, network_and_mask)
    except netmiko.exceptions.NetMikoTimeoutException and netmiko.exceptions.ReadTimeout:
        main_gui.console_commands(f'Cannot connect to {router.name} due to timeout')
        return None
    except netmiko.exceptions.NetMikoAuthenticationException:
        main_gui.console_commands(f'Cannot connect to {router.name} due to authentication error')
        return None

    if completed:
        main_gui.console_commands(output)
        router.bgp = universal_router_commands.get_bgp(None, router, user)
        bgp_networks_gui.update_window()
    return None


def remove_bgp(main_gui, router: Router, user: User) -> None:
    try:
        completed, output = universal_router_commands.remove_bgp(router, user)
    except netmiko.exceptions.NetMikoTimeoutException and netmiko.exceptions.ReadTimeout:
        main_gui.console_commands(f'Cannot connect to {router.name} due to timeout')
        return None
    except netmiko.exceptions.NetMikoAuthenticationException:
        main_gui.console_commands(f'Cannot connect to {router.name} due to authentication error')
        return None

    if completed:
        main_gui.console_commands(output)
        router.bgp = universal_router_commands.get_bgp(None, router, user)
        main_gui.update_bgp_tree()
    return None


# RIP
def enable_rip(main_gui, router: Router, user: User, auto_summary: bool, default_information_originate: bool,
               default_metric_of_redistributed_routes: int, distance: int, maximum_paths: int, version: int,
               networks: list[str]) -> None:
    try:
        completed, output = universal_router_commands.enable_rip(router, user, auto_summary,
                                                                 default_information_originate,
                                                                 default_metric_of_redistributed_routes, distance,
                                                                 maximum_paths, version, networks)
    except netmiko.exceptions.NetMikoTimeoutException and netmiko.exceptions.ReadTimeout:
        main_gui.console_commands(f'Cannot connect to {router.name} due to timeout')
        return None
    except netmiko.exceptions.NetMikoAuthenticationException:
        main_gui.console_commands(f'Cannot connect to {router.name} due to authentication error')
        return None

    if completed:
        main_gui.console_commands(output)
        router.rip = universal_router_commands.get_rip(None, router, user)
        main_gui.update_rip_tree()
    return None


def update_rip(main_gui, router: Router, user: User, auto_summary: bool, default_information_originate: bool,
               default_metric_of_redistributed_routes: int, distance: int, maximum_paths: int, version: int) -> None:
    try:
        completed, output = universal_router_commands.update_rip(router, user, auto_summary,
                                                                 default_information_originate,
                                                                 default_metric_of_redistributed_routes, distance,
                                                                 maximum_paths, version)
    except netmiko.exceptions.NetMikoTimeoutException and netmiko.exceptions.ReadTimeout:
        main_gui.console_commands(f'Cannot connect to {router.name} due to timeout')
        return None
    except netmiko.exceptions.NetMikoAuthenticationException:
        main_gui.console_commands(f'Cannot connect to {router.name} due to authentication error')
        return None

    if completed:
        main_gui.console_commands(output)
        router.rip = universal_router_commands.get_rip(None, router, user)
        main_gui.update_rip_tree()
    return None


def remove_rip_networks(main_gui, rip_networks_gui, router: Router, user: User, networks: list[str]) -> None:
    try:
        completed, output = universal_router_commands.remove_rip_networks(router, user, networks)
    except netmiko.exceptions.NetMikoTimeoutException and netmiko.exceptions.ReadTimeout:
        main_gui.console_commands(f'Cannot connect to {router.name} due to timeout')
        return None
    except netmiko.exceptions.NetMikoAuthenticationException:
        main_gui.console_commands(f'Cannot connect to {router.name} due to authentication error')
        return None

    if completed:
        main_gui.console_commands(output)
        router.rip = universal_router_commands.get_rip(None, router, user)
        rip_networks_gui.update_window()
    return None


def add_rip_networks(main_gui, rip_networks_gui, router: Router, user: User, networks: list[str]) -> None:
    try:
        completed, output = universal_router_commands.add_rip_networks(router, user, networks)
    except netmiko.exceptions.NetMikoTimeoutException and netmiko.exceptions.ReadTimeout:
        main_gui.console_commands(f'Cannot connect to {router.name} due to timeout')
        return None
    except netmiko.exceptions.NetMikoAuthenticationException:
        main_gui.console_commands(f'Cannot connect to {router.name} due to authentication error')
        return None

    if completed:
        main_gui.console_commands(output)
        router.rip = universal_router_commands.get_rip(None, router, user)
        rip_networks_gui.update_window()
    return None


def remove_rip(main_gui, router: Router, user: User) -> None:
    try:
        completed, output = universal_router_commands.remove_rip(router, user)
    except netmiko.exceptions.NetMikoTimeoutException and netmiko.exceptions.ReadTimeout:
        main_gui.console_commands(f'Cannot connect to {router.name} due to timeout')
        return None
    except netmiko.exceptions.NetMikoAuthenticationException:
        main_gui.console_commands(f'Cannot connect to {router.name} due to authentication error')
        return None

    if completed:
        main_gui.console_commands(output)
        router.rip = universal_router_commands.get_rip(None, router, user)
        main_gui.update_rip_tree()
    return None


# OSPF
def enable_ospf(main_gui, router: Router, user: User, router_id: str, auto_cost_reference_bandwidth: int,
                default_information_originate: bool, default_metric_of_redistributed_routes: int, distance: int,
                maximum_paths: int, passive_interface_default: bool, area_id: str,
                network_and_wildcard: list[list[str]],
                area_authentication_message_digest: bool, area_type: str) -> None:
    try:
        completed, output = universal_router_commands.enable_ospf(router, user, router_id,
                                                                  auto_cost_reference_bandwidth,
                                                                  default_information_originate,
                                                                  default_metric_of_redistributed_routes, distance,
                                                                  maximum_paths, passive_interface_default, area_id,
                                                                  network_and_wildcard,
                                                                  area_authentication_message_digest, area_type)
    except netmiko.exceptions.NetMikoTimeoutException and netmiko.exceptions.ReadTimeout:
        main_gui.console_commands(f'Cannot connect to {router.name} due to timeout')
        return None
    except netmiko.exceptions.NetMikoAuthenticationException:
        main_gui.console_commands(f'Cannot connect to {router.name} due to authentication error')
        return None

    if completed:
        main_gui.console_commands(output)
        router.ospf = universal_router_commands.get_ospf(None, router, user)
        main_gui.update_ospf_tree()
        import re
        if re.search(r'(passive-interface default)', output):
            router.interfaces = universal_router_commands.get_all_interfaces(None, router, user)
    return None


def update_ospf(main_gui, router: Router, user: User, router_id: str, auto_cost_reference_bandwidth: int,
                default_information_originate: bool, default_metric_of_redistributed_routes: int, distance: int,
                maximum_paths: int, passive_interface_default: bool) -> None:
    try:
        completed, output = universal_router_commands.update_ospf(router, user, router_id,
                                                                  auto_cost_reference_bandwidth,
                                                                  default_information_originate,
                                                                  default_metric_of_redistributed_routes, distance,
                                                                  maximum_paths, passive_interface_default)
    except netmiko.exceptions.NetMikoTimeoutException and netmiko.exceptions.ReadTimeout:
        main_gui.console_commands(f'Cannot connect to {router.name} due to timeout')
        return None
    except netmiko.exceptions.NetMikoAuthenticationException:
        main_gui.console_commands(f'Cannot connect to {router.name} due to authentication error')
        return None

    if completed:
        main_gui.console_commands(output)
        router.ospf = universal_router_commands.get_ospf(None, router, user)
        main_gui.update_ospf_tree()
        import re
        if re.search(r'(passive-interface default)', output):
            router.interfaces = universal_router_commands.get_all_interfaces(None, router, user)
    return None


def update_ospf_area(main_gui, router: Router, user: User, area: OSPFArea, authentication_message_digest: bool,
                     area_type: str) -> None:
    try:
        completed, output = universal_router_commands.update_ospf_area(router, user, area,
                                                                       authentication_message_digest, area_type)
    except netmiko.exceptions.NetMikoTimeoutException and netmiko.exceptions.ReadTimeout:
        main_gui.console_commands(f'Cannot connect to {router.name} due to timeout')
        return None
    except netmiko.exceptions.NetMikoAuthenticationException:
        main_gui.console_commands(f'Cannot connect to {router.name} due to authentication error')
        return None

    if completed:
        main_gui.console_commands(output)
        router.ospf = universal_router_commands.get_ospf(None, router, user)
    return None


def add_ospf_area_networks(main_gui, ospf_area_config_gui, router: Router, user: User, area: OSPFArea,
                           network_and_wildcard: list[list[str]]) -> None:
    try:
        completed, output = universal_router_commands.add_ospf_area_networks(router, user, area, network_and_wildcard)
    except netmiko.exceptions.NetMikoTimeoutException and netmiko.exceptions.ReadTimeout:
        main_gui.console_commands(f'Cannot connect to {router.name} due to timeout')
        return None
    except netmiko.exceptions.NetMikoAuthenticationException:
        main_gui.console_commands(f'Cannot connect to {router.name} due to authentication error')
        return None

    if completed:
        main_gui.console_commands(output)
        router.ospf = universal_router_commands.get_ospf(None, router, user)
        ospf_area_config_gui.update_window()
    return None


def remove_ospf_area_networks(main_gui, ospf_area_config_gui, router: Router, user: User, area: OSPFArea,
                              network_and_wildcard: list[list[str]]) -> None:
    try:
        completed, output = universal_router_commands.remove_ospf_area_networks(router, user, area,
                                                                                network_and_wildcard)
    except netmiko.exceptions.NetMikoTimeoutException and netmiko.exceptions.ReadTimeout:
        main_gui.console_commands(f'Cannot connect to {router.name} due to timeout')
        return None
    except netmiko.exceptions.NetMikoAuthenticationException:
        main_gui.console_commands(f'Cannot connect to {router.name} due to authentication error')
        return None

    if completed:
        main_gui.console_commands(output)
        router.ospf = universal_router_commands.get_ospf(None, router, user)
        ospf_area_config_gui.update_window()
    return None


def remove_ospf(main_gui, router: Router, user: User) -> None:
    try:
        completed, output = universal_router_commands.remove_ospf(router, user)
    except netmiko.exceptions.NetMikoTimeoutException and netmiko.exceptions.ReadTimeout:
        main_gui.console_commands(f'Cannot connect to {router.name} due to timeout')
        return None
    except netmiko.exceptions.NetMikoAuthenticationException:
        main_gui.console_commands(f'Cannot connect to {router.name} due to authentication error')
        return None

    if completed:
        main_gui.console_commands(output)
        router.ospf = universal_router_commands.get_ospf(None, router, user)
        main_gui.update_ospf_tree()
    return None


# RouterInterface
def update_interface_basic(main_gui, interfaces_gui, router: Router, user: User, router_interface: RouterInterface,
                           description: str, ip_address: str, subnet: int, duplex: str, speed: str, mtu: int) -> None:
    try:
        completed, output = universal_router_commands.update_interface_basic(router, user, router_interface,
                                                                             description, ip_address, subnet, duplex,
                                                                             speed, mtu)
    except netmiko.exceptions.NetMikoTimeoutException and netmiko.exceptions.ReadTimeout:
        main_gui.console_commands(f'Cannot connect to {router.name} due to timeout')
        return None
    except netmiko.exceptions.NetMikoAuthenticationException:
        main_gui.console_commands(f'Cannot connect to {router.name} due to authentication error')
        return None

    if completed:
        main_gui.console_commands(output)
        router.interfaces[router_interface.name] = universal_router_commands.get_interface(None, router, user,
                                                                                           router_interface.name)
        interfaces_gui.update_window()
    return None


def set_to_default_interface(main_gui, interfaces_gui, router: Router, user: User, router_interface: RouterInterface
                             ) -> None:
    try:
        completed, output = universal_router_commands.set_to_default_interface(router, user, router_interface)
    except netmiko.exceptions.NetMikoTimeoutException and netmiko.exceptions.ReadTimeout:
        main_gui.console_commands(f'Cannot connect to {router.name} due to timeout')
        return None
    except netmiko.exceptions.NetMikoAuthenticationException:
        main_gui.console_commands(f'Cannot connect to {router.name} due to authentication error')
        return None

    if completed:
        main_gui.console_commands(output)
        router.interfaces[router_interface.name] = universal_router_commands.get_interface(None, router, user,
                                                                                           router_interface.name)
        interfaces_gui.update_window()
    return None


def update_interface_ospf(main_gui, ospf_interfaces_details_gui, router: Router, user: User,
                          router_interface: RouterInterface, network_type: str, cost: int, priority: int,
                          authentication_message_digest: bool, authentication_password: str, hello_timer: int,
                          dead_timer: int, retransmit_timer: int) -> None:
    try:
        completed, output = universal_router_commands.update_interface_ospf(router, user, router_interface,
                                                                            network_type, cost, priority,
                                                                            authentication_message_digest,
                                                                            authentication_password, hello_timer,
                                                                            dead_timer, retransmit_timer)
    except netmiko.exceptions.NetMikoTimeoutException and netmiko.exceptions.ReadTimeout:
        main_gui.console_commands(f'Cannot connect to {router.name} due to timeout')
        return None
    except netmiko.exceptions.NetMikoAuthenticationException:
        main_gui.console_commands(f'Cannot connect to {router.name} due to authentication error')
        return None

    if completed:
        main_gui.console_commands(output)
        router.interfaces[router_interface.name] = universal_router_commands.get_interface(None, router, user,
                                                                                           router_interface.name)
        ospf_interfaces_details_gui.update_window()
    return None
