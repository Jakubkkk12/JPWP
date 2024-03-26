from netmiko import BaseConnection
from resources.connections.configure_connection import create_connection_to_router, close_connection
from resources.cisco.getting_bgp import (get_bgp_information, get_bgp_base_conf_commands_for_update_as_list,
                                         get_bgp_conf_neighbor_commands_for_update_as_list,
                                         get_bgp_conf_networks_commands_as_list,
                                         get_bgp_no_conf_networks_commands_as_list)
from resources.cisco.getting_interface import (get_base_interface_information,
                                               get_interface_base_conf_commands_for_update_as_list,
                                               get_interface_ospf_information,
                                               get_interface_ospf_conf_commands_for_update_as_list)
from resources.cisco.getting_ospf import (get_ospf_information, get_ospf_base_conf_commands_for_update_as_list,
                                          get_ospf_area_base_conf_commands_for_update_as_list,
                                          get_ospf_area_conf_networks_commands_as_list,
                                          get_ospf_area_no_conf_networks_commands_as_list)
from resources.cisco.getting_redistribution import (get_routing_protocol_redistribution,
                                                    get_redistribution_conf_commands_as_list)
from resources.cisco.getting_rip_information import (get_rip_information,
                                                     get_rip_conf_basic_commands_for_update_as_list,
                                                     get_rip_conf_networks_commands_as_list,
                                                     get_rip_no_conf_networks_commands_as_list)
from resources.cisco.getting_static_routes import (get_static_routes, get_static_route_conf_command,
                                                   get_static_route_no_conf_command)
from resources.devices.Router import Router
from resources.user.User import User
from resources.routing_protocols.StaticRoute import StaticRoute
from resources.routing_protocols.rip import RIPInformation
from resources.routing_protocols.ospf import OSPFInformation
from resources.routing_protocols.bgp import BGPInformation

########################################################################################################################
# Section: BGP

def get_bgp(connection: BaseConnection | None, router: Router = None, user: User = None) -> BGPInformation:
    was_connection_given = False if connection is None else True
    if not was_connection_given:
        connection = create_connection_to_router(router, user)
        connection.enable()

    sh_run_sec_bgp_output: str = connection.send_command("show run | sec bgp")
    sh_bgp_summary_output: str = connection.send_command("show bgp sum")

    if not was_connection_given:
        close_connection(connection)

    return get_bgp_information(sh_run_sec_bgp_output, sh_bgp_summary_output)


def update_bgp(router: Router, user: User, router_id: str, default_information_originate: bool,
               default_metric_of_redistributed_routes: int, keep_alive: int, hold_on: int) -> tuple[bool, str | None]:
    commands: list[str] = get_bgp_base_conf_commands_for_update_as_list(router.bgp, router_id,
                                                                            default_information_originate,
                                                                            default_metric_of_redistributed_routes,
                                                                            keep_alive, hold_on)
    if commands is None:
        return False, None

    commands.insert(0, f'router bgp {router.bgp.autonomous_system}')
    connection = create_connection_to_router(router, user)
    connection.enable()
    output: str = connection.send_config_set(commands)
    close_connection(connection)
    return True, output


def add_bgp_networks(router: Router, user: User, network_and_mask: list[list[str, int]]) -> tuple[bool, str | None]:
    commands: list[str] = get_bgp_conf_networks_commands_as_list(network_and_mask)

    if commands is None:
        return False, None

    commands.insert(0, f'router bgp {router.bgp.autonomous_system}')
    connection = create_connection_to_router(router, user)
    connection.enable()
    output: str = connection.send_config_set(commands)
    close_connection(connection)
    return True, output


def remove_bgp_networks(router: Router, user: User, network_and_mask: list[list[str, int]]) -> tuple[bool, str | None]:
    commands: list[str] = get_bgp_no_conf_networks_commands_as_list(network_and_mask)

    if commands is None:
        return False, None

    commands.insert(0, f'router bgp {router.bgp.autonomous_system}')
    connection = create_connection_to_router(router, user)
    connection.enable()
    output: str = connection.send_config_set(commands)
    close_connection(connection)
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
    connection = create_connection_to_router(router, user)
    connection.enable()
    output: str = connection.send_config_set(commands)
    close_connection(connection)
    return True, output

########################################################################################################################
# Section StaticRoutes

def get_static_r(connection: BaseConnection | None, router: Router = None, user: User = None) -> list[StaticRoute]:
    was_connection_given = False if connection is None else True
    if not was_connection_given:
        connection = create_connection_to_router(router, user)
        connection.enable()

    sh_run_sec_ip_route_output: str = connection.send_command("show run | sec ip route")

    if not was_connection_given:
        close_connection(connection)

    return get_static_routes(sh_run_sec_ip_route_output)


def add_static_route(router: Router, user: User, network: str, network_mask: int, route_distance: int = 1,
                     next_hop: str = None, interface_name: str = None):
    command: str = get_static_route_conf_command(network, network_mask, route_distance, next_hop, interface_name)
    connection = create_connection_to_router(router, user)
    connection.enable()
    output: str = connection.send_config_set(command)
    close_connection(connection)
    return True, output


def remove_static_route(router: Router, user: User, network: str, network_mask: int):
    command: str = get_static_route_no_conf_command(network, network_mask)
    connection = create_connection_to_router(router, user)
    connection.enable()
    output: str = connection.send_config_set(command)
    close_connection(connection)
    return True, output

########################################################################################################################