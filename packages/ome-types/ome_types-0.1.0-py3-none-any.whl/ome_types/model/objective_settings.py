from enum import Enum
from typing import Optional

from ome_types.dataclasses import ome_dataclass

from .settings import Settings
from .simple_types import ObjectiveID


class Medium(Enum):
    AIR = "Air"
    GLYCEROL = "Glycerol"
    OIL = "Oil"
    OTHER = "Other"
    WATER = "Water"


@ome_dataclass
class ObjectiveSettings(Settings):
    correction_collar: Optional[float] = None
    id: Optional[ObjectiveID] = None
    medium: Optional[Medium] = None
    refractive_index: Optional[float] = None
