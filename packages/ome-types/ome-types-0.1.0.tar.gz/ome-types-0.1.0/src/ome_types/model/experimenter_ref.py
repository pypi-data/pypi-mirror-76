from typing import Optional

from ome_types.dataclasses import ome_dataclass

from .reference import Reference
from .simple_types import ExperimenterID


@ome_dataclass
class ExperimenterRef(Reference):
    id: Optional[ExperimenterID] = None
