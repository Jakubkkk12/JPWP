from dataclasses import dataclass
from resources.interfaces.InterfaceStatistics import InterfaceStatistics


@dataclass(slots=True, kw_only=True)
class Interface:
    """
    Represents a network interface.

    Attributes:
        name (str): The name of the interface.
        statistics (InterfaceStatistics, optional): Statistics related to the interface. Defaults to None.
    """
    name: str
    statistics: InterfaceStatistics = None
