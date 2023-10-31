"""Switch platform"""
from .const import (
    COORDINATOR,
    DOMAIN,
    FILTRATION_ENABLED,
    THERMOREGULATED_FILTRATION_ENABLED,
    TREATMENT_ENABLED,
)
from .entity import TildSwitchEntity


async def async_setup_entry(hass, entry, async_add_devices):
    """Set up sensor platform."""
    coordinator = hass.data[DOMAIN][COORDINATOR]
    switchs = [
        TildTreatmentSwitch(coordinator, entry, hass),
        TildFiltrationSwitch(coordinator, entry, hass),
        TildThermoregulatedFiltrationSwitch(coordinator, entry, hass),
    ]
    async_add_devices(switchs)


class TildTreatmentSwitch(TildSwitchEntity):
    """Manage the treament"""

    _attr_id_key = "tild_treatment"
    _attr_name = "Treatment"
    _attr_icon = "mdi:spray-bottle"

    _sensor_data_key = TREATMENT_ENABLED


class TildFiltrationSwitch(TildSwitchEntity):
    """Manage the filtration"""

    _attr_id_key = "tild_filtration"
    _attr_name = "Filtration"
    _attr_icon = "mdi:filter-cog-outline"

    _sensor_data_key = FILTRATION_ENABLED

    _client_toggle_method = "toggle_filtration"


class TildThermoregulatedFiltrationSwitch(TildSwitchEntity):
    """Manage the filtration"""

    _attr_id_key = "tild_thermoregulated_filtration"
    _attr_name = "Thermoregulated filtration"
    _attr_icon = "mdi:coolant-temperature"

    _sensor_data_key = THERMOREGULATED_FILTRATION_ENABLED

    _client_toggle_method = "toggle_thermoregulated_filtration"
