from ome_types.dataclasses import EMPTY, ome_dataclass

from .shape import Shape


@ome_dataclass
class Polygon(Shape):
    points: str = EMPTY  # type: ignore
