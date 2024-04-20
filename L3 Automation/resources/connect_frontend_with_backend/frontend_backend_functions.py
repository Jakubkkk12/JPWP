from resources.devices.Router import Router
from resources.routing_protocols.Redistribution import Redistribution
from resources.user.User import User
import resources.connect_frontend_with_backend.universal_router_commands as universal_router_commands
import netmiko


def redistribution(main_gui, router: Router, user: User, routing_protocol: str,
                   routing_protocol_redistribution: Redistribution, ospf: bool, rip: bool, bgp: bool, static: bool,
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


def add_static_route(main_gui, router: Router, user: User, network: str, network_mask: int, route_distance: int,
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
    return None


def remove_static_route(main_gui, router: Router, user: User, network: str, network_mask: int) -> None:
    try:
        completed, output = universal_router_commands.remove_static_route(router, user, network, network_mask)
    except netmiko.exceptions.NetMikoTimeoutException:
        main_gui.console_commands(f'Cannot connect to {router.name}')
        return None

    if completed:
        main_gui.console_commands(output)
        router.static_routes = universal_router_commands.get_static_routes(None, router, user)
    return None
