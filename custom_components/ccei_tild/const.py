"""Constants for CCEI Tild."""

from homeassistant.components.light import DOMAIN as LIGHT
from homeassistant.components.sensor import DOMAIN as SENSOR
from homeassistant.components.switch import DOMAIN as SWITCH

MANUFACTER = "CCEI"
NAME = "Tild"
DOMAIN = "ccei_tild"
PLATFORMS = [SENSOR, LIGHT, SWITCH]
CONF_HOST = "host"
CONF_REFRESH_RATE = "refresh_rate"
CONF_REFRESH_RATE_DEFAULT = 5
COORDINATOR = "coordinator"
CLIENT = "client"

SENSORS_DATA = "sensors_data"
LAST_REFRESH = "last_refresh"
REFRESH_SERVICE_NAME = "refresh"

SYSTEM_HOST = "system_host"
SYSTEM_DATE = "system_date"
SYSTEM_DATE_YEAR = "system_date_year"
SYSTEM_DATE_MONTH = "system_date_month"
SYSTEM_DATE_DAY = "system_date_day"
SYSTEM_DATE_HOUR = "system_date_hour"
SYSTEM_DATE_MINUTE = "system_date_minute"
TOGGLES_STATUS_CODE = "toggles_status_code"
FILTRATION_STATUS_CODE = "filtration_status_code"
FILTRATION_EXPECTED_DURATION = "filtration_expected_duration"
TREATMENT_STATUS_CODE = "treatment_status_code"
LIGHT_ENABLED = "light_enabled"
LIGHT_COLOR_CODE = "light_color_code"
LIGHT_COLOR = "light_color"
LIGHT_INTENSITY_CODE = "light_intensity_code"
LIGHT_INTENSITY = "light_intensity"
ON = "on"
OFF = "off"
WATER_TEMPERATURE = "water_temperature"
WATER_RAW_TEMPERATURE = "water_raw_temperature"
WATER_TEMPERATURE_OFFSET_CODE = "water_temperature_offset_code"
WATER_TEMPERATURE_OFFSET = "water_temperature_offset"
FILTRATION_ENABLED = "filtration_enabled"
TREATMENT_ENABLED = "treatment_enabled"
RAW_DATA = "raw_data"
