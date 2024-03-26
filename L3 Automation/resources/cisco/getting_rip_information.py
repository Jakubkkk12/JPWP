import netmiko
import re
from resources.routing_protocols.Network import Network
from resources.routing_protocols.Redistribution import Redistribution
from resources.routing_protocols.rip.RIPInformation import RIPInformation
from resources.cisco.getting_redistribution import get_routing_protocol_redistribution
from resources.cisco.getting_routing_protocol import (get_routing_protocol_distance,
                                                      get_routing_protocol_default_information_originate,
                                                      get_routing_protocol_maximum_paths,
                                                      get_routing_protocol_version,
                                                      get_routing_protocol_default_metric_of_redistributed_routes,
                                                      get_conf_command_default_metric_of_redistributed_routes,
                                                      get_conf_command_default_information_originate,
                                                      get_conf_command_maximum_paths,
                                                      get_conf_command_distance,
                                                      get_conf_command_version)


########################################################################################################################
# Parsing functions:


def is_rip_enabled(sh_run_sec_ospf_output: str) -> bool:
    pattern = r'(router rip)'
    if re.search(pattern, sh_run_sec_ospf_output):
        return True
    return False


def get_rip_auto_summary(sh_run_sec_ospf_output: str) -> bool:
    pattern = r'(no auto-summary)'
    if re.search(pattern, sh_run_sec_ospf_output):
        return False
    return True


def get_rip_networks(sh_run_sec_ospf_output: str) -> dict[str, Network] | None:
    pattern = r'(network .*)'
    match = re.findall(pattern, sh_run_sec_ospf_output)
    if not match:
        return None

    networks: dict[str, Network] = {}
    nets: list[str] = [net[8:] for net in match]
    for net in nets:
        networks[net] = Network(network=net, mask=None)
    return networks


def get_rip_information(connection: netmiko.BaseConnection) -> RIPInformation | None:
    connection.enable()
    sh_run_sec_rip_output: str = connection.send_command("show run | sec rip")
    connection.exit_enable_mode()

    if not is_rip_enabled(sh_run_sec_rip_output):
        return None

    auto_summary: bool = get_rip_auto_summary(sh_run_sec_rip_output)
    default_information_originate: bool = get_routing_protocol_default_information_originate(sh_run_sec_rip_output)
    default_metric_of_redistributed_routes: int = get_routing_protocol_default_metric_of_redistributed_routes(
        'rip', sh_run_sec_rip_output)
    distance: int = get_routing_protocol_distance('rip', sh_run_sec_rip_output)
    maximum_paths: int = get_routing_protocol_maximum_paths('rip', sh_run_sec_rip_output)
    redistribution: Redistribution = get_routing_protocol_redistribution(sh_run_sec_rip_output)
    networks: dict[str, Network] = get_rip_networks(sh_run_sec_rip_output)
    version: int = get_routing_protocol_version('rip', sh_run_sec_rip_output)

    rip_info = RIPInformation(auto_summary=auto_summary,
                              default_information_originate=default_information_originate,
                              default_metric_of_redistributed_routes=default_metric_of_redistributed_routes,
                              distance=distance,
                              maximum_paths=maximum_paths,
                              redistribution=redistribution,
                              networks=networks,
                              version=version)
    return rip_info


########################################################################################################################
# Configure functions:


def get_rip_conf_command_auto_summary(auto_summary: bool) -> str:
    if auto_summary is True:
        return 'auto-summary'
    return 'no auto-summary'


def get_rip_conf_basic_commands_for_update_as_list(rip: RIPInformation, auto_summary: bool,
                                                   default_information_originate: bool,
                                                   default_metric_of_redistributed_routes: int, distance: int,
                                                   maximum_paths: int, version: int) -> list[str] | None:
    list_of_commands: list[str] = []
    if rip.is_auto_summary_different(new_auto_summary_value=auto_summary):
        list_of_commands.append(get_rip_conf_command_auto_summary(auto_summary))

    if rip.is_default_information_originate_different(
            new_default_information_originate_value=default_information_originate):
        list_of_commands.append(get_conf_command_default_information_originate(default_information_originate))

    if rip.is_default_metric_of_redistributed_routes_different(
            new_default_metric_of_redistributed_routes=default_metric_of_redistributed_routes):
        list_of_commands.append(get_conf_command_default_metric_of_redistributed_routes(
            default_metric_of_redistributed_routes))

    if rip.is_distance_different(new_distance_value=distance):
        list_of_commands.append(get_conf_command_distance(distance))

    if rip.is_maximum_paths_different(new_maximum_paths_value=maximum_paths):
        list_of_commands.append(get_conf_command_maximum_paths(maximum_paths))

    if rip.is_version_different(new_version_value=version):
        list_of_commands.append(get_conf_command_version(version))

    if len(list_of_commands) > 0:
        return list_of_commands
    return None


def get_rip_conf_networks_commands_as_list(list_of_networks: list[str]) -> list[str] | None:
    list_of_commands: list[str] = []

    for network_id in list_of_networks:
        list_of_commands.append(f'network {network_id}')

    if len(list_of_commands) > 0:
        return list_of_commands
    return None


def get_rip_no_conf_networks_commands_as_list(list_of_networks: list[str]) -> list[str] | None:
    list_of_commands: list[str] = []

    for network_id in list_of_networks:
        list_of_commands.append(f'no network {network_id}')

    if len(list_of_commands) > 0:
        return list_of_commands
    return None
