from typing import Optional

from ome_types.dataclasses import ome_dataclass

from .reference import Reference
from .simple_types import ExperimentID


@ome_dataclass
class ExperimentRef(Reference):
    id: Optional[ExperimentID] = None
