"""Switch platform"""
from .const import (
    AUX_PROG_FIRST_RANGE_STATUS_ENABLED,
    AUX_PROG_SECOND_RANGE_STATUS_ENABLED,
    AUX_PROG_STATUS_ENABLED,
    AUX_PROG_THIRD_RANGE_STATUS_ENABLED,
    AUX_PROG_WEEK_END_FIRST_RANGE_STATUS_ENABLED,
    AUX_PROG_WEEK_END_MODE_STATUS_ENABLED,
    AUX_PROG_WEEK_END_SECOND_RANGE_STATUS_ENABLED,
    AUX_PROG_WEEK_END_THIRD_RANGE_STATUS_ENABLED,
    COORDINATOR,
    DOMAIN,
    FILTRATION_ENABLED,
    FILTRATION_PROG_FIRST_RANGE_STATUS_ENABLED,
    FILTRATION_PROG_SECOND_RANGE_STATUS_ENABLED,
    FILTRATION_PROG_STATUS_ENABLED,
    FILTRATION_PROG_THERMOREGULATED_STATUS_ENABLED,
    FILTRATION_PROG_THIRD_RANGE_STATUS_ENABLED,
    FILTRATION_PROG_WEEK_END_FIRST_RANGE_STATUS_ENABLED,
    FILTRATION_PROG_WEEK_END_SECOND_RANGE_STATUS_ENABLED,
    FILTRATION_PROG_WEEK_END_STATUS_ENABLED,
    FILTRATION_PROG_WEEK_END_THIRD_RANGE_STATUS_ENABLED,
    LIGHT_PROG_MODE_DUSK_ENABLED,
    LIGHT_PROG_WEEK_END_MODE_ENABLED,
    THERMOREGULATED_FILTRATION_ENABLED,
    TREATMENT_ENABLED,
)
from .entity import TildSwitchEntity


async def async_setup_entry(hass, entry, async_add_devices):
    """Set up sensor platform."""
    coordinator = hass.data[DOMAIN][COORDINATOR]
    switchs = [
        TildTreatmentSwitch(coordinator, entry, hass),
        TildFiltrationSwitch(coordinator, entry, hass),
        TildThermoregulatedFiltrationSwitch(coordinator, entry, hass),
        TildLightProgrammingModeDuskSwitch(coordinator, entry, hass),
        TildLightProgrammingModeWeekEndSwitch(coordinator, entry, hass),
        TildFiltrationProgrammingSwitch(coordinator, entry, hass),
        TildFiltrationProgrammingThermoregulatedSwitch(coordinator, entry, hass),
        TildFiltrationProgrammingModeWeekEndSwitch(coordinator, entry, hass),
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


class TildTreatmentSwitch(TildSwitchEntity):
    """Manage the treament"""

    _attr_id_key = "tild_treatment"
    _attr_name = "Treatment"
    _attr_icon = "mdi:spray-bottle"

    _sensor_data_key = TREATMENT_ENABLED


class TildFiltrationSwitch(TildSwitchEntity):
    """Manage the filtration"""

    _attr_id_key = "tild_filtration"
    _attr_name = "Filtration"
    _attr_icon = "mdi:filter-cog-outline"

    _sensor_data_key = FILTRATION_ENABLED

    _client_toggle_method = "toggle_filtration"


class TildThermoregulatedFiltrationSwitch(TildSwitchEntity):
    """Manage the filtration"""

    _attr_id_key = "tild_thermoregulated_filtration"
    _attr_name = "Thermoregulated filtration"
    _attr_icon = "mdi:coolant-temperature"

    _sensor_data_key = THERMOREGULATED_FILTRATION_ENABLED

    _client_toggle_method = "toggle_thermoregulated_filtration"


class TildLightProgrammingModeDuskSwitch(TildSwitchEntity):
    """Manage the light programming mode dusk"""

    _attr_id_key = "tild_light_prog_mode_dusk"
    _attr_name = "Light programming mode dusk"
    _attr_icon = "mdi:lightbulb-night"

    _sensor_data_key = LIGHT_PROG_MODE_DUSK_ENABLED

    _client_toggle_method = "toggle_light_prog_mode_dusk"


class TildLightProgrammingModeWeekEndSwitch(TildSwitchEntity):
    """Manage the light programming mode week-end"""

    _attr_id_key = "tild_light_prog_week_end_mode"
    _attr_name = "Light programming mode week-end"
    _attr_icon = "mdi:calendar-weekend"

    _sensor_data_key = LIGHT_PROG_WEEK_END_MODE_ENABLED

    _client_toggle_method = "toggle_light_prog_week_end_mode"


class TildFiltrationProgrammingSwitch(TildSwitchEntity):
    """Manage the filtration programming"""

    _attr_id_key = "tild_filtration_prog_status"
    _attr_name = "Filtration programming"
    _attr_icon = "mdi:filter-cog-outline"

    _sensor_data_key = FILTRATION_PROG_STATUS_ENABLED

    _client_toggle_method = "toggle_filtration_prog_status"


class TildFiltrationProgrammingThermoregulatedSwitch(TildSwitchEntity):
    """Manage the filtration programming thermoregulated"""

    _attr_id_key = "tild_filtration_prog_thermoregulated_status"
    _attr_name = "Filtration programming thermoregulated"
    _attr_icon = "mdi:thermometer-auto"

    _sensor_data_key = FILTRATION_PROG_THERMOREGULATED_STATUS_ENABLED

    _client_toggle_method = "toggle_filtration_prog_thermoregulated_status"


class TildFiltrationProgrammingModeWeekEndSwitch(TildSwitchEntity):
    """Manage the filtration programming mode week-end"""

    _attr_id_key = "tild_filtration_prog_week_end_status"
    _attr_name = "Filtration programming mode week-end"
    _attr_icon = "mdi:calendar-weekend"

    _sensor_data_key = FILTRATION_PROG_WEEK_END_STATUS_ENABLED

    _client_toggle_method = "toggle_filtration_prog_week_end_status"


class TildFiltrationProgrammingFirstRangeSwitch(TildSwitchEntity):
    """Manage the filtration programming first range"""

    _attr_id_key = "tild_filtration_prog_first_range_status"
    _attr_name = "Filtration programming first range"
    _attr_icon = "mdi:calendar-filter"

    _sensor_data_key = FILTRATION_PROG_FIRST_RANGE_STATUS_ENABLED

    _client_toggle_method = "toggle_filtration_prog_first_range_status"


class TildFiltrationProgrammingSecondRangeSwitch(TildSwitchEntity):
    """Manage the filtration programming second range"""

    _attr_id_key = "tild_filtration_prog_second_range_status"
    _attr_name = "Filtration programming second range"
    _attr_icon = "mdi:calendar-filter"

    _sensor_data_key = FILTRATION_PROG_SECOND_RANGE_STATUS_ENABLED

    _client_toggle_method = "toggle_filtration_prog_second_range_status"


class TildFiltrationProgrammingThirdRangeSwitch(TildSwitchEntity):
    """Manage the filtration programming third range"""

    _attr_id_key = "tild_filtration_prog_third_range_status"
    _attr_name = "Filtration programming third range"
    _attr_icon = "mdi:calendar-filter"

    _sensor_data_key = FILTRATION_PROG_THIRD_RANGE_STATUS_ENABLED

    _client_toggle_method = "toggle_filtration_prog_third_range_status"


class TildFiltrationProgrammingWeekEndFirstRangeSwitch(TildSwitchEntity):
    """Manage the filtration programming week-end first range"""

    _attr_id_key = "tild_filtration_prog_week_end_first_range_status"
    _attr_name = "Filtration programming week-end first range"
    _attr_icon = "mdi:calendar-filter"

    _sensor_data_key = FILTRATION_PROG_WEEK_END_FIRST_RANGE_STATUS_ENABLED

    _client_toggle_method = "toggle_filtration_prog_week_end_first_range_status"


class TildFiltrationProgrammingWeekEndSecondRangeSwitch(TildSwitchEntity):
    """Manage the filtration programming week-end second range"""

    _attr_id_key = "tild_filtration_prog_week_end_second_range_status"
    _attr_name = "Filtration programming week-end second range"
    _attr_icon = "mdi:calendar-filter"

    _sensor_data_key = FILTRATION_PROG_WEEK_END_SECOND_RANGE_STATUS_ENABLED

    _client_toggle_method = "toggle_filtration_prog_week_end_second_range_status"


class TildFiltrationProgrammingWeekEndThirdRangeSwitch(TildSwitchEntity):
    """Manage the filtration programming week-end third range"""

    _attr_id_key = "tild_filtration_prog_week_end_third_range_status"
    _attr_name = "Filtration programming week-end third range"
    _attr_icon = "mdi:calendar-filter"

    _sensor_data_key = FILTRATION_PROG_WEEK_END_THIRD_RANGE_STATUS_ENABLED

    _client_toggle_method = "toggle_filtration_prog_week_end_third_range_status"


class TildAuxiliaryProgrammingSwitch(TildSwitchEntity):
    """Manage the auxiliary programming"""

    _attr_id_key = "tild_aux_prog_status"
    _attr_name = "Auxiliary programming"
    _attr_icon = "mdi:cog-box"

    _sensor_data_key = AUX_PROG_STATUS_ENABLED

    _client_toggle_method = "toggle_aux_prog_status"


class TildAuxiliaryProgrammingWeekEndModeSwitch(TildSwitchEntity):
    """Manage the auxiliary programming week-end mode"""

    _attr_id_key = "tild_aux_prog_week_end_mode_status"
    _attr_name = "Auxiliary programming week-end mode"
    _attr_icon = "mdi:calendar-weekend"

    _sensor_data_key = AUX_PROG_WEEK_END_MODE_STATUS_ENABLED

    _client_toggle_method = "toggle_aux_prog_week_end_mode_status"


class TildAuxiliaryProgrammingFirstRangeSwitch(TildSwitchEntity):
    """Manage the auxiliary programming first range"""

    _attr_id_key = "tild_aux_prog_first_range_status"
    _attr_name = "Auxiliary programming first range"
    _attr_icon = "mdi:calendar-clock"

    _sensor_data_key = AUX_PROG_FIRST_RANGE_STATUS_ENABLED

    _client_toggle_method = "toggle_aux_prog_first_range_status"


class TildAuxiliaryProgrammingSecondRangeSwitch(TildSwitchEntity):
    """Manage the auxiliary programming second range"""

    _attr_id_key = "tild_aux_prog_second_range_status"
    _attr_name = "Auxiliary programming second range"
    _attr_icon = "mdi:calendar-clock"

    _sensor_data_key = AUX_PROG_SECOND_RANGE_STATUS_ENABLED

    _client_toggle_method = "toggle_aux_prog_second_range_status"


class TildAuxiliaryProgrammingThirdRangeSwitch(TildSwitchEntity):
    """Manage the auxiliary programming third range"""

    _attr_id_key = "tild_aux_prog_third_range_status"
    _attr_name = "Auxiliary programming third range"
    _attr_icon = "mdi:calendar-clock"

    _sensor_data_key = AUX_PROG_THIRD_RANGE_STATUS_ENABLED

    _client_toggle_method = "toggle_aux_prog_third_range_status"


class TildAuxiliaryProgrammingWeekEndFirstRangeSwitch(TildSwitchEntity):
    """Manage the auxiliary programming week-end first range"""

    _attr_id_key = "tild_aux_prog_week_end_first_range_status"
    _attr_name = "Auxiliary programming week-end first range"
    _attr_icon = "mdi:calendar-clock"

    _sensor_data_key = AUX_PROG_WEEK_END_FIRST_RANGE_STATUS_ENABLED

    _client_toggle_method = "toggle_aux_prog_week_end_first_range_status"


class TildAuxiliaryProgrammingWeekEndSecondRangeSwitch(TildSwitchEntity):
    """Manage the auxiliary programming week-end second range"""

    _attr_id_key = "tild_aux_prog_week_end_second_range_status"
    _attr_name = "Auxiliary programming week-end second range"
    _attr_icon = "mdi:calendar-clock"

    _sensor_data_key = AUX_PROG_WEEK_END_SECOND_RANGE_STATUS_ENABLED

    _client_toggle_method = "toggle_aux_prog_week_end_second_range_status"


class TildAuxiliaryProgrammingWeekEndThirdRangeSwitch(TildSwitchEntity):
    """Manage the auxiliary programming week-end third range"""

    _attr_id_key = "tild_aux_prog_week_end_third_range_status"
    _attr_name = "Auxiliary programming week-end third range"
    _attr_icon = "mdi:calendar-clock"

    _sensor_data_key = AUX_PROG_WEEK_END_THIRD_RANGE_STATUS_ENABLED

    _client_toggle_method = "toggle_aux_prog_week_end_third_range_status"
