from dataclasses import dataclass
from resources.interfaces.Interface import Interface
from resources.interfaces.InterfaceOSPFInformation import InterfaceOSPFInformation


@dataclass(slots=True, kw_only=True)
class RouterInterface(Interface):
    """
    Represents a router interface with additional configuration for IP address and subnet information.

    Attributes:
        name (str): The name of the interface.
        statistics (InterfaceStatistics, optional): Statistics related to the interface. Defaults to None.
        ip_address (str): The IP address assigned to the interface.
        subnet (int): The subnet mask of the interface.
        ospf (InterfaceOSPFInformation, optional): OSPF (Open Shortest Path First) configuration information specific to the interface. Defaults to None.
    """
    ip_address: str
    subnet: int
    ospf: InterfaceOSPFInformation = None
