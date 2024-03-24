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
        is_authentication_message_digest (bool, optional): Indicates whether the interface is authentication message digest. Defaults to None
        timers (OSPFTimers, optional): Timer settings specific to OSPF for the interface. Defaults to None.
    """
    network_type: str = None
    cost: int = None
    state: str = None
    passive_interface: bool = None
    priority: int = None
    is_authentication_message_digest: bool = None
    timers: OSPFTimers = None

    def is_network_type_different(self, new_network_type_value: str) -> bool:
        if self.network_type == new_network_type_value:
            return False
        return True

    def is_cost_different(self, new_cost_value: int) -> bool:
        if self.cost == new_cost_value:
            return False
        return True

    def is_passive_interface_different(self, new_passive_interface_value: bool) -> bool:
        if self.passive_interface == new_passive_interface_value:
            return False
        return True

    def is_priority_different(self, new_priority_value: int) -> bool:
        if self.priority == new_priority_value:
            return False
        return True

    def is_authentication_message_digest_different(self, new_authentication_message_digest_value: bool) -> bool:
        if self.is_authentication_message_digest == new_authentication_message_digest_value:
            return False
        return True
