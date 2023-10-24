"""TildEntity class"""
from homeassistant.components.light import LightEntity
from homeassistant.components.switch import SwitchEntity
from homeassistant.core import callback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, LAST_REFRESH, MANUFACTER, NAME, SENSORS_DATA


class TildEntity(CoordinatorEntity):
    """Representation of a CCEI Tild entity."""

    _attr_id_key = None
    _attr_friendly_name = None
    _sensor_data_extra_keys = {}

    def __init__(self, coordinator, config_entry):
        """Initialize the entity."""
        super().__init__(coordinator)
        self.config_entry = config_entry
        self._attr_unique_id = f"{self.config_entry.entry_id}_{self._attr_id_key}"

    @property
    def device_info(self):
        """Return device registry information for this entity."""
        return {
            "identifiers": {(self.config_entry.entry_id, DOMAIN)},
            "manufacturer": MANUFACTER,
            "name": NAME,
        }

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        attrs = {
            "last_refresh": self.coordinator.data[LAST_REFRESH],
        }
        for attr, key in self._sensor_data_extra_keys.items():
            attrs[attr] = self.coordinator.data[SENSORS_DATA].get(key)
        return attrs


class TildSensorEntity(TildEntity):
    """Representation of a CCEI Tild sensor entity."""

    @property
    def state(self):
        """Return the state of the sensor."""
        return self.coordinator.data[SENSORS_DATA][self._sensor_data_key]


class TildLightEntity(TildEntity, LightEntity):
    """
    Representation of a CCEI Tild light entity.
    Based on https://developers.home-assistant.io/docs/integration_fetching_data
    #coordinated-single-api-poll-for-data-for-all-entities
    """

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        # pylint: disable=attribute-defined-outside-init
        self._attr_is_on = self.coordinator.data[SENSORS_DATA][self._sensor_data_key]
        self.async_write_ha_state()


class TildSwitchEntity(TildEntity, SwitchEntity):
    """Representation of a CCEI Tild switch entity."""

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        # pylint: disable=attribute-defined-outside-init
        self._attr_is_on = self.coordinator.data[SENSORS_DATA][self._sensor_data_key]
        self.async_write_ha_state()
