from dataclasses import dataclass
from resources.routing_protocols.Network import Network


@dataclass(slots=True, kw_only=True)
class StaticRoute:
    """
    Represents a static route in a network.

    Attributes:
        network (Network): The destination network for the static route.
        next_hop (str): The next hop IP address or gateway for reaching the destination network.
        interface (str, optional): The interface through which traffic for the destination network is forwarded.
            Defaults to None.
        distance (int, optional): The distance between the 1 and 255. Defaults is 1.
    """
    network: Network
    next_hop: str
    interface: str
    distance: int = 1
