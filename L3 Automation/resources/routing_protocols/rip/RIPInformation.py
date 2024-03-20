from dataclasses import dataclass
from resources.routing_protocols.Network import Network
from resources.routing_protocols.Redistribution import Redistribution


@dataclass(slots=True, kw_only=True)
class RIPInformation:
    auto_summary: bool = None
    default_information_originate: bool = None
    default_metric_of_redistributed_routes: int = None
    distance: int = None
    maximum_paths: int = None
    redistribution: Redistribution = None
    networks: dict[str, Network] = None
    version: int = None
