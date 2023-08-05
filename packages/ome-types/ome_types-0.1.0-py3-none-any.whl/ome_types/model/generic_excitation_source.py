from typing import Optional

from ome_types.dataclasses import ome_dataclass

from .light_source import LightSource
from .map import Map


@ome_dataclass
class GenericExcitationSource(LightSource):
    map: Optional[Map] = None
