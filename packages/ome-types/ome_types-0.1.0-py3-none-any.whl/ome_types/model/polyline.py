from typing import Optional

from ome_types.dataclasses import EMPTY, ome_dataclass

from .shape import Shape
from .simple_types import Marker


@ome_dataclass
class Polyline(Shape):
    points: str = EMPTY  # type: ignore
    marker_end: Optional[Marker] = None
    marker_start: Optional[Marker] = None
