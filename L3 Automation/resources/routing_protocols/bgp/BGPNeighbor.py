from dataclasses import dataclass
from resources.routing_protocols.bgp.BGPTimers import BGPTimers

@dataclass(slots=True, kw_only=True)
class BGPNeighbor:
    """
    Represents a BGP (Border Gateway Protocol) neighbor configuration.

    Attributes:
        ip_address (str): The IP address of the BGP neighbor.
        remote_as (int): The remote Autonomous System Number (ASN) of the BGP neighbor.
        state (str): The state of the BGP neighbor
        ebgp_multihop (int, optional): The TTL (Time To Live) value for establishing eBGP multihop sessions. Defaults to None.
        next_hop_self (bool, optional): Indicates whether the next hop for BGP updates should be the local router. Defaults to None.
        shutdown (bool, optional): Indicates whether the BGP neighbor is administratively shutdown. Defaults to None.
        timers (BGPTimers, optional): Timer settings for the BGP neighbor. Defaults to None.
        update_source (str, optional): The source address for BGP updates. Defaults to None.
    """
    ip_address: str
    remote_as: int
    state: str
    ebgp_multihop: int = None
    next_hop_self: bool = None
    shutdown: bool = None
    timers: BGPTimers = None
    update_source: str = None

    def is_ebgp_multihop_different(self, new_ebgp_multihop_value: int) -> bool:
        if self.ebgp_multihop == new_ebgp_multihop_value:
            return False
        return True

    def is_next_hop_self_different(self, new_next_hop_self_value: bool) -> bool:
        if self.next_hop_self == new_next_hop_self_value:
            return False
        return True

    def is_shutdown_different(self, new_shutdown_value: bool) -> bool:
        if self.shutdown == new_shutdown_value:
            return False
        return True

    def is_update_source_different(self, new_update_source_value: str) -> bool:
        if self.update_source == new_update_source_value:
            return False
        return True
