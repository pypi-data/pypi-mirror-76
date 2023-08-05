from typing import Optional

from ome_types.dataclasses import ome_dataclass

from .reference import Reference
from .simple_types import ROIID


@ome_dataclass
class ROIRef(Reference):
    id: Optional[ROIID] = None
