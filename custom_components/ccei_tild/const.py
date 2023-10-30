"""Constants for CCEI Tild."""

from homeassistant.components.light import DOMAIN as LIGHT
from homeassistant.components.select import DOMAIN as SELECT
from homeassistant.components.sensor import DOMAIN as SENSOR
from homeassistant.components.switch import DOMAIN as SWITCH

MANUFACTER = "CCEI"
NAME = "Tild"
DOMAIN = "ccei_tild"
PLATFORMS = [SENSOR, LIGHT, SWITCH, SELECT]
CONF_HOST = "host"
CONF_REFRESH_RATE = "refresh_rate"
CONF_REFRESH_RATE_DEFAULT = 5
COORDINATOR = "coordinator"
CLIENT = "client"
SERVICE = "service"

SENSORS_DATA = "sensors_data"
LAST_REFRESH = "last_refresh"
REFRESH_SERVICE_NAME = "refresh"
SET_LIGHT_COLOR_SERVICE_NAME = "set_light_color"
SET_LIGHT_INTENSITY_SERVICE_NAME = "set_light_intensity"

SYSTEM_HOST = "system_host"
SYSTEM_DATE = "system_date"
SYSTEM_DATE_YEAR = "system_date_year"
SYSTEM_DATE_MONTH = "system_date_month"
SYSTEM_DATE_DAY = "system_date_day"
SYSTEM_DATE_HOUR = "system_date_hour"
SYSTEM_DATE_MINUTE = "system_date_minute"
FILTRATION_STATUS_CODE = "filtration_status_code"
FILTRATION_EXPECTED_DURATION = "filtration_expected_duration"
THERMOREGULATED_FILTRATION_ENABLED = "thermoregulated_filtration_enabled"
TREATMENT_STATUS_CODE = "treatment_status_code"
LIGHT_ENABLED = "light_enabled"
LIGHT_STATUS_CODE = "light_status_code"
LIGHT_COLOR_CODE = "light_color_code"
LIGHT_COLOR = "light_color"
LIGHT_INTENSITY_CODE = "light_intensity_code"
LIGHT_INTENSITY = "light_intensity"
LIGHT_TIMER_DURATION_CODE = "light_timer_duration_code"
LIGHT_TIMER_DURATION = "light_timer_duration"
ON = "on"
OFF = "off"
WATER_TEMPERATURE = "water_temperature"
WATER_RAW_TEMPERATURE = "water_raw_temperature"
WATER_TEMPERATURE_OFFSET_CODE = "water_temperature_offset_code"
WATER_TEMPERATURE_OFFSET = "water_temperature_offset"
FILTRATION_ENABLED = "filtration_enabled"
TREATMENT_ENABLED = "treatment_enabled"
RAW_DATA = "raw_data"

ATTR_COLOR = "color"
ATTR_INTENSITY = "intensity"


LIGHT_COLORS_CODES = {
    "01": "cold",
    "02": "blue",
    "03": "lagoon",
    "04": "cyan",
    "05": "purple",
    "06": "magenta",
    "07": "pink",
    "08": "red",
    "09": "orange",
    "0A": "green",
    "0B": "favorite",
    "10": "gradient sequence",
    "11": "rainbow",
    "12": "parade",
    "13": "techno",
}

LIGHT_INTENSITY_CODES = {
    "0": 25,
    "4": 50,
    "8": 75,
    "C": 100,
}

WATER_TEMPERATURE_OFFSET_CODES = {
    "6": -3,
    "5": -2,
    "4": -1,
    "0": 0,
    "1": 1,
    "2": 2,
    "3": 3,
}

DURATION_CODES = {
    f"{idx:02x}".upper(): f"{int(idx*15/60):02}:{idx*15%60:02}" for idx in range(1, 96)
}
