"""Sensor platform"""
from .const import CLIENT, COORDINATOR, DOMAIN, LIGHT_ENABLED, OFF, ON
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

    async def async_turn_on(self, **kwargs):
        """Turn the light on."""
        success = await self.hass.data[DOMAIN][CLIENT].toggle_light(ON)
        if success:
            await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs):
        """Turn the light on."""
        success = await self.hass.data[DOMAIN][CLIENT].toggle_light(OFF)
        if success:
            await self.coordinator.async_request_refresh()
