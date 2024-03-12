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
