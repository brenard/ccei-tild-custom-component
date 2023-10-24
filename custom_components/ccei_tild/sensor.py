"""Sensor platform"""
from homeassistant.const import PERCENTAGE, TEMP_CELSIUS

from .const import (
    COORDINATOR,
    DOMAIN,
    LIGHT_COLOR,
    LIGHT_COLOR_CODE,
    LIGHT_INTENSITY,
    LIGHT_INTENSITY_CODE,
    RAW_DATA,
    SENSORS_DATA,
    SYSTEM_DATE,
    SYSTEM_HOST,
    WATER_REAL_TEMPERATURE,
    WATER_TEMPERATURE,
    WATER_TEMPERATURE_OFFSET,
    WATER_TEMPERATURE_OFFSET_CODE,
)
from .entity import TildSensorEntity


async def async_setup_entry(hass, entry, async_add_devices):
    """Set up sensor platform."""
    coordinator = hass.data[DOMAIN][COORDINATOR]
    sensors = [
        TildSystemHostAddressSensor(coordinator, entry),
        TildSystemDateSensor(coordinator, entry),
        TildWaterTemperatureSensor(coordinator, entry),
        TildWaterTemperatureOffsetSensor(coordinator, entry),
        TildWaterRealTemperatureSensor(coordinator, entry),
        TildLightIntensitySensor(coordinator, entry),
        TildLightColorSensor(coordinator, entry),
        TildRawStatusDataSensor(coordinator, entry),
    ]
    async_add_devices(sensors)


class TildSystemHostAddressSensor(TildSensorEntity):
    """Monitors the system host address"""

    _attr_id_key = "tild_system_host"
    _attr_name = "System host address"
    _attr_icon = "mdi:ip-network"

    _sensor_data_key = SYSTEM_HOST


class TildSystemDateSensor(TildSensorEntity):
    """Monitors the system date"""

    _attr_id_key = "tild_system_date"
    _attr_name = "System date"
    _attr_icon = "mdi:clock"

    _sensor_data_key = SYSTEM_DATE


class TildWaterTemperatureSensor(TildSensorEntity):
    """Monitors the water temperature"""

    _attr_id_key = "tild_water_temperature"
    _attr_name = "Water temperature"
    _attr_unit_of_measurement = TEMP_CELSIUS
    _attr_icon = "mdi:pool-thermometer"

    _sensor_data_key = WATER_TEMPERATURE


class TildWaterRealTemperatureSensor(TildSensorEntity):
    """Monitors the water real temperature"""

    _attr_id_key = "tild_water_real_temperature"
    _attr_name = "Water real temperature"
    _attr_unit_of_measurement = TEMP_CELSIUS
    _attr_icon = "mdi:pool-thermometer"

    _sensor_data_key = WATER_REAL_TEMPERATURE


class TildWaterTemperatureOffsetSensor(TildSensorEntity):
    """Monitors the water temperature offset"""

    _attr_id_key = "tild_water_temperature_offset"
    _attr_name = "Water temperature offset"
    _attr_unit_of_measurement = TEMP_CELSIUS
    _attr_icon = "mdi:thermometer-water"

    _sensor_data_key = WATER_TEMPERATURE_OFFSET
    _sensor_data_extra_keys = {
        "raw_offset_code": WATER_TEMPERATURE_OFFSET_CODE,
    }


class TildLightIntensitySensor(TildSensorEntity):
    """Monitors the light intensity"""

    _attr_id_key = "tild_light_intensity"
    _attr_name = "Light intensity"
    _attr_unit_of_measurement = PERCENTAGE
    _attr_icon = "mdi:brightness-percent"

    _sensor_data_key = LIGHT_INTENSITY
    _sensor_data_extra_keys = {
        "raw_intensity_code": LIGHT_INTENSITY_CODE,
    }


class TildLightColorSensor(TildSensorEntity):
    """Monitors the light color"""

    _attr_id_key = "tild_light_color"
    _attr_name = "Light color"
    _attr_icon = "mdi:palette"

    _sensor_data_key = LIGHT_COLOR
    _sensor_data_extra_keys = {
        "raw_color_code": LIGHT_COLOR_CODE,
    }


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
        attrs.update(self.coordinator.data[SENSORS_DATA])
        return attrs
