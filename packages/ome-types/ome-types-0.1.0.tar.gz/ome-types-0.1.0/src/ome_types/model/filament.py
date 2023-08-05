from enum import Enum
from typing import Optional

from ome_types.dataclasses import ome_dataclass

from .light_source import LightSource


class Type(Enum):
    HALOGEN = "Halogen"
    INCANDESCENT = "Incandescent"
    OTHER = "Other"


@ome_dataclass
class Filament(LightSource):
    type: Optional[Type] = None
