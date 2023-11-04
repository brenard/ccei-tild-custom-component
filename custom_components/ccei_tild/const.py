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
FILTRATION_ENABLED_BY_LIGHT = "filtration_enabled_by_light"
THERMOREGULATED_FILTRATION_CODE = "thermoregulated_filtration_code"
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
PROGRAMMING = "programming"
TIMER = "timer"
WATER_TEMPERATURE = "water_temperature"
WATER_RAW_TEMPERATURE = "water_raw_temperature"
WATER_TEMPERATURE_OFFSET_CODE = "water_temperature_offset_code"
WATER_TEMPERATURE_OFFSET = "water_temperature_offset"
FILTRATION_ENABLED = "filtration_enabled"
TREATMENT_ENABLED = "treatment_enabled"
RAW_DATA = "raw_data"
LIGHT_PROG_STATUS_CODE = "light_prog_status_code"
LIGHT_PROG_STATUS = "light_prog_status"
LIGHT_PROG_STATUS_CODES = {
    0: OFF,
    1: PROGRAMMING,
    2: TIMER,
}
LIGHT_PROG_MODE_DUSK_STATUS_CODE = "light_prog_mode_dusk_status_code"
LIGHT_PROG_MODE_DUSK_ENABLED = "light_prog_mode_dusk_enabled"
LIGHT_PROG_WEEK_END_MODE_STATUS_CODE = "light_prog_week_end_mode_status_code"
LIGHT_PROG_WEEK_END_MODE_ENABLED = "light_prog_week_end_mode_enabled"
LIGHT_PROG_START_HOUR_CODE = "light_prog_start_hour_code"
LIGHT_PROG_START_HOUR = "light_prog_start_hour"
LIGHT_PROG_DURATION_CODE = "light_prog_duration_code"
LIGHT_PROG_DURATION = "light_prog_duration"
LIGHT_PROG_WEEK_END_START_HOUR_CODE = "light_prog_week_end_start_hour_code"
LIGHT_PROG_WEEK_END_START_HOUR = "light_prog_week_end_start_hour"
LIGHT_PROG_WEEK_END_DURATION_CODE = "light_prog_week_end_duration_code"
LIGHT_PROG_WEEK_END_DURATION = "light_prog_week_end_duration"
LIGHT_SEQUENCE_SPEED_CODE = "light_color_speed_code"
LIGHT_SEQUENCE_SPEED = "light_color_speed"
FILTRATION_PROG_STATUS_STATUS_CODE = "filtration_prog_status_status_code"
FILTRATION_PROG_STATUS_ENABLED = "filtration_prog_status_enabled"
FILTRATION_PROG_THERMOREGULATED_STATUS_STATUS_CODE = (
    "filtration_prog_thermoregulated_status_status_code"
)
FILTRATION_PROG_THERMOREGULATED_STATUS_ENABLED = "filtration_prog_thermoregulated_status_enabled"
FILTRATION_PROG_WEEK_END_STATUS_STATUS_CODE = "filtration_prog_week_end_status_status_code"
FILTRATION_PROG_WEEK_END_STATUS_ENABLED = "filtration_prog_week_end_status_enabled"
FILTRATION_PROG_FIRST_RANGE_STATUS_STATUS_CODE = "filtration_prog_first_range_status_status_code"
FILTRATION_PROG_FIRST_RANGE_STATUS_ENABLED = "filtration_prog_first_range_status_enabled"
FILTRATION_PROG_FIRST_RANGE_START_HOUR_CODE = "filtration_prog_first_range_start_hour_code"
FILTRATION_PROG_FIRST_RANGE_START_HOUR = "filtration_prog_first_range_start_hour"
FILTRATION_PROG_FIRST_RANGE_END_HOUR_CODE = "filtration_prog_first_range_end_hour_code"
FILTRATION_PROG_FIRST_RANGE_END_HOUR = "filtration_prog_first_range_end_hour"
FILTRATION_PROG_SECOND_RANGE_STATUS_STATUS_CODE = "filtration_prog_second_range_status_status_code"
FILTRATION_PROG_SECOND_RANGE_STATUS_ENABLED = "filtration_prog_second_range_status_enabled"
FILTRATION_PROG_SECOND_RANGE_START_HOUR_CODE = "filtration_prog_second_range_start_hour_code"
FILTRATION_PROG_SECOND_RANGE_START_HOUR = "filtration_prog_second_range_start_hour"
FILTRATION_PROG_SECOND_RANGE_END_HOUR_CODE = "filtration_prog_second_range_end_hour_code"
FILTRATION_PROG_SECOND_RANGE_END_HOUR = "filtration_prog_second_range_end_hour"
FILTRATION_PROG_THIRD_RANGE_STATUS_STATUS_CODE = "filtration_prog_third_range_status_status_code"
FILTRATION_PROG_THIRD_RANGE_STATUS_ENABLED = "filtration_prog_third_range_status_enabled"
FILTRATION_PROG_THIRD_RANGE_START_HOUR_CODE = "filtration_prog_third_range_start_hour_code"
FILTRATION_PROG_THIRD_RANGE_START_HOUR = "filtration_prog_third_range_start_hour"
FILTRATION_PROG_THIRD_RANGE_END_HOUR_CODE = "filtration_prog_third_range_end_hour_code"
FILTRATION_PROG_THIRD_RANGE_END_HOUR = "filtration_prog_third_range_end_hour"
FILTRATION_PROG_WEEK_END_FIRST_RANGE_STATUS_STATUS_CODE = (
    "filtration_prog_week_end_first_range_status_status_code"
)
FILTRATION_PROG_WEEK_END_FIRST_RANGE_STATUS_ENABLED = (
    "filtration_prog_week_end_first_range_status_enabled"
)
FILTRATION_PROG_WEEK_END_FIRST_RANGE_START_HOUR_CODE = (
    "filtration_prog_week_end_first_range_start_hour_code"
)
FILTRATION_PROG_WEEK_END_FIRST_RANGE_START_HOUR = "filtration_prog_week_end_first_range_start_hour"
FILTRATION_PROG_WEEK_END_FIRST_RANGE_END_HOUR_CODE = (
    "filtration_prog_week_end_first_range_end_hour_code"
)
FILTRATION_PROG_WEEK_END_FIRST_RANGE_END_HOUR = "filtration_prog_week_end_first_range_end_hour"
FILTRATION_PROG_WEEK_END_SECOND_RANGE_STATUS_STATUS_CODE = (
    "filtration_prog_week_end_second_range_status_status_code"
)
FILTRATION_PROG_WEEK_END_SECOND_RANGE_STATUS_ENABLED = (
    "filtration_prog_week_end_second_range_status_enabled"
)
FILTRATION_PROG_WEEK_END_SECOND_RANGE_START_HOUR_CODE = (
    "filtration_prog_week_end_second_range_start_hour_code"
)
FILTRATION_PROG_WEEK_END_SECOND_RANGE_START_HOUR = (
    "filtration_prog_week_end_second_range_start_hour"
)
FILTRATION_PROG_WEEK_END_SECOND_RANGE_END_HOUR_CODE = (
    "filtration_prog_week_end_second_range_end_hour_code"
)
FILTRATION_PROG_WEEK_END_SECOND_RANGE_END_HOUR = "filtration_prog_week_end_second_range_end_hour"
FILTRATION_PROG_WEEK_END_THIRD_RANGE_STATUS_STATUS_CODE = (
    "filtration_prog_week_end_third_range_status_status_code"
)
FILTRATION_PROG_WEEK_END_THIRD_RANGE_STATUS_ENABLED = (
    "filtration_prog_week_end_third_range_status_enabled"
)
FILTRATION_PROG_WEEK_END_THIRD_RANGE_START_HOUR_CODE = (
    "filtration_prog_week_end_third_range_start_hour_code"
)
FILTRATION_PROG_WEEK_END_THIRD_RANGE_START_HOUR = "filtration_prog_week_end_third_range_start_hour"
FILTRATION_PROG_WEEK_END_THIRD_RANGE_END_HOUR_CODE = (
    "filtration_prog_week_end_third_range_end_hour_code"
)
FILTRATION_PROG_WEEK_END_THIRD_RANGE_END_HOUR = "filtration_prog_week_end_third_range_end_hour"
AUX_PROG_STATUS_STATUS_CODE = "aux_prog_status_status_code"
AUX_PROG_STATUS_ENABLED = "aux_prog_status_enabled"
AUX_PROG_WEEK_END_MODE_STATUS_STATUS_CODE = "aux_prog_week_end_mode_status_status_code"
AUX_PROG_WEEK_END_MODE_STATUS_ENABLED = "aux_prog_week_end_mode_status_enabled"
AUX_PROG_FIRST_RANGE_STATUS_STATUS_CODE = "aux_prog_first_range_status_status_code"
AUX_PROG_FIRST_RANGE_STATUS_ENABLED = "aux_prog_first_range_status_enabled"
AUX_PROG_FIRST_RANGE_START_HOUR_CODE = "aux_prog_first_range_start_hour_code"
AUX_PROG_FIRST_RANGE_START_HOUR = "aux_prog_first_range_start_hour"
AUX_PROG_FIRST_RANGE_END_HOUR_CODE = "aux_prog_first_range_end_hour_code"
AUX_PROG_FIRST_RANGE_END_HOUR = "aux_prog_first_range_end_hour"
AUX_PROG_SECOND_RANGE_STATUS_STATUS_CODE = "aux_prog_second_range_status_status_code"
AUX_PROG_SECOND_RANGE_STATUS_ENABLED = "aux_prog_second_range_status_enabled"
AUX_PROG_SECOND_RANGE_START_HOUR_CODE = "aux_prog_second_range_start_hour_code"
AUX_PROG_SECOND_RANGE_START_HOUR = "aux_prog_second_range_start_hour"
AUX_PROG_SECOND_RANGE_END_HOUR_CODE = "aux_prog_second_range_end_hour_code"
AUX_PROG_SECOND_RANGE_END_HOUR = "aux_prog_second_range_end_hour"
AUX_PROG_THIRD_RANGE_STATUS_STATUS_CODE = "aux_prog_third_range_status_status_code"
AUX_PROG_THIRD_RANGE_STATUS_ENABLED = "aux_prog_third_range_status_enabled"
AUX_PROG_THIRD_RANGE_START_HOUR_CODE = "aux_prog_third_range_start_hour_code"
AUX_PROG_THIRD_RANGE_START_HOUR = "aux_prog_third_range_start_hour"
AUX_PROG_THIRD_RANGE_END_HOUR_CODE = "aux_prog_third_range_end_hour_code"
AUX_PROG_THIRD_RANGE_END_HOUR = "aux_prog_third_range_end_hour"
AUX_PROG_WEEK_END_FIRST_RANGE_STATUS_STATUS_CODE = (
    "aux_prog_week_end_first_range_status_status_code"
)
AUX_PROG_WEEK_END_FIRST_RANGE_STATUS_ENABLED = "aux_prog_week_end_first_range_status_enabled"
AUX_PROG_WEEK_END_FIRST_RANGE_START_HOUR_CODE = "aux_prog_week_end_first_range_start_hour_code"
AUX_PROG_WEEK_END_FIRST_RANGE_START_HOUR = "aux_prog_week_end_first_range_start_hour"
AUX_PROG_WEEK_END_FIRST_RANGE_END_HOUR_CODE = "aux_prog_week_end_first_range_end_hour_code"
AUX_PROG_WEEK_END_FIRST_RANGE_END_HOUR = "aux_prog_week_end_first_range_end_hour"
AUX_PROG_WEEK_END_SECOND_RANGE_STATUS_STATUS_CODE = (
    "aux_prog_week_end_second_range_status_status_code"
)
AUX_PROG_WEEK_END_SECOND_RANGE_STATUS_ENABLED = "aux_prog_week_end_second_range_status_enabled"
AUX_PROG_WEEK_END_SECOND_RANGE_START_HOUR_CODE = "aux_prog_week_end_second_range_start_hour_code"
AUX_PROG_WEEK_END_SECOND_RANGE_START_HOUR = "aux_prog_week_end_second_range_start_hour"
AUX_PROG_WEEK_END_SECOND_RANGE_END_HOUR_CODE = "aux_prog_week_end_second_range_end_hour_code"
AUX_PROG_WEEK_END_SECOND_RANGE_END_HOUR = "aux_prog_week_end_second_range_end_hour"
AUX_PROG_WEEK_END_THIRD_RANGE_STATUS_STATUS_CODE = (
    "aux_prog_week_end_third_range_status_status_code"
)
AUX_PROG_WEEK_END_THIRD_RANGE_STATUS_ENABLED = "aux_prog_week_end_third_range_status_enabled"
AUX_PROG_WEEK_END_THIRD_RANGE_START_HOUR_CODE = "aux_prog_week_end_third_range_start_hour_code"
AUX_PROG_WEEK_END_THIRD_RANGE_START_HOUR = "aux_prog_week_end_third_range_start_hour"
AUX_PROG_WEEK_END_THIRD_RANGE_END_HOUR_CODE = "aux_prog_week_end_third_range_end_hour_code"
AUX_PROG_WEEK_END_THIRD_RANGE_END_HOUR = "aux_prog_week_end_third_range_end_hour"

ATTR_COLOR = "color"
ATTR_INTENSITY = "intensity"


LIGHT_COLORS_CODES = {
    0: "Hot",
    1: "Cold",
    2: "Blue",
    3: "Lagoon",
    4: "Cyan",
    5: "Purple",
    6: "Magenta",
    7: "Pink",
    8: "Red",
    9: "Orange",
    10: "Green",
    11: "Favorite",
    16: "Gradient sequence",
    17: "Rainbow",
    18: "Parade",
    19: "Techno",
    20: "Horizon",
    21: "Random",
    22: "Magic",
}

LIGHT_SEQUENCE_SPEED_CODES = {
    "0": 1,
    "1": 2,
    "2": 3,
}

LIGHT_INTENSITY_CODES = {
    "0": 25,
    "4": 50,
    "8": 75,
    "C": 100,
}

WATER_TEMPERATURE_OFFSET_CODES = {
    6: -3,
    5: -2,
    4: -1,
    0: 0,
    1: 1,
    2: 2,
    3: 3,
}

DURATION_CODES = {idx: f"{int(idx*15/60):02}:{idx*15%60:02}" for idx in range(1, 96)}

HOUR_CODES = {0: "00:00"}
HOUR_CODES.update(DURATION_CODES)

PROG_RANGE_DURATION_WITH_OFF_CODES = {255: OFF}
PROG_RANGE_DURATION_WITH_OFF_CODES.update(DURATION_CODES)
