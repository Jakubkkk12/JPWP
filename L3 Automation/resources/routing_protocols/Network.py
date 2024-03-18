from dataclasses import dataclass


@dataclass(slots=True, kw_only=True)
class Network:
    network: str
    mask: int | None
    wildcard: str = None
