from netmiko import BaseConnection
from resources.connections.configure_connection import (create_connection_to_router, close_connection,
                                                        execute_conf_commands)
from resources.cisco.getting_bgp import (get_bgp_information, get_bgp_base_conf_commands_for_update_as_list,
                                         get_bgp_conf_neighbor_commands_for_update_as_list,
                                         get_bgp_conf_neighbor_commands_for_add_as_list,
                                         get_bgp_conf_networks_commands_as_list,
                                         get_bgp_no_conf_networks_commands_as_list,
                                         get_bgp_base_conf_commands_for_enable_as_list)
from resources.cisco.getting_interface import (get_interfaces_name, get_base_interface_information,
                                               get_interface_base_conf_commands_for_update_as_list,
                                               get_interface_ospf_information,
                                               get_interface_ospf_conf_commands_for_update_as_list)
from resources.cisco.getting_ospf import (get_ospf_information, get_ospf_base_conf_commands_for_update_as_list,
                                          get_ospf_area_base_conf_commands_for_update_as_list,
                                          get_ospf_area_conf_networks_commands_as_list,
                                          get_ospf_area_no_conf_networks_commands_as_list,
                                          get_ospf_base_conf_commands_for_enable_as_list)
from resources.cisco.getting_redistribution import (get_routing_protocol_redistribution,
                                                    get_redistribution_conf_commands_as_list)
from resources.cisco.getting_rip_information import (get_rip_information,
                                                     get_rip_conf_basic_commands_for_update_as_list,
                                                     get_rip_conf_networks_commands_as_list,
                                                     get_rip_no_conf_networks_commands_as_list,
                                                     get_rip_conf_basic_commands_for_enable_as_list)
from resources.cisco.getting_static_routes import (get_static_routes, get_static_route_conf_command,
                                                   get_static_route_no_conf_command)
from resources.devices.Router import Router
from resources.user.User import User
from resources.routing_protocols.StaticRoute import StaticRoute
from resources.routing_protocols.rip.RIPInformation import RIPInformation
from resources.routing_protocols.ospf.OSPFArea import OSPFArea
from resources.routing_protocols.ospf.OSPFInformation import OSPFInformation
from resources.routing_protocols.bgp.BGPInformation import BGPInformation
from resources.routing_protocols.Redistribution import Redistribution
from resources.interfaces.RouterInterface import RouterInterface


########################################################################################################################
# Section: BGP


def get_bgp(connection: BaseConnection | None, router: Router, user: User | None) -> BGPInformation | None:
    was_connection_given = False if connection is None else True
    if not was_connection_given:
        connection = create_connection_to_router(router, user)
        connection.enable()

    sh_run_sec_bgp_output: str = connection.send_command("show run | sec bgp")
    sh_bgp_summary_output: str = connection.send_command("show bgp sum")

    if not was_connection_given:
        close_connection(connection)

    return get_bgp_information(sh_run_sec_bgp_output, sh_bgp_summary_output)


def enable_bgp(router: Router, user: User, autonomous_system: int, router_id: str, default_information_originate: bool,
               default_metric_of_redistributed_routes: int, keep_alive: int, hold_on: int,
               network_and_mask: list[list[str, int]]) -> tuple[bool, str | None]:
    enable_commands: list[str] = get_bgp_base_conf_commands_for_enable_as_list(autonomous_system, router_id,
                                                                               default_information_originate,
                                                                               default_metric_of_redistributed_routes,
                                                                               keep_alive, hold_on)
    network_commands: list[str] = get_bgp_conf_networks_commands_as_list(network_and_mask)
    commands: list[str] = enable_commands
    commands.extend(network_commands)
    if commands is None:
        return False, None

    output: str = execute_conf_commands(router, user, commands)
    return True, output


def update_bgp(router: Router, user: User, router_id: str, default_information_originate: bool,
               default_metric_of_redistributed_routes: int, keep_alive: int, hold_on: int) -> tuple[bool, str | None]:
    commands: list[str] = get_bgp_base_conf_commands_for_update_as_list(router.bgp, router_id,
                                                                        default_information_originate,
                                                                        default_metric_of_redistributed_routes,
                                                                        keep_alive, hold_on)
    if commands is None:
        return False, None

    commands.insert(0, f'router bgp {router.bgp.autonomous_system}')
    output: str = execute_conf_commands(router, user, commands)
    return True, output


def add_bgp_networks(router: Router, user: User, network_and_mask: list[list[str, int]]) -> tuple[bool, str | None]:
    commands: list[str] = get_bgp_conf_networks_commands_as_list(network_and_mask)

    if commands is None:
        return False, None

    commands.insert(0, f'router bgp {router.bgp.autonomous_system}')
    output: str = execute_conf_commands(router, user, commands)
    return True, output


def remove_bgp_networks(router: Router, user: User, network_and_mask: list[list[str, int]]) -> tuple[bool, str | None]:
    commands: list[str] = get_bgp_no_conf_networks_commands_as_list(network_and_mask)

    if commands is None:
        return False, None

    commands.insert(0, f'router bgp {router.bgp.autonomous_system}')
    output: str = execute_conf_commands(router, user, commands)
    return True, output


def update_bgp_neighbor(router: Router, user: User, neighbor_id: str, remote_as: int, ebgp_multihop: int,
                        next_hop_self: bool, shutdown: bool, update_source: str, keep_alive: int,
                        hold_on: int) -> tuple[bool, str | None]:
    commands: list[str] = get_bgp_conf_neighbor_commands_for_update_as_list(router.bgp.neighbors, neighbor_id,
                                                                            remote_as, ebgp_multihop, next_hop_self,
                                                                            shutdown, update_source, keep_alive,
                                                                            hold_on)
    if commands is None:
        return False, None

    commands.insert(0, f'router bgp {router.bgp.autonomous_system}')
    output: str = execute_conf_commands(router, user, commands)
    return True, output


def remove_bgp_neighbor(router: Router, user: User, neighbor_id: str):
    commands: list[str] = [f'router bgp {router.bgp.autonomous_system}', f'no neighbor {neighbor_id}']
    output: str = execute_conf_commands(router, user, commands)
    return True, output


def add_bgp_neighbor(router: Router, user: User, neighbor_id: str, remote_as: int, ebgp_multihop: int,
                     next_hop_self: bool, shutdown: bool, keep_alive: int,
                     hold_on: int) -> tuple[bool, str | None]:
    commands: list[str] = get_bgp_conf_neighbor_commands_for_add_as_list(neighbor_id, remote_as, ebgp_multihop,
                                                                         next_hop_self, shutdown, keep_alive, hold_on)
    commands.insert(0, f'router bgp {router.bgp.autonomous_system}')
    output: str = execute_conf_commands(router, user, commands)
    return True, output


########################################################################################################################
# Section StaticRoutes


def get_static_r(connection: BaseConnection | None, router: Router, user: User | None) -> list[StaticRoute]:
    was_connection_given = False if connection is None else True
    if not was_connection_given:
        connection = create_connection_to_router(router, user)
        connection.enable()

    sh_run_sec_ip_route_output: str = connection.send_command("show run | sec ip route")

    if not was_connection_given:
        close_connection(connection)

    return get_static_routes(sh_run_sec_ip_route_output)


def add_static_route(router: Router, user: User, network: str, network_mask: int, route_distance: int,
                     next_hop: str | None, interface_name: str | None) -> tuple[bool, str | None]:
    command: str = get_static_route_conf_command(network, network_mask, route_distance, next_hop, interface_name)
    output: str = execute_conf_commands(router, user, command)
    return True, output


def remove_static_route(router: Router, user: User, network: str, network_mask: int) -> tuple[bool, str | None]:
    command: str = get_static_route_no_conf_command(network, network_mask)
    output: str = execute_conf_commands(router, user, command)
    return True, output


########################################################################################################################
# Section RIP


def get_rip(connection: BaseConnection | None, router: Router, user: User | None) -> RIPInformation | None:
    was_connection_given = False if connection is None else True
    if not was_connection_given:
        connection = create_connection_to_router(router, user)
        connection.enable()

    sh_run_sec_rip_output: str = connection.send_command("show run | sec rip")

    if not was_connection_given:
        close_connection(connection)

    return get_rip_information(sh_run_sec_rip_output)


def enable_rip(router: Router, user: User, auto_summary: bool, default_information_originate: bool,
               default_metric_of_redistributed_routes: int, distance: int, maximum_paths: int, version: int,
               networks: list[str]) -> tuple[
    bool, str | None]:
    commands: list[str] = get_rip_conf_basic_commands_for_enable_as_list(auto_summary,
                                                                         default_information_originate,
                                                                         default_metric_of_redistributed_routes,
                                                                         distance, maximum_paths, version)
    commands.extend(get_rip_conf_networks_commands_as_list(networks))
    if commands is None:
        return False, None

    output: str = execute_conf_commands(router, user, commands)
    return True, output


def update_rip(router: Router, user: User, auto_summary: bool, default_information_originate: bool,
               default_metric_of_redistributed_routes: int, distance: int, maximum_paths: int, version: int) -> tuple[
    bool, str | None]:
    commands: list[str] = get_rip_conf_basic_commands_for_update_as_list(router.rip, auto_summary,
                                                                         default_information_originate,
                                                                         default_metric_of_redistributed_routes,
                                                                         distance, maximum_paths, version)
    if commands is None:
        return False, None

    commands.insert(0, 'router rip')
    output: str = execute_conf_commands(router, user, commands)
    return True, output


def add_rip_networks(router: Router, user: User, networks: list[str]) -> tuple[bool, str | None]:
    commands: list[str] = get_rip_conf_networks_commands_as_list(networks)

    if commands is None:
        return False, None

    commands.insert(0, 'router rip')
    output: str = execute_conf_commands(router, user, commands)
    return True, output


def remove_rip_networks(router: Router, user: User, networks: list[str]) -> tuple[bool, str | None]:
    commands: list[str] = get_rip_no_conf_networks_commands_as_list(networks)

    if commands is None:
        return False, None

    commands.insert(0, 'router rip')
    output: str = execute_conf_commands(router, user, commands)
    return True, output


########################################################################################################################
# Section OSPF
def enable_ospf(router: Router, user: User, router_id: str, auto_cost_reference_bandwidth: int,
                default_information_originate: bool, default_metric_of_redistributed_routes: int, distance: int,
                maximum_paths: int, passive_interface_default: bool, area_id: str, network_and_wildcard: list[list[str]],
                area_authentication_message_digest: bool, area_type: str) -> tuple[bool, str | None]:
    commands: list[str] = get_ospf_base_conf_commands_for_enable_as_list(router_id, auto_cost_reference_bandwidth,
                                                                         default_information_originate,
                                                                         default_metric_of_redistributed_routes,
                                                                         distance, maximum_paths,
                                                                         passive_interface_default, area_id,
                                                                         area_authentication_message_digest, area_type)
    commands.extend(get_ospf_area_conf_networks_commands_as_list(area_id, network_and_wildcard))

    if commands is None:
        return False, None

    output: str = execute_conf_commands(router, user, commands)
    return True, output


def get_ospf(connection: BaseConnection | None, router: Router, user: User | None) -> OSPFInformation | None:
    was_connection_given = False if connection is None else True
    if not was_connection_given:
        connection = create_connection_to_router(router, user)
        connection.enable()

    sh_run_sec_ospf_output: str = connection.send_command("show run | sec ospf")
    sh_ip_ospf_database_output: str = connection.send_command("show ip ospf database")
    sh_ip_ospf_output: str = connection.send_command("show ip ospf")
    sh_ip_ospf_neighbors_output: str = connection.send_command("show ip ospf neighbor")

    if not was_connection_given:
        close_connection(connection)

    return get_ospf_information(sh_run_sec_ospf_output, sh_ip_ospf_database_output, sh_ip_ospf_output,
                                sh_ip_ospf_neighbors_output)


def update_ospf(router: Router, user: User, router_id: str, auto_cost_reference_bandwidth: int,
                default_information_originate: bool, default_metric_of_redistributed_routes: int, distance: int,
                maximum_paths: int, passive_interface_default: bool) -> tuple[bool, str | None]:
    commands: list[str] = get_ospf_base_conf_commands_for_update_as_list(router.ospf, router_id,
                                                                         auto_cost_reference_bandwidth,
                                                                         default_information_originate,
                                                                         default_metric_of_redistributed_routes,
                                                                         distance,
                                                                         maximum_paths, passive_interface_default)
    if commands is None:
        return False, None

    commands.insert(0, f'router ospf {router.ospf.process_id}')
    output: str = execute_conf_commands(router, user, commands)
    return True, output


def update_ospf_area(router: Router, user: User, area: OSPFArea, authentication_message_digest: bool, area_type: str) -> \
        tuple[bool, str | None]:
    commands: list[str] = get_ospf_area_base_conf_commands_for_update_as_list(area, authentication_message_digest,
                                                                              area_type)
    if commands is None:
        return False, None

    commands.insert(0, f'router ospf {router.ospf.process_id}')
    output: str = execute_conf_commands(router, user, commands)
    return True, output


def add_ospf_area_networks(router: Router, user: User, area: OSPFArea, network_and_wildcard: list[list[str]]) -> tuple[
    bool, str | None]:
    commands: list[str] = get_ospf_area_conf_networks_commands_as_list(area.id, network_and_wildcard)

    if commands is None:
        return False, None

    commands.insert(0, f'router ospf {router.ospf.process_id}')
    output: str = execute_conf_commands(router, user, commands)
    return True, output


def remove_ospf_area_networks(router: Router, user: User, area: OSPFArea, network_and_wildcard: list[list[str]]) -> \
        tuple[bool, str | None]:
    commands: list[str] = get_ospf_area_no_conf_networks_commands_as_list(area.id, network_and_wildcard)

    if commands is None:
        return False, None

    commands.insert(0, f'router ospf {router.ospf.process_id}')
    output: str = execute_conf_commands(router, user, commands)
    return True, output


########################################################################################################################
# Section Redistribution


def get_redistribution(connection: BaseConnection | None, router: Router, user: User | None,
                       routing_protocol: str) -> Redistribution | None:
    was_connection_given = False if connection is None else True
    if not was_connection_given:
        connection = create_connection_to_router(router, user)
        connection.enable()

    if routing_protocol == 'rip':
        sh_run_sec_routing_protocol_output: str = connection.send_command("show run | sec rip")
    elif routing_protocol == 'ospf':
        sh_run_sec_routing_protocol_output: str = connection.send_command("show run | sec ospf")
    elif routing_protocol == 'bgp':
        sh_run_sec_routing_protocol_output: str = connection.send_command("show run | sec bgp")
    else:
        raise ValueError(f"Unknown routing protocol: {routing_protocol}")

    if not was_connection_given:
        close_connection(connection)

    return get_routing_protocol_redistribution(sh_run_sec_routing_protocol_output)


def update_redistribution(router: Router, user: User, routing_protocol: str, redistribution: Redistribution, ospf: bool,
                          rip: bool, bgp: bool, static: bool, connected: bool, subnets_on: bool) -> tuple[
    bool, str | None]:
    bgp_as: int | None = router.bgp.autonomous_system if router.bgp is not None else None
    ospf_proces: int | None = router.ospf.process_id if router.ospf is not None else None
    commands: list[str] = get_redistribution_conf_commands_as_list(redistribution, ospf, rip, bgp, static, connected,
                                                                   bgp_as=bgp_as, ospf_proces=ospf_proces,
                                                                   subnets_on=subnets_on)
    if commands is None:
        return False, None

    if routing_protocol == 'ospf':
        commands.insert(0, f'router ospf {router.ospf.process_id}')
    elif routing_protocol == 'rip':
        commands.insert(0, 'router rip')
    elif routing_protocol == 'bgp':
        commands.insert(0, f'router bgp {router.bgp.autonomous_system}')
    else:
        raise ValueError(f'Cannot be {routing_protocol}')

    output: str = execute_conf_commands(router, user, commands)
    return True, output


########################################################################################################################
# Section RouterInterface


def get_all_interfaces(connection: BaseConnection | None, router: Router, user: User | None) -> dict[
    str, RouterInterface]:
    was_connection_given = False if connection is None else True
    if not was_connection_given:
        connection = create_connection_to_router(router, user)
        connection.enable()

    sh_ip_int_br_output: str = connection.send_command("show ip int br")
    interfaces_name: list[str] = get_interfaces_name(sh_ip_int_br_output)

    interfaces: dict[str, RouterInterface] = {}
    for interface_name in interfaces_name:
        sh_int_name_output: str = connection.send_command(f"show int {interface_name}")
        sh_ip_ospf_int_name_output: str = connection.send_command(f'show ip ospf interface {interface_name}')
        interfaces[interface_name] = get_base_interface_information(interface_name, sh_int_name_output)
        interfaces[interface_name].ospf = get_interface_ospf_information(sh_ip_ospf_int_name_output)

    if not was_connection_given:
        close_connection(connection)

    return interfaces


def get_interface(connection: BaseConnection | None, router: Router, user: User | None, interface_name: str) -> RouterInterface:
    was_connection_given = False if connection is None else True
    if not was_connection_given:
        connection = create_connection_to_router(router, user)
        connection.enable()

    sh_int_name_output: str = connection.send_command(f"show int {interface_name}")
    sh_ip_ospf_int_name_output: str = connection.send_command(f'show ip ospf interface {interface_name}')

    router_interface: RouterInterface = get_base_interface_information(interface_name, sh_int_name_output)
    router_interface.ospf = get_interface_ospf_information(sh_ip_ospf_int_name_output)

    if not was_connection_given:
        close_connection(connection)

    return router_interface


def update_interface_basic(router: Router, user: User, router_interface: RouterInterface, description: str,
                           ip_address: str, subnet: int, duplex: str, speed: str, mtu: int) -> tuple[bool, str | None]:
    commands: list[str] = get_interface_base_conf_commands_for_update_as_list(router_interface, description, ip_address,
                                                                              subnet, duplex, speed, mtu)
    if commands is None:
        return False, None

    commands.insert(0, f'interface {router_interface.name}')
    output: str = execute_conf_commands(router, user, commands)
    return True, output


def update_interface_ospf(router: Router, user: User, router_interface: RouterInterface, network_type: str, cost: int,
                          priority: int, authentication_message_digest: bool, authentication_password: str,
                          hello_timer: int, dead_timer: int, retransmit_timer: int) -> tuple[bool, str | None]:
    commands: list[str] = get_interface_ospf_conf_commands_for_update_as_list(router_interface.ospf, network_type, cost,
                                                                              priority, authentication_message_digest,
                                                                              authentication_password, hello_timer,
                                                                              dead_timer, retransmit_timer)
    if commands is None:
        return False, None

    commands.insert(0, f'interface {router_interface.name}')
    output: str = execute_conf_commands(router, user, commands)
    return True, output
