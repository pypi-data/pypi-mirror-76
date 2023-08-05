from typing import Optional

from ome_types.dataclasses import ome_dataclass

from .reference import Reference
from .simple_types import WellSampleID


@ome_dataclass
class WellSampleRef(Reference):
    id: Optional[WellSampleID] = None
