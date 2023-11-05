"""TildEntity class"""
import logging

from homeassistant.components.light import ENTITY_ID_FORMAT as LIGHT_ENTITY_ID_FORMAT
from homeassistant.components.light import LightEntity
from homeassistant.components.select import ENTITY_ID_FORMAT as SELECT_ENTITY_ID_FORMAT
from homeassistant.components.select import SelectEntity
from homeassistant.components.sensor import ENTITY_ID_FORMAT as SENSOR_ENTITY_ID_FORMAT
from homeassistant.components.switch import ENTITY_ID_FORMAT as SWITCH_ENTITY_ID_FORMAT
from homeassistant.components.switch import SwitchEntity
from homeassistant.core import callback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import CLIENT, DOMAIN, LAST_REFRESH, MANUFACTER, NAME, OFF, ON, SENSORS_DATA
from .tild import PROPERTIES_CODES

LOGGER = logging.getLogger(__name__)


class TildEntity(CoordinatorEntity):
    """Representation of a CCEI Tild entity."""

    _attr_id_key = None
    _entity_id_format = None
    _sensor_data_key = None
    _sensor_data_code_key = None
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
        if self._entity_id_format:
            self.entity_id = self._entity_id_format.format(
                self._attr_id_key if self._attr_id_key else f"tild_{self._sensor_data_key}"
            )
        if self._sensor_data_code_key and self._sensor_data_code_key in PROPERTIES_CODES:
            self._attr_options = [
                str(value) for value in PROPERTIES_CODES[self._sensor_data_code_key].values()
            ]

    @property
    def sensor_data(self):
        """Return the sensor data"""
        return (
            self.coordinator.data[SENSORS_DATA].get(self._sensor_data_key)
            if self.coordinator.data[SENSORS_DATA]
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
        if self._sensor_data_code_key:
            attrs["status_code"] = (
                self.coordinator.data[SENSORS_DATA].get(self._sensor_data_code_key)
                if self.coordinator.data[SENSORS_DATA]
                else None
            )

        for attr, key in self._sensor_data_extra_keys.items():
            attrs[attr] = (
                self.coordinator.data[SENSORS_DATA].get(key)
                if self.coordinator.data[SENSORS_DATA]
                else None
            )
        return attrs


class TildSensorEntity(TildEntity):
    """Representation of a CCEI Tild sensor entity."""

    _entity_id_format = SENSOR_ENTITY_ID_FORMAT

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

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        # pylint: disable=attribute-defined-outside-init
        self._attr_is_on = {ON: True, OFF: False}.get(self.sensor_data)
        self.async_write_ha_state()

    async def async_turn_on(self, **kwargs):
        """Turn the toggleable on."""
        return await self.hass.data[DOMAIN][CLIENT].set_property_state(self._sensor_data_key, ON)

    async def async_turn_off(self, **kwargs):
        """Turn the toggleable on."""
        return await self.hass.data[DOMAIN][CLIENT].set_property_state(self._sensor_data_key, OFF)


class TildLightEntity(TildToggleableEntity, LightEntity):
    """Representation of a CCEI Tild light entity."""

    _entity_id_format = LIGHT_ENTITY_ID_FORMAT


class TildSwitchEntity(TildToggleableEntity, SwitchEntity):
    """Representation of a CCEI Tild switch entity."""

    _entity_id_format = SWITCH_ENTITY_ID_FORMAT


class TildSelectEntity(TildEntity, SelectEntity):
    """Representation of a CCEI Tild select entity."""

    _entity_id_format = SELECT_ENTITY_ID_FORMAT

    _sensor_data_type = None

    @property
    def current_option(self):
        """Return current select option"""
        return str(self.sensor_data) if self.sensor_data is not None else None

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        if self._sensor_data_type is not None:
            option = self._sensor_data_type(option)
        return await self.hass.data[DOMAIN][CLIENT].set_property_state(
            self._sensor_data_code_key, option
        )
