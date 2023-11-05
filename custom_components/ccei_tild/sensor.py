"""Sensor platform"""
from homeassistant.const import TEMP_CELSIUS

from .const import (
    COORDINATOR,
    DOMAIN,
    RAW_DATA,
    SENSORS_DATA,
    SYSTEM_DATE,
    SYSTEM_HOST,
    WATER_RAW_TEMPERATURE,
    WATER_TEMPERATURE,
)
from .entity import TildSensorEntity


async def async_setup_entry(hass, entry, async_add_devices):
    """Set up sensor platform."""
    coordinator = hass.data[DOMAIN][COORDINATOR]
    sensors = [
        TildSystemHostAddressSensor(coordinator, entry, hass),
        TildSystemDateSensor(coordinator, entry, hass),
        TildWaterTemperatureSensor(coordinator, entry, hass),
        TildWaterRawTemperatureSensor(coordinator, entry, hass),
        TildRawStatusDataSensor(coordinator, entry, hass),
    ]
    async_add_devices(sensors)


class TildSystemHostAddressSensor(TildSensorEntity):
    """Monitors the system host address"""

    _attr_name = "System host address"
    _attr_icon = "mdi:ip-network"

    _sensor_data_key = SYSTEM_HOST


class TildSystemDateSensor(TildSensorEntity):
    """Monitors the system date"""

    _attr_name = "System date"
    _attr_icon = "mdi:clock"

    _sensor_data_key = SYSTEM_DATE


class TildWaterTemperatureSensor(TildSensorEntity):
    """Monitors the water temperature"""

    _attr_name = "Water temperature"
    _attr_unit_of_measurement = TEMP_CELSIUS
    _attr_icon = "mdi:pool-thermometer"

    _sensor_data_key = WATER_TEMPERATURE


class TildWaterRawTemperatureSensor(TildSensorEntity):
    """Monitors the water raw temperature"""

    _attr_name = "Water raw temperature"
    _attr_unit_of_measurement = TEMP_CELSIUS
    _attr_icon = "mdi:pool-thermometer"

    _sensor_data_key = WATER_RAW_TEMPERATURE


class TildRawStatusDataSensor(TildSensorEntity):
    """Monitors the raw Tild status data"""

    _attr_id_key = "tild_raw_status_data"
    _attr_name = "Raw status data"
    _attr_icon = "mdi:data-matrix"

    _sensor_data_key = RAW_DATA

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        attrs = super().extra_state_attributes
        if self.coordinator.data[SENSORS_DATA]:
            attrs.update(self.coordinator.data[SENSORS_DATA])
        return attrs
