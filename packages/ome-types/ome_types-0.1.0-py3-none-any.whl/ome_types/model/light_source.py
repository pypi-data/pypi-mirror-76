from dataclasses import field
from typing import List, Optional

from ome_types.dataclasses import ome_dataclass

from .annotation_ref import AnnotationRef
from .manufacturer_spec import ManufacturerSpec
from .simple_types import LightSourceID, UnitsPower


@ome_dataclass
class LightSource(ManufacturerSpec):
    annotation_ref: List[AnnotationRef] = field(default_factory=list)
    id: Optional[LightSourceID] = None
    power: Optional[float] = None
    power_unit: Optional[UnitsPower] = UnitsPower("mW")
