from typing import Optional

from ome_types.dataclasses import ome_dataclass

from .reference import Reference
from .simple_types import LightSourceID


@ome_dataclass
class Pump(Reference):
    id: Optional[LightSourceID] = None
