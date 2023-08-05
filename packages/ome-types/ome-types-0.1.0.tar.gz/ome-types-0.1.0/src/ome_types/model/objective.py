from dataclasses import field
from enum import Enum
from typing import List, Optional

from ome_types.dataclasses import ome_dataclass

from .annotation_ref import AnnotationRef
from .manufacturer_spec import ManufacturerSpec
from .simple_types import ObjectiveID, UnitsLength


class Correction(Enum):
    ACHRO = "Achro"
    ACHROMAT = "Achromat"
    APO = "Apo"
    FL = "Fl"
    FLUAR = "Fluar"
    FLUOR = "Fluor"
    FLUOTAR = "Fluotar"
    NEOFLUAR = "Neofluar"
    OTHER = "Other"
    PLAN_APO = "PlanApo"
    PLAN_FLUOR = "PlanFluor"
    PLAN_NEOFLUAR = "PlanNeofluar"
    SUPER_FLUOR = "SuperFluor"
    UV = "UV"
    VIOLET_CORRECTED = "VioletCorrected"


class Immersion(Enum):
    AIR = "Air"
    GLYCEROL = "Glycerol"
    MULTI = "Multi"
    OIL = "Oil"
    OTHER = "Other"
    WATER = "Water"
    WATER_DIPPING = "WaterDipping"


@ome_dataclass
class Objective(ManufacturerSpec):
    annotation_ref: List[AnnotationRef] = field(default_factory=list)
    calibrated_magnification: Optional[float] = None
    correction: Optional[Correction] = None
    id: Optional[ObjectiveID] = None
    immersion: Optional[Immersion] = None
    iris: Optional[bool] = None
    lens_na: Optional[float] = None
    nominal_magnification: Optional[float] = None
    working_distance: Optional[float] = None
    working_distance_unit: Optional[UnitsLength] = UnitsLength("µm")
