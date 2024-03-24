import netmiko
import re
from resources.routing_protocols.bgp.BGPTimers import BGPTimers
from resources.routing_protocols.bgp.BGPNeighbor import BGPNeighbor
from resources.routing_protocols.bgp.BGPInformation import BGPInformation
from resources.routing_protocols.Redistribution import Redistribution
from resources.routing_protocols.Network import Network
from resources.cisco.getting_redistribution import get_routing_protocol_redistribution
from resources.cisco.getting_routing_protocol import (get_routing_protocol_distance,
                                                      get_routing_protocol_default_information_originate,
                                                      get_routing_protocol_default_metric_of_redistributed_routes)
from resources.constants import NETWORK_MASK_REVERSED


def is_bgp_enabled(sh_run_sec_bgp_output: str) -> bool:
    pattern = r'(router bgp)'
    if re.search(pattern, sh_run_sec_bgp_output):
        return True
    return False


def get_bgp_autonomous_system(sh_run_sec_bgp_output: str) -> int | None:
    pattern = r'(router bgp )\d*'
    match = re.search(pattern, sh_run_sec_bgp_output)
    if match:
        autonomous_system = int(match.group()[len('router bgp '):])
        return autonomous_system
    return None


def get_bgp_router_id(sh_bgp_summary_output: str, sh_run_sec_bgp_output: str) -> str | None:
    pattern = r'(BGP router identifier ).*(,)'
    match = re.search(pattern, sh_bgp_summary_output)
    if match:
        router_id = match.group()[len('BGP router identifier '):-1]
        return router_id

    pattern = r'(bgp router-id ).*'
    match = re.search(pattern, sh_run_sec_bgp_output)
    if match:
        router_id = match.group()[len('bgp router-id '):]
        return router_id
    return None


def get_bgp_networks(sh_run_sec_bgp_output: str) -> dict[str, Network] | None:
    pattern = r'(network .*)'
    match = re.findall(pattern, sh_run_sec_bgp_output)
    if not match:
        return {}
    # 'network 11.0.0.0 mask 255.255.255.0'
    networks_list: list[list[str]] = [[line.split(' ')[1], line.split(' ')[-1]] for line in match]
    networks: dict[str, Network] = {}
    for net in networks_list:
        networks[f"{net[0]} {net[1]}"] = Network(network=net[0],
                                                 mask=NETWORK_MASK_REVERSED[net[1]])
    return networks


def is_bgp_timers(sh_run_sec_bgp_output: str) -> bool:
    pattern = r'(timers bgp)'
    if re.search(pattern, sh_run_sec_bgp_output):
        return True
    return False


def get_bgp_timers(sh_run_sec_bgp_output: str) -> BGPTimers | None:
    if not is_bgp_timers(sh_run_sec_bgp_output):
        return None

    pattern = r'(timers bgp ).*'
    match = re.search(pattern, sh_run_sec_bgp_output)
    timers: list[str] = match.group()[len('timers bgp '):].split(' ')
    keep_alive: int = int(timers[0])
    hold_time: int = int(timers[1])
    return BGPTimers(keep_alive=keep_alive, hold_time=hold_time)


def get_bgp_neighbors_list(sh_run_sec_bgp_output: str) -> list[str] | None:
    pattern = r'(neighbor .* remote-as)'
    match = re.findall(pattern, sh_run_sec_bgp_output)
    if len(match) == 0:
        return None

    neighbors: list[str] = [neighbor.split(' ')[1] for neighbor in match]
    neighbors = list(set(neighbors))
    return neighbors


def get_bgp_neighbor_remote_as(neighbor: str, sh_run_sec_bgp_output: str) -> int | None:
    pattern = f'(neighbor {neighbor} remote-as .*)'
    match = re.search(pattern, sh_run_sec_bgp_output)
    if match:
        remote_as = int(match.group()[len(f'(neighbor {neighbor} remote-as)'):])
        return remote_as
    return None


def get_bgp_neighbor_state(neighbor: str, sh_bgp_summary_output: str) -> str | None:
    pattern = f'({neighbor}.*)'
    match = re.search(pattern, sh_bgp_summary_output)
    if match:
        state = match.group()[len(f'(neighbor {neighbor} remote-as)'):].split()[-1]
        if state == '(Admin)':
            return 'Idle (Admin)'
        return state
    return None


def get_bgp_neighbor_ebgp_multihop(neighbor: str, sh_run_sec_bgp_output: str) -> int:
    pattern = f'(neighbor {neighbor} ebgp-multihop .*)'
    match = re.search(pattern, sh_run_sec_bgp_output)
    if match:
        ebgp_multihop = int(match.group()[len(f'(neighbor {neighbor} remote-as)'):])
        return ebgp_multihop
    return 1


def get_bgp_neighbor_next_hop_self(neighbor: str, sh_run_sec_bgp_output: str) -> bool:
    pattern = f'(neighbor {neighbor} next-hop-self)'
    if re.search(pattern, sh_run_sec_bgp_output):
        return True
    return False


def get_bgp_neighbor_shutdown(neighbor: str, sh_run_sec_bgp_output: str) -> bool:
    pattern = f'(neighbor {neighbor} shutdown)'
    if re.search(pattern, sh_run_sec_bgp_output):
        return True
    return False


def get_bgp_neighbor_timers(neighbor: str, sh_run_sec_bgp_output: str) -> BGPTimers | None:
    pattern = f'(neighbor {neighbor} timers .*)'
    match = re.search(pattern, sh_run_sec_bgp_output)
    if not match:
        return None

    timers: list[str] = match.group()[len(f'neighbor {neighbor} timers '):].split(' ')
    keep_alive: int = int(timers[0])
    hold_time: int = int(timers[1])
    return BGPTimers(keep_alive=keep_alive, hold_time=hold_time)


def get_bgp_neighbor_update_source(neighbor: str, sh_run_sec_bgp_output: str) -> str | None:
    pattern = f'(neighbor {neighbor} update-source .*)'
    match = re.search(pattern, sh_run_sec_bgp_output)
    if match:
        update_source = match.group()[len(f'(neighbor {neighbor} update-source )'):]
        return update_source
    return None


def get_bgp_neighbors(sh_run_sec_bgp_output: str, sh_bgp_summary_output: str) -> dict[str, BGPNeighbor] | None:
    neighbors_list: list[str] = get_bgp_neighbors_list(sh_run_sec_bgp_output)
    if neighbors_list is None:
        return None

    neighbors: dict[str, BGPNeighbor] = {}
    for neighbor in neighbors_list:
        ip_address: str = neighbor
        remote_as: int = get_bgp_neighbor_remote_as(neighbor, sh_run_sec_bgp_output)
        state: str = get_bgp_neighbor_state(neighbor, sh_bgp_summary_output)
        ebgp_multihop: int = get_bgp_neighbor_ebgp_multihop(neighbor, sh_run_sec_bgp_output)
        next_hop_self: bool = get_bgp_neighbor_next_hop_self(neighbor, sh_run_sec_bgp_output)
        shutdown: bool = get_bgp_neighbor_shutdown(neighbor, sh_run_sec_bgp_output)
        timers: BGPTimers = get_bgp_neighbor_timers(neighbor, sh_run_sec_bgp_output)
        update_source: str = get_bgp_neighbor_update_source(neighbor, sh_run_sec_bgp_output)
        neighbors[neighbor] = BGPNeighbor(ip_address=ip_address,
                                          remote_as=remote_as,
                                          state=state,
                                          ebgp_multihop=ebgp_multihop,
                                          next_hop_self=next_hop_self,
                                          shutdown=shutdown,
                                          timers=timers,
                                          update_source=update_source)
    return neighbors


def get_bgp_information(connection: netmiko.BaseConnection) -> BGPInformation | None:
    connection.enable()
    sh_run_sec_bgp_output: str = connection.send_command("show run | sec bgp")
    sh_bgp_summary_output: str = connection.send_command("show bgp sum")
    connection.exit_enable_mode()

    if not is_bgp_enabled(sh_run_sec_bgp_output):
        return None

    autonomous_system: int = get_bgp_autonomous_system(sh_run_sec_bgp_output)
    router_id: str = get_bgp_router_id(sh_bgp_summary_output, sh_run_sec_bgp_output)
    default_information_originate: bool = get_routing_protocol_default_information_originate(sh_run_sec_bgp_output)
    default_metric_of_redistributed_routes: int = (
        get_routing_protocol_default_metric_of_redistributed_routes('bgp', sh_run_sec_bgp_output))
    redistribution: Redistribution = get_routing_protocol_redistribution(sh_run_sec_bgp_output)
    networks: dict[str, Network] = get_bgp_networks(sh_run_sec_bgp_output)
    timers: BGPTimers = get_bgp_timers(sh_run_sec_bgp_output)
    neighbors: dict[str, BGPNeighbor] = get_bgp_neighbors(sh_run_sec_bgp_output, sh_bgp_summary_output)

    bgp_info: BGPInformation = BGPInformation(autonomous_system=autonomous_system,
                                              router_id=router_id,
                                              default_information_originate=default_information_originate,
                                              default_metric_of_redistributed_routes=default_metric_of_redistributed_routes,
                                              redistribution=redistribution,
                                              networks=networks,
                                              timers=timers,
                                              neighbors=neighbors)
    return bgp_info
