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

