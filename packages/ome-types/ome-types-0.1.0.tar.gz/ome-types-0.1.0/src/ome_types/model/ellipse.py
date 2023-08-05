from ome_types.dataclasses import EMPTY, ome_dataclass

from .shape import Shape


@ome_dataclass
class Ellipse(Shape):
    radius_x: float = EMPTY  # type: ignore
    radius_y: float = EMPTY  # type: ignore
    x: float = EMPTY  # type: ignore
    y: float = EMPTY  # type: ignore
