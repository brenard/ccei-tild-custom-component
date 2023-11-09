"""
Custom integration to integrate CCEI Tild pool with Home Assistant.

For more details about this integration, please refer to
https://github.com/brenard/ccei-tild-custom-component
"""
import logging

import voluptuous as vol
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import Config, HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady

from .const import (
    CLIENT,
    CONF_HOST,
    CONF_REFRESH_RATE,
    CONF_REFRESH_RATE_DEFAULT,
    COORDINATOR,
    DOMAIN,
    PLATFORMS,
    SERVICE,
)
from .service import CceiTildService
from .tild import CceiTildClient
from .update_coordinator import CceiTildDataUpdateCoordinator

CONFIG_SCHEMA = {
    vol.Required(CONF_HOST): str,
    vol.Required(CONF_REFRESH_RATE, default=CONF_REFRESH_RATE_DEFAULT): int,
}
LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: Config):
    """Set up this integration using YAML is not supported."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up this integration using UI."""
    if hass.data.get(DOMAIN) is None:
        hass.data.setdefault(DOMAIN, {})

    host = entry.data.get(CONF_HOST)
    refresh_rate = entry.data.get(CONF_REFRESH_RATE)

    hass.data[DOMAIN][CLIENT] = CceiTildClient(host, hass=hass)

    coordinator = CceiTildDataUpdateCoordinator(hass, LOGGER, refresh_rate=refresh_rate)
    hass.data[DOMAIN][COORDINATOR] = coordinator

    async def update_listener(hass, entry):
        """Handle options update."""
        host = entry.options.get(CONF_HOST)
        refresh_rate = entry.options.get(CONF_REFRESH_RATE)
        LOGGER.debug("Options updated: host=%s / refresh rate=%d", host, refresh_rate)

        hass.data[DOMAIN][CLIENT] = CceiTildClient(host, hass=hass)

        LOGGER.debug("Update coordinator refresh interval (%d minutes)", refresh_rate)
        hass.data[DOMAIN][COORDINATOR].set_refresh_rate(refresh_rate)
        LOGGER.debug("Force update coordinator")
        await hass.data[DOMAIN][COORDINATOR].async_refresh()

    entry.async_on_unload(entry.add_update_listener(update_listener))

    await coordinator.async_refresh()

    hass.data[DOMAIN][SERVICE] = CceiTildService(hass)

    if not coordinator.last_update_success:
        raise ConfigEntryNotReady

    for platform in PLATFORMS:
        hass.async_add_job(hass.config_entries.async_forward_entry_setup(entry, platform))

    return True
