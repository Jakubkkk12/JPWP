from dataclasses import dataclass


@dataclass(slots=True, kw_only=True)
class BGPTimers:
    """
    Represents BGP (Border Gateway Protocol) timer settings.

    Attributes:
        keep_alive (int): The interval (in seconds) between BGP keep-alive messages.
        hold_time (int): The duration (in seconds) that BGP will wait for a keep-alive message before declaring a neighbor dead.
    """
    keep_alive: int
    hold_time: int
