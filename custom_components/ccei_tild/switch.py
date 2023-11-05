"""Switch platform"""
from .const import (
    AUX_PROG_ENABLED,
    AUX_PROG_FIRST_RANGE_ENABLED,
    AUX_PROG_SECOND_RANGE_ENABLED,
    AUX_PROG_THIRD_RANGE_ENABLED,
    AUX_PROG_WEEK_END_FIRST_RANGE_ENABLED,
    AUX_PROG_WEEK_END_MODE_ENABLED,
    AUX_PROG_WEEK_END_SECOND_RANGE_ENABLED,
    AUX_PROG_WEEK_END_THIRD_RANGE_ENABLED,
    COORDINATOR,
    DOMAIN,
    FIL_ENABLED,
    FIL_ENSLAVED_BY_LIGHT_ENABLED,
    FIL_PROG_ENABLED,
    FIL_PROG_FIRST_RANGE_ENABLED,
    FIL_PROG_SECOND_RANGE_ENABLED,
    FIL_PROG_THERMOREGULATED_ENABLED,
    FIL_PROG_THIRD_RANGE_ENABLED,
    FIL_PROG_WEEK_END_FIRST_RANGE_ENABLED,
    FIL_PROG_WEEK_END_MODE_ENABLED,
    FIL_PROG_WEEK_END_SECOND_RANGE_ENABLED,
    FIL_PROG_WEEK_END_THIRD_RANGE_ENABLED,
    LIGHT_PROG_DUSK_MODE_ENABLED,
    LIGHT_PROG_WEEK_END_MODE_ENABLED,
)
from .entity import TildSwitchEntity


async def async_setup_entry(hass, entry, async_add_devices):
    """Set up sensor platform."""
    coordinator = hass.data[DOMAIN][COORDINATOR]
    switchs = [
        TildFiltrationSwitch(coordinator, entry, hass),
        TildLightProgrammingDuskModeSwitch(coordinator, entry, hass),
        TildLightProgrammingWeekEndModeSwitch(coordinator, entry, hass),
        TildFiltrationProgrammingSwitch(coordinator, entry, hass),
        TildFiltrationProgrammingThermoregulatedSwitch(coordinator, entry, hass),
        TildFiltrationProgrammingWeekEndModeSwitch(coordinator, entry, hass),
        TildFiltrationProgrammingFirstRangeSwitch(coordinator, entry, hass),
        TildFiltrationProgrammingSecondRangeSwitch(coordinator, entry, hass),
        TildFiltrationProgrammingThirdRangeSwitch(coordinator, entry, hass),
        TildFiltrationProgrammingWeekEndFirstRangeSwitch(coordinator, entry, hass),
        TildFiltrationProgrammingWeekEndSecondRangeSwitch(coordinator, entry, hass),
        TildFiltrationProgrammingWeekEndThirdRangeSwitch(coordinator, entry, hass),
        TildAuxiliaryProgrammingSwitch(coordinator, entry, hass),
        TildAuxiliaryProgrammingWeekEndModeSwitch(coordinator, entry, hass),
        TildAuxiliaryProgrammingFirstRangeSwitch(coordinator, entry, hass),
        TildAuxiliaryProgrammingSecondRangeSwitch(coordinator, entry, hass),
        TildAuxiliaryProgrammingThirdRangeSwitch(coordinator, entry, hass),
        TildAuxiliaryProgrammingWeekEndFirstRangeSwitch(coordinator, entry, hass),
        TildAuxiliaryProgrammingWeekEndSecondRangeSwitch(coordinator, entry, hass),
        TildAuxiliaryProgrammingWeekEndThirdRangeSwitch(coordinator, entry, hass),
    ]
    async_add_devices(switchs)


class TildFiltrationSwitch(TildSwitchEntity):
    """Manage the filtration"""

    _attr_id_key = "tild_filtration"
    _attr_name = "Filtration"
    _attr_icon = "mdi:filter-cog-outline"

    _sensor_data_key = FIL_ENABLED
    _sensor_data_extra_keys = {
        "enslaved_by_light": FIL_ENSLAVED_BY_LIGHT_ENABLED,
    }


class TildLightProgrammingDuskModeSwitch(TildSwitchEntity):
    """Manage the light programming dusk mode"""

    _attr_id_key = "tild_light_prog_dusk_mode_status"
    _attr_name = "Light programming dusk mode"
    _attr_icon = "mdi:lightbulb-night"

    _sensor_data_key = LIGHT_PROG_DUSK_MODE_ENABLED


class TildLightProgrammingWeekEndModeSwitch(TildSwitchEntity):
    """Manage the light programming week-end mode"""

    _attr_id_key = "tild_light_prog_week_end_mode_status"
    _attr_name = "Light programming week-end mode"
    _attr_icon = "mdi:calendar-weekend"

    _sensor_data_key = LIGHT_PROG_WEEK_END_MODE_ENABLED


class TildFiltrationProgrammingSwitch(TildSwitchEntity):
    """Manage the filtration programming"""

    _attr_id_key = "tild_filtration_prog_status"
    _attr_name = "Filtration programming"
    _attr_icon = "mdi:filter-cog-outline"

    _sensor_data_key = FIL_PROG_ENABLED


class TildFiltrationProgrammingThermoregulatedSwitch(TildSwitchEntity):
    """Manage the filtration thermoregulated programming"""

    _attr_id_key = "tild_filtration_prog_thermoregulated_status"
    _attr_name = "Filtration thermoregulated programming"
    _attr_icon = "mdi:thermometer-auto"

    _sensor_data_key = FIL_PROG_THERMOREGULATED_ENABLED


class TildFiltrationProgrammingWeekEndModeSwitch(TildSwitchEntity):
    """Manage the filtration programming week-end mode"""

    _attr_id_key = "tild_filtration_prog_week_end_mode status"
    _attr_name = "Filtration programming week-end mode"
    _attr_icon = "mdi:calendar-weekend"

    _sensor_data_key = FIL_PROG_WEEK_END_MODE_ENABLED


class TildFiltrationProgrammingFirstRangeSwitch(TildSwitchEntity):
    """Manage the filtration programming first range"""

    _attr_id_key = "tild_filtration_prog_first_range_status"
    _attr_name = "Filtration programming first range"
    _attr_icon = "mdi:calendar-filter"

    _sensor_data_key = FIL_PROG_FIRST_RANGE_ENABLED


class TildFiltrationProgrammingSecondRangeSwitch(TildSwitchEntity):
    """Manage the filtration programming second range"""

    _attr_id_key = "tild_filtration_prog_second_range_status"
    _attr_name = "Filtration programming second range"
    _attr_icon = "mdi:calendar-filter"

    _sensor_data_key = FIL_PROG_SECOND_RANGE_ENABLED


class TildFiltrationProgrammingThirdRangeSwitch(TildSwitchEntity):
    """Manage the filtration programming third range"""

    _attr_id_key = "tild_filtration_prog_third_range_status"
    _attr_name = "Filtration programming third range"
    _attr_icon = "mdi:calendar-filter"

    _sensor_data_key = FIL_PROG_THIRD_RANGE_ENABLED


class TildFiltrationProgrammingWeekEndFirstRangeSwitch(TildSwitchEntity):
    """Manage the filtration programming week-end first range"""

    _attr_id_key = "tild_filtration_prog_week_end_first_range_status"
    _attr_name = "Filtration programming week-end first range"
    _attr_icon = "mdi:calendar-filter"

    _sensor_data_key = FIL_PROG_WEEK_END_FIRST_RANGE_ENABLED


class TildFiltrationProgrammingWeekEndSecondRangeSwitch(TildSwitchEntity):
    """Manage the filtration programming week-end second range"""

    _attr_id_key = "tild_filtration_prog_week_end_second_range_status"
    _attr_name = "Filtration programming week-end second range"
    _attr_icon = "mdi:calendar-filter"

    _sensor_data_key = FIL_PROG_WEEK_END_SECOND_RANGE_ENABLED


class TildFiltrationProgrammingWeekEndThirdRangeSwitch(TildSwitchEntity):
    """Manage the filtration programming week-end third range"""

    _attr_id_key = "tild_filtration_prog_week_end_third_range_status"
    _attr_name = "Filtration programming week-end third range"
    _attr_icon = "mdi:calendar-filter"

    _sensor_data_key = FIL_PROG_WEEK_END_THIRD_RANGE_ENABLED


class TildAuxiliaryProgrammingSwitch(TildSwitchEntity):
    """Manage the auxiliary programming"""

    _attr_id_key = "tild_aux_prog_status"
    _attr_name = "Auxiliary programming"
    _attr_icon = "mdi:cog-box"

    _sensor_data_key = AUX_PROG_ENABLED


class TildAuxiliaryProgrammingWeekEndModeSwitch(TildSwitchEntity):
    """Manage the auxiliary programming week-end mode"""

    _attr_id_key = "tild_aux_prog_week_end_mode_status"
    _attr_name = "Auxiliary programming week-end mode"
    _attr_icon = "mdi:calendar-weekend"

    _sensor_data_key = AUX_PROG_WEEK_END_MODE_ENABLED


class TildAuxiliaryProgrammingFirstRangeSwitch(TildSwitchEntity):
    """Manage the auxiliary programming first range"""

    _attr_id_key = "tild_aux_prog_first_range_status"
    _attr_name = "Auxiliary programming first range"
    _attr_icon = "mdi:calendar-clock"

    _sensor_data_key = AUX_PROG_FIRST_RANGE_ENABLED


class TildAuxiliaryProgrammingSecondRangeSwitch(TildSwitchEntity):
    """Manage the auxiliary programming second range"""

    _attr_id_key = "tild_aux_prog_second_range_status"
    _attr_name = "Auxiliary programming second range"
    _attr_icon = "mdi:calendar-clock"

    _sensor_data_key = AUX_PROG_SECOND_RANGE_ENABLED


class TildAuxiliaryProgrammingThirdRangeSwitch(TildSwitchEntity):
    """Manage the auxiliary programming third range"""

    _attr_id_key = "tild_aux_prog_third_range_status"
    _attr_name = "Auxiliary programming third range"
    _attr_icon = "mdi:calendar-clock"

    _sensor_data_key = AUX_PROG_THIRD_RANGE_ENABLED


class TildAuxiliaryProgrammingWeekEndFirstRangeSwitch(TildSwitchEntity):
    """Manage the auxiliary programming week-end first range"""

    _attr_id_key = "tild_aux_prog_week_end_first_range_status"
    _attr_name = "Auxiliary programming week-end first range"
    _attr_icon = "mdi:calendar-clock"

    _sensor_data_key = AUX_PROG_WEEK_END_FIRST_RANGE_ENABLED


class TildAuxiliaryProgrammingWeekEndSecondRangeSwitch(TildSwitchEntity):
    """Manage the auxiliary programming week-end second range"""

    _attr_id_key = "tild_aux_prog_week_end_second_range_status"
    _attr_name = "Auxiliary programming week-end second range"
    _attr_icon = "mdi:calendar-clock"

    _sensor_data_key = AUX_PROG_WEEK_END_SECOND_RANGE_ENABLED


class TildAuxiliaryProgrammingWeekEndThirdRangeSwitch(TildSwitchEntity):
    """Manage the auxiliary programming week-end third range"""

    _attr_id_key = "tild_aux_prog_week_end_third_range_status"
    _attr_name = "Auxiliary programming week-end third range"
    _attr_icon = "mdi:calendar-clock"

    _sensor_data_key = AUX_PROG_WEEK_END_THIRD_RANGE_ENABLED
