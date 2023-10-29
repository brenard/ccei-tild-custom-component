"""Services"""

import logging

from .const import (
    ATTR_COLOR,
    ATTR_INTENSITY,
    CLIENT,
    COORDINATOR,
    DOMAIN,
    REFRESH_SERVICE_NAME,
    SET_LIGHT_COLOR_SERVICE_NAME,
    SET_LIGHT_INTENSITY_SERVICE_NAME,
)

LOGGER = logging.getLogger(__name__)


class CceiTildService:
    """CCEI Tild services"""

    def __init__(self, hass):
        self.hass = hass
        hass.services.async_register(DOMAIN, REFRESH_SERVICE_NAME, self.handle_refresh)
        hass.services.async_register(
            DOMAIN, SET_LIGHT_COLOR_SERVICE_NAME, self.handle_set_light_color
        )
        hass.services.async_register(
            DOMAIN, SET_LIGHT_INTENSITY_SERVICE_NAME, self.handle_set_light_intensity
        )

    async def handle_refresh(self, call):
        """Handle refresh service call"""
        LOGGER.debug("Refresh service called: force refresh sensors data")
        await self.hass.data[DOMAIN][COORDINATOR].async_refresh()

    async def handle_set_light_color(self, call):
        """Handle set_light_color service call"""
        color = call.data.get(ATTR_COLOR)
        LOGGER.debug("Set light color service called: set color to %s", color)
        success = await self.hass.data[DOMAIN][CLIENT].set_light_color(color)
        if success:
            await self.hass.data[DOMAIN][COORDINATOR].async_refresh()
            return True
        return False

    async def handle_set_light_intensity(self, call):
        """Handle set_light_intensity service call"""
        intensity = call.data.get(ATTR_INTENSITY)
        LOGGER.debug("Set light intensity service called: set intensity to %s", intensity)
        success = await self.hass.data[DOMAIN][CLIENT].set_light_intensity(intensity)
        if success:
            await self.hass.data[DOMAIN][COORDINATOR].async_refresh()
            return True
        return False
