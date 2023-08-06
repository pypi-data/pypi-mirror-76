"""Models for aio_osservaprezzi."""

import attr
from typing import Dict


@attr.s(auto_attribs=True, frozen=True)
class Fuel:
    """Fuel object."""

    name: str
    id: str
    is_self: bool
    price: float

    @staticmethod
    def from_dict(data):
        """Initialize the Fuel object from a dictionary."""
        return Fuel(
            name=data["carb"],
            id=data["idCarb"],
            is_self=bool(data["isSelf"]),
            price=data["prezzo"],
        )


@attr.s(auto_attribs=True, frozen=True)
class Station:
    """Station object."""

    name: str
    latitude: str
    longitude: str
    id: int
    bnd: str
    addr: str
    fuels: Dict[Fuel, None]
    update: str

    @staticmethod
    def from_dict(data):
        """Initialize the Station object from a dictionary."""
        return Station(
            name=data["name"],
            latitude=data["lat"],
            longitude=data["lon"],
            id=data["id"],
            bnd=data["bnd"],
            addr=data["addr"],
            fuels=[Fuel.from_dict(k) for k in data["carburanti"]],
            update=data["dIns"],
        )
