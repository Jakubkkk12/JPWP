from dataclasses import dataclass
from resources.routing_protocols.Network import Network
from resources.routing_protocols.Redistribution import Redistribution
from resources.routing_protocols.bgp.BGPTimers import BGPTimers
from resources.routing_protocols.bgp.BGPNeighbor import BGPNeighbor

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
        networks (dict[str, Network], optional): A dictionary of networks advertised via BGP, where keys are network IDs and values are Network objects. Defaults to None.
        timers (BGPTimers, optional): Timer settings for BGP. Defaults to None.
        neighbors (dict[str, BGPNeighbor], optional): A dictionary of BGP neighbors, where keys are neighbor IP addresses and values are BGPNeighbor objects. Defaults to None.
    """
    autonomous_system: int
    router_id: str
    default_information_originate: bool = None
    default_metric_of_redistributed_routes: int = None
    redistribution: Redistribution = None
    networks: dict[str, Network] = None
    timers: BGPTimers = None
    neighbors: dict[str, BGPNeighbor] = None

