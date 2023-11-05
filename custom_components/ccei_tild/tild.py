"""CCEI Tild client"""
import asyncio
import json
import logging
import random
import socket
from datetime import datetime

from bitstring import BitArray

from .const import (
    AUX_PROG_ENABLED,
    AUX_PROG_FIRST_RANGE_ENABLED,
    AUX_PROG_FIRST_RANGE_END_HOUR,
    AUX_PROG_FIRST_RANGE_END_HOUR_CODE,
    AUX_PROG_FIRST_RANGE_START_HOUR,
    AUX_PROG_FIRST_RANGE_START_HOUR_CODE,
    AUX_PROG_SECOND_RANGE_ENABLED,
    AUX_PROG_SECOND_RANGE_END_HOUR,
    AUX_PROG_SECOND_RANGE_END_HOUR_CODE,
    AUX_PROG_SECOND_RANGE_START_HOUR,
    AUX_PROG_SECOND_RANGE_START_HOUR_CODE,
    AUX_PROG_THIRD_RANGE_ENABLED,
    AUX_PROG_THIRD_RANGE_END_HOUR,
    AUX_PROG_THIRD_RANGE_END_HOUR_CODE,
    AUX_PROG_THIRD_RANGE_START_HOUR,
    AUX_PROG_THIRD_RANGE_START_HOUR_CODE,
    AUX_PROG_WEEK_END_FIRST_RANGE_ENABLED,
    AUX_PROG_WEEK_END_FIRST_RANGE_END_HOUR,
    AUX_PROG_WEEK_END_FIRST_RANGE_END_HOUR_CODE,
    AUX_PROG_WEEK_END_FIRST_RANGE_START_HOUR,
    AUX_PROG_WEEK_END_FIRST_RANGE_START_HOUR_CODE,
    AUX_PROG_WEEK_END_MODE_ENABLED,
    AUX_PROG_WEEK_END_SECOND_RANGE_ENABLED,
    AUX_PROG_WEEK_END_SECOND_RANGE_END_HOUR,
    AUX_PROG_WEEK_END_SECOND_RANGE_END_HOUR_CODE,
    AUX_PROG_WEEK_END_SECOND_RANGE_START_HOUR,
    AUX_PROG_WEEK_END_SECOND_RANGE_START_HOUR_CODE,
    AUX_PROG_WEEK_END_THIRD_RANGE_ENABLED,
    AUX_PROG_WEEK_END_THIRD_RANGE_END_HOUR,
    AUX_PROG_WEEK_END_THIRD_RANGE_END_HOUR_CODE,
    AUX_PROG_WEEK_END_THIRD_RANGE_START_HOUR,
    AUX_PROG_WEEK_END_THIRD_RANGE_START_HOUR_CODE,
    BIN_BITS_CODE_FORMAT,
    COORDINATOR,
    DOMAIN,
    FIL_ENABLED,
    FIL_ENSLAVED_BY_LIGHT_ENABLED,
    FIL_PROG_ENABLED,
    FIL_PROG_FIRST_RANGE_ENABLED,
    FIL_PROG_FIRST_RANGE_END_HOUR,
    FIL_PROG_FIRST_RANGE_END_HOUR_CODE,
    FIL_PROG_FIRST_RANGE_START_HOUR,
    FIL_PROG_FIRST_RANGE_START_HOUR_CODE,
    FIL_PROG_SECOND_RANGE_ENABLED,
    FIL_PROG_SECOND_RANGE_END_HOUR,
    FIL_PROG_SECOND_RANGE_END_HOUR_CODE,
    FIL_PROG_SECOND_RANGE_START_HOUR,
    FIL_PROG_SECOND_RANGE_START_HOUR_CODE,
    FIL_PROG_THERMOREGULATED_ENABLED,
    FIL_PROG_THIRD_RANGE_ENABLED,
    FIL_PROG_THIRD_RANGE_END_HOUR,
    FIL_PROG_THIRD_RANGE_END_HOUR_CODE,
    FIL_PROG_THIRD_RANGE_START_HOUR,
    FIL_PROG_THIRD_RANGE_START_HOUR_CODE,
    FIL_PROG_WEEK_END_FIRST_RANGE_ENABLED,
    FIL_PROG_WEEK_END_FIRST_RANGE_END_HOUR,
    FIL_PROG_WEEK_END_FIRST_RANGE_END_HOUR_CODE,
    FIL_PROG_WEEK_END_FIRST_RANGE_START_HOUR,
    FIL_PROG_WEEK_END_FIRST_RANGE_START_HOUR_CODE,
    FIL_PROG_WEEK_END_MODE_ENABLED,
    FIL_PROG_WEEK_END_SECOND_RANGE_ENABLED,
    FIL_PROG_WEEK_END_SECOND_RANGE_END_HOUR,
    FIL_PROG_WEEK_END_SECOND_RANGE_END_HOUR_CODE,
    FIL_PROG_WEEK_END_SECOND_RANGE_START_HOUR,
    FIL_PROG_WEEK_END_SECOND_RANGE_START_HOUR_CODE,
    FIL_PROG_WEEK_END_THIRD_RANGE_ENABLED,
    FIL_PROG_WEEK_END_THIRD_RANGE_END_HOUR,
    FIL_PROG_WEEK_END_THIRD_RANGE_END_HOUR_CODE,
    FIL_PROG_WEEK_END_THIRD_RANGE_START_HOUR,
    FIL_PROG_WEEK_END_THIRD_RANGE_START_HOUR_CODE,
    HOUR_CODES,
    LIGHT_COLOR,
    LIGHT_COLOR_CODE,
    LIGHT_COLORS_CODES,
    LIGHT_ENABLED,
    LIGHT_INTENSITY,
    LIGHT_INTENSITY_CODE,
    LIGHT_INTENSITY_CODES,
    LIGHT_PROG_DURATION,
    LIGHT_PROG_DURATION_CODE,
    LIGHT_PROG_DUSK_MODE_ENABLED,
    LIGHT_PROG_START_HOUR,
    LIGHT_PROG_START_HOUR_CODE,
    LIGHT_PROG_STATUS,
    LIGHT_PROG_STATUS_CODE,
    LIGHT_PROG_STATUS_CODES,
    LIGHT_PROG_WEEK_END_DURATION,
    LIGHT_PROG_WEEK_END_DURATION_CODE,
    LIGHT_PROG_WEEK_END_MODE_ENABLED,
    LIGHT_PROG_WEEK_END_START_HOUR,
    LIGHT_PROG_WEEK_END_START_HOUR_CODE,
    LIGHT_SEQUENCE_SPEED,
    LIGHT_SEQUENCE_SPEED_CODE,
    LIGHT_SEQUENCE_SPEED_CODES,
    LIGHT_TIMER_DURATION,
    LIGHT_TIMER_DURATION_CODE,
    OFF,
    ON,
    ON_OFF_CODES,
    PROG_RANGE_DURATION_WITH_OFF_CODES,
    RAW_DATA,
    SYSTEM_DATE,
    SYSTEM_DATE_DAY,
    SYSTEM_DATE_HOUR,
    SYSTEM_DATE_MINUTE,
    SYSTEM_DATE_MONTH,
    SYSTEM_DATE_YEAR,
    SYSTEM_HOST,
    WATER_RAW_TEMPERATURE,
    WATER_TEMPERATURE,
    WATER_TEMPERATURE_OFFSET,
    WATER_TEMPERATURE_OFFSET_CODE,
    WATER_TEMPERATURE_OFFSET_CODES,
)

LOGGER = logging.getLogger(__name__)

IDENTIFIED_PROPERTIES_POSITIONS = {
    SYSTEM_DATE_YEAR: [132, 133],
    SYSTEM_DATE_MONTH: [130, 131],
    SYSTEM_DATE_DAY: [128, 129],
    SYSTEM_DATE_HOUR: [124, 125],
    SYSTEM_DATE_MINUTE: [122, 123],
    LIGHT_COLOR_CODE: [64, 65],
    LIGHT_INTENSITY_CODE: [71],
    WATER_TEMPERATURE: [66, 67],
    WATER_TEMPERATURE_OFFSET_CODE: [155],
    LIGHT_TIMER_DURATION_CODE: [72, 73],
    LIGHT_PROG_START_HOUR_CODE: [24, 25],
    LIGHT_PROG_DURATION_CODE: [26, 27],
    FIL_PROG_FIRST_RANGE_START_HOUR_CODE: [0, 1],
    FIL_PROG_FIRST_RANGE_END_HOUR_CODE: [2, 3],
    FIL_PROG_SECOND_RANGE_START_HOUR_CODE: [4, 5],
    FIL_PROG_SECOND_RANGE_END_HOUR_CODE: [6, 7],
    FIL_PROG_THIRD_RANGE_START_HOUR_CODE: [8, 9],
    FIL_PROG_THIRD_RANGE_END_HOUR_CODE: [10, 11],
    FIL_PROG_WEEK_END_FIRST_RANGE_START_HOUR_CODE: [12, 13],
    FIL_PROG_WEEK_END_FIRST_RANGE_END_HOUR_CODE: [14, 15],
    FIL_PROG_WEEK_END_SECOND_RANGE_START_HOUR_CODE: [16, 17],
    FIL_PROG_WEEK_END_SECOND_RANGE_END_HOUR_CODE: [18, 19],
    FIL_PROG_WEEK_END_THIRD_RANGE_START_HOUR_CODE: [20, 21],
    FIL_PROG_WEEK_END_THIRD_RANGE_END_HOUR_CODE: [22, 23],
    AUX_PROG_FIRST_RANGE_START_HOUR_CODE: [40, 41],
    AUX_PROG_FIRST_RANGE_END_HOUR_CODE: [42, 43],
    AUX_PROG_SECOND_RANGE_START_HOUR_CODE: [44, 45],
    AUX_PROG_SECOND_RANGE_END_HOUR_CODE: [46, 47],
    AUX_PROG_THIRD_RANGE_START_HOUR_CODE: [48, 49],
    AUX_PROG_THIRD_RANGE_END_HOUR_CODE: [50, 51],
    AUX_PROG_WEEK_END_FIRST_RANGE_START_HOUR_CODE: [52, 53],
    AUX_PROG_WEEK_END_FIRST_RANGE_END_HOUR_CODE: [54, 55],
    AUX_PROG_WEEK_END_SECOND_RANGE_START_HOUR_CODE: [56, 57],
    AUX_PROG_WEEK_END_SECOND_RANGE_END_HOUR_CODE: [58, 59],
    AUX_PROG_WEEK_END_THIRD_RANGE_START_HOUR_CODE: [60, 61],
    AUX_PROG_WEEK_END_THIRD_RANGE_END_HOUR_CODE: [62, 63],
}

IDENTIFIED_PROPERTIES_BIN_POSITIONS = {
    71: {
        LIGHT_INTENSITY_CODE: [0, 1],
        LIGHT_PROG_STATUS_CODE: [2, 3],
    },
}

# Toggleable binary bits
TOGGLEABLES_BIN_BITS = {
    33: [
        None,
        None,
        FIL_ENSLAVED_BY_LIGHT_ENABLED,
        FIL_ENABLED,
    ],
    68: [
        None,
        None,
        AUX_PROG_WEEK_END_MODE_ENABLED,
        FIL_PROG_WEEK_END_MODE_ENABLED,
    ],
    69: [
        LIGHT_PROG_WEEK_END_MODE_ENABLED,
        AUX_PROG_ENABLED,
        FIL_PROG_THERMOREGULATED_ENABLED,
        FIL_PROG_ENABLED,
    ],
    70: [
        LIGHT_PROG_DUSK_MODE_ENABLED,
        LIGHT_ENABLED,
        None,
        None,
    ],
    92: [
        None,
        None,
        AUX_PROG_WEEK_END_THIRD_RANGE_ENABLED,
        AUX_PROG_WEEK_END_SECOND_RANGE_ENABLED,
    ],
    93: [
        AUX_PROG_WEEK_END_FIRST_RANGE_ENABLED,
        AUX_PROG_THIRD_RANGE_ENABLED,
        AUX_PROG_SECOND_RANGE_ENABLED,
        AUX_PROG_FIRST_RANGE_ENABLED,
    ],
    119: [
        FIL_PROG_WEEK_END_FIRST_RANGE_ENABLED,
        FIL_PROG_THIRD_RANGE_ENABLED,
        FIL_PROG_SECOND_RANGE_ENABLED,
        FIL_PROG_FIRST_RANGE_ENABLED,
    ],
}

GET_SENSORS_DATA_MESSAGE = "Begin"

PROPERTIES_MESSAGE_KEY = {
    WATER_TEMPERATURE_OFFSET_CODE: "toft",  # water temperature offset code
    FIL_ENSLAVED_BY_LIGHT_ENABLED: "cmff",  # 0 or 1
    LIGHT_ENABLED: "sprj",  # 0 or 1
    LIGHT_COLOR_CODE: "prcn",  # color code
    LIGHT_INTENSITY_CODE: "plum",  # 0, 1, 2 or 3
    LIGHT_SEQUENCE_SPEED_CODE: "pspd",  # 0, 1 or 2
    LIGHT_PROG_STATUS_CODE: "mprj",  # 0 = off, 1 = prog or 2 = timer
    LIGHT_TIMER_DURATION_CODE: "pret",  # duration code or 255 = OFF
    LIGHT_PROG_DUSK_MODE_ENABLED: "aprj",  # 0 or 1
    LIGHT_PROG_WEEK_END_MODE_ENABLED: "mprw",  # 0 or 1
    LIGHT_PROG_START_HOUR_CODE: "prjs",  # hour code
    LIGHT_PROG_DURATION_CODE: "prjl",  # duration code or 255 = OFF
    LIGHT_PROG_WEEK_END_START_HOUR_CODE: "prws",  # hour code
    LIGHT_PROG_WEEK_END_DURATION_CODE: "prwl",  # duration code or 255 = OFF
    FIL_ENABLED: "sfil",  # 0 or 1
    FIL_PROG_ENABLED: "mfil",  # 0 or 1
    FIL_PROG_THERMOREGULATED_ENABLED: "afil",  # 0 or 1
    FIL_PROG_WEEK_END_MODE_ENABLED: "mpfw",  # 0 or 1
    FIL_PROG_FIRST_RANGE_ENABLED: "fip1",  # 0 or 1
    FIL_PROG_FIRST_RANGE_START_HOUR_CODE: "fis1",  # hour code
    FIL_PROG_FIRST_RANGE_END_HOUR_CODE: "fie1",  # hour code
    FIL_PROG_SECOND_RANGE_ENABLED: "fip2",  # 0 or 1
    FIL_PROG_SECOND_RANGE_START_HOUR_CODE: "fis2",  # hour code
    FIL_PROG_SECOND_RANGE_END_HOUR_CODE: "fie2",  # hour code
    FIL_PROG_THIRD_RANGE_ENABLED: "fip3",  # 0 or 1
    FIL_PROG_THIRD_RANGE_START_HOUR_CODE: "fis3",  # hour code
    FIL_PROG_THIRD_RANGE_END_HOUR_CODE: "fie3",  # hour code
    FIL_PROG_WEEK_END_FIRST_RANGE_ENABLED: "fwp1",  # 0 or 1
    FIL_PROG_WEEK_END_FIRST_RANGE_START_HOUR_CODE: "fws1",  # hour code
    FIL_PROG_WEEK_END_FIRST_RANGE_END_HOUR_CODE: "fwe1",  # hour code
    FIL_PROG_WEEK_END_SECOND_RANGE_ENABLED: "fwp1",  # 0 or 1
    FIL_PROG_WEEK_END_SECOND_RANGE_START_HOUR_CODE: "fws2",  # hour code
    FIL_PROG_WEEK_END_SECOND_RANGE_END_HOUR_CODE: "fwe2",  # hour code
    FIL_PROG_WEEK_END_THIRD_RANGE_ENABLED: "fwp3",  # 0 or 1
    FIL_PROG_WEEK_END_THIRD_RANGE_START_HOUR_CODE: "fws3",  # hour code
    FIL_PROG_WEEK_END_THIRD_RANGE_END_HOUR_CODE: "fwe3",  # hour code
    AUX_PROG_ENABLED: "maux",  # 0 or 1
    AUX_PROG_WEEK_END_MODE_ENABLED: "mapw",  # 0 or 1
    AUX_PROG_FIRST_RANGE_ENABLED: "axp1",  # 0 or 1
    AUX_PROG_FIRST_RANGE_START_HOUR_CODE: "axs1",  # hour code
    AUX_PROG_FIRST_RANGE_END_HOUR_CODE: "axe1",  # hour code
    AUX_PROG_SECOND_RANGE_ENABLED: "axp2",  # 0 or 1
    AUX_PROG_SECOND_RANGE_START_HOUR_CODE: "axs2",  # hour code
    AUX_PROG_SECOND_RANGE_END_HOUR_CODE: "axe2",  # hour code
    AUX_PROG_THIRD_RANGE_ENABLED: "axp3",  # 0 or 1
    AUX_PROG_THIRD_RANGE_START_HOUR_CODE: "axs3",  # hour code
    AUX_PROG_THIRD_RANGE_END_HOUR_CODE: "axe3",  # hour code
    AUX_PROG_WEEK_END_FIRST_RANGE_ENABLED: "awp1",  # 0 or 1
    AUX_PROG_WEEK_END_FIRST_RANGE_START_HOUR_CODE: "aws1",  # hour code
    AUX_PROG_WEEK_END_FIRST_RANGE_END_HOUR_CODE: "awe1",  # hour code
    AUX_PROG_WEEK_END_SECOND_RANGE_ENABLED: "awp2",  # 0 or 1
    AUX_PROG_WEEK_END_SECOND_RANGE_START_HOUR_CODE: "aws2",  # hour code
    AUX_PROG_WEEK_END_SECOND_RANGE_END_HOUR_CODE: "awe2",  # hour code
    AUX_PROG_WEEK_END_THIRD_RANGE_ENABLED: "awp3",  # 0 or 1
    AUX_PROG_WEEK_END_THIRD_RANGE_START_HOUR_CODE: "aws3",  # hour code
    AUX_PROG_WEEK_END_THIRD_RANGE_END_HOUR_CODE: "awe3",  # hour code
}

PROPERTIES_CODES = {
    WATER_TEMPERATURE_OFFSET_CODE: WATER_TEMPERATURE_OFFSET_CODES,  # water temperature offset code
    FIL_ENSLAVED_BY_LIGHT_ENABLED: ON_OFF_CODES,  # 0 or 1
    LIGHT_ENABLED: ON_OFF_CODES,  # 0 or 1
    LIGHT_COLOR_CODE: LIGHT_COLORS_CODES,  # color code
    LIGHT_INTENSITY_CODE: LIGHT_INTENSITY_CODES,  # 0, 1, 2 or 3
    LIGHT_SEQUENCE_SPEED_CODE: LIGHT_SEQUENCE_SPEED_CODES,  # 0, 1 or 2
    LIGHT_PROG_STATUS_CODE: LIGHT_PROG_STATUS_CODES,  # 0 = off, 1 = prog or 2 = timer
    LIGHT_TIMER_DURATION_CODE: PROG_RANGE_DURATION_WITH_OFF_CODES,  # duration code or 255 = OFF
    LIGHT_PROG_DUSK_MODE_ENABLED: ON_OFF_CODES,  # 0 or 1
    LIGHT_PROG_WEEK_END_MODE_ENABLED: ON_OFF_CODES,  # 0 or 1
    LIGHT_PROG_START_HOUR_CODE: HOUR_CODES,  # hour code
    LIGHT_PROG_DURATION_CODE: PROG_RANGE_DURATION_WITH_OFF_CODES,  # duration code or 255 = OFF
    LIGHT_PROG_WEEK_END_START_HOUR_CODE: HOUR_CODES,  # hour code
    LIGHT_PROG_WEEK_END_DURATION_CODE: PROG_RANGE_DURATION_WITH_OFF_CODES,  # dur. code or 255 = OFF
    FIL_ENABLED: ON_OFF_CODES,  # 0 or 1
    FIL_PROG_ENABLED: ON_OFF_CODES,  # 0 or 1
    FIL_PROG_THERMOREGULATED_ENABLED: ON_OFF_CODES,  # 0 or 1
    FIL_PROG_WEEK_END_MODE_ENABLED: ON_OFF_CODES,  # 0 or 1
    FIL_PROG_FIRST_RANGE_ENABLED: ON_OFF_CODES,  # 0 or 1
    FIL_PROG_FIRST_RANGE_START_HOUR_CODE: HOUR_CODES,  # hour code
    FIL_PROG_FIRST_RANGE_END_HOUR_CODE: HOUR_CODES,  # hour code
    FIL_PROG_SECOND_RANGE_ENABLED: ON_OFF_CODES,  # 0 or 1
    FIL_PROG_SECOND_RANGE_START_HOUR_CODE: HOUR_CODES,  # hour code
    FIL_PROG_SECOND_RANGE_END_HOUR_CODE: HOUR_CODES,  # hour code
    FIL_PROG_THIRD_RANGE_ENABLED: ON_OFF_CODES,  # 0 or 1
    FIL_PROG_THIRD_RANGE_START_HOUR_CODE: HOUR_CODES,  # hour code
    FIL_PROG_THIRD_RANGE_END_HOUR_CODE: HOUR_CODES,  # hour code
    FIL_PROG_WEEK_END_FIRST_RANGE_ENABLED: ON_OFF_CODES,  # 0 or 1
    FIL_PROG_WEEK_END_FIRST_RANGE_START_HOUR_CODE: HOUR_CODES,  # hour code
    FIL_PROG_WEEK_END_FIRST_RANGE_END_HOUR_CODE: HOUR_CODES,  # hour code
    FIL_PROG_WEEK_END_SECOND_RANGE_ENABLED: ON_OFF_CODES,  # 0 or 1
    FIL_PROG_WEEK_END_SECOND_RANGE_START_HOUR_CODE: HOUR_CODES,  # hour code
    FIL_PROG_WEEK_END_SECOND_RANGE_END_HOUR_CODE: HOUR_CODES,  # hour code
    FIL_PROG_WEEK_END_THIRD_RANGE_ENABLED: ON_OFF_CODES,  # 0 or 1
    FIL_PROG_WEEK_END_THIRD_RANGE_START_HOUR_CODE: HOUR_CODES,  # hour code
    FIL_PROG_WEEK_END_THIRD_RANGE_END_HOUR_CODE: HOUR_CODES,  # hour code
    AUX_PROG_ENABLED: ON_OFF_CODES,  # 0 or 1
    AUX_PROG_WEEK_END_MODE_ENABLED: ON_OFF_CODES,  # 0 or 1
    AUX_PROG_FIRST_RANGE_ENABLED: ON_OFF_CODES,  # 0 or 1
    AUX_PROG_WEEK_END_MODE_ENABLED: ON_OFF_CODES,  # 0 or 1
    AUX_PROG_FIRST_RANGE_ENABLED: ON_OFF_CODES,  # 0 or 1
    AUX_PROG_FIRST_RANGE_START_HOUR_CODE: HOUR_CODES,  # hour code
    AUX_PROG_FIRST_RANGE_END_HOUR_CODE: HOUR_CODES,  # hour code
    AUX_PROG_SECOND_RANGE_ENABLED: ON_OFF_CODES,  # 0 or 1
    AUX_PROG_SECOND_RANGE_START_HOUR_CODE: HOUR_CODES,  # hour code
    AUX_PROG_SECOND_RANGE_END_HOUR_CODE: HOUR_CODES,  # hour code
    AUX_PROG_THIRD_RANGE_ENABLED: ON_OFF_CODES,  # 0 or 1
    AUX_PROG_THIRD_RANGE_START_HOUR_CODE: HOUR_CODES,  # hour code
    AUX_PROG_THIRD_RANGE_END_HOUR_CODE: HOUR_CODES,  # hour code
    AUX_PROG_WEEK_END_FIRST_RANGE_ENABLED: ON_OFF_CODES,  # 0 or 1
    AUX_PROG_WEEK_END_FIRST_RANGE_START_HOUR_CODE: HOUR_CODES,  # hour code
    AUX_PROG_WEEK_END_FIRST_RANGE_END_HOUR_CODE: HOUR_CODES,  # hour code
    AUX_PROG_WEEK_END_SECOND_RANGE_ENABLED: ON_OFF_CODES,  # 0 or 1
    AUX_PROG_WEEK_END_SECOND_RANGE_START_HOUR_CODE: HOUR_CODES,  # hour code
    AUX_PROG_WEEK_END_SECOND_RANGE_END_HOUR_CODE: HOUR_CODES,  # hour code
    AUX_PROG_WEEK_END_THIRD_RANGE_ENABLED: ON_OFF_CODES,  # 0 or 1
    AUX_PROG_WEEK_END_THIRD_RANGE_START_HOUR_CODE: HOUR_CODES,  # hour code
    AUX_PROG_WEEK_END_THIRD_RANGE_END_HOUR_CODE: HOUR_CODES,  # hour code
}

DEDUCED_PROPERTIES = {
    WATER_TEMPERATURE_OFFSET: WATER_TEMPERATURE_OFFSET_CODE,
    LIGHT_COLOR: LIGHT_COLOR_CODE,
    LIGHT_INTENSITY: LIGHT_INTENSITY_CODE,
    LIGHT_SEQUENCE_SPEED: LIGHT_SEQUENCE_SPEED_CODE,
    LIGHT_PROG_STATUS: LIGHT_PROG_STATUS_CODE,
    LIGHT_TIMER_DURATION: LIGHT_TIMER_DURATION_CODE,
    LIGHT_PROG_START_HOUR: LIGHT_PROG_START_HOUR_CODE,
    LIGHT_PROG_DURATION: LIGHT_PROG_DURATION_CODE,
    LIGHT_PROG_WEEK_END_START_HOUR: LIGHT_PROG_WEEK_END_START_HOUR_CODE,
    LIGHT_PROG_WEEK_END_DURATION: LIGHT_PROG_WEEK_END_DURATION_CODE,
    FIL_PROG_FIRST_RANGE_START_HOUR: FIL_PROG_FIRST_RANGE_START_HOUR_CODE,
    FIL_PROG_FIRST_RANGE_END_HOUR: FIL_PROG_FIRST_RANGE_END_HOUR_CODE,
    FIL_PROG_SECOND_RANGE_START_HOUR: FIL_PROG_SECOND_RANGE_START_HOUR_CODE,
    FIL_PROG_SECOND_RANGE_END_HOUR: FIL_PROG_SECOND_RANGE_END_HOUR_CODE,
    FIL_PROG_THIRD_RANGE_START_HOUR: FIL_PROG_THIRD_RANGE_START_HOUR_CODE,
    FIL_PROG_THIRD_RANGE_END_HOUR: FIL_PROG_THIRD_RANGE_END_HOUR_CODE,
    FIL_PROG_WEEK_END_FIRST_RANGE_START_HOUR: FIL_PROG_WEEK_END_FIRST_RANGE_START_HOUR_CODE,
    FIL_PROG_WEEK_END_FIRST_RANGE_END_HOUR: (FIL_PROG_WEEK_END_FIRST_RANGE_END_HOUR_CODE),
    FIL_PROG_WEEK_END_SECOND_RANGE_START_HOUR: (FIL_PROG_WEEK_END_SECOND_RANGE_START_HOUR_CODE),
    FIL_PROG_WEEK_END_SECOND_RANGE_END_HOUR: (FIL_PROG_WEEK_END_SECOND_RANGE_END_HOUR_CODE),
    FIL_PROG_WEEK_END_THIRD_RANGE_START_HOUR: (FIL_PROG_WEEK_END_THIRD_RANGE_START_HOUR_CODE),
    FIL_PROG_WEEK_END_THIRD_RANGE_END_HOUR: (FIL_PROG_WEEK_END_THIRD_RANGE_END_HOUR_CODE),
    AUX_PROG_FIRST_RANGE_START_HOUR: AUX_PROG_FIRST_RANGE_START_HOUR_CODE,
    AUX_PROG_FIRST_RANGE_END_HOUR: AUX_PROG_FIRST_RANGE_END_HOUR_CODE,
    AUX_PROG_SECOND_RANGE_START_HOUR: AUX_PROG_SECOND_RANGE_START_HOUR_CODE,
    AUX_PROG_SECOND_RANGE_END_HOUR: AUX_PROG_SECOND_RANGE_END_HOUR_CODE,
    AUX_PROG_THIRD_RANGE_START_HOUR: AUX_PROG_THIRD_RANGE_START_HOUR_CODE,
    AUX_PROG_THIRD_RANGE_END_HOUR: AUX_PROG_THIRD_RANGE_END_HOUR_CODE,
    AUX_PROG_WEEK_END_FIRST_RANGE_START_HOUR: AUX_PROG_WEEK_END_FIRST_RANGE_START_HOUR_CODE,
    AUX_PROG_WEEK_END_FIRST_RANGE_END_HOUR: AUX_PROG_WEEK_END_FIRST_RANGE_END_HOUR_CODE,
    AUX_PROG_WEEK_END_SECOND_RANGE_START_HOUR: AUX_PROG_WEEK_END_SECOND_RANGE_START_HOUR_CODE,
    AUX_PROG_WEEK_END_SECOND_RANGE_END_HOUR: AUX_PROG_WEEK_END_SECOND_RANGE_END_HOUR_CODE,
    AUX_PROG_WEEK_END_THIRD_RANGE_START_HOUR: AUX_PROG_WEEK_END_THIRD_RANGE_START_HOUR_CODE,
    AUX_PROG_WEEK_END_THIRD_RANGE_END_HOUR: AUX_PROG_WEEK_END_THIRD_RANGE_END_HOUR_CODE,
}

PROPERTIES_RAW_VALUE = [
    SYSTEM_DATE_YEAR,
    SYSTEM_DATE_MONTH,
    SYSTEM_DATE_DAY,
    SYSTEM_DATE_HOUR,
    SYSTEM_DATE_MINUTE,
]


def int16():
    """Convert integer base 16 on integer base 10"""


def parse_sensors_data(data, system_host=None):
    """Parse sensors state data"""
    # Limit to last 160 characters to handle case when multiple state data strings are sent by the
    # Tild after requesting action
    LOGGER.debug("Raw data received: %s", data)
    data = data[-160:] if len(data) > 160 else data

    # Compute initial state from idendified properties positions
    state = {
        key: "".join(map(lambda x: data[x], pos))
        for key, pos in IDENTIFIED_PROPERTIES_POSITIONS.items()
    }

    # Convert properties values to integer base 10 (expect properties with raw value)
    state = {
        prop: value if prop in PROPERTIES_RAW_VALUE else int(value, 16)
        for prop, value in state.items()
    }

    # Compute system data
    state[SYSTEM_DATE] = datetime(
        year=int(state[SYSTEM_DATE_YEAR]) + 2000,
        month=int(state[SYSTEM_DATE_MONTH]),
        day=int(state[SYSTEM_DATE_DAY]),
        hour=int(state[SYSTEM_DATE_HOUR]),
        minute=int(state[SYSTEM_DATE_MINUTE]),
    ).isoformat()

    # Remove raw date parts
    for prop in [
        SYSTEM_DATE_YEAR,
        SYSTEM_DATE_MONTH,
        SYSTEM_DATE_DAY,
        SYSTEM_DATE_HOUR,
        SYSTEM_DATE_MINUTE,
    ]:
        del state[prop]

    # Compute binary properties state
    for bit, properties in IDENTIFIED_PROPERTIES_BIN_POSITIONS.items():
        bit_key = BIN_BITS_CODE_FORMAT.format(bit)
        state[bit_key] = BitArray(hex=f"0x{data[bit]}").bin
        LOGGER.debug("Binary properties bit %d = %s (%s)", bit, data[bit], state[bit_key])
        for prop, pos in properties.items():
            # pylint: disable=cell-var-from-loop
            bin_value = "".join(map(lambda x: state[bit_key][x], pos))
            state[prop] = int(bin_value, 2)
            LOGGER.debug("- property %s = %s (%s)", prop, state[prop], bin_value)

    # Compute toggleables state
    for bit, properties in TOGGLEABLES_BIN_BITS.items():
        bit_key = BIN_BITS_CODE_FORMAT.format(bit)
        state[bit_key] = BitArray(hex=f"0x{data[bit]}").bin
        # LOGGER.debug("Toggleables bit %d = %s (%s)", bit, data[bit], state[bit_key])
        for idx, prop in enumerate(properties):
            if not prop:
                # LOGGER.debug("Toggleables bit %d / property %d: unknown", bit, idx)
                continue
            state[prop] = ON if int(state[bit_key][idx]) else OFF
            # LOGGER.debug(
            #     "Toggleables bit %d / property %d = %s: %s => %s",
            #     bit,
            #     idx,
            #     prop,
            #     state[bit_key][idx],
            #     state[prop],
            # )

    # Compute deduced properties
    for prop, code_prop in DEDUCED_PROPERTIES.items():
        state[prop] = (
            PROPERTIES_CODES[code_prop].get(state[code_prop]) if code_prop in state else None
        )

    # Compute water raw temperature
    state[WATER_RAW_TEMPERATURE] = (
        state[WATER_TEMPERATURE] - state[WATER_TEMPERATURE_OFFSET]
        if state[WATER_TEMPERATURE_OFFSET] is not None
        else None
    )

    # Add raw data
    state[RAW_DATA] = data
    state[SYSTEM_HOST] = system_host

    # Add None state for non-idendified properties
    for prop in PROPERTIES_CODES:
        if prop not in state:
            state[prop] = None

    return state


def diff_sensors_data(ref_raw_data, *other_raw_data):
    """Compute differences between sensors data strings"""
    ref_parsed_data = parse_sensors_data(ref_raw_data)

    # Detect differences
    result = {
        "ref_raw_data": ref_raw_data,
        "identified_pos": {p: k for k, pos in IDENTIFIED_PROPERTIES_POSITIONS.items() for p in pos},
        "parsed_data": {ref_raw_data: ref_parsed_data},
        "diff": {},
        "diff_keys": {},
    }
    for raw_data in other_raw_data:
        data = list(raw_data)
        result["parsed_data"][raw_data] = parse_sensors_data(raw_data)
        for idx, char in enumerate(list(ref_raw_data)):
            if char == data[idx]:
                continue
            result["diff"][idx] = (
                (result["diff"][idx] + [data[idx]]) if idx in result["diff"] else [char, data[idx]]
            )

        for k, v in ref_parsed_data.items():
            if result["parsed_data"][raw_data][k] == v:
                continue
            result["diff_keys"][k] = (
                (result["diff_keys"][k] + [result["parsed_data"][raw_data][k]])
                if k in result["diff_keys"]
                else [v, result["parsed_data"][raw_data][k]]
            )
    result["identified_pos"] = dict(sorted(result["identified_pos"].items()))
    result["diff"] = dict(sorted(result["diff"].items()))
    result["diff_keys"] = dict(sorted(result["diff_keys"].items()))

    result["identified_pos_diff"] = [
        pos for pos in sorted(result["diff"]) if pos in result["identified_pos"]
    ]
    result["non_identified_pos_diff"] = [
        pos for pos in sorted(result["diff"]) if pos not in result["identified_pos"]
    ]
    return result


def log_sensors_data_diff(ref_raw_data, *other_raw_data):
    """Detect and log sensors data differences"""
    diff = diff_sensors_data(ref_raw_data, *other_raw_data)
    msg = [f"New data: {raw_data}" for raw_data in other_raw_data]
    msg.insert(0, f"Reference data: {ref_raw_data}")
    diff_msg = []
    if diff["identified_pos_diff"]:
        diff_msg.append(
            "Raw idendified position differences:\n"
            + "\n".join(
                [
                    f" - {idx} ({diff['identified_pos'][idx]}, {' => '.join(diff['diff'][idx])})"
                    for idx in diff["identified_pos_diff"]
                ]
            )
        )
    if diff["non_identified_pos_diff"]:
        diff_msg.append(
            "Raw non-idendified position differences:\n"
            + "\n".join(
                [
                    f" - {idx} ({' => '.join(diff['diff'][idx])})"
                    for idx in diff["non_identified_pos_diff"]
                ]
            )
        )

    if diff["diff_keys"]:
        diff_msg.append(
            "Keys differences:\n"
            + "\n".join(
                [
                    f" - {key} ({' => '.join([str(value) for value in values])})"
                    for key, values in diff["diff_keys"].items()
                ]
            )
        )

    LOGGER.debug(
        "Differences:%s",
        " No deteted differences" if not diff_msg else ("\n" + "\n".join(diff_msg)),
    )


class CceiTildClient:
    """CCEI Tild client"""

    host = None
    port = None
    encoding = "utf8"

    last_sensors_data = None

    def __init__(self, hass, host, port=None):
        self.hass = hass
        self.host = host
        self.port = int(port) if port else 30302
        LOGGER.debug("Instanciate Tild client on %s:%d", self.host, self.port)

    @staticmethod
    def discover_host():
        """Try to discover host"""
        sock_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock_udp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock_udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock_udp.settimeout(10)

        server = None
        name = None
        try:
            sock_udp.sendto(b"D", ("255.255.255.255", 30303))
            data, server = sock_udp.recvfrom(256)
            name = data.decode("UTF-8")
        finally:
            sock_udp.close()
        return (str(server[0]) if server else None, name if name else None)

    async def _call_tild(self, message, awaiting_answser=True):
        """Call tild"""
        message = json.dumps(message) if isinstance(message, dict) else message
        LOGGER.debug("Start connection to tcp://%s:%d...", self.host, self.port)
        reader, writer = await asyncio.open_connection(self.host, self.port)
        LOGGER.debug("Connection established")
        try:
            LOGGER.debug(
                "Send message '%s' and awaiting answer..."
                if awaiting_answser
                else "Send message '%s' without awaiting answer...",
                message,
            )
            writer.write(message.encode(self.encoding))
            if not awaiting_answser:
                return True
            data = await reader.read(256)
            data = data.decode(self.encoding)
            LOGGER.debug("Answer received: %s", data)
            return data
        finally:
            writer.close()
        return False

    async def get_sensors_data(self):
        """Async retrieve sensors state data"""
        return await self._get_sensors_data()

    async def _get_sensors_data(self):
        """Retrieve sensors state data"""
        LOGGER.debug("Call Tild for sensors data")
        data = await self._call_tild(GET_SENSORS_DATA_MESSAGE)
        if not data:
            LOGGER.debug("No data received from Tild for sensors data")
            return False
        LOGGER.debug("Parse answer and compute state")
        state = parse_sensors_data(data, self.host)
        LOGGER.debug(
            "State:%s",
            "\n - {}".format("\n - ".join([f"{key}={state[key]}" for key in sorted(state)])),
        )
        self.log_sensors_data_diff(state)
        return state

    def log_sensors_data_diff(self, new_data):
        """Log sensors data change differences"""
        if not new_data:
            return
        if self.last_sensors_data:
            log_sensors_data_diff(self.last_sensors_data[RAW_DATA], new_data[RAW_DATA])
        self.last_sensors_data = new_data

    async def set_property_state(self, prop, state, prop_is_state=False):
        """Set property on Tild"""
        if prop not in PROPERTIES_MESSAGE_KEY:
            raise NotImplementedError(f"No message key known for property {prop}.")
        if state in PROPERTIES_CODES[prop]:
            code = state
            state = PROPERTIES_CODES[prop][state]
        else:
            assert state in PROPERTIES_CODES[prop].values(), f"Invalid {prop} '{state}'"
            idx = list(PROPERTIES_CODES[prop].values()).index(state)
            code = list(PROPERTIES_CODES[prop].keys())[idx]
        await self._call_tild({PROPERTIES_MESSAGE_KEY[prop]: code})
        await asyncio.sleep(1)
        sensors_data = await self.get_sensors_data()
        if not sensors_data:
            LOGGER.error(
                "Fail to parse sensors data after setting %s to %s (%s)",
                prop,
                state,
                code,
            )
            return False
        # Log new sensors data and update it in coordinator data
        self.log_sensors_data_diff(sensors_data)
        self.hass.data[DOMAIN][COORDINATOR].async_set_updated_sensors_data(sensors_data)
        return True
        # pylint: disable=unreachable
        if (prop_is_state and sensors_data[prop] == state) or (
            not prop_is_state and sensors_data[prop] == code
        ):
            return True
        LOGGER.error("Fail to set %s to %s (%s)", prop, state, code)
        return False


class FakeTildBox:
    """Fake Tild box"""

    host = "0.0.0.0"
    port = 30302
    sock = None

    toggleable_properties = [
        prop for bit, properties in TOGGLEABLES_BIN_BITS.items() for prop in properties
    ]

    message_key_to_property = {
        message_key: prop for prop, message_key in PROPERTIES_MESSAGE_KEY.items()
    }

    def __init__(self, host=None, port=None):
        if host:
            self.host = host
        if port:
            self.port = port if port is int else int(port)
        print(f"Start fake Tild service on {self.host}:{self.port}")

        # Initialize properties state
        self.properties_state = {
            prop: random.choice(list(codes.keys())) for prop, codes in PROPERTIES_CODES.items()
        }
        self.properties_state[WATER_TEMPERATURE] = random.randrange(20, 30)
        print(
            "Properties initialized:\n"
            + (
                "\n".join(
                    [
                        f"- {item}: {PROPERTIES_CODES[item][self.properties_state[item]]} "
                        f"({self.properties_state[item]})"
                        if item in PROPERTIES_CODES
                        else f"- {item}: {self.properties_state[item]}"
                        for item in sorted(self.properties_state)
                    ]
                )
            )
        )

    def get_state_data(self):
        """Generate state data string"""
        # Water temperature evolution
        self.properties_state[WATER_TEMPERATURE] += random.choice([-1, 0, 1])
        now = datetime.now()

        properties = {
            SYSTEM_DATE_YEAR: f"{now.year-2000:02}",
            SYSTEM_DATE_MONTH: f"{now.month:02}",
            SYSTEM_DATE_DAY: f"{now.day:02}",
            SYSTEM_DATE_HOUR: f"{now.hour:02}",
            SYSTEM_DATE_MINUTE: f"{now.minute:02}",
        }

        data = ["0" for idx in range(1, 160)]  # pylint: disable=unused-variable

        for prop, pos in IDENTIFIED_PROPERTIES_POSITIONS.items():
            if prop in self.toggleable_properties:
                continue
            if prop in self.properties_state:
                data[pos[0] : pos[-1] + 1] = list(
                    f"{self.properties_state[prop]:02x}"
                    if len(pos) == 2
                    else f"{self.properties_state[prop]:x}"
                )
                continue
            assert (
                prop in properties
            ), f"Property {prop} identified on position {','.join(map(str, pos))} is not provided"
            data[pos[0] : pos[-1] + 1] = list(properties[prop])

        for bit, properties in IDENTIFIED_PROPERTIES_BIN_POSITIONS.items():
            print(f"Computing binary properties bit {bit}:")
            bin_status_code = ["0", "0", "0", "0"]
            for prop, pos in properties.items():
                bin_code = f"{self.properties_state[prop]:02b}"
                bin_status_code[pos[0] : pos[-1] + 1] = list(bin_code)
                print(f"- {prop}: {bin_code} ({self.properties_state[prop]})")
            bin_status_code = "".join(bin_status_code)

            data[bit] = f"{int(bin_status_code, 2):x}".upper()
            print(f" => binary properties bit {bit} = {data[bit]} ({bin_status_code})")

        for bit, properties in TOGGLEABLES_BIN_BITS.items():
            print(f"Computing toggleables bit {bit}:")
            bin_status_code = ["0", "0", "0", "0"]
            for idx, prop in enumerate(properties):
                if prop is None:
                    print(f"- {idx}: unknown => 0")
                    continue
                print(f"- {idx}: {prop}: {self.properties_state[prop]}")
                bin_status_code[idx] = str(self.properties_state[prop])
            bin_status_code = "".join(bin_status_code)

            data[bit] = BitArray(bin=bin_status_code).hex
            print(f" => toggleables bit {bit} = {data[bit]} ({bin_status_code})")

        return "".join(data)

    def handle_set_property_request(self, connection, address, code, prop):
        """Handle a request to set an Tild property"""
        print(f"Handle set {prop} request to '{code}' from {address[0]}:{address[1]}")
        if code not in PROPERTIES_CODES[prop]:
            print(f"Invalid {prop} code '{code}'")
            connection.send(f"ERROR: Invalid {prop} code '{code}'".encode())
        else:
            print(f"{prop} set to {PROPERTIES_CODES[prop][code]} ({code})")
            self.properties_state[prop] = code
            connection.send(self.get_state_data().encode("utf8"))

    def run(self):
        """Run service"""
        print(f"Fake Tild service on {self.host}:{self.port} is running")
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.sock.listen(5)

        while True:
            connection, address = self.sock.accept()
            message = connection.recv(1024).decode("utf-8").strip()
            if message == GET_SENSORS_DATA_MESSAGE:
                print(f"Handle a {GET_SENSORS_DATA_MESSAGE} request from {address[0]}:{address[1]}")
                connection.send(self.get_state_data().encode("utf8"))
            else:
                try:
                    message = json.loads(message)
                    if not isinstance(message, dict):
                        raise ValueError("Unexpected JSON message, must be a dict")
                except json.decoder.JSONDecodeError:
                    print(f"Fail to decode JSON message '{message}' from {address[0]}:{address[1]}")
                    connection.send(b"ERROR: fail to decode JSON message")
                    connection.close()
                    continue
                except ValueError:
                    print(f"Unexpected JSON message '{message}' from {address[0]}:{address[1]}")
                    connection.send(b"ERROR: unexcepected JSON message")
                    connection.close()
                    continue

                for key, value in message.items():
                    if key in self.message_key_to_property:
                        self.handle_set_property_request(
                            connection, address, value, self.message_key_to_property[key]
                        )
                    else:
                        print(
                            f"Handle unknown JSON message key '{key}' => '{value}' request from "
                            f"{address[0]}:{address[1]}: '{message}'"
                        )
                        connection.send(
                            f"ERROR: unknown JSON message key '{key}' => '{value}' request".encode()
                        )

                    connection.send(b"ERROR: unknown JSON request")
            print(f"Close connection from {address[0]}:{address[1]}")
            connection.close()
