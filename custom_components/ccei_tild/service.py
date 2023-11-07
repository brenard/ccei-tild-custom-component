"""Services"""

import logging

from .const import COORDINATOR, DOMAIN, REFRESH_SERVICE_NAME

LOGGER = logging.getLogger(__name__)


class CceiTildService:
    """CCEI Tild services"""

    def __init__(self, hass):
        self.hass = hass
        hass.services.async_register(DOMAIN, REFRESH_SERVICE_NAME, self.handle_refresh)

    async def handle_refresh(self, call):
        """Handle refresh service call"""
        LOGGER.debug("Refresh service called: force refresh sensors data")
        await self.hass.data[DOMAIN][COORDINATOR].async_refresh()
