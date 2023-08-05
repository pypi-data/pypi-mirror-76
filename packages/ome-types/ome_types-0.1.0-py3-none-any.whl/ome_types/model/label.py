from ome_types.dataclasses import EMPTY, ome_dataclass

from .shape import Shape


@ome_dataclass
class Label(Shape):
    x: float = EMPTY  # type: ignore
    y: float = EMPTY  # type: ignore
