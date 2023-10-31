"""TildEntity class"""
import logging

from homeassistant.components.light import LightEntity
from homeassistant.components.select import SelectEntity
from homeassistant.components.switch import SwitchEntity
from homeassistant.core import callback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import CLIENT, DOMAIN, LAST_REFRESH, MANUFACTER, NAME, OFF, ON, SENSORS_DATA

LOGGER = logging.getLogger(__name__)


class TildEntity(CoordinatorEntity):
    """Representation of a CCEI Tild entity."""

    _attr_id_key = None
    _sensor_data_extra_keys = {}

    def __init__(self, coordinator, config_entry, hass):
        """Initialize the entity."""
        super().__init__(coordinator)
        self.config_entry = config_entry
        self.hass = hass
        assert (
            self._attr_id_key or self._sensor_data_key
        ), "At least _attr_id_key or _sensor_data_key is required to set the entity ID."
        self._attr_unique_id = (
            f"{self.config_entry.entry_id}_tild_"
            f"{self._attr_id_key if self._attr_id_key else self._sensor_data_key}"
        )

    @property
    def sensor_data(self):
        """Return the sensor data"""
        return (
            self.coordinator.data[SENSORS_DATA][self._sensor_data_key]
            if self.coordinator.data[SENSORS_DATA]
            and self._sensor_data_key in self.coordinator.data[SENSORS_DATA]
            else None
        )

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
        return self.sensor_data


class TildToggleableEntity(TildEntity):
    """
    Representation of a CCEI Tild toggleable entity.
    Based on https://developers.home-assistant.io/docs/integration_fetching_data
    #coordinated-single-api-poll-for-data-for-all-entities
    """

    _client_toggle_method = None

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        # pylint: disable=attribute-defined-outside-init
        self._attr_is_on = {ON: True, OFF: False}.get(self.sensor_data)
        self.async_write_ha_state()

    async def async_turn_on(self, **kwargs):
        """Turn the toggleable on."""
        if self._client_toggle_method is None:
            raise NotImplementedError()
        return await getattr(self.hass.data[DOMAIN][CLIENT], self._client_toggle_method)(ON)

    async def async_turn_off(self, **kwargs):
        """Turn the toggleable on."""
        if self._client_toggle_method is None:
            raise NotImplementedError()
        return await getattr(self.hass.data[DOMAIN][CLIENT], self._client_toggle_method)(OFF)


class TildLightEntity(TildToggleableEntity, LightEntity):
    """Representation of a CCEI Tild light entity."""


class TildSwitchEntity(TildToggleableEntity, SwitchEntity):
    """Representation of a CCEI Tild switch entity."""


class TildSelectEntity(TildEntity, SelectEntity):
    """Representation of a CCEI Tild select entity."""

    _client_set_method = None
    _sensor_data_type = None

    @property
    def current_option(self):
        """Return current select option"""
        return str(self.sensor_data) if self.sensor_data is not None else None

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        if self._client_set_method is None:
            raise NotImplementedError()
        if self._sensor_data_type is not None:
            option = self._sensor_data_type(option)
        return await getattr(self.hass.data[DOMAIN][CLIENT], self._client_set_method)(option)
