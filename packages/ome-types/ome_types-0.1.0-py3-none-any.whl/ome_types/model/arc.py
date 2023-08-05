from enum import Enum
from typing import Optional

from ome_types.dataclasses import ome_dataclass

from .light_source import LightSource


class Type(Enum):
    HG = "Hg"
    HG_XE = "HgXe"
    OTHER = "Other"
    XE = "Xe"


@ome_dataclass
class Arc(LightSource):
    type: Optional[Type] = None
