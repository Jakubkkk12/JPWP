import re
from resources.routing_protocols.Redistribution import Redistribution


def is_any_redistribution(sh_run_sec_routing_protocol_output: str) -> bool:
    pattern = r'(redistribute)'
    if re.search(pattern, sh_run_sec_routing_protocol_output):
        return True
    return False


def is_ospf_redistribution(sh_run_sec_routing_protocol_output: str) -> bool:
    pattern = r'(redistribute ospf)'
    if re.search(pattern, sh_run_sec_routing_protocol_output):
        return True
    return False


def is_rip_redistribution(sh_run_sec_routing_protocol_output: str) -> bool:
    pattern = r'(redistribute rip)'
    if re.search(pattern, sh_run_sec_routing_protocol_output):
        return True
    return False


def is_bgp_redistribution(sh_run_sec_routing_protocol_output: str) -> bool:
    pattern = r'(redistribute bgp)'
    if re.search(pattern, sh_run_sec_routing_protocol_output):
        return True
    return False


def is_connected_redistribution(sh_run_sec_routing_protocol_output: str) -> bool:
    pattern = r'(redistribute connected)'
    if re.search(pattern, sh_run_sec_routing_protocol_output):
        return True
    return False


def is_static_redistribution(sh_run_sec_routing_protocol_output: str) -> bool:
    pattern = r'(redistribute static)'
    if re.search(pattern, sh_run_sec_routing_protocol_output):
        return True
    return False


def get_routing_protocol_redistribution(sh_run_sec_routing_protocol_output: str) -> Redistribution | None:
    if not is_any_redistribution(sh_run_sec_routing_protocol_output):
        return None

    is_redistribute_ospf: bool = is_ospf_redistribution(sh_run_sec_routing_protocol_output)
    is_redistribute_rip: bool = is_rip_redistribution(sh_run_sec_routing_protocol_output)
    is_redistribute_bgp: bool = is_bgp_redistribution(sh_run_sec_routing_protocol_output)
    is_redistribute_static: bool = is_static_redistribution(sh_run_sec_routing_protocol_output)
    is_redistribute_connected: bool = is_connected_redistribution(sh_run_sec_routing_protocol_output)

    return Redistribution(is_redistribute_ospf=is_redistribute_ospf,
                          is_redistribute_rip=is_redistribute_rip,
                          is_redistribute_bgp=is_redistribute_bgp,
                          is_redistribute_static=is_redistribute_static,
                          is_redistribute_connected=is_redistribute_connected)