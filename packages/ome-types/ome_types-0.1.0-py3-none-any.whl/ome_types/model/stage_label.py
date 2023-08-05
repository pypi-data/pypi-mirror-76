from typing import Optional

from ome_types.dataclasses import ome_dataclass

from .simple_types import UnitsLength


@ome_dataclass
class StageLabel:
    name: str
    x: Optional[float] = None
    x_unit: Optional[UnitsLength] = UnitsLength("reference frame")
    y: Optional[float] = None
    y_unit: Optional[UnitsLength] = UnitsLength("reference frame")
    z: Optional[float] = None
    z_unit: Optional[UnitsLength] = UnitsLength("reference frame")
