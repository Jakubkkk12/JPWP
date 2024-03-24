from dataclasses import dataclass
from resources.routing_protocols.Network import Network
from resources.routing_protocols.Redistribution import Redistribution


@dataclass(slots=True, kw_only=True)
class RIPInformation:
    auto_summary: bool = None
    default_information_originate: bool = None
    default_metric_of_redistributed_routes: int = None
    distance: int = None
    maximum_paths: int = None
    version: int = None
    redistribution: Redistribution = None
    networks: dict[str, Network] = None

    def is_auto_summary_different(self, new_auto_summary_value: bool) -> bool:
        if self.auto_summary == new_auto_summary_value:
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

    def is_distance_different(self, new_distance_value: int) -> bool:
        if self.distance == new_distance_value:
            return False
        return True

    def is_maximum_paths_different(self, new_maximum_paths_value: int) -> bool:
        if self.maximum_paths == new_maximum_paths_value:
            return False
        return True

    def is_version_different(self, new_version_value: int) -> bool:
        if self.version == new_version_value:
            return False
        return True

    def is_network_in_networks(self, network_id: str) -> bool:
        if network_id in self.networks.keys():
            return True
        return False

    def add_network(self, network: Network) -> None:
        network_id: str = network.network
        if self.is_network_in_networks(network_id):
            raise Exception('Network already exists')
        self.networks[network_id] = network
        return None

    def remove_network(self, network_id: str) -> None:
        if self.is_network_in_networks(network_id):
            self.networks.pop(network_id)
        return None
