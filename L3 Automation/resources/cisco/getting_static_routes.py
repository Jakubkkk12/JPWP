import netmiko
import re
from resources.routing_protocols.StaticRoute import StaticRoute
from resources.routing_protocols.Network import Network
from resources.constants import NETWORK_MASK_REVERSED, NETWORK_MASK


########################################################################################################################
# Parsing functions:


def get_all_static_route_info(sh_run_sec_ip_route_output: str) -> list[str] | None:
    pattern = r'(ip route .*)'
    match = re.findall(pattern, sh_run_sec_ip_route_output)
    if not match:
        return None

    all_static_route_info: list[str] = [static_route_info[9:] for static_route_info in match]
    return all_static_route_info


def get_static_route(static_route_info: list[str]) -> StaticRoute:
    # [10.20.1.0, 255.255.255.0, FastEthernet0/1, 10.0.1.1, 56] allways 3 items
    print(static_route_info)
    network_ip_address: str = static_route_info[0]
    network_mask: int = NETWORK_MASK_REVERSED[static_route_info[1]]
    network: Network = Network(network=network_ip_address, mask=network_mask)
    distance: int = int(static_route_info[-1]) if static_route_info[-1].isdecimal() else 1
    next_hop: str | None = None
    interface: str | None = None
    if re.search(r'\d*(.)\d*(.)\d*(.)\d*', static_route_info[2]):
        next_hop = static_route_info[2]
    else:
        interface = static_route_info[2]

    if len(static_route_info) >= 4 and not static_route_info[3].isdecimal():
        next_hop = static_route_info[3]

    static_route = StaticRoute(network=network,
                               next_hop=next_hop,
                               interface=interface,
                               distance=distance)

    return static_route


def get_static_routes(sh_run_sec_ip_route_output: str) -> list[StaticRoute] | None:
    all_static_route_info: list[str] | None = get_all_static_route_info(sh_run_sec_ip_route_output)
    if all_static_route_info is None:
        return None

    static_routes: list[StaticRoute] = []
    for static_route_inf in all_static_route_info:
        static_route_info: list[str] = static_route_inf.split(' ')
        static_routes.append(get_static_route(static_route_info))

    return static_routes


########################################################################################################################
# Configure functions:


def get_static_route_conf_command(network: str, network_mask: int, route_distance: int = 1, next_hop: str = None,
                                  interface_name: str = None) -> str:
    if next_hop is None and interface_name is None:
        raise ValueError('next_hop and interface_name are None')
    network_mask: str = NETWORK_MASK[network_mask]
    if next_hop is None:
        return f'ip route {network} {network_mask} {interface_name} {route_distance}'
    if interface_name is None:
        return f'ip route {network} {network_mask} {next_hop} {route_distance}'
    return f'ip route {network} {network_mask} {interface_name} {next_hop} {route_distance}'


def get_static_route_no_conf_command(network: str, network_mask: int) -> str:
    return f'no ip route {network} {NETWORK_MASK[network_mask]}'
