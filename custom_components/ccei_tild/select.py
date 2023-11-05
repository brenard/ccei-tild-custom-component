"""Select platform"""
from homeassistant.const import PERCENTAGE, TEMP_CELSIUS

from .const import (
    AUX_PROG_FIRST_RANGE_END_HOUR,
    AUX_PROG_FIRST_RANGE_END_HOUR_CODE,
    AUX_PROG_FIRST_RANGE_START_HOUR,
    AUX_PROG_FIRST_RANGE_START_HOUR_CODE,
    AUX_PROG_SECOND_RANGE_END_HOUR,
    AUX_PROG_SECOND_RANGE_END_HOUR_CODE,
    AUX_PROG_SECOND_RANGE_START_HOUR,
    AUX_PROG_SECOND_RANGE_START_HOUR_CODE,
    AUX_PROG_THIRD_RANGE_END_HOUR,
    AUX_PROG_THIRD_RANGE_END_HOUR_CODE,
    AUX_PROG_THIRD_RANGE_START_HOUR,
    AUX_PROG_THIRD_RANGE_START_HOUR_CODE,
    AUX_PROG_WEEK_END_FIRST_RANGE_END_HOUR,
    AUX_PROG_WEEK_END_FIRST_RANGE_END_HOUR_CODE,
    AUX_PROG_WEEK_END_FIRST_RANGE_START_HOUR,
    AUX_PROG_WEEK_END_FIRST_RANGE_START_HOUR_CODE,
    AUX_PROG_WEEK_END_SECOND_RANGE_END_HOUR,
    AUX_PROG_WEEK_END_SECOND_RANGE_END_HOUR_CODE,
    AUX_PROG_WEEK_END_SECOND_RANGE_START_HOUR,
    AUX_PROG_WEEK_END_SECOND_RANGE_START_HOUR_CODE,
    AUX_PROG_WEEK_END_THIRD_RANGE_END_HOUR,
    AUX_PROG_WEEK_END_THIRD_RANGE_END_HOUR_CODE,
    AUX_PROG_WEEK_END_THIRD_RANGE_START_HOUR,
    AUX_PROG_WEEK_END_THIRD_RANGE_START_HOUR_CODE,
    COORDINATOR,
    DOMAIN,
    FIL_PROG_FIRST_RANGE_END_HOUR,
    FIL_PROG_FIRST_RANGE_END_HOUR_CODE,
    FIL_PROG_FIRST_RANGE_START_HOUR,
    FIL_PROG_FIRST_RANGE_START_HOUR_CODE,
    FIL_PROG_SECOND_RANGE_END_HOUR,
    FIL_PROG_SECOND_RANGE_END_HOUR_CODE,
    FIL_PROG_SECOND_RANGE_START_HOUR,
    FIL_PROG_SECOND_RANGE_START_HOUR_CODE,
    FIL_PROG_THIRD_RANGE_END_HOUR,
    FIL_PROG_THIRD_RANGE_END_HOUR_CODE,
    FIL_PROG_THIRD_RANGE_START_HOUR,
    FIL_PROG_THIRD_RANGE_START_HOUR_CODE,
    FIL_PROG_WEEK_END_FIRST_RANGE_END_HOUR,
    FIL_PROG_WEEK_END_FIRST_RANGE_END_HOUR_CODE,
    FIL_PROG_WEEK_END_FIRST_RANGE_START_HOUR,
    FIL_PROG_WEEK_END_FIRST_RANGE_START_HOUR_CODE,
    FIL_PROG_WEEK_END_SECOND_RANGE_END_HOUR,
    FIL_PROG_WEEK_END_SECOND_RANGE_END_HOUR_CODE,
    FIL_PROG_WEEK_END_SECOND_RANGE_START_HOUR,
    FIL_PROG_WEEK_END_SECOND_RANGE_START_HOUR_CODE,
    FIL_PROG_WEEK_END_THIRD_RANGE_END_HOUR,
    FIL_PROG_WEEK_END_THIRD_RANGE_END_HOUR_CODE,
    FIL_PROG_WEEK_END_THIRD_RANGE_START_HOUR,
    FIL_PROG_WEEK_END_THIRD_RANGE_START_HOUR_CODE,
    LIGHT_COLOR,
    LIGHT_COLOR_CODE,
    LIGHT_INTENSITY,
    LIGHT_INTENSITY_CODE,
    LIGHT_PROG_DURATION,
    LIGHT_PROG_DURATION_CODE,
    LIGHT_PROG_START_HOUR,
    LIGHT_PROG_START_HOUR_CODE,
    LIGHT_PROG_STATUS,
    LIGHT_PROG_STATUS_CODE,
    LIGHT_PROG_WEEK_END_DURATION,
    LIGHT_PROG_WEEK_END_DURATION_CODE,
    LIGHT_PROG_WEEK_END_START_HOUR,
    LIGHT_PROG_WEEK_END_START_HOUR_CODE,
    LIGHT_SEQUENCE_SPEED,
    LIGHT_SEQUENCE_SPEED_CODE,
    LIGHT_TIMER_DURATION,
    LIGHT_TIMER_DURATION_CODE,
    WATER_TEMPERATURE_OFFSET,
    WATER_TEMPERATURE_OFFSET_CODE,
)
from .entity import TildSelectEntity


async def async_setup_entry(hass, entry, async_add_devices):
    """Set up sensor platform."""
    coordinator = hass.data[DOMAIN][COORDINATOR]
    selects = [
        TildLightIntensitySelect(coordinator, entry, hass),
        TildLightColorSelect(coordinator, entry, hass),
        TildLightSequenceSpeedSelect(coordinator, entry, hass),
        TildLightTimerDurationSelect(coordinator, entry, hass),
        TildLightProgrammingStatusSelect(coordinator, entry, hass),
        TildLightProgrammingStartHourSelect(coordinator, entry, hass),
        TildLightProgrammingDurationSelect(coordinator, entry, hass),
        TildLightProgrammingWeekEndStartHourSelect(coordinator, entry, hass),
        TildLightProgrammingWeekEndDurationSelect(coordinator, entry, hass),
        TildFiltrationProgrammingFirstRangeStartHourSelect(coordinator, entry, hass),
        TildFiltrationProgrammingFirstRangeEndHourSelect(coordinator, entry, hass),
        TildFiltrationProgrammingSecondRangeStartHourSelect(coordinator, entry, hass),
        TildFiltrationProgrammingSecondRangeEndHourSelect(coordinator, entry, hass),
        TildFiltrationProgrammingThirdRangeStartHourSelect(coordinator, entry, hass),
        TildFiltrationProgrammingThirdRangeEndHourSelect(coordinator, entry, hass),
        TildFiltrationProgrammingWeekEndFirstRangeStartHourSelect(coordinator, entry, hass),
        TildFiltrationProgrammingWeekEndFirstRangeEndHourSelect(coordinator, entry, hass),
        TildFiltrationProgrammingWeekEndSecondRangeStartHourSelect(coordinator, entry, hass),
        TildFiltrationProgrammingWeekEndSecondRangeEndHourSelect(coordinator, entry, hass),
        TildFiltrationProgrammingWeekEndThirdRangeStartHourSelect(coordinator, entry, hass),
        TildFiltrationProgrammingWeekEndThirdRangeEndHourSelect(coordinator, entry, hass),
        TildAuxiliaryProgrammingFirstRangeStartHourSelect(coordinator, entry, hass),
        TildAuxiliaryProgrammingFirstRangeEndHourSelect(coordinator, entry, hass),
        TildAuxiliaryProgrammingSecondRangeStartHourSelect(coordinator, entry, hass),
        TildAuxiliaryProgrammingSecondRangeEndHourSelect(coordinator, entry, hass),
        TildAuxiliaryProgrammingThirdRangeStartHourSelect(coordinator, entry, hass),
        TildAuxiliaryProgrammingThirdRangeEndHourSelect(coordinator, entry, hass),
        TildAuxiliaryProgrammingWeekEndFirstRangeStartHourSelect(coordinator, entry, hass),
        TildAuxiliaryProgrammingWeekEndFirstRangeEndHourSelect(coordinator, entry, hass),
        TildAuxiliaryProgrammingWeekEndSecondRangeStartHourSelect(coordinator, entry, hass),
        TildAuxiliaryProgrammingWeekEndSecondRangeEndHourSelect(coordinator, entry, hass),
        TildAuxiliaryProgrammingWeekEndThirdRangeStartHourSelect(coordinator, entry, hass),
        TildAuxiliaryProgrammingWeekEndThirdRangeEndHourSelect(coordinator, entry, hass),
        TildWaterTemperatureOffsetSelect(coordinator, entry, hass),
    ]
    async_add_devices(selects)


class TildLightIntensitySelect(TildSelectEntity):
    """Select the light intensity"""

    _attr_name = "Light intensity"
    _attr_unit_of_measurement = PERCENTAGE
    _attr_icon = "mdi:brightness-percent"

    _sensor_data_key = LIGHT_INTENSITY
    _sensor_data_code_key = LIGHT_INTENSITY_CODE
    _sensor_data_type = int


class TildLightColorSelect(TildSelectEntity):
    """Select the light color"""

    _attr_name = "Light color"
    _attr_icon = "mdi:palette"

    _sensor_data_key = LIGHT_COLOR
    _sensor_data_code_key = LIGHT_COLOR_CODE


class TildLightTimerDurationSelect(TildSelectEntity):
    """Select the light timer duration"""

    _attr_name = "Light timer duration"
    _attr_icon = "mdi:timer-cog-outline"

    _sensor_data_key = LIGHT_TIMER_DURATION
    _sensor_data_code_key = LIGHT_TIMER_DURATION_CODE


class TildWaterTemperatureOffsetSelect(TildSelectEntity):
    """Select the water temperature offset"""

    _attr_name = "Water temperature offset"
    _attr_unit_of_measurement = TEMP_CELSIUS
    _attr_icon = "mdi:thermometer-water"

    _sensor_data_key = WATER_TEMPERATURE_OFFSET
    _sensor_data_code_key = WATER_TEMPERATURE_OFFSET_CODE
    _sensor_data_type = int


class TildLightProgrammingStatusSelect(TildSelectEntity):
    """Select the light programming status"""

    _attr_name = "Light programming status"
    _attr_icon = "mdi:home-lightbulb-outline"

    _sensor_data_key = LIGHT_PROG_STATUS
    _sensor_data_code_key = LIGHT_PROG_STATUS_CODE


class TildLightProgrammingStartHourSelect(TildSelectEntity):
    """Select the light programming start hour"""

    _attr_name = "Light programming start hour"
    _attr_icon = "mdi:clock-start"

    _sensor_data_key = LIGHT_PROG_START_HOUR
    _sensor_data_code_key = LIGHT_PROG_START_HOUR_CODE


class TildLightProgrammingDurationSelect(TildSelectEntity):
    """Select the light programming duration"""

    _attr_name = "Light programming duration"
    _attr_icon = "mdi:clock-time-eight-outline"

    _sensor_data_key = LIGHT_PROG_DURATION
    _sensor_data_code_key = LIGHT_PROG_DURATION_CODE


class TildLightProgrammingWeekEndStartHourSelect(TildSelectEntity):
    """Select the light programming week-end start hour"""

    _attr_name = "Light programming week-end start hour"
    _attr_icon = "mdi:clock-start"

    _sensor_data_key = LIGHT_PROG_WEEK_END_START_HOUR
    _sensor_data_code_key = LIGHT_PROG_WEEK_END_START_HOUR_CODE


class TildLightProgrammingWeekEndDurationSelect(TildSelectEntity):
    """Select the light programming week-end duration"""

    _attr_name = "Light programming week-end duration"
    _attr_icon = "mdi:clock-time-eight-outline"

    _sensor_data_key = LIGHT_PROG_WEEK_END_DURATION
    _sensor_data_code_key = LIGHT_PROG_WEEK_END_DURATION_CODE


class TildLightSequenceSpeedSelect(TildSelectEntity):
    """Select the light sequence speed"""

    _attr_name = "Light sequence speed"
    _attr_icon = "mdi:speedometer"

    _sensor_data_key = LIGHT_SEQUENCE_SPEED
    _sensor_data_code_key = LIGHT_SEQUENCE_SPEED_CODE
    _sensor_data_type = int


class TildFiltrationProgrammingFirstRangeStartHourSelect(TildSelectEntity):
    """Select the filtration programming first range start hour"""

    _attr_name = "Filtration programming first range start hour"
    _attr_icon = "mdi:clock-start"

    _sensor_data_key = FIL_PROG_FIRST_RANGE_START_HOUR
    _sensor_data_code_key = FIL_PROG_FIRST_RANGE_START_HOUR_CODE


class TildFiltrationProgrammingFirstRangeEndHourSelect(TildSelectEntity):
    """Select the filtration programming first range end hour"""

    _attr_name = "Filtration programming first range end hour"
    _attr_icon = "mdi:clock-end"

    _sensor_data_key = FIL_PROG_FIRST_RANGE_END_HOUR
    _sensor_data_code_key = FIL_PROG_FIRST_RANGE_END_HOUR_CODE


class TildFiltrationProgrammingSecondRangeStartHourSelect(TildSelectEntity):
    """Select the filtration programming second range start hour"""

    _attr_name = "Filtration programming second range start hour"
    _attr_icon = "mdi:clock-start"

    _sensor_data_key = FIL_PROG_SECOND_RANGE_START_HOUR
    _sensor_data_code_key = FIL_PROG_SECOND_RANGE_START_HOUR_CODE


class TildFiltrationProgrammingSecondRangeEndHourSelect(TildSelectEntity):
    """Select the filtration programming second range end hour"""

    _attr_name = "Filtration programming second range end hour"
    _attr_icon = "mdi:clock-end"

    _sensor_data_key = FIL_PROG_SECOND_RANGE_END_HOUR
    _sensor_data_code_key = FIL_PROG_SECOND_RANGE_END_HOUR_CODE
    _sensor_data_extra_keys = {
        "raw_hour_code": FIL_PROG_SECOND_RANGE_END_HOUR_CODE,
    }


class TildFiltrationProgrammingThirdRangeStartHourSelect(TildSelectEntity):
    """Select the filtration programming third range start hour"""

    _attr_name = "Filtration programming third range start hour"
    _attr_icon = "mdi:clock-start"

    _sensor_data_key = FIL_PROG_THIRD_RANGE_START_HOUR
    _sensor_data_code_key = FIL_PROG_THIRD_RANGE_START_HOUR_CODE
    _sensor_data_extra_keys = {
        "raw_hour_code": FIL_PROG_THIRD_RANGE_START_HOUR_CODE,
    }


class TildFiltrationProgrammingThirdRangeEndHourSelect(TildSelectEntity):
    """Select the filtration programming third range end hour"""

    _attr_name = "Filtration programming third range end hour"
    _attr_icon = "mdi:clock-end"

    _sensor_data_key = FIL_PROG_THIRD_RANGE_END_HOUR
    _sensor_data_code_key = FIL_PROG_THIRD_RANGE_END_HOUR_CODE


class TildFiltrationProgrammingWeekEndFirstRangeStartHourSelect(TildSelectEntity):
    """Select the filtration programming week-end first range start hour"""

    _attr_name = "Filtration programming week-end first range start hour"
    _attr_icon = "mdi:clock-start"

    _sensor_data_key = FIL_PROG_WEEK_END_FIRST_RANGE_START_HOUR
    _sensor_data_code_key = FIL_PROG_WEEK_END_FIRST_RANGE_START_HOUR_CODE


class TildFiltrationProgrammingWeekEndFirstRangeEndHourSelect(TildSelectEntity):
    """Select the filtration programming week-end first range end hour"""

    _attr_name = "Filtration programming week-end first range end hour"
    _attr_icon = "mdi:clock-end"

    _sensor_data_key = FIL_PROG_WEEK_END_FIRST_RANGE_END_HOUR
    _sensor_data_code_key = FIL_PROG_WEEK_END_FIRST_RANGE_END_HOUR_CODE


class TildFiltrationProgrammingWeekEndSecondRangeStartHourSelect(TildSelectEntity):
    """Select the filtration programming week-end second range start hour"""

    _attr_name = "Filtration programming week-end second range start hour"
    _attr_icon = "mdi:clock-start"

    _sensor_data_key = FIL_PROG_WEEK_END_SECOND_RANGE_START_HOUR
    _sensor_data_code_key = FIL_PROG_WEEK_END_SECOND_RANGE_START_HOUR_CODE


class TildFiltrationProgrammingWeekEndSecondRangeEndHourSelect(TildSelectEntity):
    """Select the filtration programming week-end second range end hour"""

    _attr_name = "Filtration programming week-end second range end hour"
    _attr_icon = "mdi:clock-end"

    _sensor_data_key = FIL_PROG_WEEK_END_SECOND_RANGE_END_HOUR
    _sensor_data_code_key = FIL_PROG_WEEK_END_SECOND_RANGE_END_HOUR_CODE


class TildFiltrationProgrammingWeekEndThirdRangeStartHourSelect(TildSelectEntity):
    """Select the filtration programming week-end third range start hour"""

    _attr_name = "Filtration programming week-end third range start hour"
    _attr_icon = "mdi:clock-start"

    _sensor_data_key = FIL_PROG_WEEK_END_THIRD_RANGE_START_HOUR
    _sensor_data_code_key = FIL_PROG_WEEK_END_THIRD_RANGE_START_HOUR_CODE


class TildFiltrationProgrammingWeekEndThirdRangeEndHourSelect(TildSelectEntity):
    """Select the filtration programming week-end third range end hour"""

    _attr_name = "Filtration programming week-end third range end hour"
    _attr_icon = "mdi:clock-end"

    _sensor_data_key = FIL_PROG_WEEK_END_THIRD_RANGE_END_HOUR
    _sensor_data_code_key = FIL_PROG_WEEK_END_THIRD_RANGE_END_HOUR_CODE


class TildAuxiliaryProgrammingFirstRangeStartHourSelect(TildSelectEntity):
    """Select the auxiliary programming first range start hour"""

    _attr_name = "Auxiliary programming first range start hour"
    _attr_icon = "mdi:clock-start"

    _sensor_data_key = AUX_PROG_FIRST_RANGE_START_HOUR
    _sensor_data_code_key = AUX_PROG_FIRST_RANGE_START_HOUR_CODE


class TildAuxiliaryProgrammingFirstRangeEndHourSelect(TildSelectEntity):
    """Select the auxiliary programming first range end hour"""

    _attr_name = "Auxiliary programming first range end hour"
    _attr_icon = "mdi:clock-end"

    _sensor_data_key = AUX_PROG_FIRST_RANGE_END_HOUR
    _sensor_data_code_key = AUX_PROG_FIRST_RANGE_END_HOUR_CODE


class TildAuxiliaryProgrammingSecondRangeStartHourSelect(TildSelectEntity):
    """Select the auxiliary programming second range start hour"""

    _attr_name = "Auxiliary programming second range start hour"
    _attr_icon = "mdi:clock-start"

    _sensor_data_key = AUX_PROG_SECOND_RANGE_START_HOUR
    _sensor_data_code_key = AUX_PROG_SECOND_RANGE_START_HOUR_CODE


class TildAuxiliaryProgrammingSecondRangeEndHourSelect(TildSelectEntity):
    """Select the auxiliary programming second range end hour"""

    _attr_name = "Auxiliary programming second range end hour"
    _attr_icon = "mdi:clock-end"

    _sensor_data_key = AUX_PROG_SECOND_RANGE_END_HOUR
    _sensor_data_code_key = AUX_PROG_SECOND_RANGE_END_HOUR_CODE


class TildAuxiliaryProgrammingThirdRangeStartHourSelect(TildSelectEntity):
    """Select the auxiliary programming third range start hour"""

    _attr_name = "Auxiliary programming third range start hour"
    _attr_icon = "mdi:clock-start"

    _sensor_data_key = AUX_PROG_THIRD_RANGE_START_HOUR
    _sensor_data_code_key = AUX_PROG_THIRD_RANGE_START_HOUR_CODE


class TildAuxiliaryProgrammingThirdRangeEndHourSelect(TildSelectEntity):
    """Select the auxiliary programming third range end hour"""

    _attr_name = "Auxiliary programming third range end hour"
    _attr_icon = "mdi:clock-end"

    _sensor_data_key = AUX_PROG_THIRD_RANGE_END_HOUR
    _sensor_data_code_key = AUX_PROG_THIRD_RANGE_END_HOUR_CODE


class TildAuxiliaryProgrammingWeekEndFirstRangeStartHourSelect(TildSelectEntity):
    """Select the auxiliary programming week-end first range start hour"""

    _attr_name = "Auxiliary programming week-end first range start hour"
    _attr_icon = "mdi:clock-start"

    _sensor_data_key = AUX_PROG_WEEK_END_FIRST_RANGE_START_HOUR
    _sensor_data_code_key = AUX_PROG_WEEK_END_FIRST_RANGE_START_HOUR_CODE


class TildAuxiliaryProgrammingWeekEndFirstRangeEndHourSelect(TildSelectEntity):
    """Select the auxiliary programming week-end first range end hour"""

    _attr_name = "Auxiliary programming week-end first range end hour"
    _attr_icon = "mdi:clock-end"

    _sensor_data_key = AUX_PROG_WEEK_END_FIRST_RANGE_END_HOUR
    _sensor_data_code_key = AUX_PROG_WEEK_END_FIRST_RANGE_END_HOUR_CODE


class TildAuxiliaryProgrammingWeekEndSecondRangeStartHourSelect(TildSelectEntity):
    """Select the auxiliary programming week-end second range start hour"""

    _attr_name = "Auxiliary programming week-end second range start hour"
    _attr_icon = "mdi:clock-start"

    _sensor_data_key = AUX_PROG_WEEK_END_SECOND_RANGE_START_HOUR
    _sensor_data_code_key = AUX_PROG_WEEK_END_SECOND_RANGE_START_HOUR_CODE


class TildAuxiliaryProgrammingWeekEndSecondRangeEndHourSelect(TildSelectEntity):
    """Select the auxiliary programming week-end second range end hour"""

    _attr_name = "Auxiliary programming week-end second range end hour"
    _attr_icon = "mdi:clock-end"

    _sensor_data_key = AUX_PROG_WEEK_END_SECOND_RANGE_END_HOUR
    _sensor_data_code_key = AUX_PROG_WEEK_END_SECOND_RANGE_END_HOUR_CODE


class TildAuxiliaryProgrammingWeekEndThirdRangeStartHourSelect(TildSelectEntity):
    """Select the auxiliary programming week-end third range start hour"""

    _attr_name = "Auxiliary programming week-end third range start hour"
    _attr_icon = "mdi:clock-start"

    _sensor_data_key = AUX_PROG_WEEK_END_THIRD_RANGE_START_HOUR
    _sensor_data_code_key = AUX_PROG_WEEK_END_THIRD_RANGE_START_HOUR_CODE


class TildAuxiliaryProgrammingWeekEndThirdRangeEndHourSelect(TildSelectEntity):
    """Select the auxiliary programming week-end third range end hour"""

    _attr_name = "Auxiliary programming week-end third range end hour"
    _attr_icon = "mdi:clock-end"

    _sensor_data_key = AUX_PROG_WEEK_END_THIRD_RANGE_END_HOUR
    _sensor_data_code_key = AUX_PROG_WEEK_END_THIRD_RANGE_END_HOUR_CODE
