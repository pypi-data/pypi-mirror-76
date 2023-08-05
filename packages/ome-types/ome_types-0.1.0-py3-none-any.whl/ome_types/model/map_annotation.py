from ome_types.dataclasses import EMPTY, ome_dataclass

from .annotation import Annotation
from .map import Map


@ome_dataclass
class MapAnnotation(Annotation):
    value: Map = EMPTY  # type: ignore
