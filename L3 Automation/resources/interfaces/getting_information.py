import re
import netmiko
from resources.interfaces.RouterInterface import RouterInterface
from resources.interfaces.InterfaceStatistics import InterfaceStatistics, InformationStatistics, ErrorsStatistics


def get_interfaces_name(connection: netmiko.BaseConnection) -> list[str]:
    connection.enable()
    output: str = connection.send_command("show ip int br")
    connection.exit_enable_mode()
    interfaces_name: list[str] = [line.split()[0] for line in output.splitlines()]
    except_first: slice = slice(1, len(interfaces_name))
    interfaces_name = [int_name for int_name in interfaces_name[except_first] if not int_name.startswith('Vlan')]
    return interfaces_name


def get_interfaces_statistics_input_errors(sh_int_name_output: str) -> int | None:
    pattern: str = r'\d*( input errors)'
    match: re.Match = re.search(pattern, sh_int_name_output)
    if match:
        input_errors = int(match.group()[:-len(' input errors')])
        return input_errors
    return None


def get_interfaces_statistics_output_errors(sh_int_name_output: str) -> int | None:
    pattern = r'\d*( output errors)'
    match = re.search(pattern, sh_int_name_output)
    if match:
        output_errors = int(match.group()[:-len(' output errors')])
        return output_errors
    return None


def get_interfaces_statistics_output_buffer_failures(sh_int_name_output: str) -> int | None:
    pattern = r'\d*( output buffer failures)'
    match = re.search(pattern, sh_int_name_output)
    if match:
        output_buffer_failures = int(match.group()[:-len(' output buffer failures')])
        return output_buffer_failures
    return None


def get_interfaces_statistics_runts(sh_int_name_output: str) -> int | None:
    pattern = r'\d*( runts)'
    match = re.search(pattern, sh_int_name_output)
    if match:
        runts = int(match.group()[:-len(' runts')])
        return runts
    return None


def get_interfaces_statistics_giants(sh_int_name_output: str) -> int | None:
    pattern = r'\d*( giants)'
    match = re.search(pattern, sh_int_name_output)
    if match:
        giants = int(match.group()[:-len(' giants')])
        return giants
    return None


def get_interfaces_statistics_throttles(sh_int_name_output: str) -> int | None:
    pattern = r'\d*( throttles)'
    match = re.search(pattern, sh_int_name_output)
    if match:
        throttles = int(match.group()[:-len(' throttles')])
        return throttles
    return None


def get_interfaces_statistics_crc(sh_int_name_output: str) -> int | None:
    pattern = r'\d*( CRC)'
    match = re.search(pattern, sh_int_name_output)
    if match:
        crc = int(match.group()[:-len(' CRC')])
        return crc
    return None


def get_interfaces_statistics_frame(sh_int_name_output: str) -> int | None:
    pattern = r'\d*( frame)'
    match = re.search(pattern, sh_int_name_output)
    if match:
        frame = int(match.group()[:-len(' frame')])
        return frame
    return None


def get_interfaces_statistics_overrun(sh_int_name_output: str) -> int | None:
    pattern = r'\d*( overrun)'
    match = re.search(pattern, sh_int_name_output)
    if match:
        overrun = int(match.group()[:-len(' overrun')])
        return overrun
    return None


def get_interfaces_statistics_ignored(sh_int_name_output: str) -> int | None:
    pattern = r'\d*( ignored)'
    match = re.search(pattern, sh_int_name_output)
    if match:
        ignored = int(match.group()[:-len(' ignored')])
        return ignored
    return None


def get_interfaces_statistics_collision(sh_int_name_output: str) -> int | None:
    pattern = r'\d*( collisions)'
    match = re.search(pattern, sh_int_name_output)
    if match:
        collision = int(match.group()[:-len(' collisions')])
        return collision
    return None


def get_interfaces_statistics_late_collision(sh_int_name_output: str) -> int | None:
    pattern = r'\d*( late collision)'
    match = re.search(pattern, sh_int_name_output)
    if match:
        late_collision = int(match.group()[:-len(' late collision')])
        return late_collision
    return None


def get_interfaces_statistics_broadcast(sh_int_name_output: str) -> int | None:
    pattern = r'\d*( broadcasts)'
    match = re.search(pattern, sh_int_name_output)
    if match:
        broadcast = int(match.group()[:-len(' broadcasts')])
        return broadcast
    return None


def get_interfaces_statistics_packets_input(sh_int_name_output: str) -> int | None:
    pattern = r'\d*( packets input)'
    match = re.search(pattern, sh_int_name_output)
    if match:
        packets_input = int(match.group()[:-len(' packets input')])
        return packets_input
    return None


def get_interfaces_statistics_packets_output(sh_int_name_output: str) -> int | None:
    pattern = r'\d*( packets output)'
    match = re.search(pattern, sh_int_name_output)
    if match:
        packets_output = int(match.group()[:-len(' packets output')])
        return packets_output
    return None


def get_interfaces_statistics_mtu(sh_int_name_output: str) -> int | None:
    pattern = r'(MTU )\d*'
    match = re.search(pattern, sh_int_name_output)
    if match:
        mtu = int(match.group()[len('MTU '):])
        return mtu
    return None


def get_interfaces_statistics_dulpex(sh_int_name_output: str) -> str:
    if re.search(r'(Half-duplex)', sh_int_name_output):
        duplex = 'half'
    elif re.search(r'(Full-duplex)', sh_int_name_output):
        duplex = 'full'
    else:
        duplex = 'auto'
    return duplex


def get_interfaces_statistics_speed(sh_int_name_output: str) -> str | None:
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


def get_interfaces_statistics_layer1_status(sh_int_name_output: str) -> str | None:
    pattern = r'(is ).*(, line protocol)'
    match = re.search(pattern, sh_int_name_output)
    if match:
        layer1_status = match.group()[len('is '):-len(', line protocol')]
        return layer1_status
    return None


def get_interfaces_statistics_layer2_status(sh_int_name_output: str) -> str | None:
    pattern = r'(line protocol is ).*'
    match = re.search(pattern, sh_int_name_output)
    if match:
        layer2_status = match.group()[len('line protocol is '):]
        return layer2_status
    return None


def get_interfaces_statistics_encapsulation(sh_int_name_output: str) -> str | None:
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
    input_errors: int = get_interfaces_statistics_input_errors(sh_int_name_output)
    output_errors: int = get_interfaces_statistics_output_errors(sh_int_name_output)
    output_buffer_failures: int = get_interfaces_statistics_output_buffer_failures(sh_int_name_output)
    runts: int = get_interfaces_statistics_runts(sh_int_name_output)
    giants: int = get_interfaces_statistics_giants(sh_int_name_output)
    crc: int = get_interfaces_statistics_crc(sh_int_name_output)
    frame: int = get_interfaces_statistics_frame(sh_int_name_output)
    throttles: int = get_interfaces_statistics_throttles(sh_int_name_output)
    overrun: int = get_interfaces_statistics_overrun(sh_int_name_output)
    ignored: int = get_interfaces_statistics_ignored(sh_int_name_output)

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
    collision: int = get_interfaces_statistics_collision(sh_int_name_output)
    late_collision: int = get_interfaces_statistics_late_collision(sh_int_name_output)
    broadcast: int = get_interfaces_statistics_broadcast(sh_int_name_output)
    packets_input: int = get_interfaces_statistics_packets_input(sh_int_name_output)
    packets_output: int = get_interfaces_statistics_packets_output(sh_int_name_output)
    duplex: str = get_interfaces_statistics_dulpex(sh_int_name_output)
    speed: str = get_interfaces_statistics_speed(sh_int_name_output)
    layer1_status: str = get_interfaces_statistics_layer1_status(sh_int_name_output)
    layer2_status: str = get_interfaces_statistics_layer2_status(sh_int_name_output)
    mtu: int = get_interfaces_statistics_mtu(sh_int_name_output)
    encapsulation: str = get_interfaces_statistics_encapsulation(sh_int_name_output)

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


def get_base_interface_information(connection: netmiko.BaseConnection, interface_name: str) -> RouterInterface:
    connection.enable()
    sh_int_name_output: str = connection.send_command(f"show int {interface_name}")
    connection.exit_enable_mode()

    interface_ip_address: dict[str, str | int | None] = get_interface_ip_address(sh_int_name_output)
    description: str | None = get_interface_description(sh_int_name_output)
    statistics: InterfaceStatistics = get_interface_statistics(sh_int_name_output)

    router_interface: RouterInterface = RouterInterface(name=interface_name,
                                                        description=description,
                                                        ip_address=interface_ip_address['ip_address'],
                                                        subnet=interface_ip_address['subnet'],
                                                        statistics=statistics)
    return router_interface
