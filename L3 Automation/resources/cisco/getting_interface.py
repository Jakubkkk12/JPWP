import re
import netmiko

from resources.interfaces.InterfaceOSPFInformation import InterfaceOSPFInformation
from resources.interfaces.RouterInterface import RouterInterface
from resources.interfaces.InterfaceStatistics import InterfaceStatistics, InformationStatistics, ErrorsStatistics
from resources.routing_protocols.ospf.OSPFTimers import OSPFTimers
from resources.constants import NETWORK_MASK


########################################################################################################################
# Parsing Interface/RouterInterface functions:


def get_interfaces_name(sh_ip_int_br_output: str) -> list[str]:
    interfaces_name: list[str] = [line.split()[0] for line in sh_ip_int_br_output.splitlines()]
    except_first: slice = slice(1, len(interfaces_name))
    interfaces_name = [int_name for int_name in interfaces_name[except_first] if not int_name.startswith('Vlan')]
    return interfaces_name


def get_interface_statistics_input_errors(sh_int_name_output: str) -> int | None:
    pattern: str = r'\d*( input errors)'
    match: re.Match = re.search(pattern, sh_int_name_output)
    if match:
        input_errors = int(match.group()[:-len(' input errors')])
        return input_errors
    return None


def get_interface_statistics_output_errors(sh_int_name_output: str) -> int | None:
    pattern = r'\d*( output errors)'
    match = re.search(pattern, sh_int_name_output)
    if match:
        output_errors = int(match.group()[:-len(' output errors')])
        return output_errors
    return None


def get_interface_statistics_output_buffer_failures(sh_int_name_output: str) -> int | None:
    pattern = r'\d*( output buffer failures)'
    match = re.search(pattern, sh_int_name_output)
    if match:
        output_buffer_failures = int(match.group()[:-len(' output buffer failures')])
        return output_buffer_failures
    return None


def get_interface_statistics_runts(sh_int_name_output: str) -> int | None:
    pattern = r'\d*( runts)'
    match = re.search(pattern, sh_int_name_output)
    if match:
        runts = int(match.group()[:-len(' runts')])
        return runts
    return None


def get_interface_statistics_giants(sh_int_name_output: str) -> int | None:
    pattern = r'\d*( giants)'
    match = re.search(pattern, sh_int_name_output)
    if match:
        giants = int(match.group()[:-len(' giants')])
        return giants
    return None


def get_interface_statistics_throttles(sh_int_name_output: str) -> int | None:
    pattern = r'\d*( throttles)'
    match = re.search(pattern, sh_int_name_output)
    if match:
        throttles = int(match.group()[:-len(' throttles')])
        return throttles
    return None


def get_interface_statistics_crc(sh_int_name_output: str) -> int | None:
    pattern = r'\d*( CRC)'
    match = re.search(pattern, sh_int_name_output)
    if match:
        crc = int(match.group()[:-len(' CRC')])
        return crc
    return None


def get_interface_statistics_frame(sh_int_name_output: str) -> int | None:
    pattern = r'\d*( frame)'
    match = re.search(pattern, sh_int_name_output)
    if match:
        frame = int(match.group()[:-len(' frame')])
        return frame
    return None


def get_interface_statistics_overrun(sh_int_name_output: str) -> int | None:
    pattern = r'\d*( overrun)'
    match = re.search(pattern, sh_int_name_output)
    if match:
        overrun = int(match.group()[:-len(' overrun')])
        return overrun
    return None


def get_interface_statistics_ignored(sh_int_name_output: str) -> int | None:
    pattern = r'\d*( ignored)'
    match = re.search(pattern, sh_int_name_output)
    if match:
        ignored = int(match.group()[:-len(' ignored')])
        return ignored
    return None


def get_interface_statistics_collision(sh_int_name_output: str) -> int | None:
    pattern = r'\d*( collisions)'
    match = re.search(pattern, sh_int_name_output)
    if match:
        collision = int(match.group()[:-len(' collisions')])
        return collision
    return None


def get_interface_statistics_late_collision(sh_int_name_output: str) -> int | None:
    pattern = r'\d*( late collision)'
    match = re.search(pattern, sh_int_name_output)
    if match:
        late_collision = int(match.group()[:-len(' late collision')])
        return late_collision
    return None


def get_interface_statistics_broadcast(sh_int_name_output: str) -> int | None:
    pattern = r'\d*( broadcasts)'
    match = re.search(pattern, sh_int_name_output)
    if match:
        broadcast = int(match.group()[:-len(' broadcasts')])
        return broadcast
    return None


def get_interface_statistics_packets_input(sh_int_name_output: str) -> int | None:
    pattern = r'\d*( packets input)'
    match = re.search(pattern, sh_int_name_output)
    if match:
        packets_input = int(match.group()[:-len(' packets input')])
        return packets_input
    return None


def get_interface_statistics_packets_output(sh_int_name_output: str) -> int | None:
    pattern = r'\d*( packets output)'
    match = re.search(pattern, sh_int_name_output)
    if match:
        packets_output = int(match.group()[:-len(' packets output')])
        return packets_output
    return None


def get_interface_statistics_mtu(sh_int_name_output: str) -> int | None:
    pattern = r'(MTU )\d*'
    match = re.search(pattern, sh_int_name_output)
    if match:
        mtu = int(match.group()[len('MTU '):])
        return mtu
    return None


def get_interface_statistics_dulpex(sh_int_name_output: str) -> str:
    if re.search(r'(Half-duplex)', sh_int_name_output):
        duplex = 'half'
    elif re.search(r'(Full-duplex)', sh_int_name_output):
        duplex = 'full'
    else:
        duplex = 'auto'
    return duplex


def get_interface_statistics_speed(sh_int_name_output: str) -> str | None:
    if (re.search(r'(Auto-speed)', sh_int_name_output)
            or re.search(r'(Auto Speed)', sh_int_name_output)):
        speed = 'auto'
        return speed
    else:
        pattern = r'(duplex, ).*(,)'
        match = re.search(pattern, sh_int_name_output)
        if match:
            speed = match.group()[len('duplex, '):-1]
            return speed
    return None


def get_interface_statistics_layer1_status(sh_int_name_output: str) -> str | None:
    pattern = r'(is ).*(, line protocol)'
    match = re.search(pattern, sh_int_name_output)
    if match:
        layer1_status = match.group()[len('is '):-len(', line protocol')]
        return layer1_status
    return None


def get_interface_statistics_layer2_status(sh_int_name_output: str) -> str | None:
    pattern = r'(line protocol is ).*'
    match = re.search(pattern, sh_int_name_output)
    if match:
        layer2_status = match.group()[len('line protocol is '):]
        return layer2_status
    return None


def get_interface_statistics_encapsulation(sh_int_name_output: str) -> str | None:
    pattern = r'(Encapsulation ).*(,)'
    match = re.search(pattern, sh_int_name_output)
    if match:
        encapsulation = match.group()[len('Encapsulation '):-1]
        return encapsulation
    return None


def get_interface_description(sh_int_name_output: str) -> str | None:
    pattern: str = r'(Description:)\s.*'
    match: re.Match[str] = re.search(pattern, sh_int_name_output)
    only_description: slice = slice(13, None, None)
    if match:
        return match.group()[only_description]
    return None


def get_interface_ip_address(sh_int_name_output: str) -> dict[str, str | int | None]:
    full_ip_address_pattern: str = r'\d*[.]\d*[.]\d*[.]\d*[/]\d*'
    is_found_full_ip_address_match: re.Match[str] = re.search(full_ip_address_pattern, sh_int_name_output)
    ip_address: str = 'unassigned'
    subnet: int | None = None
    if is_found_full_ip_address_match:
        full_ip_address: str = is_found_full_ip_address_match.group()
        ip_address = re.search(r'\d*[.]\d*[.]\d*[.]\d*', full_ip_address).group()
        without_slash: slice = slice(1, None, None)
        subnet = int(re.search(r'[/]\d*', full_ip_address).group()[without_slash])

    return {'ip_address': ip_address, 'subnet': subnet}


def get_interface_errors_statistics(sh_int_name_output: str) -> ErrorsStatistics:
    input_errors: int = get_interface_statistics_input_errors(sh_int_name_output)
    output_errors: int = get_interface_statistics_output_errors(sh_int_name_output)
    output_buffer_failures: int = get_interface_statistics_output_buffer_failures(sh_int_name_output)
    runts: int = get_interface_statistics_runts(sh_int_name_output)
    giants: int = get_interface_statistics_giants(sh_int_name_output)
    crc: int = get_interface_statistics_crc(sh_int_name_output)
    frame: int = get_interface_statistics_frame(sh_int_name_output)
    throttles: int = get_interface_statistics_throttles(sh_int_name_output)
    overrun: int = get_interface_statistics_overrun(sh_int_name_output)
    ignored: int = get_interface_statistics_ignored(sh_int_name_output)

    err_stat: ErrorsStatistics = ErrorsStatistics(input_errors=input_errors,
                                                  output_errors=output_errors,
                                                  output_buffer_failures=output_buffer_failures,
                                                  runts=runts,
                                                  giants=giants,
                                                  crc=crc,
                                                  frame=frame,
                                                  throttles=throttles,
                                                  overrun=overrun,
                                                  ignored=ignored)
    return err_stat


def get_interface_information_statistics(sh_int_name_output: str) -> InformationStatistics:
    collision: int = get_interface_statistics_collision(sh_int_name_output)
    late_collision: int = get_interface_statistics_late_collision(sh_int_name_output)
    broadcast: int = get_interface_statistics_broadcast(sh_int_name_output)
    packets_input: int = get_interface_statistics_packets_input(sh_int_name_output)
    packets_output: int = get_interface_statistics_packets_output(sh_int_name_output)
    duplex: str = get_interface_statistics_dulpex(sh_int_name_output)
    speed: str = get_interface_statistics_speed(sh_int_name_output)
    layer1_status: str = get_interface_statistics_layer1_status(sh_int_name_output)
    layer2_status: str = get_interface_statistics_layer2_status(sh_int_name_output)
    mtu: int = get_interface_statistics_mtu(sh_int_name_output)
    encapsulation: str = get_interface_statistics_encapsulation(sh_int_name_output)

    info_stat: InformationStatistics = InformationStatistics(collision=collision,
                                                             late_collision=late_collision,
                                                             broadcast=broadcast,
                                                             packets_input=packets_input,
                                                             packets_output=packets_output,
                                                             duplex=duplex,
                                                             speed=speed,
                                                             layer1_status=layer1_status,
                                                             layer2_status=layer2_status,
                                                             mtu=mtu,
                                                             encapsulation=encapsulation)
    return info_stat


def get_interface_statistics(sh_int_name_output: str) -> InterfaceStatistics:
    info_stat: InformationStatistics = get_interface_information_statistics(sh_int_name_output)
    err_stat: ErrorsStatistics = get_interface_errors_statistics(sh_int_name_output)
    int_stat: InterfaceStatistics = InterfaceStatistics(information=info_stat, errors=err_stat)

    return int_stat


def get_base_interface_information(interface_name: str, sh_int_name_output: str) -> RouterInterface:
    interface_ip_address: dict[str, str | int | None] = get_interface_ip_address(sh_int_name_output)
    description: str | None = get_interface_description(sh_int_name_output)
    statistics: InterfaceStatistics = get_interface_statistics(sh_int_name_output)

    router_interface: RouterInterface = RouterInterface(name=interface_name,
                                                        description=description,
                                                        ip_address=interface_ip_address['ip_address'],
                                                        subnet=interface_ip_address['subnet'],
                                                        statistics=statistics)
    return router_interface


########################################################################################################################
# Configure Interface/RouterInterface functions:


def get_interface_conf_command_interface_description(description: str) -> str:
    return f'description {description}'


def get_interface_conf_command_interface_ip_address(interface_name: str, subnet: str) -> str:
    return f'ip address {interface_name} {subnet}'


def get_interface_conf_no_command_interface_ip_address() -> str:
    return f'no ip address'


def get_interface_conf_command_interface_duplex(duplex: str) -> str | None:
    if duplex == 'None':
        return None
    return f'duplex {duplex}'


def get_interface_conf_command_interface_speed(speed: str) -> str | None:
    if speed == 'None':
        return None
    if speed == '1000Mbps':
        return f'speed 1000'
    if speed == '100Mbps':
        return f'speed 100'
    if speed == '10Mbps':
        return f'speed 10'
    return f'speed auto'


def get_interface_conf_command_interface_mtu(mtu: int) -> str:
    return f'mtu {mtu}'


def get_interface_base_conf_commands_for_update_as_list(router_interface: RouterInterface, description: str,
                                                        ip_address: str, subnet: int, duplex: str, speed: str,
                                                        mtu: int) -> list[str] | None:
    list_of_commands: list[str] = []
    if router_interface.is_description_different(new_description_value=description):
        list_of_commands.append(get_interface_conf_command_interface_description(description))

    if (router_interface.is_ip_address_different(new_ip_address_value=ip_address)
            or router_interface.is_subnet_different(new_subnet_value=subnet)):
        list_of_commands.append(get_interface_conf_command_interface_ip_address(ip_address, NETWORK_MASK[subnet]))

    if router_interface.statistics.information.is_speed_different(new_speed_value=speed):
        command: str | None = get_interface_conf_command_interface_speed(speed)
        if command is not None:
            list_of_commands.append(command)

    if router_interface.statistics.information.is_duplex_different(new_duplex_value=duplex):
        command: str | None = get_interface_conf_command_interface_duplex(duplex)
        if command is not None:
            list_of_commands.append(command)

    if router_interface.statistics.information.is_mtu_different(new_mtu_value=mtu):
        list_of_commands.append(get_interface_conf_command_interface_mtu(mtu))

    if len(list_of_commands) > 0:
        return list_of_commands
    return None


def get_interface_base_conf_commands_for_set_default(router_interface: RouterInterface) -> str:
    return f'default interface {router_interface.name}'

########################################################################################################################
# Parsing InterfaceOSPFInformation functions:


def is_ospf_enabled(sh_ip_ospf_int_name_output: str) -> bool:
    pattern = r'(OSPF not enabled)'
    if re.search(pattern, sh_ip_ospf_int_name_output):
        return False
    return True


def get_interface_ospf_network_type(sh_ip_ospf_int_name_output: str) -> str | None:
    pattern = r'(Network Type ).*(,)'
    match = re.search(pattern, sh_ip_ospf_int_name_output)
    if match:
        network_type = match.group()[len('Network Type '):-1].lower()
        return network_type
    return None


def get_interface_ospf_cost(sh_ip_ospf_int_name_output: str) -> int | None:
    pattern = r'(Cost: )\d*'
    match = re.search(pattern, sh_ip_ospf_int_name_output)
    if match:
        cost = int(match.group()[len('Cost: '):])
        return cost
    return None


def get_interface_ospf_state(sh_ip_ospf_int_name_output: str) -> str | None:
    pattern = r'(State ).*(,)'
    match = re.search(pattern, sh_ip_ospf_int_name_output)
    if match:
        state = match.group()[len('State '):-1]
        return state
    return None


def get_interface_ospf_priority(sh_ip_ospf_int_name_output: str) -> int | None:
    pattern = r'(Priority )\d*'
    match = re.search(pattern, sh_ip_ospf_int_name_output)
    if match:
        priority = int(match.group()[len('Priority '):])
        return priority
    return None


def get_interface_ospf_passive_interface(sh_ip_ospf_int_name_output: str) -> bool:
    pattern = r'(Passive interface)'
    if re.search(pattern, sh_ip_ospf_int_name_output):
        return True
    return False


def get_interface_ospf_timer_hello(sh_ip_ospf_int_name_output: str) -> int | None:
    pattern = r'(Hello )\d*'
    match = re.search(pattern, sh_ip_ospf_int_name_output)
    if match:
        hello = int(match.group()[len('Hello '):])
        return hello
    return None


def get_interface_ospf_timer_dead(sh_ip_ospf_int_name_output: str) -> int | None:
    pattern = r'(Dead )\d*'
    match = re.search(pattern, sh_ip_ospf_int_name_output)
    if match:
        dead = int(match.group()[len('Dead '):])
        return dead
    return None


def get_interface_ospf_timer_wait(sh_ip_ospf_int_name_output: str) -> int | None:
    pattern = r'(Wait )\d*'
    match = re.search(pattern, sh_ip_ospf_int_name_output)
    if match:
        wait = int(match.group()[len('Wait '):])
        return wait
    return None


def get_interface_ospf_timer_retransmit(sh_ip_ospf_int_name_output: str) -> int | None:
    pattern = r'(Retransmit )\d*'
    match = re.search(pattern, sh_ip_ospf_int_name_output)
    if match:
        retransmit = int(match.group()[len('Retransmit '):])
        return retransmit
    return None


def get_interface_ospf_timers(sh_ip_ospf_int_name_output: str) -> OSPFTimers | None:
    hello_timer: int = get_interface_ospf_timer_hello(sh_ip_ospf_int_name_output)
    dead_timer: int = get_interface_ospf_timer_dead(sh_ip_ospf_int_name_output)
    wait_timer: int = get_interface_ospf_timer_wait(sh_ip_ospf_int_name_output)
    retransmit_timer: int = get_interface_ospf_timer_retransmit(sh_ip_ospf_int_name_output)

    timers = OSPFTimers(hello_timer=hello_timer,
                        dead_timer=dead_timer,
                        wait_timer=wait_timer,
                        retransmit_timer=retransmit_timer)

    return timers


def get_interface_ospf_information(sh_ip_ospf_int_name_output: str) -> InterfaceOSPFInformation | None:
    if not is_ospf_enabled(sh_ip_ospf_int_name_output):
        return None

    network_type: str = get_interface_ospf_network_type(sh_ip_ospf_int_name_output)
    cost: int = get_interface_ospf_cost(sh_ip_ospf_int_name_output)
    state: str = get_interface_ospf_state(sh_ip_ospf_int_name_output)
    passive_interface: bool = get_interface_ospf_passive_interface(sh_ip_ospf_int_name_output)
    priority: int = get_interface_ospf_priority(sh_ip_ospf_int_name_output)
    timers: OSPFTimers = get_interface_ospf_timers(sh_ip_ospf_int_name_output)

    ospf_info: InterfaceOSPFInformation = InterfaceOSPFInformation(network_type=network_type,
                                                                   cost=cost,
                                                                   state=state,
                                                                   passive_interface=passive_interface,
                                                                   priority=priority,
                                                                   timers=timers)
    return ospf_info


########################################################################################################################
# Configure InterfaceOSPF functions:


def get_interface_ospf_conf_command_network_type(network_type: str) -> str:
    return f'ip ospf network {network_type}'


def get_interface_ospf_conf_command_cost(cost: int) -> str:
    return f'ip ospf cost {cost}'


def get_interface_ospf_conf_priority(priority: int) -> str:
    return f'ip ospf priority {priority}'


def get_interface_ospf_conf_authentication_message_digest(authentication_message_digest: bool,
                                                          authentication_password: str) -> list[str]:
    if authentication_message_digest is True:
        return ['ip ospf authentication message-digest', f'ip ospf message-digest-key 1 md5 {authentication_password}']
    return ['no ip ospf authentication', f'no ip ospf message-digest-key 1 md5']


def get_interface_ospf_conf_hello_timer(hello_timer: int) -> str:
    return f'ip ospf hello-interval {hello_timer}'


def get_interface_ospf_conf_dead_timer(dead_timer: int) -> str:
    return f'ip ospf dead-interval {dead_timer}'


def get_interface_ospf_conf_retransmit_timer(retransmit_timer: int) -> str:
    return f'ip ospf retransmit-interval {retransmit_timer}'


def get_interface_ospf_conf_commands_for_update_as_list(ospf_info: InterfaceOSPFInformation, network_type: str,
                                                        cost: int, priority: int, authentication_message_digest: bool,
                                                        authentication_password: str, hello_timer: int, dead_timer: int,
                                                        retransmit_timer: int) -> list[str] | None:
    list_of_commands: list[str] = []
    if ospf_info.is_network_type_different(new_network_type_value=network_type):
        list_of_commands.append(get_interface_ospf_conf_command_network_type(network_type))

    if ospf_info.is_cost_different(new_cost_value=cost):
        list_of_commands.append(get_interface_ospf_conf_command_cost(cost))

    if ospf_info.is_priority_different(new_priority_value=priority):
        list_of_commands.append(get_interface_ospf_conf_priority(priority))

    if ospf_info.is_authentication_message_digest_different(
            new_authentication_message_digest_value=authentication_message_digest):
        list_of_commands.extend(get_interface_ospf_conf_authentication_message_digest(authentication_message_digest,
                                                                                      authentication_password))

    if ospf_info.timers.is_hello_timer_different(new_hello_timer_value=hello_timer):
        list_of_commands.append(get_interface_ospf_conf_hello_timer(hello_timer))

    if ospf_info.timers.is_dead_timer_different(new_dead_timer_value=dead_timer):
        list_of_commands.append(get_interface_ospf_conf_dead_timer(dead_timer))

    if ospf_info.timers.is_retransmit_timer_different(new_retransmit_timer_value=retransmit_timer):
        list_of_commands.append(get_interface_ospf_conf_retransmit_timer(retransmit_timer))

    if len(list_of_commands) > 0:
        return list_of_commands
    return None
