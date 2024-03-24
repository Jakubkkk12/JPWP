import netmiko
import re

from resources.devices.Router import Router
from resources.routing_protocols.ospf.OSPFArea import OSPFArea
from resources.routing_protocols.ospf.OSPFInformation import OSPFInformation
from resources.routing_protocols.Network import Network
from resources.routing_protocols.Redistribution import Redistribution
from resources.cisco.getting_redistribution import get_routing_protocol_redistribution
from resources.cisco.getting_routing_protocol import (get_routing_protocol_distance,
                                                      get_routing_protocol_default_information_originate,
                                                      get_routing_protocol_maximum_paths,
                                                      get_routing_protocol_default_metric_of_redistributed_routes,
                                                      get_conf_command_default_metric_of_redistributed_routes,
                                                      get_conf_command_default_information_originate,
                                                      get_conf_command_maximum_paths,
                                                      get_conf_command_distance)
from resources.routing_protocols.ospf.OSPFNeighbor import OSPFNeighbor


def is_ospf_enabled(sh_run_sec_ospf_output: str) -> bool:
    pattern = r'(router ospf)'
    if re.search(pattern, sh_run_sec_ospf_output):
        return True
    return False


def get_ospf_process_id(sh_run_sec_ospf_output: str) -> int | None:
    pattern = r'(router ospf )\d*'
    match = re.search(pattern, sh_run_sec_ospf_output)
    if match:
        process_id = int(match.group()[len('router ospf '):])
        return process_id
    return None


def get_ospf_router_id(sh_ip_ospf_database_output: str) -> str | None:
    pattern = r'(OSPF Router with ID ).*(Pro)'
    match = re.search(pattern, sh_ip_ospf_database_output)
    if match:
        router_id = match.group()[len('OSPF Router with ID ') + 1:-len('  (Pro')]
        return router_id
    return None


def get_ospf_auto_cost_reference_bandwidth(sh_run_sec_ospf_output: str) -> int:
    pattern = r'(auto-cost reference-bandwidth )\d*'
    match = re.search(pattern, sh_run_sec_ospf_output)
    if match:
        auto_cost_reference_bandwidth = int(match.group()[len('auto-cost reference-bandwidth '):])
        return auto_cost_reference_bandwidth
    return 100


def get_ospf_passive_interface_default(sh_run_sec_ospf_output: str) -> bool:
    pattern = r'(passive-interface default)'
    if re.search(pattern, sh_run_sec_ospf_output):
        return True
    return False


def get_ospf_area_ids(sh_ip_ospf_output: str) -> list[str] | None:
    pattern = r'(Area \d*)'
    match = re.findall(pattern, sh_ip_ospf_output)
    list_of_areas_id: list[str] = [m[5:] for m in match if len(m) > 5]
    if re.search(r'Area BACKBONE', sh_ip_ospf_output):
        list_of_areas_id.append('0')
    if len(list_of_areas_id) == 0:
        return None
    return list_of_areas_id


def get_ospf_area_authentication_message_digest(area_id: str, sh_run_sec_ospf_output: str) -> bool:
    pattern = f'(area {area_id} authentication message-digest)'
    if re.search(pattern, sh_run_sec_ospf_output):
        return True
    return False


def get_ospf_area_type(area_id: str, sh_run_sec_ospf_output: str) -> str:
    if re.search(f'(area {area_id} nssa)', sh_run_sec_ospf_output):
        return 'nssa'
    if re.search(f'(area {area_id} stub)', sh_run_sec_ospf_output):
        return 'stub'
    return 'standard'


def get_ospf_area_networks(area_id: str, sh_run_sec_ospf_output: str) -> dict[str, Network] | None:
    pattern = f'(network .* area {area_id})'
    match = re.findall(pattern, sh_run_sec_ospf_output)
    if not match:
        return None

    list_of_networks: list[str] = [line[len('network '):-len(f' area {area_id}')] for line in match]

    networks: dict[str, Network] = {}
    for network in list_of_networks:
        network_name, wildcard = network.split(' ')
        networks[network] = Network(network=network_name,
                                    mask=None,
                                    wildcard=wildcard)
    return networks


def get_ospf_area_information(area_id: str, sh_run_sec_ospf_output: str) -> OSPFArea:
    is_authentication_message_digest: bool = get_ospf_area_authentication_message_digest(area_id, sh_run_sec_ospf_output)
    area_type: str = get_ospf_area_type(area_id, sh_run_sec_ospf_output)
    networks: dict[str, Network] = get_ospf_area_networks(area_id, sh_run_sec_ospf_output)

    area_info = OSPFArea(id=area_id,
                         is_authentication_message_digest=is_authentication_message_digest,
                         type=area_type,
                         networks=networks)
    return area_info


def get_ospf_areas(sh_ip_ospf_output: str, sh_run_sec_ospf_output: str) -> dict[str, OSPFArea] | None:
    list_of_areas_id = get_ospf_area_ids(sh_ip_ospf_output)
    if list_of_areas_id is None:
        return None

    areas: dict[str, OSPFArea] = {}
    for area_id in list_of_areas_id:
        areas[area_id] = get_ospf_area_information(area_id, sh_run_sec_ospf_output)
    return areas


def get_ospf_neighbors(sh_ip_ospf_neighbors_output: str) -> dict[str, OSPFNeighbor] | None:
    pattern = r'(Neighbor ID)'
    match = re.findall(pattern, sh_ip_ospf_neighbors_output)
    if not match:
        return None

    neighbors: dict[str, OSPFNeighbor] = {}
    output_in_lines: list[str] = sh_ip_ospf_neighbors_output.splitlines()[2:]
    for output_line in output_in_lines:
        split_line = output_line.split()
        # ['192.168.1.1', '1', 'FULL/DR', '00:00:37', '192.168.1.1', 'FastEthernet0/1']
        neighbor_id: str = split_line[0]
        state: str = split_line[2]
        ip_address: str = split_line[-2]
        interface: str = split_line[-1]
        neighbors[neighbor_id] = OSPFNeighbor(neighbor_id=neighbor_id,
                                              state=state,
                                              ip_address=ip_address,
                                              interface=interface)
    return neighbors


def get_ospf_information(connection: netmiko.BaseConnection) -> OSPFInformation | None:
    connection.enable()
    sh_run_sec_ospf_output: str = connection.send_command("show run | sec ospf")
    sh_ip_ospf_database_output: str = connection.send_command("show ip ospf database")
    sh_ip_ospf_output: str = connection.send_command("show ip ospf")
    sh_ip_ospf_neighbors_output: str = connection.send_command("show ip ospf neighbor")
    connection.exit_enable_mode()

    if not is_ospf_enabled(sh_run_sec_ospf_output):
        return None

    process_id: int = get_ospf_process_id(sh_run_sec_ospf_output)
    router_id: str = get_ospf_router_id(sh_ip_ospf_database_output)
    auto_cost_reference_bandwidth: int = get_ospf_auto_cost_reference_bandwidth(sh_run_sec_ospf_output)
    default_information_originate: bool = get_routing_protocol_default_information_originate(sh_run_sec_ospf_output)
    default_metric_of_redistributed_routes: int = (
        get_routing_protocol_default_metric_of_redistributed_routes('ospf', sh_run_sec_ospf_output))
    distance: int = get_routing_protocol_distance('ospf', sh_run_sec_ospf_output)
    maximum_paths: int = get_routing_protocol_maximum_paths('ospf', sh_run_sec_ospf_output)
    passive_interface_default: bool = get_ospf_passive_interface_default(sh_run_sec_ospf_output)
    redistribution: Redistribution = get_routing_protocol_redistribution(sh_run_sec_ospf_output)
    areas: dict[str, OSPFArea] = get_ospf_areas(sh_ip_ospf_output, sh_run_sec_ospf_output)
    neighbors: dict[str, OSPFNeighbor] = get_ospf_neighbors(sh_ip_ospf_neighbors_output)

    ospf_info = OSPFInformation(process_id=process_id,
                                router_id=router_id,
                                auto_cost_reference_bandwidth=auto_cost_reference_bandwidth,
                                default_information_originate=default_information_originate,
                                default_metric_of_redistributed_routes=default_metric_of_redistributed_routes,
                                distance=distance,
                                maximum_paths=maximum_paths,
                                passive_interface_default=passive_interface_default,
                                redistribution=redistribution,
                                areas=areas,
                                neighbors=neighbors)
    return ospf_info


def get_ospf_conf_command_passive_interface(interface_name: str, passive_interface: bool) -> str:
    if passive_interface is True:
        return f'passive-interface {interface_name}'
    return f'no passive-interface {interface_name}'


def get_ospf_conf_commands_for_update_passive_interface_as_list(router: Router,
                                                                interfaces_names_and_passive_interface: list[list[str, bool]]) -> list[str] | None:
    list_of_commands: list[str] = []
    for interface_name, passive_interface in interfaces_names_and_passive_interface:
        if router.interfaces[interface_name].ospf.is_passive_interface_different(passive_interface):
            list_of_commands.append(get_ospf_conf_command_passive_interface(interface_name, passive_interface))

    if len(list_of_commands) > 0:
        return list_of_commands
    return None


def get_ospf_command_router_id(router_id: str) -> str:
    return f'router-id {router_id}'


def get_ospf_command_auto_cost_reference_bandwidth(auto_cost_reference_bandwidth: int) -> str:
    return f'auto-cost reference-bandwidth {auto_cost_reference_bandwidth}'


def get_ospf_command_passive_interface_default(passive_interface_default: bool) -> str:
    if passive_interface_default is True:
        return 'passive-interface default'
    return 'no passive-interface default'


def get_ospf_base_conf_commands_for_update_as_list(ospf: OSPFInformation, router_id: str,
                                                   auto_cost_reference_bandwidth: int,
                                                   default_information_originate: bool,
                                                   default_metric_of_redistributed_routes: int, distance: int,
                                                   maximum_paths: int, passive_interface_default: bool) -> list[str] | None:
    list_of_commands: list[str] = []
    if ospf.is_router_id_different(new_router_id_value=router_id):
        list_of_commands.append(get_ospf_command_router_id(router_id))

    if ospf.is_auto_cost_reference_bandwidth_different(
            new_auto_cost_reference_bandwidth_value=auto_cost_reference_bandwidth):
        list_of_commands.append(get_ospf_command_auto_cost_reference_bandwidth(auto_cost_reference_bandwidth))

    if ospf.is_default_information_originate_different(
            new_default_information_originate_value=default_information_originate):
        list_of_commands.append(get_conf_command_default_information_originate(default_information_originate))

    if ospf.is_default_metric_of_redistributed_routes_different(
            new_default_metric_of_redistributed_routes=default_metric_of_redistributed_routes):
        list_of_commands.append(get_conf_command_default_metric_of_redistributed_routes(
            default_metric_of_redistributed_routes))

    if ospf.is_distance_different(new_distance_value=distance):
        list_of_commands.append(get_conf_command_distance(distance))

    if ospf.is_maximum_paths_different(new_maximum_paths_value=maximum_paths):
        list_of_commands.append(get_conf_command_maximum_paths(maximum_paths))

    if ospf.is_passive_interface_default_different(new_passive_interface_default=passive_interface_default):
        list_of_commands.append(get_ospf_command_passive_interface_default(passive_interface_default))

    if len(list_of_commands) > 0:
        return list_of_commands
    return None


def get_ospf_area_base_conf_command_authentication_message_digest(area_id: str,
                                                                  authentication_message_digest: bool) -> str:
    if authentication_message_digest is True:
        return f'area {area_id} authentication message-digest'
    return f'no area {area_id} authentication message-digest'


def get_ospf_area_base_conf_command_type_as_list(area_id: str, current_type: str, new_type: str) -> list[str]:
    list_of_commands: list[str] = []
    if current_type == 'stub':
        list_of_commands.append(f'no area {area_id} stub')
    elif current_type == 'nssa':
        list_of_commands.append(f'no area {area_id} nssa')

    if new_type == 'stub':
        list_of_commands.append(f'area {area_id} stub')
    elif new_type == 'nssa':
        list_of_commands.append(f'area {area_id} nssa')

    return list_of_commands


def get_ospf_area_base_conf_commands_for_update_as_list(area: OSPFArea, authentication_message_digest: bool,
                                                        type: str) -> list[str] | None:
    list_of_commands: list[str] = []
    if area.is_authentication_message_digest_different(
            new_is_authentication_message_digest_value=authentication_message_digest):
        list_of_commands.append(get_ospf_area_base_conf_command_authentication_message_digest(
            area_id=area.id, authentication_message_digest=authentication_message_digest))

    if area.is_type_different(new_type_value=type):
        list_of_commands.extend(
            get_ospf_area_base_conf_command_type_as_list(area_id=area.id, current_type=area.type, new_type=type))

    if len(list_of_commands) > 0:
        return list_of_commands
    return None


def get_ospf_area_conf_networks_commands_as_list(area_id: str, network_and_wildcard: list[list[str]]) -> list[str] | None:
    list_of_commands: list[str] = []

    for network, wildcard in network_and_wildcard:
        list_of_commands.append(f'network {network} {wildcard} area {area_id}')

    if len(list_of_commands) > 0:
        return list_of_commands
    return None


def get_ospf_area_no_conf_networks_commands_as_list(area_id: str, network_and_wildcard: list[list[str]]) -> list[str] | None:
    list_of_commands: list[str] = []

    for network, wildcard in network_and_wildcard:
        list_of_commands.append(f'no network {network} {wildcard} area {area_id}')

    if len(list_of_commands) > 0:
        return list_of_commands
    return None
