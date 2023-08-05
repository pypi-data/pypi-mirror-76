from enum import Enum
from typing import Optional

from ome_types.dataclasses import ome_dataclass

from .manufacturer_spec import ManufacturerSpec


class Type(Enum):
    DISSECTION = "Dissection"
    ELECTROPHYSIOLOGY = "Electrophysiology"
    INVERTED = "Inverted"
    OTHER = "Other"
    UPRIGHT = "Upright"


@ome_dataclass
class Microscope(ManufacturerSpec):
    type: Optional[Type] = None
