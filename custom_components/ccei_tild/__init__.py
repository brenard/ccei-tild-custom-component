"""
Custom integration to integrate CCEI Tild pool with Home Assistant.

For more details about this integration, please refer to
https://github.com/brenard/ccei-tild-custom-component
"""
import logging
from datetime import datetime, timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import Config, HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import (
    CLIENT,
    CONF_HOST,
    CONF_REFRESH_RATE,
    CONF_REFRESH_RATE_DEFAULT,
    COORDINATOR,
    DOMAIN,
    LAST_REFRESH,
    PLATFORMS,
    SENSORS_DATA,
)
from .tild import CceiTildClient

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

    hass.data[DOMAIN][CLIENT] = CceiTildClient(host)

    async def _get_sensors_data():
        """Return the water consumption."""
        client = hass.data[DOMAIN][CLIENT]
        sensors_data = await client.get_sensors_data()
        return {
            SENSORS_DATA: sensors_data,
            LAST_REFRESH: datetime.now().isoformat(),
        }

    coordinator = DataUpdateCoordinator(
        hass,
        LOGGER,
        name="CCEI Tild sensors data update",
        update_method=_get_sensors_data,
        update_interval=timedelta(
            minutes=refresh_rate if refresh_rate else CONF_REFRESH_RATE_DEFAULT
        ),
    )

    hass.data[DOMAIN][COORDINATOR] = coordinator

    async def update_listener(hass, entry):
        """Handle options update."""
        host = entry.options.get(CONF_HOST)
        refresh_rate = entry.options.get(CONF_REFRESH_RATE)
        LOGGER.debug("Options updated: host=%s / refresh rate=%d", host, refresh_rate)

        hass.data[DOMAIN][CLIENT] = CceiTildClient(host)

        LOGGER.debug("Update coordinator update interval (%d minutes)", refresh_rate)
        hass.data[DOMAIN][COORDINATOR].update_interval = timedelta(
            minutes=refresh_rate if refresh_rate else CONF_REFRESH_RATE_DEFAULT
        )
        LOGGER.debug("Force update coordinator")
        await hass.data[DOMAIN][COORDINATOR].async_refresh()

    entry.async_on_unload(entry.add_update_listener(update_listener))

    await coordinator.async_refresh()

    if not coordinator.last_update_success:
        raise ConfigEntryNotReady

    for platform in PLATFORMS:
        hass.async_add_job(hass.config_entries.async_forward_entry_setup(entry, platform))

    return True
