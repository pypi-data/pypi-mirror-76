from typing import Optional

from ome_types.dataclasses import ome_dataclass

from .reference import Reference
from .simple_types import ReagentID


@ome_dataclass
class ReagentRef(Reference):
    id: Optional[ReagentID] = None
