from dataclasses import dataclass
from resources.routing_protocols.Network import Network


@dataclass(slots=True, kw_only=True)
class OSPFArea:
    """
    Represents an OSPF (Open Shortest Path First) area configuration.

    Attributes:
        id (str): The identifier of the OSPF area.
        is_authentication_message_digest (bool, optional): Indicates whether authentication is enabled for OSPF messages within this area. Defaults to None.
        type (str, optional): The type of OSPF area (e.g., stub, standard, NSSA). Defaults to None.
        networks (dict[str, Network], optional): A dictionary of networks within this OSPF area, where keys are network IDs and values are Network objects. Defaults to None.
    """
    id: str
    is_authentication_message_digest: bool = None
    type: str = None
    networks: dict[str, Network] = None

    def is_authentication_message_digest_different(self, new_is_authentication_message_digest_value: bool) -> bool:
        if self.is_authentication_message_digest == new_is_authentication_message_digest_value:
            return False
        return True

    def is_type_different(self, new_type_value: str) -> bool:
        if self.type == new_type_value:
            return False
        return True

    def is_network_in_networks(self, network_id: str) -> bool:
        if network_id in self.networks.keys():
            return True
        return False

    def add_network(self, network: Network) -> None:
        network_id: str = f'{network.network} {network.wildcard}'
        if self.is_network_in_networks(network_id):
            raise Exception('Network already exists')
        self.networks[network_id] = network
        return None

