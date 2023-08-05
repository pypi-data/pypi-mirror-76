from typing import Optional

from ome_types.dataclasses import ome_dataclass

from .reference import Reference
from .simple_types import ExperimenterID


@ome_dataclass
class Leader(Reference):
    id: Optional[ExperimenterID] = None
