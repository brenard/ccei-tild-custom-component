"""Select platform"""
from homeassistant.const import PERCENTAGE, TEMP_CELSIUS

from .const import (
    CLIENT,
    COORDINATOR,
    DOMAIN,
    LIGHT_COLOR,
    LIGHT_COLOR_CODE,
    LIGHT_COLORS_CODES,
    LIGHT_INTENSITY,
    LIGHT_INTENSITY_CODE,
    LIGHT_INTENSITY_CODES,
    WATER_TEMPERATURE_OFFSET,
    WATER_TEMPERATURE_OFFSET_CODE,
    WATER_TEMPERATURE_OFFSET_CODES,
)
from .entity import TildSelectEntity


async def async_setup_entry(hass, entry, async_add_devices):
    """Set up sensor platform."""
    coordinator = hass.data[DOMAIN][COORDINATOR]
    selects = [
        TildLightIntensitySelect(coordinator, entry, hass),
        TildLightColorSelect(coordinator, entry, hass),
        TildWaterTemperatureOffsetSelect(coordinator, entry, hass),
    ]
    async_add_devices(selects)


class TildLightIntensitySelect(TildSelectEntity):
    """Monitors the light intensity"""

    _attr_name = "Light intensity"
    _attr_unit_of_measurement = PERCENTAGE
    _attr_icon = "mdi:brightness-percent"

    _sensor_data_key = LIGHT_INTENSITY
    _sensor_data_extra_keys = {
        "raw_intensity_code": LIGHT_INTENSITY_CODE,
    }

    _attr_options = [str(intensity) for intensity in LIGHT_INTENSITY_CODES.values()]

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        await self.hass.data[DOMAIN][CLIENT].set_light_intensity(int(option))


class TildLightColorSelect(TildSelectEntity):
    """Monitors the light color"""

    _attr_name = "Light color"
    _attr_icon = "mdi:palette"

    _sensor_data_key = LIGHT_COLOR
    _sensor_data_extra_keys = {
        "raw_color_code": LIGHT_COLOR_CODE,
    }

    _attr_options = list(LIGHT_COLORS_CODES.values())

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        await self.hass.data[DOMAIN][CLIENT].set_light_color(option)


class TildWaterTemperatureOffsetSelect(TildSelectEntity):
    """Monitors the water temperature offset"""

    _attr_name = "Water temperature offset"
    _attr_unit_of_measurement = TEMP_CELSIUS
    _attr_icon = "mdi:thermometer-water"

    _sensor_data_key = WATER_TEMPERATURE_OFFSET
    _sensor_data_extra_keys = {
        "raw_offset_code": WATER_TEMPERATURE_OFFSET_CODE,
    }

    _attr_options = [str(offset) for offset in WATER_TEMPERATURE_OFFSET_CODES.values()]
