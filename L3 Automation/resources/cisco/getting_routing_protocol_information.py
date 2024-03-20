import re


def get_routing_protocol_default_information_originate(sh_run_sec_routing_protocol_output: str) -> bool:
    pattern = r'(default-information originate)'
    if re.search(pattern, sh_run_sec_routing_protocol_output):
        return True
    return False


def get_routing_protocol_default_metric_of_redistributed_routes(routing_protocol: str,
                                                                sh_run_sec_routing_protocol_output: str) -> int | None:
    pattern = r'(default-metric )\d*'
    match = re.search(pattern, sh_run_sec_routing_protocol_output)
    if match:
        default_metric_of_redistributed_routes = int(match.group()[len('default-metric '):])
        return default_metric_of_redistributed_routes
    if routing_protocol == 'ospf':
        return 10
    if routing_protocol == 'bgp':
        return 1
    return None


def get_routing_protocol_distance(routing_protocol: str, sh_run_sec_routing_protocol_output: str) -> int | None:
    # ibgp ???
    pattern = r'(distance )\d*'
    match = re.search(pattern, sh_run_sec_routing_protocol_output)
    if match:
        distance = int(match.group()[len('distance '):])
        return distance
    if routing_protocol == 'ospf':
        return 110
    return None
