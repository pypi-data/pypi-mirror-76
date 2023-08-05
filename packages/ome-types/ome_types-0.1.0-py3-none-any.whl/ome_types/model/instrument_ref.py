from typing import Optional

from ome_types.dataclasses import ome_dataclass

from .reference import Reference
from .simple_types import InstrumentID


@ome_dataclass
class InstrumentRef(Reference):
    id: Optional[InstrumentID] = None
