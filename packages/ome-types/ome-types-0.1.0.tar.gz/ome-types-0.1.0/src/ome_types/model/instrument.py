from dataclasses import field
from typing import Any, Dict, List, Optional, Union

from pydantic import validator

from ome_types.dataclasses import ome_dataclass

from .annotation_ref import AnnotationRef
from .arc import Arc
from .detector import Detector
from .dichroic import Dichroic
from .filament import Filament
from .filter import Filter
from .filter_set import FilterSet
from .generic_excitation_source import GenericExcitationSource
from .laser import Laser
from .light_emitting_diode import LightEmittingDiode
from .light_source import LightSource
from .microscope import Microscope
from .objective import Objective
from .simple_types import InstrumentID

_light_source_types: Dict[str, type] = {
    "laser": Laser,
    "arc": Arc,
    "filament": Filament,
    "light_emitting_diode": LightEmittingDiode,
    "generic_excitation_source": GenericExcitationSource,
}


@ome_dataclass
class Instrument:
    annotation_ref: List[AnnotationRef] = field(default_factory=list)
    detectors: List[Detector] = field(default_factory=list)
    dichroics: List[Dichroic] = field(default_factory=list)
    filter_sets: List[FilterSet] = field(default_factory=list)
    filters: List[Filter] = field(default_factory=list)
    id: Optional[InstrumentID] = None
    light_source_group: List[LightSource] = field(default_factory=list)
    microscope: Optional[Microscope] = None
    objectives: List[Objective] = field(default_factory=list)

    @validator("light_source_group", pre=True, each_item=True)
    def validate_light_source_group(
        cls, value: Union[LightSource, Dict[Any, Any]]
    ) -> LightSource:
        if isinstance(value, LightSource):
            return value
        elif isinstance(value, dict):
            try:
                _type = value.pop("_type")
            except KeyError:
                raise ValueError(
                    "dict initialization requires _type"
                ) from None
            try:
                light_source_cls = _light_source_types[_type]
            except KeyError:
                raise ValueError(
                    f"unknown LightSource type '{_type}'"
                ) from None
            return light_source_cls(**value)
        else:
            raise ValueError("invalid type for light_source_group values")
