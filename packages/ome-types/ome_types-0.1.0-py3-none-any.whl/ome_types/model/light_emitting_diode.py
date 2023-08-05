from ome_types.dataclasses import ome_dataclass

from .light_source import LightSource


@ome_dataclass
class LightEmittingDiode(LightSource):
    pass
