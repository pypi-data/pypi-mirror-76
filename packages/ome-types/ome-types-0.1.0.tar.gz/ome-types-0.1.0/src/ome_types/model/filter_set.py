from dataclasses import field
from typing import List, Optional

from ome_types.dataclasses import ome_dataclass

from .dichroic_ref import DichroicRef
from .filter_ref import FilterRef
from .manufacturer_spec import ManufacturerSpec
from .simple_types import FilterSetID


@ome_dataclass
class FilterSet(ManufacturerSpec):
    dichroic_ref: Optional[DichroicRef] = None
    emission_filter_ref: List[FilterRef] = field(default_factory=list)
    excitation_filter_ref: List[FilterRef] = field(default_factory=list)
    id: Optional[FilterSetID] = None
