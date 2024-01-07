"""Diagnostics support for CCEI Tild."""

import logging
from time import time
from typing import Any

from homeassistant.components.diagnostics import async_redact_data
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import CLIENT, COORDINATOR, DOMAIN, SENSORS_DATA
from .tild import diff_sensors_data, discover_host

TO_REDACT = {}

_LOGGER = logging.getLogger(__name__)


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, entry: ConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    _LOGGER.debug("Start building diagnostics data...")
    start_time = time()
    client = hass.data[DOMAIN][CLIENT]
    coordinator = hass.data[DOMAIN][COORDINATOR]

    _LOGGER.debug("Discover Tild device...")
    discovered_host_address, discovered_host_name = discover_host()

    _LOGGER.debug("Retrieve sensors data...")
    sensors_data = await client.get_sensors_data()

    _LOGGER.debug("Retrieve sensors data...")
    coordinator_data = coordinator.data[SENSORS_DATA]

    _LOGGER.debug("Compute differences between retrieved sensors data and coordinator data...")
    diff = (
        diff_sensors_data(coordinator_data["raw_data"], sensors_data["raw_data"])
        if isinstance(coordinator_data, dict)
        and coordinator_data.get("raw_data")
        and isinstance(sensors_data, dict)
        and sensors_data.get("raw_data")
        else None
    )

    _LOGGER.debug("Diagnostics data builded in %0.1fs", time() - start_time)

    return {
        "entry": {
            "data": async_redact_data(entry.data, TO_REDACT),
            "options": async_redact_data(entry.options, TO_REDACT),
        },
        "discovered_host": {
            "address": discovered_host_address,
            "name": discovered_host_name,
        },
        "sensors_data": async_redact_data(sensors_data, TO_REDACT),
        "coordinator_data": async_redact_data(coordinator_data, TO_REDACT),
        "data_diff": async_redact_data(diff, TO_REDACT),
    }
