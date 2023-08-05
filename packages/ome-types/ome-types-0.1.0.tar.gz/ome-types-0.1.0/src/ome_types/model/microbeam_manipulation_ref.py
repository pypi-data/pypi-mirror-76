from typing import Optional

from ome_types.dataclasses import ome_dataclass

from .reference import Reference
from .simple_types import MicrobeamManipulationID


@ome_dataclass
class MicrobeamManipulationRef(Reference):
    id: Optional[MicrobeamManipulationID] = None
