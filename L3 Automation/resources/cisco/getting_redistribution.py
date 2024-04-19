import re
from resources.routing_protocols.Redistribution import Redistribution
from resources.devices.Router import Router


########################################################################################################################
# Parsing functions:


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


########################################################################################################################
# Configure functions:


def get_conf_command_for_ospf(ospf: bool, ospf_proces: int, subnets: str) -> str:
    if ospf is True:
        return f'redistribute ospf {ospf_proces} {subnets}'
    return f'no redistribute ospf {ospf_proces}'


def get_conf_command_for_rip(rip: bool, subnets: str) -> str:
    if rip is True:
        return f'redistribute rip {subnets}'
    return f'no redistribute rip'


def get_conf_command_for_bgp(bgp: bool, bgp_as: int, subnets: str) -> str:
    if bgp is True:
        return f'redistribute bgp {bgp_as} {subnets}'
    return f'no redistribute bgp {bgp_as}'


def get_conf_command_for_static(static: bool, subnets: str) -> str:
    if static is True:
        return f'redistribute static {subnets}'
    return f'no redistribute static'


def get_conf_command_for_connected(connected: bool, subnets: str) -> str:
    if connected:
        return f'redistribute connected {subnets}'
    return f'no redistribute connected'


def get_redistribution_conf_commands_as_list(redistribution: Redistribution, ospf: bool, rip: bool, bgp: bool,
                                             static: bool, connected: bool, bgp_as: int | None,
                                             ospf_proces: int | None, subnets_on: bool) -> list[str] | None:
    list_of_commands: list[str] = []
    subnets: str = ''
    if subnets_on:
        subnets = 'subnets'

    if ospf_proces is not None and redistribution.is_redistribute_ospf_different(new_is_redistribute_ospf_value=ospf):
        list_of_commands.append(get_conf_command_for_ospf(ospf, ospf_proces, subnets))

    if bgp_as is not None and redistribution.is_redistribute_bgp_different(new_is_redistribute_bgp_value=bgp):
        list_of_commands.append(get_conf_command_for_bgp(bgp, bgp_as, subnets))

    if redistribution.is_redistribute_rip_different(new_is_redistribute_rip_value=rip):
        list_of_commands.append(get_conf_command_for_rip(rip, subnets))

    if redistribution.is_is_redistribute_static_different(new_is_is_redistribute_static_value=static):
        list_of_commands.append(get_conf_command_for_static(static, subnets))

    if redistribution.is_redistribute_connected_different(new_is_redistribute_connected_value=connected):
        list_of_commands.append(get_conf_command_for_connected(connected, subnets))

    if len(list_of_commands) > 0:
        return list_of_commands
    return None
