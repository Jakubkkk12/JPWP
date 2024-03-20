from dataclasses import dataclass


@dataclass(slots=True, kw_only=True)
class OSPFNeighbor:
    neighbor_id: str
    state: str
    ip_address: str
    interface: str
