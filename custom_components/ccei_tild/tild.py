"""CCEI Tild client"""
import asyncio
import json
import logging
import random
import socket
from datetime import datetime

from .const import (
    AUX_PROG_FIRST_RANGE_END_HOUR_CODE,
    AUX_PROG_FIRST_RANGE_START_HOUR_CODE,
    AUX_PROG_FIRST_RANGE_STATUS_ENABLED,
    AUX_PROG_SECOND_RANGE_END_HOUR_CODE,
    AUX_PROG_SECOND_RANGE_START_HOUR_CODE,
    AUX_PROG_SECOND_RANGE_STATUS_ENABLED,
    AUX_PROG_STATUS_ENABLED,
    AUX_PROG_THIRD_RANGE_END_HOUR_CODE,
    AUX_PROG_THIRD_RANGE_START_HOUR_CODE,
    AUX_PROG_THIRD_RANGE_STATUS_ENABLED,
    AUX_PROG_WEEK_END_FIRST_RANGE_END_HOUR_CODE,
    AUX_PROG_WEEK_END_FIRST_RANGE_START_HOUR_CODE,
    AUX_PROG_WEEK_END_FIRST_RANGE_STATUS_ENABLED,
    AUX_PROG_WEEK_END_MODE_STATUS_ENABLED,
    AUX_PROG_WEEK_END_SECOND_RANGE_END_HOUR_CODE,
    AUX_PROG_WEEK_END_SECOND_RANGE_START_HOUR_CODE,
    AUX_PROG_WEEK_END_SECOND_RANGE_STATUS_ENABLED,
    AUX_PROG_WEEK_END_THIRD_RANGE_END_HOUR_CODE,
    AUX_PROG_WEEK_END_THIRD_RANGE_START_HOUR_CODE,
    AUX_PROG_WEEK_END_THIRD_RANGE_STATUS_ENABLED,
    COORDINATOR,
    DOMAIN,
    DURATION_CODES,
    FILTRATION_ENABLED,
    FILTRATION_ENABLED_BY_LIGHT,
    FILTRATION_PROG_FIRST_RANGE_END_HOUR_CODE,
    FILTRATION_PROG_FIRST_RANGE_START_HOUR_CODE,
    FILTRATION_PROG_FIRST_RANGE_STATUS_ENABLED,
    FILTRATION_PROG_SECOND_RANGE_END_HOUR_CODE,
    FILTRATION_PROG_SECOND_RANGE_START_HOUR_CODE,
    FILTRATION_PROG_SECOND_RANGE_STATUS_ENABLED,
    FILTRATION_PROG_STATUS_ENABLED,
    FILTRATION_PROG_THERMOREGULATED_STATUS_ENABLED,
    FILTRATION_PROG_THIRD_RANGE_END_HOUR_CODE,
    FILTRATION_PROG_THIRD_RANGE_START_HOUR_CODE,
    FILTRATION_PROG_THIRD_RANGE_STATUS_ENABLED,
    FILTRATION_PROG_WEEK_END_FIRST_RANGE_END_HOUR_CODE,
    FILTRATION_PROG_WEEK_END_FIRST_RANGE_START_HOUR_CODE,
    FILTRATION_PROG_WEEK_END_FIRST_RANGE_STATUS_ENABLED,
    FILTRATION_PROG_WEEK_END_SECOND_RANGE_END_HOUR_CODE,
    FILTRATION_PROG_WEEK_END_SECOND_RANGE_START_HOUR_CODE,
    FILTRATION_PROG_WEEK_END_SECOND_RANGE_STATUS_ENABLED,
    FILTRATION_PROG_WEEK_END_STATUS_ENABLED,
    FILTRATION_PROG_WEEK_END_THIRD_RANGE_END_HOUR_CODE,
    FILTRATION_PROG_WEEK_END_THIRD_RANGE_START_HOUR_CODE,
    FILTRATION_PROG_WEEK_END_THIRD_RANGE_STATUS_ENABLED,
    FILTRATION_STATUS_CODE,
    HOUR_CODES,
    LIGHT_COLOR,
    LIGHT_COLOR_CODE,
    LIGHT_COLORS_CODES,
    LIGHT_ENABLED,
    LIGHT_INTENSITY,
    LIGHT_INTENSITY_CODE,
    LIGHT_INTENSITY_CODES,
    LIGHT_INTENSITY_CODES_TO_SEND,
    LIGHT_PROG_DURATION_CODE,
    LIGHT_PROG_MODE_DUSK_ENABLED,
    LIGHT_PROG_START_HOUR_CODE,
    LIGHT_PROG_STATUS_CODE,
    LIGHT_PROG_STATUS_CODES,
    LIGHT_PROG_WEEK_END_DURATION_CODE,
    LIGHT_PROG_WEEK_END_MODE_ENABLED,
    LIGHT_PROG_WEEK_END_START_HOUR_CODE,
    LIGHT_SEQUENCE_SPEED_CODE,
    LIGHT_SEQUENCE_SPEED_CODES,
    LIGHT_STATUS_CODE,
    LIGHT_TIMER_DURATION,
    LIGHT_TIMER_DURATION_CODE,
    OFF,
    ON,
    PROG_RANGE_DURATION_WITH_OFF_CODES,
    RAW_DATA,
    SYSTEM_DATE,
    SYSTEM_DATE_DAY,
    SYSTEM_DATE_HOUR,
    SYSTEM_DATE_MINUTE,
    SYSTEM_DATE_MONTH,
    SYSTEM_DATE_YEAR,
    SYSTEM_HOST,
    THERMOREGULATED_FILTRATION_CODE,
    THERMOREGULATED_FILTRATION_ENABLED,
    TREATMENT_ENABLED,
    TREATMENT_STATUS_CODE,
    WATER_RAW_TEMPERATURE,
    WATER_TEMPERATURE,
    WATER_TEMPERATURE_OFFSET,
    WATER_TEMPERATURE_OFFSET_CODE,
    WATER_TEMPERATURE_OFFSET_CODES,
)

LOGGER = logging.getLogger(__name__)

LIGHT_STATUS_CODES = {"4": ON, "0": OFF}
FILTRATION_STATUS_CODES = {"1": ON, "0": OFF, "3": ON}  # 3 = enslave to light
FILTRATION_ENABLED_BY_LIGHT_CODE = "3"
TREATMENT_STATUS_CODES = {"7": ON, "3": OFF}

IDENTIFIED_FIELDS = {
    SYSTEM_DATE_YEAR: [132, 133],
    SYSTEM_DATE_MONTH: [130, 131],
    SYSTEM_DATE_DAY: [128, 129],
    SYSTEM_DATE_HOUR: [124, 125],
    SYSTEM_DATE_MINUTE: [122, 123],
    LIGHT_STATUS_CODE: [70],
    LIGHT_COLOR_CODE: [64, 65],
    LIGHT_INTENSITY_CODE: [71],
    WATER_TEMPERATURE: [66, 67],
    WATER_TEMPERATURE_OFFSET_CODE: [155],
    FILTRATION_STATUS_CODE: [33],
    TREATMENT_STATUS_CODE: [69],
    LIGHT_TIMER_DURATION_CODE: [72, 73],
}

GET_SENSORS_DATA_MESSAGE = "Begin"

SET_WATER_TEMPERATURE_OFFSET_MESSAGE_KEY = "toft"  # water temperature offset code
SET_FORCE_FILTRATION_WITH_LIGHT_STATUS_MESSAGE_KEY = "cmff"  # 0 or 1

SET_LIGHT_STATUS_MESSAGE_KEY = "sprj"  # 0 or 1
SET_LIGHT_COLOR_MESSAGE_KEY = "prcn"  # color code
SET_LIGHT_INTENSITY_MESSAGE_KEY = "plum"  # 0, 1, 2 or 3
SET_LIGHT_SEQUENCE_SPEED_MESSAGE_KEY = "pspd"  # 0, 1 or 2

SET_LIGHT_PROG_STATUS_MESSAGE_KEY = "mprj"  # 0 = off, 1 = prog or 2 = timer
SET_LIGHT_TIMER_DURATION_MESSAGE_KEY = "pret"  # duration code or 255 = OFF
SET_LIGHT_PROG_MODE_DUSK_MESSAGE_KEY = "aprj"  # 0 or 1
SET_LIGHT_PROG_WEEK_END_MODE_MESSAGE_KEY = "mprw"  # 0 or 1
SET_LIGHT_PROG_START_HOUR_MESSAGE_KEY = "prjs"  # hour code
SET_LIGHT_PROG_DURATION_MESSAGE_KEY = "prjl"  # duration code or 255 = OFF
SET_LIGHT_PROG_WEEK_END_START_HOUR_MESSAGE_KEY = "prws"  # hour code
SET_LIGHT_PROG_WEEK_END_DURATION_MESSAGE_KEY = "prwl"  # duration code or 255 = OFF

SET_FILTRATION_STATUS_MESSAGE_KEY = "sfil"  # 0 or 1
SET_FILTRATION_PROG_STATUS_MESSAGE_KEY = "mfil"  # 0 or 1
SET_FILTRATION_PROG_THERMOREGULATED_STATUS_MESSAGE_KEY = "afil"  # 0 or 1
SET_FILTRATION_PROG_WEEK_END_STATUS_MESSAGE_KEY = "mpfw"  # 0 or 1

SET_FILTRATION_PROG_FIRST_RANGE_STATUS_MESSAGE_KEY = "fip1"  # 0 or 1
SET_FILTRATION_PROG_FIRST_RANGE_START_HOUR_MESSAGE_KEY = "fis1"  # hour code
SET_FILTRATION_PROG_FIRST_RANGE_END_HOUR_MESSAGE_KEY = "fie1"  # hour code
SET_FILTRATION_PROG_SECOND_RANGE_STATUS_MESSAGE_KEY = "fip2"  # 0 or 1
SET_FILTRATION_PROG_SECOND_RANGE_START_HOUR_MESSAGE_KEY = "fis2"  # hour code
SET_FILTRATION_PROG_SECOND_RANGE_END_HOUR_MESSAGE_KEY = "fie2"  # hour code
SET_FILTRATION_PROG_THIRD_RANGE_STATUS_MESSAGE_KEY = "fip3"  # 0 or 1
SET_FILTRATION_PROG_THIRD_RANGE_START_HOUR_MESSAGE_KEY = "fis3"  # hour code
SET_FILTRATION_PROG_THIRD_RANGE_END_HOUR_MESSAGE_KEY = "fie3"  # hour code

SET_FILTRATION_PROG_WEEK_END_FIRST_RANGE_STATUS_MESSAGE_KEY = "fwp1"  # 0 or 1
SET_FILTRATION_PROG_WEEK_END_FIRST_RANGE_START_HOUR_MESSAGE_KEY = "fws1"  # hour code
SET_FILTRATION_PROG_WEEK_END_FIRST_RANGE_END_HOUR_MESSAGE_KEY = "fwe1"  # hour code
SET_FILTRATION_PROG_WEEK_END_SECOND_RANGE_STATUS_MESSAGE_KEY = "fwp1"  # 0 or 1
SET_FILTRATION_PROG_WEEK_END_SECOND_RANGE_START_HOUR_MESSAGE_KEY = "fws1"  # hour code
SET_FILTRATION_PROG_WEEK_END_SECOND_RANGE_END_HOUR_MESSAGE_KEY = "fwe1"  # hour code
SET_FILTRATION_PROG_WEEK_END_THIRD_RANGE_STATUS_MESSAGE_KEY = "fwp1"  # 0 or 1
SET_FILTRATION_PROG_WEEK_END_THIRD_RANGE_START_HOUR_MESSAGE_KEY = "fws1"  # hour code
SET_FILTRATION_PROG_WEEK_END_THIRD_RANGE_END_HOUR_MESSAGE_KEY = "fwe1"  # hour code

SET_AUX_PROG_STATUS_MESSAGE_KEY = "maux"  # 0 or 1
SET_AUX_PROG_WEEK_END_MODE_STATUS_MESSAGE_KEY = "maux"  # 0 or 1
SET_AUX_PROG_FIRST_RANGE_STATUS_MESSAGE_KEY = "axp1"  # 0 or 1
SET_AUX_PROG_FIRST_RANGE_START_HOUR_MESSAGE_KEY = "axs1"  # hour code
SET_AUX_PROG_FIRST_RANGE_END_HOUR_MESSAGE_KEY = "axe1"  # hour code
SET_AUX_PROG_SECOND_RANGE_STATUS_MESSAGE_KEY = "axp2"  # 0 or 1
SET_AUX_PROG_SECOND_RANGE_START_HOUR_MESSAGE_KEY = "axs2"  # hour code
SET_AUX_PROG_SECOND_RANGE_END_HOUR_MESSAGE_KEY = "axe2"  # hour code
SET_AUX_PROG_THIRD_RANGE_STATUS_MESSAGE_KEY = "axp3"  # 0 or 1
SET_AUX_PROG_THIRD_RANGE_START_HOUR_MESSAGE_KEY = "axs3"  # hour code
SET_AUX_PROG_THIRD_RANGE_END_HOUR_MESSAGE_KEY = "axe3"  # hour code

SET_AUX_PROG_WEEK_END_FIRST_RANGE_STATUS_MESSAGE_KEY = "awp1"  # 0 or 1
SET_AUX_PROG_WEEK_END_FIRST_RANGE_START_HOUR_MESSAGE_KEY = "aws1"  # hour code
SET_AUX_PROG_WEEK_END_FIRST_RANGE_END_HOUR_MESSAGE_KEY = "awe1"  # hour code
SET_AUX_PROG_WEEK_END_SECOND_RANGE_STATUS_MESSAGE_KEY = "awp2"  # 0 or 1
SET_AUX_PROG_WEEK_END_SECOND_RANGE_START_HOUR_MESSAGE_KEY = "aws2"  # hour code
SET_AUX_PROG_WEEK_END_SECOND_RANGE_END_HOUR_MESSAGE_KEY = "awe2"  # hour code
SET_AUX_PROG_WEEK_END_THIRD_RANGE_STATUS_MESSAGE_KEY = "awp3"  # 0 or 1
SET_AUX_PROG_WEEK_END_THIRD_RANGE_START_HOUR_MESSAGE_KEY = "aws3"  # hour code
SET_AUX_PROG_WEEK_END_THIRD_RANGE_END_HOUR_MESSAGE_KEY = "awe3"  # hour code


def parse_sensors_data(data, system_host=None):
    """Parse sensors state data"""
    # Limit to last 160 characters to handle case when multiple state data strings are sent by the
    # Tild after requesting action
    LOGGER.debug("Raw data received: %s", data)
    data = data[-160:] if len(data) > 160 else data

    state = {RAW_DATA: data, SYSTEM_HOST: system_host}
    for key, fields in IDENTIFIED_FIELDS.items():
        state[key] = "".join(map(lambda x: data[x], fields))

    state[SYSTEM_DATE] = datetime(
        year=int(state[SYSTEM_DATE_YEAR]) + 2000,
        month=int(state[SYSTEM_DATE_MONTH]),
        day=int(state[SYSTEM_DATE_DAY]),
        hour=int(state[SYSTEM_DATE_HOUR]),
        minute=int(state[SYSTEM_DATE_MINUTE]),
    ).isoformat()

    for field in [
        SYSTEM_DATE_YEAR,
        SYSTEM_DATE_MONTH,
        SYSTEM_DATE_DAY,
        SYSTEM_DATE_HOUR,
        SYSTEM_DATE_MINUTE,
    ]:
        del state[field]

    state[WATER_TEMPERATURE] = int(state[WATER_TEMPERATURE], 16)
    state[LIGHT_ENABLED] = LIGHT_STATUS_CODES.get(state[LIGHT_STATUS_CODE])
    state[TREATMENT_ENABLED] = TREATMENT_STATUS_CODES.get(state[TREATMENT_STATUS_CODE])
    state[FILTRATION_ENABLED] = FILTRATION_STATUS_CODES.get(state[FILTRATION_STATUS_CODE])
    state[FILTRATION_ENABLED_BY_LIGHT] = FILTRATION_STATUS_CODE == FILTRATION_ENABLED_BY_LIGHT_CODE
    state[WATER_TEMPERATURE_OFFSET] = WATER_TEMPERATURE_OFFSET_CODES.get(
        int(state[WATER_TEMPERATURE_OFFSET_CODE])
    )
    state[WATER_RAW_TEMPERATURE] = (
        state[WATER_TEMPERATURE] - state[WATER_TEMPERATURE_OFFSET]
        if state[WATER_TEMPERATURE_OFFSET] is not None
        else None
    )
    state[LIGHT_COLOR] = LIGHT_COLORS_CODES.get(int(state[LIGHT_COLOR_CODE], 16))
    state[LIGHT_INTENSITY] = LIGHT_INTENSITY_CODES.get(state[LIGHT_INTENSITY_CODE])
    state[THERMOREGULATED_FILTRATION_CODE] = state[THERMOREGULATED_FILTRATION_ENABLED] = None
    state[LIGHT_TIMER_DURATION] = DURATION_CODES.get(int(state[LIGHT_TIMER_DURATION_CODE], 16))
    return state


def diff_sensors_data(ref_raw_data, *other_raw_data):
    """Compute differences between sensors data strings"""
    ref_parsed_data = parse_sensors_data(ref_raw_data)

    # Detect differences
    result = {
        "ref_raw_data": ref_raw_data,
        "identified_pos": {p: k for k, pos in IDENTIFIED_FIELDS.items() for p in pos},
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
            "\n - {}".format("\n - ".join([f"{key}={value}" for key, value in state.items()])),
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

    async def toggle_light(self, state=None):
        """Turn on/off the Tild light"""
        return await self._toggle_item_state(
            label="light",
            sensor_key=LIGHT_ENABLED,
            message_key=SET_LIGHT_STATUS_MESSAGE_KEY,
            state=state,
        )

    async def toggle_filtration(self, state=None):
        """Turn on/off the Tild filtration"""
        return await self._toggle_item_state(
            label="filtration",
            sensor_key=FILTRATION_ENABLED,
            message_key=SET_FILTRATION_STATUS_MESSAGE_KEY,
            state=state,
        )

    async def toggle_thermoregulated_filtration(self, state=None):
        """Turn on/off the Tild thermoregulated filtration"""
        return await self._toggle_item_state(
            label="thermoregulated filtration",
            sensor_key=THERMOREGULATED_FILTRATION_ENABLED,
            message_key=SET_FILTRATION_PROG_THERMOREGULATED_STATUS_MESSAGE_KEY,
            state=state,
        )

    async def set_light_color(self, color):
        """Set the light color"""
        return await self._set_item_state(
            label="light color",
            sensor_key=LIGHT_COLOR_CODE,
            state=color,
            codes=LIGHT_COLORS_CODES,
            message_key=SET_LIGHT_COLOR_MESSAGE_KEY,
        )

    async def set_light_intensity(self, intensity):
        """Set the light intensity"""
        return await self._set_item_state(
            label="light intensity",
            sensor_key=LIGHT_INTENSITY_CODE,
            state=intensity,
            codes=LIGHT_INTENSITY_CODES,
            codes_to_send=LIGHT_INTENSITY_CODES_TO_SEND,
            message_key=SET_LIGHT_INTENSITY_MESSAGE_KEY,
        )

    async def set_light_timer_duration(self, duration):
        """Set the light timer duration"""
        return await self._set_item_state(
            label="light timer duration",
            sensor_key=LIGHT_TIMER_DURATION_CODE,
            state=duration,
            codes=DURATION_CODES,
            message_key=SET_LIGHT_TIMER_DURATION_MESSAGE_KEY,
        )

    async def set_water_temperature_offset(self, offset):
        """Set the water temperature offset"""
        return await self._set_item_state(
            label="water temperature offset",
            sensor_key=WATER_TEMPERATURE_OFFSET_CODE,
            state=offset,
            codes=WATER_TEMPERATURE_OFFSET_CODES,
            message_key=SET_WATER_TEMPERATURE_OFFSET_MESSAGE_KEY,
        )

    async def set_light_prog_status(self, state):
        """Set the light programming status"""
        return await self._set_item_state(
            label="light programming status",
            sensor_key=LIGHT_PROG_STATUS_CODE,
            state=state,
            codes=LIGHT_PROG_STATUS_CODES,
            message_key=SET_LIGHT_PROG_STATUS_MESSAGE_KEY,
        )

    async def toggle_light_prog_mode_dusk(self, state=None):
        """Turn on/off the Tild light programming mode dusk"""
        return await self._toggle_item_state(
            label="light programming mode dusk",
            sensor_key=LIGHT_PROG_MODE_DUSK_ENABLED,
            message_key=SET_LIGHT_PROG_MODE_DUSK_MESSAGE_KEY,
            state=state,
        )

    async def toggle_light_prog_week_end_mode(self, state=None):
        """Turn on/off the Tild light programming mode week-end"""
        return await self._toggle_item_state(
            label="light programming mode week-end",
            sensor_key=LIGHT_PROG_WEEK_END_MODE_ENABLED,
            message_key=SET_LIGHT_PROG_WEEK_END_MODE_MESSAGE_KEY,
            state=state,
        )

    async def set_light_prog_start_hour(self, state):
        """Set the light programming start hour"""
        return await self._set_item_state(
            label="light programming start hour",
            sensor_key=LIGHT_PROG_START_HOUR_CODE,
            state=state,
            codes=HOUR_CODES,
            message_key=SET_LIGHT_PROG_START_HOUR_MESSAGE_KEY,
        )

    async def set_light_prog_duration(self, state):
        """Set the light programming duration"""
        return await self._set_item_state(
            label="light programming duration",
            sensor_key=LIGHT_PROG_DURATION_CODE,
            state=state,
            codes=PROG_RANGE_DURATION_WITH_OFF_CODES,
            message_key=SET_LIGHT_PROG_DURATION_MESSAGE_KEY,
        )

    async def set_light_prog_week_end_start_hour(self, state):
        """Set the light programming week-end start hour"""
        return await self._set_item_state(
            label="light programming week-end start hour",
            sensor_key=LIGHT_PROG_WEEK_END_START_HOUR_CODE,
            state=state,
            codes=HOUR_CODES,
            message_key=SET_LIGHT_PROG_WEEK_END_START_HOUR_MESSAGE_KEY,
        )

    async def set_light_prog_week_end_duration(self, state):
        """Set the light programming week-end duration"""
        return await self._set_item_state(
            label="light programming week-end duration",
            sensor_key=LIGHT_PROG_WEEK_END_DURATION_CODE,
            state=state,
            codes=PROG_RANGE_DURATION_WITH_OFF_CODES,
            message_key=SET_LIGHT_PROG_WEEK_END_DURATION_MESSAGE_KEY,
        )

    async def set_light_sequence_speed(self, state):
        """Set the light sequence speed"""
        return await self._set_item_state(
            label="light sequence speed",
            sensor_key=LIGHT_SEQUENCE_SPEED_CODE,
            state=state,
            codes=LIGHT_SEQUENCE_SPEED_CODES,
            message_key=SET_LIGHT_SEQUENCE_SPEED_MESSAGE_KEY,
        )

    async def toggle_filtration_prog_status(self, state=None):
        """Turn on/off the Tild filtration programming"""
        return await self._toggle_item_state(
            label="filtration programming",
            sensor_key=FILTRATION_PROG_STATUS_ENABLED,
            message_key=SET_FILTRATION_PROG_STATUS_MESSAGE_KEY,
            state=state,
        )

    async def toggle_filtration_prog_thermoregulated_status(self, state=None):
        """Turn on/off the Tild filtration programming thermoregulated"""
        return await self._toggle_item_state(
            label="filtration programming thermoregulated",
            sensor_key=FILTRATION_PROG_THERMOREGULATED_STATUS_ENABLED,
            message_key=SET_FILTRATION_PROG_THERMOREGULATED_STATUS_MESSAGE_KEY,
            state=state,
        )

    async def toggle_filtration_prog_week_end_status(self, state=None):
        """Turn on/off the Tild filtration programming mode week-end"""
        return await self._toggle_item_state(
            label="filtration programming mode week-end",
            sensor_key=FILTRATION_PROG_WEEK_END_STATUS_ENABLED,
            message_key=SET_FILTRATION_PROG_WEEK_END_STATUS_MESSAGE_KEY,
            state=state,
        )

    async def toggle_filtration_prog_first_range_status(self, state=None):
        """Turn on/off the Tild filtration programming first range"""
        return await self._toggle_item_state(
            label="filtration programming first range",
            sensor_key=FILTRATION_PROG_FIRST_RANGE_STATUS_ENABLED,
            message_key=SET_FILTRATION_PROG_FIRST_RANGE_STATUS_MESSAGE_KEY,
            state=state,
        )

    async def set_filtration_prog_first_range_start_hour(self, state):
        """Set the filtration programming first range start hour"""
        return await self._set_item_state(
            label="filtration programming first range start hour",
            sensor_key=FILTRATION_PROG_FIRST_RANGE_START_HOUR_CODE,
            state=state,
            codes=HOUR_CODES,
            message_key=SET_FILTRATION_PROG_FIRST_RANGE_START_HOUR_MESSAGE_KEY,
        )

    async def set_filtration_prog_first_range_end_hour(self, state):
        """Set the filtration programming first range end hour"""
        return await self._set_item_state(
            label="filtration programming first range end hour",
            sensor_key=FILTRATION_PROG_FIRST_RANGE_END_HOUR_CODE,
            state=state,
            codes=HOUR_CODES,
            message_key=SET_FILTRATION_PROG_FIRST_RANGE_END_HOUR_MESSAGE_KEY,
        )

    async def toggle_filtration_prog_second_range_status(self, state=None):
        """Turn on/off the Tild filtration programming second range"""
        return await self._toggle_item_state(
            label="filtration programming second range",
            sensor_key=FILTRATION_PROG_SECOND_RANGE_STATUS_ENABLED,
            message_key=SET_FILTRATION_PROG_SECOND_RANGE_STATUS_MESSAGE_KEY,
            state=state,
        )

    async def set_filtration_prog_second_range_start_hour(self, state):
        """Set the filtration programming second range start hour"""
        return await self._set_item_state(
            label="filtration programming second range start hour",
            sensor_key=FILTRATION_PROG_SECOND_RANGE_START_HOUR_CODE,
            state=state,
            codes=HOUR_CODES,
            message_key=SET_FILTRATION_PROG_SECOND_RANGE_START_HOUR_MESSAGE_KEY,
        )

    async def set_filtration_prog_second_range_end_hour(self, state):
        """Set the filtration programming second range end hour"""
        return await self._set_item_state(
            label="filtration programming second range end hour",
            sensor_key=FILTRATION_PROG_SECOND_RANGE_END_HOUR_CODE,
            state=state,
            codes=HOUR_CODES,
            message_key=SET_FILTRATION_PROG_SECOND_RANGE_END_HOUR_MESSAGE_KEY,
        )

    async def toggle_filtration_prog_third_range_status(self, state=None):
        """Turn on/off the Tild filtration programming third range"""
        return await self._toggle_item_state(
            label="filtration programming third range",
            sensor_key=FILTRATION_PROG_THIRD_RANGE_STATUS_ENABLED,
            message_key=SET_FILTRATION_PROG_THIRD_RANGE_STATUS_MESSAGE_KEY,
            state=state,
        )

    async def set_filtration_prog_third_range_start_hour(self, state):
        """Set the filtration programming third range start hour"""
        return await self._set_item_state(
            label="filtration programming third range start hour",
            sensor_key=FILTRATION_PROG_THIRD_RANGE_START_HOUR_CODE,
            state=state,
            codes=HOUR_CODES,
            message_key=SET_FILTRATION_PROG_THIRD_RANGE_START_HOUR_MESSAGE_KEY,
        )

    async def set_filtration_prog_third_range_end_hour(self, state):
        """Set the filtration programming third range end hour"""
        return await self._set_item_state(
            label="filtration programming third range end hour",
            sensor_key=FILTRATION_PROG_THIRD_RANGE_END_HOUR_CODE,
            state=state,
            codes=HOUR_CODES,
            message_key=SET_FILTRATION_PROG_THIRD_RANGE_END_HOUR_MESSAGE_KEY,
        )

    async def toggle_filtration_prog_week_end_first_range_status(self, state=None):
        """Turn on/off the Tild filtration programming week-end first range"""
        return await self._toggle_item_state(
            label="filtration programming week-end first range",
            sensor_key=FILTRATION_PROG_WEEK_END_FIRST_RANGE_STATUS_ENABLED,
            message_key=SET_FILTRATION_PROG_WEEK_END_FIRST_RANGE_STATUS_MESSAGE_KEY,
            state=state,
        )

    async def set_filtration_prog_week_end_first_range_start_hour(self, state):
        """Set the filtration programming week-end first range start hour"""
        return await self._set_item_state(
            label="filtration programming week-end first range start hour",
            sensor_key=FILTRATION_PROG_WEEK_END_FIRST_RANGE_START_HOUR_CODE,
            state=state,
            codes=HOUR_CODES,
            message_key=SET_FILTRATION_PROG_WEEK_END_FIRST_RANGE_START_HOUR_MESSAGE_KEY,
        )

    async def set_filtration_prog_week_end_first_range_end_hour(self, state):
        """Set the filtration programming week-end first range end hour"""
        return await self._set_item_state(
            label="filtration programming week-end first range end hour",
            sensor_key=FILTRATION_PROG_WEEK_END_FIRST_RANGE_END_HOUR_CODE,
            state=state,
            codes=HOUR_CODES,
            message_key=SET_FILTRATION_PROG_WEEK_END_FIRST_RANGE_END_HOUR_MESSAGE_KEY,
        )

    async def toggle_filtration_prog_week_end_second_range_status(self, state=None):
        """Turn on/off the Tild filtration programming week-end second range"""
        return await self._toggle_item_state(
            label="filtration programming week-end second range",
            sensor_key=FILTRATION_PROG_WEEK_END_SECOND_RANGE_STATUS_ENABLED,
            message_key=SET_FILTRATION_PROG_WEEK_END_SECOND_RANGE_STATUS_MESSAGE_KEY,
            state=state,
        )

    async def set_filtration_prog_week_end_second_range_start_hour(self, state):
        """Set the filtration programming week-end second range start hour"""
        return await self._set_item_state(
            label="filtration programming week-end second range start hour",
            sensor_key=FILTRATION_PROG_WEEK_END_SECOND_RANGE_START_HOUR_CODE,
            state=state,
            codes=HOUR_CODES,
            message_key=SET_FILTRATION_PROG_WEEK_END_SECOND_RANGE_START_HOUR_MESSAGE_KEY,
        )

    async def set_filtration_prog_week_end_second_range_end_hour(self, state):
        """Set the filtration programming week-end second range end hour"""
        return await self._set_item_state(
            label="filtration programming week-end second range end hour",
            sensor_key=FILTRATION_PROG_WEEK_END_SECOND_RANGE_END_HOUR_CODE,
            state=state,
            codes=HOUR_CODES,
            message_key=SET_FILTRATION_PROG_WEEK_END_SECOND_RANGE_END_HOUR_MESSAGE_KEY,
        )

    async def toggle_filtration_prog_week_end_third_range_status(self, state=None):
        """Turn on/off the Tild filtration programming week-end third range"""
        return await self._toggle_item_state(
            label="filtration programming week-end third range",
            sensor_key=FILTRATION_PROG_WEEK_END_THIRD_RANGE_STATUS_ENABLED,
            message_key=SET_FILTRATION_PROG_WEEK_END_THIRD_RANGE_STATUS_MESSAGE_KEY,
            state=state,
        )

    async def set_filtration_prog_week_end_third_range_start_hour(self, state):
        """Set the filtration programming week-end third range start hour"""
        return await self._set_item_state(
            label="filtration programming week-end third range start hour",
            sensor_key=FILTRATION_PROG_WEEK_END_THIRD_RANGE_START_HOUR_CODE,
            state=state,
            codes=HOUR_CODES,
            message_key=SET_FILTRATION_PROG_WEEK_END_THIRD_RANGE_START_HOUR_MESSAGE_KEY,
        )

    async def set_filtration_prog_week_end_third_range_end_hour(self, state):
        """Set the filtration programming week-end third range end hour"""
        return await self._set_item_state(
            label="filtration programming week-end third range end hour",
            sensor_key=FILTRATION_PROG_WEEK_END_THIRD_RANGE_END_HOUR_CODE,
            state=state,
            codes=HOUR_CODES,
            message_key=SET_FILTRATION_PROG_WEEK_END_THIRD_RANGE_END_HOUR_MESSAGE_KEY,
        )

    async def toggle_aux_prog_status(self, state=None):
        """Turn on/off the Tild auxiliary programming"""
        return await self._toggle_item_state(
            label="auxiliary programming",
            sensor_key=AUX_PROG_STATUS_ENABLED,
            message_key=SET_AUX_PROG_STATUS_MESSAGE_KEY,
            state=state,
        )

    async def toggle_aux_prog_week_end_mode_status(self, state=None):
        """Turn on/off the Tild auxiliary programming week-end mode"""
        return await self._toggle_item_state(
            label="auxiliary programming week-end mode",
            sensor_key=AUX_PROG_WEEK_END_MODE_STATUS_ENABLED,
            message_key=SET_AUX_PROG_WEEK_END_MODE_STATUS_MESSAGE_KEY,
            state=state,
        )

    async def toggle_aux_prog_first_range_status(self, state=None):
        """Turn on/off the Tild auxiliary programming first range"""
        return await self._toggle_item_state(
            label="auxiliary programming first range",
            sensor_key=AUX_PROG_FIRST_RANGE_STATUS_ENABLED,
            message_key=SET_AUX_PROG_FIRST_RANGE_STATUS_MESSAGE_KEY,
            state=state,
        )

    async def set_aux_prog_first_range_start_hour(self, state):
        """Set the auxiliary programming first range start hour"""
        return await self._set_item_state(
            label="auxiliary programming first range start hour",
            sensor_key=AUX_PROG_FIRST_RANGE_START_HOUR_CODE,
            state=state,
            codes=HOUR_CODES,
            message_key=SET_AUX_PROG_FIRST_RANGE_START_HOUR_MESSAGE_KEY,
        )

    async def set_aux_prog_first_range_end_hour(self, state):
        """Set the auxiliary programming first range end hour"""
        return await self._set_item_state(
            label="auxiliary programming first range end hour",
            sensor_key=AUX_PROG_FIRST_RANGE_END_HOUR_CODE,
            state=state,
            codes=HOUR_CODES,
            message_key=SET_AUX_PROG_FIRST_RANGE_END_HOUR_MESSAGE_KEY,
        )

    async def toggle_aux_prog_second_range_status(self, state=None):
        """Turn on/off the Tild auxiliary programming second range"""
        return await self._toggle_item_state(
            label="auxiliary programming second range",
            sensor_key=AUX_PROG_SECOND_RANGE_STATUS_ENABLED,
            message_key=SET_AUX_PROG_SECOND_RANGE_STATUS_MESSAGE_KEY,
            state=state,
        )

    async def set_aux_prog_second_range_start_hour(self, state):
        """Set the auxiliary programming second range start hour"""
        return await self._set_item_state(
            label="auxiliary programming second range start hour",
            sensor_key=AUX_PROG_SECOND_RANGE_START_HOUR_CODE,
            state=state,
            codes=HOUR_CODES,
            message_key=SET_AUX_PROG_SECOND_RANGE_START_HOUR_MESSAGE_KEY,
        )

    async def set_aux_prog_second_range_end_hour(self, state):
        """Set the auxiliary programming second range end hour"""
        return await self._set_item_state(
            label="auxiliary programming second range end hour",
            sensor_key=AUX_PROG_SECOND_RANGE_END_HOUR_CODE,
            state=state,
            codes=HOUR_CODES,
            message_key=SET_AUX_PROG_SECOND_RANGE_END_HOUR_MESSAGE_KEY,
        )

    async def toggle_aux_prog_third_range_status(self, state=None):
        """Turn on/off the Tild auxiliary programming third range"""
        return await self._toggle_item_state(
            label="auxiliary programming third range",
            sensor_key=AUX_PROG_THIRD_RANGE_STATUS_ENABLED,
            message_key=SET_AUX_PROG_THIRD_RANGE_STATUS_MESSAGE_KEY,
            state=state,
        )

    async def set_aux_prog_third_range_start_hour(self, state):
        """Set the auxiliary programming third range start hour"""
        return await self._set_item_state(
            label="auxiliary programming third range start hour",
            sensor_key=AUX_PROG_THIRD_RANGE_START_HOUR_CODE,
            state=state,
            codes=HOUR_CODES,
            message_key=SET_AUX_PROG_THIRD_RANGE_START_HOUR_MESSAGE_KEY,
        )

    async def set_aux_prog_third_range_end_hour(self, state):
        """Set the auxiliary programming third range end hour"""
        return await self._set_item_state(
            label="auxiliary programming third range end hour",
            sensor_key=AUX_PROG_THIRD_RANGE_END_HOUR_CODE,
            state=state,
            codes=HOUR_CODES,
            message_key=SET_AUX_PROG_THIRD_RANGE_END_HOUR_MESSAGE_KEY,
        )

    async def toggle_aux_prog_week_end_first_range_status(self, state=None):
        """Turn on/off the Tild auxiliary programming week-end first range"""
        return await self._toggle_item_state(
            label="auxiliary programming week-end first range",
            sensor_key=AUX_PROG_WEEK_END_FIRST_RANGE_STATUS_ENABLED,
            message_key=SET_AUX_PROG_WEEK_END_FIRST_RANGE_STATUS_MESSAGE_KEY,
            state=state,
        )

    async def set_aux_prog_week_end_first_range_start_hour(self, state):
        """Set the auxiliary programming week-end first range start hour"""
        return await self._set_item_state(
            label="auxiliary programming week-end first range start hour",
            sensor_key=AUX_PROG_WEEK_END_FIRST_RANGE_START_HOUR_CODE,
            state=state,
            codes=HOUR_CODES,
            message_key=SET_AUX_PROG_WEEK_END_FIRST_RANGE_START_HOUR_MESSAGE_KEY,
        )

    async def set_aux_prog_week_end_first_range_end_hour(self, state):
        """Set the auxiliary programming week-end first range end hour"""
        return await self._set_item_state(
            label="auxiliary programming week-end first range end hour",
            sensor_key=AUX_PROG_WEEK_END_FIRST_RANGE_END_HOUR_CODE,
            state=state,
            codes=HOUR_CODES,
            message_key=SET_AUX_PROG_WEEK_END_FIRST_RANGE_END_HOUR_MESSAGE_KEY,
        )

    async def toggle_aux_prog_week_end_second_range_status(self, state=None):
        """Turn on/off the Tild auxiliary programming week-end second range"""
        return await self._toggle_item_state(
            label="auxiliary programming week-end second range",
            sensor_key=AUX_PROG_WEEK_END_SECOND_RANGE_STATUS_ENABLED,
            message_key=SET_AUX_PROG_WEEK_END_SECOND_RANGE_STATUS_MESSAGE_KEY,
            state=state,
        )

    async def set_aux_prog_week_end_second_range_start_hour(self, state):
        """Set the auxiliary programming week-end second range start hour"""
        return await self._set_item_state(
            label="auxiliary programming week-end second range start hour",
            sensor_key=AUX_PROG_WEEK_END_SECOND_RANGE_START_HOUR_CODE,
            state=state,
            codes=HOUR_CODES,
            message_key=SET_AUX_PROG_WEEK_END_SECOND_RANGE_START_HOUR_MESSAGE_KEY,
        )

    async def set_aux_prog_week_end_second_range_end_hour(self, state):
        """Set the auxiliary programming week-end second range end hour"""
        return await self._set_item_state(
            label="auxiliary programming week-end second range end hour",
            sensor_key=AUX_PROG_WEEK_END_SECOND_RANGE_END_HOUR_CODE,
            state=state,
            codes=HOUR_CODES,
            message_key=SET_AUX_PROG_WEEK_END_SECOND_RANGE_END_HOUR_MESSAGE_KEY,
        )

    async def toggle_aux_prog_week_end_third_range_status(self, state=None):
        """Turn on/off the Tild auxiliary programming week-end third range"""
        return await self._toggle_item_state(
            label="auxiliary programming week-end third range",
            sensor_key=AUX_PROG_WEEK_END_THIRD_RANGE_STATUS_ENABLED,
            message_key=SET_AUX_PROG_WEEK_END_THIRD_RANGE_STATUS_MESSAGE_KEY,
            state=state,
        )

    async def set_aux_prog_week_end_third_range_start_hour(self, state):
        """Set the auxiliary programming week-end third range start hour"""
        return await self._set_item_state(
            label="auxiliary programming week-end third range start hour",
            sensor_key=AUX_PROG_WEEK_END_THIRD_RANGE_START_HOUR_CODE,
            state=state,
            codes=HOUR_CODES,
            message_key=SET_AUX_PROG_WEEK_END_THIRD_RANGE_START_HOUR_MESSAGE_KEY,
        )

    async def set_aux_prog_week_end_third_range_end_hour(self, state):
        """Set the auxiliary programming week-end third range end hour"""
        return await self._set_item_state(
            label="auxiliary programming week-end third range end hour",
            sensor_key=AUX_PROG_WEEK_END_THIRD_RANGE_END_HOUR_CODE,
            state=state,
            codes=HOUR_CODES,
            message_key=SET_AUX_PROG_WEEK_END_THIRD_RANGE_END_HOUR_MESSAGE_KEY,
        )

    async def _set_item_state(
        self,
        label,
        sensor_key,
        state,
        codes,
        message_key,
        sensor_key_is_state=False,
        codes_to_send=None,
    ):
        """Set item on Tild"""
        if state in codes:
            code = state
            state = codes[state]
        else:
            assert state in codes.values(), f"Invalid {label} '{state}'"
            idx = list(codes.values()).index(state)
            code = list(codes.keys())[idx]
        if codes_to_send:
            assert state in codes_to_send, f"Unknown code to send for state '{state}' of {label}"
            code_to_send = codes_to_send[state]
        else:
            code_to_send = code
        await self._call_tild({message_key: code_to_send})
        await asyncio.sleep(1)
        sensors_data = await self.get_sensors_data()
        if not sensors_data:
            LOGGER.error(
                "Fail to parse sensors data after setting %s to %s (%s)",
                label,
                state,
                code,
            )
            return False
        # Update coordinator data
        self._update_coordinator_sensors_data(sensors_data)
        return True
        # pylint: disable=unreachable
        if (sensor_key_is_state and sensors_data[sensor_key] == state) or (
            not sensor_key_is_state and sensors_data[sensor_key] == code
        ):
            return True
        LOGGER.error("Fail to set %s to %s (%s)", label, state, code)
        return False

    async def _toggle_item_state(self, label, sensor_key, message_key, state=None):
        """Turn on/off an item on Tild"""
        if state is None:
            LOGGER.debug("Ask for toogling the %s, call Tild to retreive it current state", label)
            if not self.last_sensors_data:
                sensors_data = await self.get_sensors_data()
                if not sensors_data:
                    LOGGER.warning("Fail to retreive current %s state, cant't toggling it.", label)
                    return False
            state = ON if sensors_data[sensor_key] else OFF
        assert state in [ON, OFF], f"Invalid {label} state '{state}'"
        LOGGER.debug("Call Tild to turn %s the %s", state, label)
        return await self._set_item_state(label, sensor_key, state, {1: ON, 0: OFF}, message_key)

    def _update_coordinator_sensors_data(self, sensors_data):
        """Update coordinator data after some Tild action"""
        self.log_sensors_data_diff(sensors_data)
        self.hass.data[DOMAIN][COORDINATOR].async_set_updated_sensors_data(sensors_data)


class FakeTildBox:
    """Fake Tild box"""

    host = "0.0.0.0"
    port = 30302
    sock = None

    def __init__(self, host=None, port=None):
        if host:
            self.host = host
        if port:
            self.port = port if port is int else int(port)

        self.light_state = random.choice([ON, OFF])
        self.light_color_code = random.choice(list(LIGHT_COLORS_CODES.keys()))
        self.light_intensity_code = random.choice(list(LIGHT_INTENSITY_CODES.keys()))
        self.light_timer_duration_code = random.choice(list(DURATION_CODES.keys()))
        self.filtration_state = random.choice([ON, OFF])
        self.thermoregulated_filtration_state = random.choice([ON, OFF])
        self.water_temperature = random.randrange(20, 30)
        self.water_temperature_offset_code = random.choice(list(WATER_TEMPERATURE_OFFSET_CODES))
        self.light_prog_mode_dusk_state = random.choice([ON, OFF])
        self.light_prog_week_end_mode_state = random.choice([ON, OFF])
        self.filtration_prog_status_state = random.choice([ON, OFF])
        self.filtration_prog_thermoregulated_status_state = random.choice([ON, OFF])
        self.filtration_prog_week_end_status_state = random.choice([ON, OFF])
        self.filtration_prog_first_range_status_state = random.choice([ON, OFF])
        self.filtration_prog_second_range_status_state = random.choice([ON, OFF])
        self.filtration_prog_third_range_status_state = random.choice([ON, OFF])
        self.filtration_prog_week_end_first_range_status_state = random.choice([ON, OFF])
        self.filtration_prog_week_end_second_range_status_state = random.choice([ON, OFF])
        self.filtration_prog_week_end_third_range_status_state = random.choice([ON, OFF])
        self.aux_prog_status_state = random.choice([ON, OFF])
        self.aux_prog_week_end_mode_status_state = random.choice([ON, OFF])
        self.aux_prog_first_range_status_state = random.choice([ON, OFF])
        self.aux_prog_second_range_status_state = random.choice([ON, OFF])
        self.aux_prog_third_range_status_state = random.choice([ON, OFF])
        self.aux_prog_week_end_first_range_status_state = random.choice([ON, OFF])
        self.aux_prog_week_end_second_range_status_state = random.choice([ON, OFF])
        self.aux_prog_week_end_third_range_status_state = random.choice([ON, OFF])
        self.light_prog_status_code = random.choice(list(LIGHT_PROG_STATUS_CODES))
        self.light_prog_start_hour_code = random.choice(list(HOUR_CODES))
        self.light_prog_duration_code = random.choice(list(PROG_RANGE_DURATION_WITH_OFF_CODES))
        self.light_prog_week_end_start_hour_code = random.choice(list(HOUR_CODES))
        self.light_prog_week_end_duration_code = random.choice(
            list(PROG_RANGE_DURATION_WITH_OFF_CODES)
        )
        self.light_sequence_speed_code = random.choice(list(LIGHT_SEQUENCE_SPEED_CODES))
        self.filtration_prog_first_range_start_hour_code = random.choice(list(HOUR_CODES))
        self.filtration_prog_first_range_end_hour_code = random.choice(list(HOUR_CODES))
        self.filtration_prog_second_range_start_hour_code = random.choice(list(HOUR_CODES))
        self.filtration_prog_second_range_end_hour_code = random.choice(list(HOUR_CODES))
        self.filtration_prog_third_range_start_hour_code = random.choice(list(HOUR_CODES))
        self.filtration_prog_third_range_end_hour_code = random.choice(list(HOUR_CODES))
        self.filtration_prog_week_end_first_range_start_hour_code = random.choice(list(HOUR_CODES))
        self.filtration_prog_week_end_first_range_end_hour_code = random.choice(list(HOUR_CODES))
        self.filtration_prog_week_end_second_range_start_hour_code = random.choice(list(HOUR_CODES))
        self.filtration_prog_week_end_second_range_end_hour_code = random.choice(list(HOUR_CODES))
        self.filtration_prog_week_end_third_range_start_hour_code = random.choice(list(HOUR_CODES))
        self.filtration_prog_week_end_third_range_end_hour_code = random.choice(list(HOUR_CODES))
        self.aux_prog_first_range_start_hour_code = random.choice(list(HOUR_CODES))
        self.aux_prog_first_range_end_hour_code = random.choice(list(HOUR_CODES))
        self.aux_prog_second_range_start_hour_code = random.choice(list(HOUR_CODES))
        self.aux_prog_second_range_end_hour_code = random.choice(list(HOUR_CODES))
        self.aux_prog_third_range_start_hour_code = random.choice(list(HOUR_CODES))
        self.aux_prog_third_range_end_hour_code = random.choice(list(HOUR_CODES))
        self.aux_prog_week_end_first_range_start_hour_code = random.choice(list(HOUR_CODES))
        self.aux_prog_week_end_first_range_end_hour_code = random.choice(list(HOUR_CODES))
        self.aux_prog_week_end_second_range_start_hour_code = random.choice(list(HOUR_CODES))
        self.aux_prog_week_end_second_range_end_hour_code = random.choice(list(HOUR_CODES))
        self.aux_prog_week_end_third_range_start_hour_code = random.choice(list(HOUR_CODES))
        self.aux_prog_week_end_third_range_end_hour_code = random.choice(list(HOUR_CODES))

    def get_light_status_code(self):
        """Retrieve light status code according current state"""
        for code, state in LIGHT_STATUS_CODES.items():
            if state == self.light_state:
                return code
        LOGGER.warning(
            "No light status code found for %s",
            "on" if self.light_state else "off",
        )
        return "X"

    def get_filtration_status_code(self):
        """Retrieve filtration status code according current state"""
        for code, state in FILTRATION_STATUS_CODES.items():
            if state == self.filtration_state:
                return code
        LOGGER.warning(
            "No filtration status code found for %s",
            "on" if self.filtration_state else "off",
        )
        return "X"

    def get_state_data(self):
        """Generate state data string"""
        # Water temperature evolution
        self.water_temperature += random.choice([-1, 0, 1])
        now = datetime.now()

        fields = {
            SYSTEM_DATE_YEAR: f"{now.year-2000:02}",
            SYSTEM_DATE_MONTH: f"{now.month:02}",
            SYSTEM_DATE_DAY: f"{now.day:02}",
            SYSTEM_DATE_HOUR: f"{now.hour:02}",
            SYSTEM_DATE_MINUTE: f"{now.minute:02}",
            WATER_TEMPERATURE: f"{self.water_temperature:02x}",
            LIGHT_STATUS_CODE: self.get_light_status_code(),
            LIGHT_COLOR_CODE: f"{self.light_color_code:02x}",
            LIGHT_INTENSITY_CODE: str(self.light_intensity_code),
            LIGHT_TIMER_DURATION_CODE: f"{self.light_timer_duration_code:02x}",
            FILTRATION_STATUS_CODE: self.get_filtration_status_code(),
            TREATMENT_STATUS_CODE: random.choice(list(TREATMENT_STATUS_CODES.keys())),
            WATER_TEMPERATURE_OFFSET_CODE: str(self.water_temperature_offset_code),
        }

        data = []
        for idx in range(1, 160):  # pylint: disable=unused-variable
            data.append("0")

        for field, pos in IDENTIFIED_FIELDS.items():
            assert field in fields
            data[pos[0] : pos[-1] + 1] = list(fields[field])

        return "".join(data)

    def handle_toogleable_request(self, connection, address, label, code, attr):
        """Handle a request to set an Tild toogleable item"""
        print(f"Handle set {label} request to '{code}' from {address[0]}:{address[1]}")
        state = {1: ON, 0: OFF}.get(code)
        if state is None:
            print(f"Invalid {label} state '{code}'")
            connection.send(b"ERROR: Invalid state")
        else:
            setattr(self, attr, state)
            print(f"{label} turned {'on' if state is ON else 'off'}")
            connection.send(self.get_state_data().encode("utf8"))

    def handle_set_item_request(
        self, connection, address, label, code, codes, attr, codes_to_send=None
    ):
        """Handle a request to set an Tild item"""
        print(f"Handle set {label} request to '{code}' from {address[0]}:{address[1]}")
        if codes_to_send:
            state = [s for s, c in codes_to_send.items() if c == code]
            if not state:
                print(f"Invalid {label} code '{code}' (not in codes to send mapping)")
                connection.send(
                    f"ERROR: Invalid {label} code '{code}' (not in codes to send mapping)".encode()
                )
                return
            state = state[0]
            sent_code = code
            code = [c for c, s in codes.items() if s == state]
            if not code:
                print(f"No corresponding code found for sent code '{sent_code}' of {label}")
                connection.send(
                    f"ERROR: No corresponding code found for sent code '{sent_code}' of "
                    f"{label}".encode()
                )
                return
            code = code[0]
            print(f"{label}: map sent code '{sent_code}' to '{code}' ({state})")
        if code not in codes:
            print(f"Invalid {label} code '{code}'")
            connection.send(f"ERROR: Invalid {label} code '{code}'".encode())
        else:
            print(f"{label} set to {codes[code]} ({code})")
            setattr(self, attr, code)
            connection.send(self.get_state_data().encode("utf8"))

    def run(self):
        """Run service"""
        print(f"Start fake Tild service on {self.host}:{self.port}")
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
                if SET_LIGHT_STATUS_MESSAGE_KEY in message:
                    self.handle_toogleable_request(
                        connection,
                        address,
                        "light",
                        message[SET_LIGHT_STATUS_MESSAGE_KEY],
                        "light_state",
                    )
                elif SET_FILTRATION_STATUS_MESSAGE_KEY in message:
                    self.handle_toogleable_request(
                        connection,
                        address,
                        "fitration",
                        message[SET_FILTRATION_STATUS_MESSAGE_KEY],
                        "filtration_state",
                    )
                elif SET_FILTRATION_PROG_THERMOREGULATED_STATUS_MESSAGE_KEY in message:
                    self.handle_toogleable_request(
                        connection,
                        address,
                        "filtration programming thermoregulated",
                        message[SET_FILTRATION_PROG_THERMOREGULATED_STATUS_MESSAGE_KEY],
                        "thermoregulated_filtration_state",
                    )
                elif SET_LIGHT_PROG_MODE_DUSK_MESSAGE_KEY in message:
                    self.handle_toogleable_request(
                        connection,
                        address,
                        "light programming mode dusk",
                        message[SET_LIGHT_PROG_MODE_DUSK_MESSAGE_KEY],
                        "light_prog_mode_dusk_state",
                    )
                elif SET_LIGHT_PROG_WEEK_END_MODE_MESSAGE_KEY in message:
                    self.handle_toogleable_request(
                        connection,
                        address,
                        "light programming mode week-end",
                        message[SET_LIGHT_PROG_WEEK_END_MODE_MESSAGE_KEY],
                        "light_prog_week_end_mode_state",
                    )
                elif SET_FILTRATION_PROG_STATUS_MESSAGE_KEY in message:
                    self.handle_toogleable_request(
                        connection,
                        address,
                        "filtration programming",
                        message[SET_FILTRATION_PROG_STATUS_MESSAGE_KEY],
                        "filtration_prog_status_state",
                    )
                elif SET_FILTRATION_PROG_THERMOREGULATED_STATUS_MESSAGE_KEY in message:
                    self.handle_toogleable_request(
                        connection,
                        address,
                        "filtration programming thermoregulated",
                        message[SET_FILTRATION_PROG_THERMOREGULATED_STATUS_MESSAGE_KEY],
                        "filtration_prog_thermoregulated_status_state",
                    )
                elif SET_FILTRATION_PROG_WEEK_END_STATUS_MESSAGE_KEY in message:
                    self.handle_toogleable_request(
                        connection,
                        address,
                        "filtration programming mode week-end",
                        message[SET_FILTRATION_PROG_WEEK_END_STATUS_MESSAGE_KEY],
                        "filtration_prog_week_end_status_state",
                    )
                elif SET_FILTRATION_PROG_FIRST_RANGE_STATUS_MESSAGE_KEY in message:
                    self.handle_toogleable_request(
                        connection,
                        address,
                        "filtration programming first range",
                        message[SET_FILTRATION_PROG_FIRST_RANGE_STATUS_MESSAGE_KEY],
                        "filtration_prog_first_range_status_state",
                    )
                elif SET_FILTRATION_PROG_SECOND_RANGE_STATUS_MESSAGE_KEY in message:
                    self.handle_toogleable_request(
                        connection,
                        address,
                        "filtration programming second range",
                        message[SET_FILTRATION_PROG_SECOND_RANGE_STATUS_MESSAGE_KEY],
                        "filtration_prog_second_range_status_state",
                    )
                elif SET_FILTRATION_PROG_THIRD_RANGE_STATUS_MESSAGE_KEY in message:
                    self.handle_toogleable_request(
                        connection,
                        address,
                        "filtration programming third range",
                        message[SET_FILTRATION_PROG_THIRD_RANGE_STATUS_MESSAGE_KEY],
                        "filtration_prog_third_range_status_state",
                    )
                elif SET_FILTRATION_PROG_WEEK_END_FIRST_RANGE_STATUS_MESSAGE_KEY in message:
                    self.handle_toogleable_request(
                        connection,
                        address,
                        "filtration programming week-end first range",
                        message[SET_FILTRATION_PROG_WEEK_END_FIRST_RANGE_STATUS_MESSAGE_KEY],
                        "filtration_prog_week_end_first_range_status_state",
                    )
                elif SET_FILTRATION_PROG_WEEK_END_SECOND_RANGE_STATUS_MESSAGE_KEY in message:
                    self.handle_toogleable_request(
                        connection,
                        address,
                        "filtration programming week-end second range",
                        message[SET_FILTRATION_PROG_WEEK_END_SECOND_RANGE_STATUS_MESSAGE_KEY],
                        "filtration_prog_week_end_second_range_status_state",
                    )
                elif SET_FILTRATION_PROG_WEEK_END_THIRD_RANGE_STATUS_MESSAGE_KEY in message:
                    self.handle_toogleable_request(
                        connection,
                        address,
                        "filtration programming week-end third range",
                        message[SET_FILTRATION_PROG_WEEK_END_THIRD_RANGE_STATUS_MESSAGE_KEY],
                        "filtration_prog_week_end_third_range_status_state",
                    )
                elif SET_AUX_PROG_STATUS_MESSAGE_KEY in message:
                    self.handle_toogleable_request(
                        connection,
                        address,
                        "auxiliary programming",
                        message[SET_AUX_PROG_STATUS_MESSAGE_KEY],
                        "aux_prog_status_state",
                    )
                elif SET_AUX_PROG_WEEK_END_MODE_STATUS_MESSAGE_KEY in message:
                    self.handle_toogleable_request(
                        connection,
                        address,
                        "auxiliary programming week-end mode",
                        message[SET_AUX_PROG_WEEK_END_MODE_STATUS_MESSAGE_KEY],
                        "aux_prog_week_end_mode_status_state",
                    )
                elif SET_AUX_PROG_FIRST_RANGE_STATUS_MESSAGE_KEY in message:
                    self.handle_toogleable_request(
                        connection,
                        address,
                        "auxiliary programming first range",
                        message[SET_AUX_PROG_FIRST_RANGE_STATUS_MESSAGE_KEY],
                        "aux_prog_first_range_status_state",
                    )
                elif SET_AUX_PROG_SECOND_RANGE_STATUS_MESSAGE_KEY in message:
                    self.handle_toogleable_request(
                        connection,
                        address,
                        "auxiliary programming second range",
                        message[SET_AUX_PROG_SECOND_RANGE_STATUS_MESSAGE_KEY],
                        "aux_prog_second_range_status_state",
                    )
                elif SET_AUX_PROG_THIRD_RANGE_STATUS_MESSAGE_KEY in message:
                    self.handle_toogleable_request(
                        connection,
                        address,
                        "auxiliary programming third range",
                        message[SET_AUX_PROG_THIRD_RANGE_STATUS_MESSAGE_KEY],
                        "aux_prog_third_range_status_state",
                    )
                elif SET_AUX_PROG_WEEK_END_FIRST_RANGE_STATUS_MESSAGE_KEY in message:
                    self.handle_toogleable_request(
                        connection,
                        address,
                        "auxiliary programming week-end first range",
                        message[SET_AUX_PROG_WEEK_END_FIRST_RANGE_STATUS_MESSAGE_KEY],
                        "aux_prog_week_end_first_range_status_state",
                    )
                elif SET_AUX_PROG_WEEK_END_SECOND_RANGE_STATUS_MESSAGE_KEY in message:
                    self.handle_toogleable_request(
                        connection,
                        address,
                        "auxiliary programming week-end second range",
                        message[SET_AUX_PROG_WEEK_END_SECOND_RANGE_STATUS_MESSAGE_KEY],
                        "aux_prog_week_end_second_range_status_state",
                    )
                elif SET_AUX_PROG_WEEK_END_THIRD_RANGE_STATUS_MESSAGE_KEY in message:
                    self.handle_toogleable_request(
                        connection,
                        address,
                        "auxiliary programming week-end third range",
                        message[SET_AUX_PROG_WEEK_END_THIRD_RANGE_STATUS_MESSAGE_KEY],
                        "aux_prog_week_end_third_range_status_state",
                    )
                elif SET_LIGHT_COLOR_MESSAGE_KEY in message:
                    self.handle_set_item_request(
                        connection,
                        address,
                        "light color",
                        message[SET_LIGHT_COLOR_MESSAGE_KEY],
                        LIGHT_COLORS_CODES,
                        "light_color_code",
                    )
                elif SET_LIGHT_INTENSITY_MESSAGE_KEY in message:
                    self.handle_set_item_request(
                        connection,
                        address,
                        "light intensity",
                        message[SET_LIGHT_INTENSITY_MESSAGE_KEY],
                        LIGHT_INTENSITY_CODES,
                        "light_intensity_code",
                        codes_to_send=LIGHT_INTENSITY_CODES_TO_SEND,
                    )
                elif SET_LIGHT_TIMER_DURATION_MESSAGE_KEY in message:
                    self.handle_set_item_request(
                        connection,
                        address,
                        "light timer duration",
                        message[SET_LIGHT_TIMER_DURATION_MESSAGE_KEY],
                        DURATION_CODES,
                        "light_timer_duration_code",
                    )
                elif SET_WATER_TEMPERATURE_OFFSET_MESSAGE_KEY in message:
                    self.handle_set_item_request(
                        connection,
                        address,
                        "water temperature offset",
                        message[SET_WATER_TEMPERATURE_OFFSET_MESSAGE_KEY],
                        WATER_TEMPERATURE_OFFSET_CODES,
                        "water_temperature_offset_code",
                    )
                elif SET_LIGHT_PROG_STATUS_MESSAGE_KEY in message:
                    self.handle_set_item_request(
                        connection,
                        address,
                        "light programming status",
                        message[SET_LIGHT_PROG_STATUS_MESSAGE_KEY],
                        LIGHT_PROG_STATUS_CODES,
                        "light_prog_status_code",
                    )
                elif SET_LIGHT_PROG_START_HOUR_MESSAGE_KEY in message:
                    self.handle_set_item_request(
                        connection,
                        address,
                        "light programming start hour",
                        message[SET_LIGHT_PROG_START_HOUR_MESSAGE_KEY],
                        HOUR_CODES,
                        "light_prog_start_hour_code",
                    )
                elif SET_LIGHT_PROG_DURATION_MESSAGE_KEY in message:
                    self.handle_set_item_request(
                        connection,
                        address,
                        "light programming duration",
                        message[SET_LIGHT_PROG_DURATION_MESSAGE_KEY],
                        PROG_RANGE_DURATION_WITH_OFF_CODES,
                        "light_prog_duration_code",
                    )
                elif SET_LIGHT_PROG_WEEK_END_START_HOUR_MESSAGE_KEY in message:
                    self.handle_set_item_request(
                        connection,
                        address,
                        "light programming week-end start hour",
                        message[SET_LIGHT_PROG_WEEK_END_START_HOUR_MESSAGE_KEY],
                        HOUR_CODES,
                        "light_prog_week_end_start_hour_code",
                    )
                elif SET_LIGHT_PROG_WEEK_END_DURATION_MESSAGE_KEY in message:
                    self.handle_set_item_request(
                        connection,
                        address,
                        "light programming week-end duration",
                        message[SET_LIGHT_PROG_WEEK_END_DURATION_MESSAGE_KEY],
                        PROG_RANGE_DURATION_WITH_OFF_CODES,
                        "light_prog_week_end_duration_code",
                    )
                elif SET_LIGHT_SEQUENCE_SPEED_MESSAGE_KEY in message:
                    self.handle_set_item_request(
                        connection,
                        address,
                        "light sequence speed",
                        message[SET_LIGHT_SEQUENCE_SPEED_MESSAGE_KEY],
                        LIGHT_SEQUENCE_SPEED_CODES,
                        "light_sequence_speed_code",
                    )
                elif SET_FILTRATION_PROG_FIRST_RANGE_START_HOUR_MESSAGE_KEY in message:
                    self.handle_set_item_request(
                        connection,
                        address,
                        "filtration programming first range start hour",
                        message[SET_FILTRATION_PROG_FIRST_RANGE_START_HOUR_MESSAGE_KEY],
                        HOUR_CODES,
                        "filtration_prog_first_range_start_hour_code",
                    )
                elif SET_FILTRATION_PROG_FIRST_RANGE_END_HOUR_MESSAGE_KEY in message:
                    self.handle_set_item_request(
                        connection,
                        address,
                        "filtration programming first range end hour",
                        message[SET_FILTRATION_PROG_FIRST_RANGE_END_HOUR_MESSAGE_KEY],
                        HOUR_CODES,
                        "filtration_prog_first_range_end_hour_code",
                    )
                elif SET_FILTRATION_PROG_SECOND_RANGE_START_HOUR_MESSAGE_KEY in message:
                    self.handle_set_item_request(
                        connection,
                        address,
                        "filtration programming second range start hour",
                        message[SET_FILTRATION_PROG_SECOND_RANGE_START_HOUR_MESSAGE_KEY],
                        HOUR_CODES,
                        "filtration_prog_second_range_start_hour_code",
                    )
                elif SET_FILTRATION_PROG_SECOND_RANGE_END_HOUR_MESSAGE_KEY in message:
                    self.handle_set_item_request(
                        connection,
                        address,
                        "filtration programming second range end hour",
                        message[SET_FILTRATION_PROG_SECOND_RANGE_END_HOUR_MESSAGE_KEY],
                        HOUR_CODES,
                        "filtration_prog_second_range_end_hour_code",
                    )
                elif SET_FILTRATION_PROG_THIRD_RANGE_START_HOUR_MESSAGE_KEY in message:
                    self.handle_set_item_request(
                        connection,
                        address,
                        "filtration programming third range start hour",
                        message[SET_FILTRATION_PROG_THIRD_RANGE_START_HOUR_MESSAGE_KEY],
                        HOUR_CODES,
                        "filtration_prog_third_range_start_hour_code",
                    )
                elif SET_FILTRATION_PROG_THIRD_RANGE_END_HOUR_MESSAGE_KEY in message:
                    self.handle_set_item_request(
                        connection,
                        address,
                        "filtration programming third range end hour",
                        message[SET_FILTRATION_PROG_THIRD_RANGE_END_HOUR_MESSAGE_KEY],
                        HOUR_CODES,
                        "filtration_prog_third_range_end_hour_code",
                    )
                elif SET_FILTRATION_PROG_WEEK_END_FIRST_RANGE_START_HOUR_MESSAGE_KEY in message:
                    self.handle_set_item_request(
                        connection,
                        address,
                        "filtration programming week-end first range start hour",
                        message[SET_FILTRATION_PROG_WEEK_END_FIRST_RANGE_START_HOUR_MESSAGE_KEY],
                        HOUR_CODES,
                        "filtration_prog_week_end_first_range_start_hour_code",
                    )
                elif SET_FILTRATION_PROG_WEEK_END_FIRST_RANGE_END_HOUR_MESSAGE_KEY in message:
                    self.handle_set_item_request(
                        connection,
                        address,
                        "filtration programming week-end first range end hour",
                        message[SET_FILTRATION_PROG_WEEK_END_FIRST_RANGE_END_HOUR_MESSAGE_KEY],
                        HOUR_CODES,
                        "filtration_prog_week_end_first_range_end_hour_code",
                    )
                elif SET_FILTRATION_PROG_WEEK_END_SECOND_RANGE_START_HOUR_MESSAGE_KEY in message:
                    self.handle_set_item_request(
                        connection,
                        address,
                        "filtration programming week-end second range start hour",
                        message[SET_FILTRATION_PROG_WEEK_END_SECOND_RANGE_START_HOUR_MESSAGE_KEY],
                        HOUR_CODES,
                        "filtration_prog_week_end_second_range_start_hour_code",
                    )
                elif SET_FILTRATION_PROG_WEEK_END_SECOND_RANGE_END_HOUR_MESSAGE_KEY in message:
                    self.handle_set_item_request(
                        connection,
                        address,
                        "filtration programming week-end second range end hour",
                        message[SET_FILTRATION_PROG_WEEK_END_SECOND_RANGE_END_HOUR_MESSAGE_KEY],
                        HOUR_CODES,
                        "filtration_prog_week_end_second_range_end_hour_code",
                    )
                elif SET_FILTRATION_PROG_WEEK_END_THIRD_RANGE_START_HOUR_MESSAGE_KEY in message:
                    self.handle_set_item_request(
                        connection,
                        address,
                        "filtration programming week-end third range start hour",
                        message[SET_FILTRATION_PROG_WEEK_END_THIRD_RANGE_START_HOUR_MESSAGE_KEY],
                        HOUR_CODES,
                        "filtration_prog_week_end_third_range_start_hour_code",
                    )
                elif SET_FILTRATION_PROG_WEEK_END_THIRD_RANGE_END_HOUR_MESSAGE_KEY in message:
                    self.handle_set_item_request(
                        connection,
                        address,
                        "filtration programming week-end third range end hour",
                        message[SET_FILTRATION_PROG_WEEK_END_THIRD_RANGE_END_HOUR_MESSAGE_KEY],
                        HOUR_CODES,
                        "filtration_prog_week_end_third_range_end_hour_code",
                    )
                elif SET_AUX_PROG_FIRST_RANGE_START_HOUR_MESSAGE_KEY in message:
                    self.handle_set_item_request(
                        connection,
                        address,
                        "auxiliary programming first range start hour",
                        message[SET_AUX_PROG_FIRST_RANGE_START_HOUR_MESSAGE_KEY],
                        HOUR_CODES,
                        "aux_prog_first_range_start_hour_code",
                    )
                elif SET_AUX_PROG_FIRST_RANGE_END_HOUR_MESSAGE_KEY in message:
                    self.handle_set_item_request(
                        connection,
                        address,
                        "auxiliary programming first range end hour",
                        message[SET_AUX_PROG_FIRST_RANGE_END_HOUR_MESSAGE_KEY],
                        HOUR_CODES,
                        "aux_prog_first_range_end_hour_code",
                    )
                elif SET_AUX_PROG_SECOND_RANGE_START_HOUR_MESSAGE_KEY in message:
                    self.handle_set_item_request(
                        connection,
                        address,
                        "auxiliary programming second range start hour",
                        message[SET_AUX_PROG_SECOND_RANGE_START_HOUR_MESSAGE_KEY],
                        HOUR_CODES,
                        "aux_prog_second_range_start_hour_code",
                    )
                elif SET_AUX_PROG_SECOND_RANGE_END_HOUR_MESSAGE_KEY in message:
                    self.handle_set_item_request(
                        connection,
                        address,
                        "auxiliary programming second range end hour",
                        message[SET_AUX_PROG_SECOND_RANGE_END_HOUR_MESSAGE_KEY],
                        HOUR_CODES,
                        "aux_prog_second_range_end_hour_code",
                    )
                elif SET_AUX_PROG_THIRD_RANGE_START_HOUR_MESSAGE_KEY in message:
                    self.handle_set_item_request(
                        connection,
                        address,
                        "auxiliary programming third range start hour",
                        message[SET_AUX_PROG_THIRD_RANGE_START_HOUR_MESSAGE_KEY],
                        HOUR_CODES,
                        "aux_prog_third_range_start_hour_code",
                    )
                elif SET_AUX_PROG_THIRD_RANGE_END_HOUR_MESSAGE_KEY in message:
                    self.handle_set_item_request(
                        connection,
                        address,
                        "auxiliary programming third range end hour",
                        message[SET_AUX_PROG_THIRD_RANGE_END_HOUR_MESSAGE_KEY],
                        HOUR_CODES,
                        "aux_prog_third_range_end_hour_code",
                    )
                elif SET_AUX_PROG_WEEK_END_FIRST_RANGE_START_HOUR_MESSAGE_KEY in message:
                    self.handle_set_item_request(
                        connection,
                        address,
                        "auxiliary programming week-end first range start hour",
                        message[SET_AUX_PROG_WEEK_END_FIRST_RANGE_START_HOUR_MESSAGE_KEY],
                        HOUR_CODES,
                        "aux_prog_week_end_first_range_start_hour_code",
                    )
                elif SET_AUX_PROG_WEEK_END_FIRST_RANGE_END_HOUR_MESSAGE_KEY in message:
                    self.handle_set_item_request(
                        connection,
                        address,
                        "auxiliary programming week-end first range end hour",
                        message[SET_AUX_PROG_WEEK_END_FIRST_RANGE_END_HOUR_MESSAGE_KEY],
                        HOUR_CODES,
                        "aux_prog_week_end_first_range_end_hour_code",
                    )
                elif SET_AUX_PROG_WEEK_END_SECOND_RANGE_START_HOUR_MESSAGE_KEY in message:
                    self.handle_set_item_request(
                        connection,
                        address,
                        "auxiliary programming week-end second range start hour",
                        message[SET_AUX_PROG_WEEK_END_SECOND_RANGE_START_HOUR_MESSAGE_KEY],
                        HOUR_CODES,
                        "aux_prog_week_end_second_range_start_hour_code",
                    )
                elif SET_AUX_PROG_WEEK_END_SECOND_RANGE_END_HOUR_MESSAGE_KEY in message:
                    self.handle_set_item_request(
                        connection,
                        address,
                        "auxiliary programming week-end second range end hour",
                        message[SET_AUX_PROG_WEEK_END_SECOND_RANGE_END_HOUR_MESSAGE_KEY],
                        HOUR_CODES,
                        "aux_prog_week_end_second_range_end_hour_code",
                    )
                elif SET_AUX_PROG_WEEK_END_THIRD_RANGE_START_HOUR_MESSAGE_KEY in message:
                    self.handle_set_item_request(
                        connection,
                        address,
                        "auxiliary programming week-end third range start hour",
                        message[SET_AUX_PROG_WEEK_END_THIRD_RANGE_START_HOUR_MESSAGE_KEY],
                        HOUR_CODES,
                        "aux_prog_week_end_third_range_start_hour_code",
                    )
                elif SET_AUX_PROG_WEEK_END_THIRD_RANGE_END_HOUR_MESSAGE_KEY in message:
                    self.handle_set_item_request(
                        connection,
                        address,
                        "auxiliary programming week-end third range end hour",
                        message[SET_AUX_PROG_WEEK_END_THIRD_RANGE_END_HOUR_MESSAGE_KEY],
                        HOUR_CODES,
                        "aux_prog_week_end_third_range_end_hour_code",
                    )

                else:
                    print(
                        f"Handle unknown JSON request from {address[0]}:{address[1]}: '{message}'"
                    )
                    connection.send(b"ERROR: unknown JSON request")
            print(f"Close connection from {address[0]}:{address[1]}")
            connection.close()
