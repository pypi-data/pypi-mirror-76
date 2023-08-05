from dataclasses import field
from enum import Enum
from typing import List, Optional

from ome_types.dataclasses import ome_dataclass

from .annotation_ref import AnnotationRef
from .manufacturer_spec import ManufacturerSpec
from .simple_types import FilterID
from .transmittance_range import TransmittanceRange


class Type(Enum):
    BAND_PASS = "BandPass"
    DICHROIC = "Dichroic"
    LONG_PASS = "LongPass"
    MULTI_PASS = "MultiPass"
    NEUTRAL_DENSITY = "NeutralDensity"
    OTHER = "Other"
    SHORT_PASS = "ShortPass"
    TUNEABLE = "Tuneable"


@ome_dataclass
class Filter(ManufacturerSpec):
    annotation_ref: List[AnnotationRef] = field(default_factory=list)
    filter_wheel: Optional[str] = None
    id: Optional[FilterID] = None
    transmittance_range: Optional[TransmittanceRange] = None
    type: Optional[Type] = None
