from dataclasses import field
from typing import List, Optional

from ome_types.dataclasses import ome_dataclass

from .experimenter_ref import ExperimenterRef
from .microbeam_manipulation import MicrobeamManipulation
from .simple_types import ExperimentID


@ome_dataclass
class Experiment:
    description: Optional[str] = None
    experimenter_ref: Optional[ExperimenterRef] = None
    id: Optional[ExperimentID] = None
    microbeam_manipulations: List[MicrobeamManipulation] = field(
        default_factory=list
    )
    type = None
