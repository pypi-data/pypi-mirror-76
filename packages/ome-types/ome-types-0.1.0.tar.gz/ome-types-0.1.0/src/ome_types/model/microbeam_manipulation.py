from dataclasses import field
from typing import List, Optional

from ome_types.dataclasses import ome_dataclass

from .experimenter_ref import ExperimenterRef
from .light_source_settings import LightSourceSettings
from .roi_ref import ROIRef
from .simple_types import MicrobeamManipulationID


@ome_dataclass
class MicrobeamManipulation:
    experimenter_ref: ExperimenterRef
    roi_ref: List[ROIRef]
    description: Optional[str] = None
    id: Optional[MicrobeamManipulationID] = None
    light_source_settings: List[LightSourceSettings] = field(
        default_factory=list
    )
    type = None
