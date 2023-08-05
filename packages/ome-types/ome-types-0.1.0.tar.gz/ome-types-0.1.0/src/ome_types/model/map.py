from dataclasses import field
from typing import List, Optional

from ome_types.dataclasses import ome_dataclass


@ome_dataclass
class M:
    k: Optional[str] = None


@ome_dataclass
class Map:
    k: Optional[str] = None
    m: List[M] = field(default_factory=list)
