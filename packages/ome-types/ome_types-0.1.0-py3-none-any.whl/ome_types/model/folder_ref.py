from typing import Optional

from ome_types.dataclasses import ome_dataclass

from .reference import Reference
from .simple_types import FolderID


@ome_dataclass
class FolderRef(Reference):
    id: Optional[FolderID] = None
