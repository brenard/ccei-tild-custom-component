"""Sensor platform"""
from .const import COORDINATOR, DOMAIN, LIGHT_ENABLED, LIGHT_STATUS_CODE
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
    _attr_name = "Light"
    _attr_icon = "mdi:light-flood-up"

    _sensor_data_key = LIGHT_ENABLED
    _sensor_data_extra_keys = {
        "raw_status_code": LIGHT_STATUS_CODE,
    }

    _client_toggle_method = "toggle_light_status"
