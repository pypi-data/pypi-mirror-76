from typing import Optional

from ome_types.dataclasses import ome_dataclass

from .reference import Reference
from .simple_types import ProjectID


@ome_dataclass
class ProjectRef(Reference):
    id: Optional[ProjectID] = None
