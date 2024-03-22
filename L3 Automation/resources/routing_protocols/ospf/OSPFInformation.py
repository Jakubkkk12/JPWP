from dataclasses import dataclass
from resources.routing_protocols.Redistribution import Redistribution
from resources.routing_protocols.ospf.OSPFArea import OSPFArea
from resources.routing_protocols.ospf.OSPFNeighbor import OSPFNeighbor


@dataclass(slots=True, kw_only=True)
class OSPFInformation:
    """
    Represents OSPF (Open Shortest Path First) configuration information.

    Attributes:
        process_id (int, optional): The OSPF process ID (only applicable for Cisco routers). Defaults to None.
        router_id (str, optional): The OSPF router ID. Defaults to None.
        auto_cost_reference_bandwidth (int, optional): The reference bandwidth used for automatic cost calculation. Defaults to None.
        default_information_originate (bool, optional): Indicates whether default route information is originated. Defaults to None.
        default_metric_of_redistributed_routes (int, optional): The default metric of redistributed routes. Defaults to None.
        distance (int, optional): The administrative distance for OSPF routes. Defaults to None.
        maximum_paths (int, optional): The maximum number of equal-cost paths allowed. Defaults to None.
        passive_interface_default (bool, optional): Indicates whether interfaces are passive by default. Defaults to None.
        redistribution (Redistribution, optional): Redistribution settings for OSPF. Defaults to None.
        areas (dict[str, OSPFArea], optional): A dictionary of OSPF areas where keys are area IDs and values are OSPFArea objects. Defaults to None.
        neighbors (dict[str, OSPFNeighbor], optional): A dictionary of active neighbors where keys are neighbor IDs. Defaults to None
    """
    process_id: int = None
    router_id: str = None
    auto_cost_reference_bandwidth: int = None
    default_information_originate: bool = None
    default_metric_of_redistributed_routes: int = None
    distance: int = None
    maximum_paths: int = None
    passive_interface_default: bool = None
    redistribution: Redistribution = None
    areas: dict[str, OSPFArea] = None
    neighbors: dict[str, OSPFNeighbor] = None

    def is_router_id_different(self, new_router_id_value: str) -> bool:
        if self.router_id == new_router_id_value:
            return False
        return True

    def is_auto_cost_reference_bandwidth_different(self, new_auto_cost_reference_bandwidth_value: int) -> bool:
        if self.auto_cost_reference_bandwidth == new_auto_cost_reference_bandwidth_value:
            return False
        return True

    def is_default_information_originate_different(self, new_default_information_originate_value: bool) -> bool:
        if self.default_information_originate == new_default_information_originate_value:
            return False
        return True

    def is_default_metric_of_redistributed_routes_different(self, new_default_metric_of_redistributed_routes: int) -> bool:
        if self.default_metric_of_redistributed_routes == new_default_metric_of_redistributed_routes:
            return False
        return True

    def is_distance_different(self, new_distance_value: int) -> bool:
        if self.distance == new_distance_value:
            return False
        return True

    def is_maximum_paths_different(self, new_maximum_paths_value: int) -> bool:
        if self.maximum_paths == new_maximum_paths_value:
            return False
        return True

    def is_passive_interface_default_different(self, new_passive_interface_default: bool) -> bool:
        if self.passive_interface_default == new_passive_interface_default:
            return False
        return True

    def is_area_in_areas(self, area_id: str) -> bool:
        if area_id in self.areas.keys():
            return True
        return False

    def add_area(self, area: OSPFArea) -> None:
        if self.is_area_in_areas(area.id):
            raise Exception('Area already exists')
        self.areas[area.id] = area
        return None
