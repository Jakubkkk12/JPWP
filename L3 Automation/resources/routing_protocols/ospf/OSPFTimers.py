from dataclasses import dataclass


@dataclass(slots=True, kw_only=True)
class OSPFTimers:
    """
    Represents OSPF (Open Shortest Path First) timer settings.

    Attributes:
        hello_timer (int, optional): The interval (in seconds) between OSPF hello packets. Defaults to None.
        dead_timer (int, optional): The duration (in seconds) before a neighboring router is declared dead. Defaults to None.
        wait_timer (int, optional): The interval (in seconds) to wait before OSPF starts after router startup or interface changes. Defaults to None.
        retransmit_timer (int, optional): The interval (in seconds) between OSPF retransmitting unacknowledged LSAs (Link State Advertisements). Defaults to None.
    """
    hello_timer: int = None
    dead_timer: int = None
    wait_timer: int = None
    retransmit_timer: int = None
