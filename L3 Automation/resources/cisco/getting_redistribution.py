import re
from resources.routing_protocols.Redistribution import Redistribution
from resources.devices.Router import Router


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


def get_conf_command_as_list(redistribution: Redistribution, ospf: bool, rip: bool, bgp: bool, static: bool,
                             connected: bool, bgp_as: int = None, ospf_proces: int = None, subnets_on: bool = False) -> list[str] | None:

    list_of_commands: list[str] = []
    subnets: str = ''
    if subnets_on:
        subnets = 'subnets'

    if ospf_proces is not None and redistribution.is_redistribute_ospf_different(new_is_redistribute_ospf_value=ospf):
        if ospf is True:
            list_of_commands.append(f'redistribute ospf {ospf_proces} {subnets}')
        else:
            list_of_commands.append(f'no redistribute ospf {ospf_proces}')

    if bgp_as is not None and redistribution.is_redistribute_bgp_different(new_is_redistribute_bgp_value=bgp):
        if bgp_as is True:
            list_of_commands.append(f'redistribute bgp {bgp_as} {subnets}')
        else:
            list_of_commands.append(f'no redistribute bgp {bgp_as}')

    if redistribution.is_redistribute_rip_different(new_is_redistribute_rip_value=rip):
        if rip is True:
            list_of_commands.append(f'redistribute rip {subnets}')
        else:
            list_of_commands.append(f'no redistribute rip')

    if redistribution.is_is_redistribute_static_different(new_is_is_redistribute_static_value=static):
        if static is True:
            list_of_commands.append(f'redistribute static {subnets}')
        else:
            list_of_commands.append(f'no redistribute static')

    if redistribution.is_redistribute_connected_different(new_is_redistribute_connected_value=connected):
        if connected is True:
            list_of_commands.append(f'redistribute connected {subnets}')
        else:
            list_of_commands.append(f'redistribute connected')

    if len(list_of_commands) > 0:
        return list_of_commands
    return None

