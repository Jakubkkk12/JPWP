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

    def is_keep_alive_different(self, new_keep_alive_value: int) -> bool:
        if self.keep_alive == new_keep_alive_value:
            return False
        return True

    def is_hold_time_different(self, new_hold_time_value: int) -> bool:
        if self.hold_time == new_hold_time_value:
            return False
        return True
