from dataclasses import dataclass
from resources.routing_protocols.ospf.OSPFTimers import OSPFTimers


@dataclass(slots=True, kw_only=True)
class InterfaceOSPFInformation:
    """
    Represents OSPF (Open Shortest Path First) configuration information specific to an interface.

    Attributes:
        network_type (str, optional): The OSPF network type of the interface (e.g., broadcast, point-to-point). Defaults to None.
        cost (int, optional): The OSPF cost associated with the interface. Defaults to None.
        state (str, optional): The OSPF state of the interface (e.g., DR, BDR, DROTHER). Defaults to None.
        passive_interface (bool, optional): Indicates whether the interface is passive for OSPF. Defaults to None.
        priority (int, optional): The OSPF priority of the interface in DR/BDR election process. Defaults to None.
        timers (OSPFTimers, optional): Timer settings specific to OSPF for the interface. Defaults to None.
    """
    network_type: str = None
    cost: int = None
    state: str = None
    passive_interface: bool = None
    priority: int = None
    timers: OSPFTimers = None
