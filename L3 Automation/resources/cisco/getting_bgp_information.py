import netmiko
import re
from resources.routing_protocols.bgp.BGPTimers import BGPTimers
from resources.routing_protocols.bgp.BGPNeighbor import BGPNeighbor
from resources.routing_protocols.bgp.BGPInformation import BGPInformation
from resources.routing_protocols.Redistribution import Redistribution
from resources.routing_protocols.Network import Network
from resources.cisco.getting_redistribution import get_routing_protocol_redistribution
from resources.cisco.getting_routing_protocol_information import (get_routing_protocol_distance,
                                                                  get_routing_protocol_default_information_originate,
                                                                  get_routing_protocol_default_metric_of_redistributed_routes)


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

## tddo
def get_bgp_router_id(sh_run_sec_bgp_output: str) -> int | None:
    pattern = r'(router bgp )\d*'
    match = re.search(pattern, sh_run_sec_bgp_output)
    if match:
        autonomous_system = int(match.group()[len('router bgp '):])
        return autonomous_system
    return None


def get_bgp_information(connection: netmiko.BaseConnection) -> BGPInformation | None:
    connection.enable()
    sh_run_sec_bgp_output: str = connection.send_command("show run | sec bgp")
    connection.exit_enable_mode()

    if not is_bgp_enabled(sh_run_sec_bgp_output):
        return None

    autonomous_system: int = get_bgp_autonomous_system(sh_run_sec_bgp_output)
    router_id: str = get
    default_information_originate: bool = get_routing_protocol_default_information_originate(sh_run_sec_bgp_output)
    default_metric_of_redistributed_routes: int = (
        get_routing_protocol_default_metric_of_redistributed_routes('bgp', sh_run_sec_bgp_output))
    redistribution: Redistribution = get_routing_protocol_redistribution(sh_run_sec_bgp_output)
    networks: dict[str, Network] = None
    timers: BGPTimers = None
    neighbors: dict[str, BGPNeighbor] = None
