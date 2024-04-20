from resources.devices.Router import Router
from resources.routing_protocols.Redistribution import Redistribution
from resources.user.User import User
from resources.connections.configure_connection import create_connection_to_router, close_connection
import resources.connect_frontend_with_backend.universal_router_commands as universal_router_commands
import netmiko


## Add Router
def get_info_router(main_gui, router: Router, user: User) -> None:
    try:
        connection = create_connection_to_router(router, user)
        router.interfaces = universal_router_commands.get_all_interfaces(connection, router, user)
        router.static_routes = universal_router_commands.get_static_routes(connection, router, user)
        router.rip = universal_router_commands.get_rip(connection, router, user)
        router.bgp = universal_router_commands.get_bgp(connection, router, user)
        router.ospf = universal_router_commands.get_ospf(connection, router, user)
        close_connection(connection)
    except netmiko.exceptions.NetMikoTimeoutException:
        main_gui.console_commands(f'Cannot connect to {router.name}')
        return None

    # todo do usunięcia po beta
    main_gui.console_commands(f'I {router.name}')
    return None


## Redistribution
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
    except netmiko.exceptions.NetMikoTimeoutException:
        main_gui.console_commands(f'Cannot connect to {router.name}')
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


## Static Route
def add_static_route(main_gui, add_static_route, router: Router, user: User, network: str, network_mask: int,
                     route_distance: int,
                     next_hop: str, interface_name: str) -> None:
    try:
        if interface_name == '-':
            completed, output = universal_router_commands.add_static_route(router, user, network, network_mask,
                                                                           route_distance, next_hop)
        else:
            completed, output = universal_router_commands.add_static_route(router, user, network, network_mask,
                                                                           route_distance, next_hop, interface_name)
    except netmiko.exceptions.NetMikoTimeoutException:
        main_gui.console_commands(f'Cannot connect to {router.name}')
        return None

    if completed:
        main_gui.console_commands(output)
        router.static_routes = universal_router_commands.get_static_routes(None, router, user)
        # add_static_route.update
    return None


def remove_static_route(main_gui, static_route_gui, item, router: Router, user: User, network: str,
                        network_mask: int) -> None:
    try:
        completed, output = universal_router_commands.remove_static_route(router, user, network, network_mask)
    except netmiko.exceptions.NetMikoTimeoutException:
        main_gui.console_commands(f'Cannot connect to {router.name}')
        return None

    if completed:
        main_gui.console_commands(output)
        router.static_routes = universal_router_commands.get_static_routes(None, router, user)
        static_route_gui.tree.delete(item)
        # todo BEZ tego bo ma być funkcja odświerz
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
    except netmiko.exceptions.NetMikoTimeoutException:
        main_gui.console_commands(f'Cannot connect to {router.name}')
        return None

    if completed:
        main_gui.console_commands(output)
        router.bgp = universal_router_commands.get_bgp(None, router, user)
        main_gui.add_router_bgp(router)
    return None


def update_bgp(main_gui, router: Router, user: User, router_id: str, default_information_originate: bool,
               default_metric_of_redistributed_routes: int, keep_alive: int, hold_on: int) -> None:
    try:
        completed, output = universal_router_commands.update_bgp(router, user, router_id, default_information_originate,
                                                                 default_metric_of_redistributed_routes, keep_alive,
                                                                 hold_on)
    except netmiko.exceptions.NetMikoTimeoutException:
        main_gui.console_commands(f'Cannot connect to {router.name}')
        return None

    if completed:
        main_gui.console_commands(output)
        router.bgp = universal_router_commands.get_bgp(None, router, user)
        main_gui.update_bgp_tree(router.bgp)
    return None


def add_bgp_neighbor(main_gui, router: Router, user: User, neighbor_id: str, remote_as: int, ebgp_multihop: int,
                     next_hop_self: bool, shutdown: bool, keep_alive: int, hold_on: int) -> None:
    try:
        completed, output = universal_router_commands.add_bgp_neighbor(router, user, neighbor_id, remote_as,
                                                                       ebgp_multihop, next_hop_self, shutdown,
                                                                       keep_alive, hold_on)
    except netmiko.exceptions.NetMikoTimeoutException:
        main_gui.console_commands(f'Cannot connect to {router.name}')
        return None

    if completed:
        main_gui.console_commands(output)
        router.bgp = universal_router_commands.get_bgp(None, router, user)
    return None


def remove_bgp_neighbor(main_gui, router: Router, user: User, neighbor_id: str) -> None:
    try:
        completed, output = universal_router_commands.remove_bgp_neighbor(router, user, neighbor_id)
    except netmiko.exceptions.NetMikoTimeoutException:
        main_gui.console_commands(f'Cannot connect to {router.name}')
        return None

    if completed:
        main_gui.console_commands(output)
        router.bgp = universal_router_commands.get_bgp(None, router, user)
    return None


def update_bgp_neighbor(main_gui, router: Router, user: User, neighbor_id: str, remote_as: int, ebgp_multihop: int,
                        next_hop_self: bool, shutdown: bool, keep_alive: int, hold_on: int) -> None:
    try:
        completed, output = universal_router_commands.update_bgp_neighbor(router, user, neighbor_id, remote_as,
                                                                          ebgp_multihop, next_hop_self, shutdown,
                                                                          keep_alive, hold_on)
    except netmiko.exceptions.NetMikoTimeoutException:
        main_gui.console_commands(f'Cannot connect to {router.name}')
        return None

    if completed:
        main_gui.console_commands(output)
        router.bgp = universal_router_commands.get_bgp(None, router, user)
    return None


def add_bgp_networks(main_gui, router: Router, user: User, network_and_mask: list[list[str, int]]) -> None:
    try:
        completed, output = universal_router_commands.add_bgp_networks(router, user, network_and_mask)
    except netmiko.exceptions.NetMikoTimeoutException:
        main_gui.console_commands(f'Cannot connect to {router.name}')
        return None

    if completed:
        main_gui.console_commands(output)
        router.bgp = universal_router_commands.get_bgp(None, router, user)
    return None


def remove_bgp_networks(main_gui, router: Router, user: User, network_and_mask: list[list[str, int]]) -> None:
    try:
        completed, output = universal_router_commands.remove_bgp_networks(router, user, network_and_mask)
    except netmiko.exceptions.NetMikoTimeoutException:
        main_gui.console_commands(f'Cannot connect to {router.name}')
        return None

    if completed:
        main_gui.console_commands(output)
        router.bgp = universal_router_commands.get_bgp(None, router, user)
    return None


## RIP
def enable_rip(main_gui, router: Router, user: User, auto_summary: bool, default_information_originate: bool,
               default_metric_of_redistributed_routes: int, distance: int, maximum_paths: int, version: int,
               networks: list[str]) -> None:
    try:
        completed, output = universal_router_commands.enable_rip(router, user, auto_summary,
                                                                 default_information_originate,
                                                                 default_metric_of_redistributed_routes, distance,
                                                                 maximum_paths, version, networks)
    except netmiko.exceptions.NetMikoTimeoutException:
        main_gui.console_commands(f'Cannot connect to {router.name}')
        return None

    if completed:
        main_gui.console_commands(output)
        router.rip = universal_router_commands.get_rip(None, router, user)
        main_gui.add_router_rip(router)
    return None


def update_rip(main_gui, router: Router, user: User, auto_summary: bool, default_information_originate: bool,
               default_metric_of_redistributed_routes: int, distance: int, maximum_paths: int, version: int) -> None:
    try:
        completed, output = universal_router_commands.update_rip(router, user, auto_summary,
                                                                 default_information_originate,
                                                                 default_metric_of_redistributed_routes, distance,
                                                                 maximum_paths, version)
    except netmiko.exceptions.NetMikoTimeoutException:
        main_gui.console_commands(f'Cannot connect to {router.name}')
        return None

    if completed:
        main_gui.console_commands(output)
        router.rip = universal_router_commands.get_rip(None, router, user)
        main_gui.update_rip_tree(router.rip)
    return None


def remove_rip_networks(main_gui, router: Router, user: User, networks: list[str]) -> None:
    try:
        completed, output = universal_router_commands.remove_rip_networks(router, user, networks)
    except netmiko.exceptions.NetMikoTimeoutException:
        main_gui.console_commands(f'Cannot connect to {router.name}')
        return None

    if completed:
        main_gui.console_commands(output)
        router.rip = universal_router_commands.get_rip(None, router, user)
    return None


def add_rip_networks(main_gui, router: Router, user: User, networks: list[str]) -> None:
    try:
        completed, output = universal_router_commands.add_rip_networks(router, user, networks)
    except netmiko.exceptions.NetMikoTimeoutException:
        main_gui.console_commands(f'Cannot connect to {router.name}')
        return None

    if completed:
        main_gui.console_commands(output)
        router.rip = universal_router_commands.get_rip(None, router, user)
    return None
