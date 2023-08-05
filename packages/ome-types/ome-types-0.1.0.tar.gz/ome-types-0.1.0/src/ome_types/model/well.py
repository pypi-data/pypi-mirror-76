from dataclasses import field
from typing import List, Optional, cast

from ome_types.dataclasses import ome_dataclass

from .annotation_ref import AnnotationRef
from .reagent_ref import ReagentRef
from .simple_types import Color, NonNegativeInt, WellID
from .well_sample import WellSample


@ome_dataclass
class Well:
    column: NonNegativeInt
    row: NonNegativeInt
    annotation_ref: List[AnnotationRef] = field(default_factory=list)
    color: Optional[Color] = cast(Color, -1)
    external_description: Optional[str] = None
    external_identifier: Optional[str] = None
    id: Optional[WellID] = None
    reagent_ref: Optional[ReagentRef] = None
    type: Optional[str] = None
    well_samples: List[WellSample] = field(default_factory=list)
