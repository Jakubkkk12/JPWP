import netmiko
import re
from resources.routing_protocols.Network import Network
from resources.routing_protocols.Redistribution import Redistribution
from resources.routing_protocols.rip.RIPInformation import RIPInformation
from resources.cisco.getting_redistribution import get_routing_protocol_redistribution
from resources.cisco.getting_routing_protocol_information import (get_routing_protocol_distance,
                                                                  get_routing_protocol_default_information_originate,
                                                                  get_routing_protocol_maximum_paths,
                                                                  get_routing_protocol_version,
                                                                  get_routing_protocol_default_metric_of_redistributed_routes)


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
