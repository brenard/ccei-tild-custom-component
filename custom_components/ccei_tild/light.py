"""Sensor platform"""
from .const import COORDINATOR, DOMAIN, LIGHT_ENABLED
from .entity import TildLightEntity


async def async_setup_entry(hass, entry, async_add_devices):
    """Set up sensor platform."""
    coordinator = hass.data[DOMAIN][COORDINATOR]
    lights = [
        TildLight(coordinator, entry, hass),
    ]
    async_add_devices(lights)


class TildLight(TildLightEntity):
    """Manage the light"""

    _attr_id_key = "tild_light"
    _attr_icon = "mdi:light-flood-up"

    _sensor_data_key = LIGHT_ENABLED
