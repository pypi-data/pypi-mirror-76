from typing import Optional

from ome_types.dataclasses import ome_dataclass

from .reference import Reference
from .simple_types import ExperimenterGroupID


@ome_dataclass
class ExperimenterGroupRef(Reference):
    id: Optional[ExperimenterGroupID] = None
