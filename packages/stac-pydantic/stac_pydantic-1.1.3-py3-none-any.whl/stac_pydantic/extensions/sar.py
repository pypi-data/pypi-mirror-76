from enum import auto
from typing import List, Optional

from pydantic import BaseModel

from ..shared import NumType
from ..utils import AutoValueEnum


class PolarizationEnum(str, AutoValueEnum):
    HH = auto()
    VV = auto()
    HV = auto()
    VH = auto()


class Polarizations(BaseModel):
    __root__: List[PolarizationEnum]

    def __getitem__(self, item):
        return self.__root__[item].value


class FrequencyBands(str, AutoValueEnum):
    """
    https://github.com/radiantearth/stac-spec/tree/v0.9.0/extensions/sar#common-frequency-band-names
    """

    P = auto()
    L = auto()
    S = auto()
    C = auto()
    X = auto()
    Ku = auto()
    K = auto()
    Ka = auto()


class ObservationDirections(str, AutoValueEnum):
    """
    https://github.com/radiantearth/stac-spec/tree/v0.9.0/extensions/sar#item-fields
    """

    left = auto()
    right = auto()


class SARExtension(BaseModel):
    """
    https://github.com/radiantearth/stac-spec/tree/v0.9.0/extensions/sar#sar-extension-specification
    """

    instrument_mode: str
    center_frequency: Optional[NumType]
    polarizations: Polarizations
    product_type: str
    resolution_range: Optional[int]
    resolution_azimuth: Optional[int]
    pixel_spacing_range: Optional[int]
    pixel_spacing_azimuth: Optional[int]
    looks_range: Optional[int]
    looks_azimuth: Optional[NumType]
    looks_equivalent_number: Optional[NumType]
    observation_direction: Optional[ObservationDirections]
    frequency_band: FrequencyBands

    class Config:
        allow_population_by_field_name = True
        alias_generator = lambda field_name: f"sar:{field_name}"
        use_enum_values = True
