from dataclasses import dataclass
from resources.routing_protocols.Network import Network
from resources.routing_protocols.Redistribution import Redistribution
from resources.routing_protocols.bgp.BGPTimers import BGPTimers
from resources.routing_protocols.bgp.BGPNeighbor import BGPNeighbor
from resources.constants import NETWORK_MASK


@dataclass(slots=True, kw_only=True)
class BGPInformation:
    """
    Represents BGP (Border Gateway Protocol) configuration information.

    Attributes:
        autonomous_system (int): Autonomous system number
        router_id (str): The BGP router ID.
        default_information_originate (bool, optional): Indicates whether default route information is originated. Defaults to None.
        default_metric_of_redistributed_routes (int, optional): The default metric of redistributed routes. Defaults to None.
        redistribution (Redistribution, optional): Redistribution settings for BGP. Defaults to None.
        timers (BGPTimers, optional): Timer settings for BGP. Defaults to None.
        networks (dict[str, Network], optional): A dictionary of networks advertised via BGP, where keys are network IDs and values are Network objects. Defaults to None.
        neighbors (dict[str, BGPNeighbor], optional): A dictionary of BGP neighbors, where keys are neighbor IP addresses and values are BGPNeighbor objects. Defaults to None.
    """
    autonomous_system: int
    router_id: str
    default_information_originate: bool = None
    default_metric_of_redistributed_routes: int = None
    redistribution: Redistribution = None
    timers: BGPTimers = None
    networks: dict[str, Network] = None
    neighbors: dict[str, BGPNeighbor] = None

    def is_router_id_different(self, new_router_id_value: str) -> bool:
        if self.router_id == new_router_id_value:
            return False
        return True

    def is_default_information_originate_different(self, new_default_information_originate_value: bool) -> bool:
        if self.default_information_originate == new_default_information_originate_value:
            return False
        return True

    def is_default_metric_of_redistributed_routes_different(self, new_default_metric_of_redistributed_routes: int) -> bool:
        if self.default_metric_of_redistributed_routes == new_default_metric_of_redistributed_routes:
            return False
        return True

    def is_network_in_networks(self, network_id: str) -> bool:
        if network_id in self.networks.keys():
            return True
        return False

    def add_network(self, network: Network) -> None:
        network_id: str = f'{network.network} {NETWORK_MASK[network.mask]}'
        if self.is_network_in_networks(network_id):
            raise Exception('Network already exists')
        self.networks[network_id] = network
        return None

    def remove_network(self, network_id: str) -> None:
        if self.is_network_in_networks(network_id):
            self.networks.pop(network_id)
        return None

    def is_neighbor_in_neighbors(self, neighbor_id: str) -> bool:
        if neighbor_id in self.neighbors.keys():
            return True
        return False

    def add_neighbor(self, neighbor: BGPNeighbor) -> None:
        neighbor_id: str = neighbor.ip_address
        if self.is_neighbor_in_neighbors(neighbor_id):
            raise Exception('Neighbor already exists')
        self.neighbors[neighbor_id] = neighbor
        return None

    def remove_neighbor(self, neighbor_id: str) -> None:
        if self.is_neighbor_in_neighbors(neighbor_id):
            self.neighbors.pop(neighbor_id)
        return None
