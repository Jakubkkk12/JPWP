from dataclasses import dataclass


@dataclass(slots=True, kw_only=True)
class Redistribution:
    """
    Represents redistribution settings for different routing protocols.

    Attributes:
        is_redistribute_ospf (bool, optional): Indicates whether OSPF routes are redistributed. Defaults to None.
        is_redistribute_rip (bool, optional): Indicates whether RIP routes are redistributed. Defaults to None.
        is_redistribute_bgp (bool, optional): Indicates whether BGP routes are redistributed. Defaults to None.
        is_redistribute_static (bool, optional): Indicates whether static routes are redistributed. Defaults to None.
        is_redistribute_connected (bool, optional): Indicates whether connected routes are redistributed. Defaults to None.
    """
    is_redistribute_ospf: bool = None
    is_redistribute_rip: bool = None
    is_redistribute_bgp: bool = None
    is_redistribute_static: bool = None
    is_redistribute_connected: bool = None

    def is_redistribute_ospf_different(self, new_is_redistribute_ospf_value: bool) -> bool:
        if self.is_redistribute_ospf == new_is_redistribute_ospf_value:
            return False
        return True

    def is_redistribute_rip_different(self, new_is_redistribute_rip_value: bool) -> bool:
        if self.is_redistribute_rip == new_is_redistribute_rip_value:
            return False
        return True

    def is_redistribute_bgp_different(self, new_is_redistribute_bgp_value: bool) -> bool:
        if self.is_redistribute_bgp == new_is_redistribute_bgp_value:
            return False
        return True

    def is_is_redistribute_static_different(self, new_is_is_redistribute_static_value: bool) -> bool:
        if self.is_redistribute_static == new_is_is_redistribute_static_value:
            return False
        return True

    def is_redistribute_connected_different(self, new_is_redistribute_connected_value: bool) -> bool:
        if self.is_redistribute_connected == new_is_redistribute_connected_value:
            return False
        return True
