from typing import Optional

from ome_types.dataclasses import ome_dataclass

from .reference import Reference
from .simple_types import ChannelID


@ome_dataclass
class ChannelRef(Reference):
    id: Optional[ChannelID] = None
