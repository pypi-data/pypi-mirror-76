from typing import Optional

from ome_types.dataclasses import ome_dataclass

from .reference import Reference
from .simple_types import DichroicID


@ome_dataclass
class DichroicRef(Reference):
    id: Optional[DichroicID] = None
