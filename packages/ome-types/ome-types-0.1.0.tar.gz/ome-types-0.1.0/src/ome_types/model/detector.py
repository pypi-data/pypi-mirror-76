from dataclasses import field
from enum import Enum
from typing import List, Optional

from ome_types.dataclasses import ome_dataclass

from .annotation_ref import AnnotationRef
from .manufacturer_spec import ManufacturerSpec
from .simple_types import DetectorID, UnitsElectricPotential


class Type(Enum):
    ANALOG_VIDEO = "AnalogVideo"
    APD = "APD"
    CCD = "CCD"
    CMOS = "CMOS"
    CORRELATION_SPECTROSCOPY = "CorrelationSpectroscopy"
    EBCCD = "EBCCD"
    EMCCD = "EMCCD"
    FTIR = "FTIR"
    INTENSIFIED_CCD = "IntensifiedCCD"
    LIFETIME_IMAGING = "LifetimeImaging"
    OTHER = "Other"
    PHOTODIODE = "Photodiode"
    PMT = "PMT"
    SPECTROSCOPY = "Spectroscopy"


@ome_dataclass
class Detector(ManufacturerSpec):
    amplification_gain: Optional[float] = None
    annotation_ref: List[AnnotationRef] = field(default_factory=list)
    gain: Optional[float] = None
    id: Optional[DetectorID] = None
    offset: Optional[float] = None
    type: Optional[Type] = None
    voltage: Optional[float] = None
    voltage_unit: Optional[UnitsElectricPotential] = UnitsElectricPotential(
        "V"
    )
    zoom: Optional[float] = None
