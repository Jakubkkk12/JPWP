from dataclasses import dataclass
from resources.interfaces.InterfaceStatistics import InterfaceStatistics


@dataclass(slots=True, kw_only=True)
class Interface:
    """
    Represents a network interface.

    Attributes:
        name (str): The name of the interface.
        description (str, optional): The description of the interface. Defaults to None.
        statistics (InterfaceStatistics, optional): Statistics related to the interface. Defaults to None.
    """
    name: str
    description: str = None
    statistics: InterfaceStatistics = None
