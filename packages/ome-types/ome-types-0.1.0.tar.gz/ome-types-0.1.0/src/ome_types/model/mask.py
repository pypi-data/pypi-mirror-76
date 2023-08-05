from ome_types.dataclasses import EMPTY, ome_dataclass

from .bin_data import BinData
from .shape import Shape


@ome_dataclass
class Mask(Shape):
    bin_data: BinData = EMPTY  # type: ignore
    height: float = EMPTY  # type: ignore
    width: float = EMPTY  # type: ignore
    x: float = EMPTY  # type: ignore
    y: float = EMPTY  # type: ignore
