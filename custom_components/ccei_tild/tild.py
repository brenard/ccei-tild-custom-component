"""CCEI Tild client"""
import asyncio
import json
import logging
import random
import socket
from datetime import datetime

from .const import (
    COORDINATOR,
    DOMAIN,
    DURATION_CODES,
    FILTRATION_ENABLED,
    FILTRATION_EXPECTED_DURATION,
    FILTRATION_STATUS_CODE,
    LIGHT_COLOR,
    LIGHT_COLOR_CODE,
    LIGHT_COLORS_CODES,
    LIGHT_ENABLED,
    LIGHT_INTENSITY,
    LIGHT_INTENSITY_CODE,
    LIGHT_INTENSITY_CODES,
    LIGHT_STATUS_CODE,
    LIGHT_TIMER_DURATION,
    LIGHT_TIMER_DURATION_CODE,
    OFF,
    ON,
    RAW_DATA,
    SYSTEM_DATE,
    SYSTEM_DATE_DAY,
    SYSTEM_DATE_HOUR,
    SYSTEM_DATE_MINUTE,
    SYSTEM_DATE_MONTH,
    SYSTEM_DATE_YEAR,
    SYSTEM_HOST,
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

LIGHT_STATUS_CODES = {
    "C": True,
    "8": False,
}

FILTRATION_STATUS_CODES = {
    "2": True,
    "0": False,
}

TREATMENT_STATUS_CODES = {
    "7": True,
    "3": False,
}

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
    FILTRATION_STATUS_CODE: [32],
    FILTRATION_EXPECTED_DURATION: [33],
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
    state[FILTRATION_EXPECTED_DURATION] = int(state[FILTRATION_EXPECTED_DURATION])
    state[WATER_TEMPERATURE_OFFSET] = WATER_TEMPERATURE_OFFSET_CODES.get(
        state[WATER_TEMPERATURE_OFFSET_CODE]
    )
    state[WATER_RAW_TEMPERATURE] = (
        state[WATER_TEMPERATURE] - state[WATER_TEMPERATURE_OFFSET]
        if state[WATER_TEMPERATURE_OFFSET] is not None
        else None
    )
    state[LIGHT_COLOR] = LIGHT_COLORS_CODES.get(state[LIGHT_COLOR_CODE])
    state[LIGHT_INTENSITY] = LIGHT_INTENSITY_CODES.get(state[LIGHT_INTENSITY_CODE])
    state[THERMOREGULATED_FILTRATION_ENABLED] = None
    state[LIGHT_TIMER_DURATION] = DURATION_CODES.get(state[LIGHT_TIMER_DURATION_CODE])
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
        data = await self._call_tild("Begin")
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
        """Turn on/off import names the Tild light"""
        if state is None:
            LOGGER.debug("Ask for toogling the light, call Tild to retreive it current state")
            sensors_data = await self.get_sensors_data()
            if not sensors_data:
                LOGGER.warning("Fail to retreive current light state, cant't toggling it.")
                return False
            state = ON if sensors_data[LIGHT_ENABLED] else ON
        assert state in [ON, OFF], f"Invalid light state '{state}'"
        LOGGER.debug("Call Tild to turn %s the light", state)
        data = await self._call_tild({SET_LIGHT_STATUS_MESSAGE_KEY: 1 if state == ON else 0})
        if not data:
            LOGGER.error("Fail to turn %s the light (invalid data return)", state)
            return False
        sensors_data = parse_sensors_data(data)
        if not sensors_data:
            LOGGER.error("Fail to parse sensors data after turning %s the light", state)
            return False
        # Update coordinator data
        self._update_coordinator_sensors_data(sensors_data)
        return True
        if (sensors_data[LIGHT_ENABLED] and state == ON) or (
            not sensors_data[LIGHT_ENABLED] and state == OFF
        ):
            return True
        LOGGER.error("Fail to turn %s the light", state)
        return False

    async def toggle_filtration(self, state=None):
        """Turn on/off the Tild filtration"""
        if state is None:
            LOGGER.debug("Ask for toogling the filtration, call Tild to retreive it current state")
            sensors_data = await self.get_sensors_data()
            if not sensors_data:
                LOGGER.warning("Fail to retreive current filtration state, cant't toggling it.")
                return False
            state = ON if sensors_data[FILTRATION_ENABLED] else ON
        assert state in [ON, OFF], f"Invalid filtration state '{state}'"
        LOGGER.debug("Call Tild to turn %s the filtration", state)
        data = await self._call_tild({SET_FILTRATION_STATUS_MESSAGE_KEY: 1 if state == ON else 0})
        if not data:
            LOGGER.debug("Fail to turn %s the filtration", state)
            return False
        sensors_data = parse_sensors_data(data)
        if not sensors_data:
            LOGGER.error("Fail to parse sensors data after turning %s the filtration", state)
            return False
        # Update coordinator data
        self._update_coordinator_sensors_data(sensors_data)
        return True
        if (sensors_data[FILTRATION_ENABLED] and state == ON) or (
            not sensors_data[FILTRATION_ENABLED] and state == OFF
        ):
            return True
        LOGGER.error("Fail to turn %s the filtration", state)
        return False

    async def toggle_thermoregulated_filtration(self, state=None):
        """Turn on/off the Tild thermoregulated filtration"""
        if state is None:
            LOGGER.debug(
                "Ask for toogling the thermoregulated filtration, call Tild to retreive it "
                "current state"
            )
            sensors_data = await self.get_sensors_data()
            if not sensors_data:
                LOGGER.warning(
                    "Fail to retreive current thermoregulated filtration state, cant't "
                    "toggling it."
                )
                return False
            state = ON if sensors_data[THERMOREGULATED_FILTRATION_ENABLED] else ON
        assert state in [ON, OFF], f"Invalid thermoregulated filtration state '{state}'"
        LOGGER.debug("Call Tild to turn %s the thermoregulated filtration", state)
        data = await self._call_tild(
            {SET_FILTRATION_PROG_THERMOREGULATED_STATUS_MESSAGE_KEY: 1 if state == ON else 0}
        )
        if not data:
            LOGGER.debug("Fail to turn %s the thermoregulated filtration", state)
            return False
        sensors_data = parse_sensors_data(data)
        if not sensors_data:
            LOGGER.error(
                "Fail to parse sensors data after turning %s the thermoregulated filtration", state
            )
            return False
        # Update coordinator data
        self._update_coordinator_sensors_data(sensors_data)
        return True
        if (sensors_data[THERMOREGULATED_FILTRATION_ENABLED] and state == ON) or (
            not sensors_data[THERMOREGULATED_FILTRATION_ENABLED] and state == OFF
        ):
            return True
        LOGGER.error("Fail to turn %s the thermoregulated filtration", state)
        return False

    async def set_light_color(self, color):
        """Set the light color"""
        if color in LIGHT_COLORS_CODES:
            color_code = color
            color = LIGHT_COLORS_CODES[color]
        else:
            assert color in LIGHT_COLORS_CODES.values(), f"Invalid light color '{color}'"
            color_idx = list(LIGHT_COLORS_CODES.values()).index(color)
            color_code = list(LIGHT_COLORS_CODES.keys())[color_idx]
        data = await self._call_tild({SET_LIGHT_COLOR_MESSAGE_KEY: color_code})
        if not data:
            LOGGER.debug("Fail to set light color to %s (%s)", color, color_code)
            return False
        sensors_data = parse_sensors_data(data)
        if not sensors_data:
            LOGGER.error(
                "Fail to parse sensors data after setting light color to %s (%s)", color, color_code
            )
            return False
        # Update coordinator data
        self._update_coordinator_sensors_data(sensors_data)
        return True
        if sensors_data[LIGHT_COLOR_CODE] == color_code:
            return True
        LOGGER.error("Fail to set light color to %s (%s)", color, color_code)
        return False

    async def set_light_intensity(self, intensity):
        """Set the light intensity"""
        if intensity in LIGHT_INTENSITY_CODES:
            intensity_code = intensity
            intensity = LIGHT_INTENSITY_CODES[intensity]
        else:
            intensity = int(intensity)
            assert (
                intensity in LIGHT_INTENSITY_CODES.values()
            ), f"Invalid light intensity '{intensity}'"
            intensity_idx = list(LIGHT_INTENSITY_CODES.values()).index(intensity)
            intensity_code = list(LIGHT_INTENSITY_CODES.keys())[intensity_idx]
        data = await self._call_tild({SET_LIGHT_INTENSITY_MESSAGE_KEY: intensity_code})
        if not data:
            LOGGER.debug("Fail to set light intensity to %s (%s)", intensity, intensity_code)
            return False
        sensors_data = parse_sensors_data(data)
        if not sensors_data:
            LOGGER.error(
                "Fail to parse sensors data after setting light intensity to %s (%s)",
                intensity,
                intensity_code,
            )
            return False
        # Update coordinator data
        self._update_coordinator_sensors_data(sensors_data)
        return True
        if sensors_data[LIGHT_INTENSITY_CODE] == intensity_code:
            return True
        LOGGER.error("Fail to set light intensity to %s (%s)", intensity, intensity_code)
        return False

    async def set_light_timer_duration(self, duration):
        """Set the light timer duration"""
        if duration in DURATION_CODES:
            duration_code = duration
            duration = DURATION_CODES[duration]
        else:
            assert duration in DURATION_CODES.values(), f"Invalid light timer duration '{duration}'"
            duration_idx = list(DURATION_CODES.values()).index(duration)
            duration_code = list(DURATION_CODES.keys())[duration_idx]
        data = await self._call_tild({SET_LIGHT_TIMER_DURATION_MESSAGE_KEY: duration_code})
        if not data:
            LOGGER.debug("Fail to set light timer duration to %s (%s)", duration, duration_code)
            return False
        sensors_data = parse_sensors_data(data)
        if not sensors_data:
            LOGGER.error(
                "Fail to parse sensors data after setting light timer duration to %s (%s)",
                duration,
                duration_code,
            )
            return False
        # Update coordinator data
        self._update_coordinator_sensors_data(sensors_data)
        return True
        if sensors_data[LIGHT_TIMER_DURATION_CODE] == duration_code:
            return True
        LOGGER.error("Fail to set light timer duration to %s (%s)", duration, duration_code)
        return False

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

        self.light_state = random.choice([True, False])
        self.light_color_code = random.choice(list(LIGHT_COLORS_CODES.keys()))
        self.light_intensity_code = random.choice(list(LIGHT_INTENSITY_CODES.keys()))
        self.light_timer_duration_code = random.choice(list(DURATION_CODES.keys()))
        self.filtration_state = random.choice([True, False])
        self.thermoregulated_filtration_state = random.choice([True, False])

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

        now = datetime.now()

        # temperature (base 16, eg. 17 mean 23°C)
        temp = random.randrange(20, 30)
        temp = hex(temp).replace("0x", "")
        temp = f"0{temp}" if len(temp) == 1 else temp

        fields = {
            SYSTEM_DATE_YEAR: f"{now.year-2000:02}",
            SYSTEM_DATE_MONTH: f"{now.month:02}",
            SYSTEM_DATE_DAY: f"{now.day:02}",
            SYSTEM_DATE_HOUR: f"{now.hour:02}",
            SYSTEM_DATE_MINUTE: f"{now.minute:02}",
            WATER_TEMPERATURE: temp,
            LIGHT_STATUS_CODE: self.get_light_status_code(),
            LIGHT_COLOR_CODE: self.light_color_code,
            LIGHT_INTENSITY_CODE: str(self.light_intensity_code),
            LIGHT_TIMER_DURATION_CODE: self.light_timer_duration_code,
            FILTRATION_STATUS_CODE: self.get_filtration_status_code(),
            TREATMENT_STATUS_CODE: random.choice(list(TREATMENT_STATUS_CODES.keys())),
            WATER_TEMPERATURE_OFFSET_CODE: random.choice(
                list(WATER_TEMPERATURE_OFFSET_CODES.keys())
            ),
            FILTRATION_EXPECTED_DURATION: str(random.randrange(0, 8)),
        }

        data = []
        for idx in range(1, 160):  # pylint: disable=unused-variable
            data.append("0")

        for field, pos in IDENTIFIED_FIELDS.items():
            assert field in fields
            data[pos[0] : pos[-1] + 1] = list(fields[field])

        return "".join(data)

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
                    self.light_state = bool(message[SET_LIGHT_STATUS_MESSAGE_KEY])
                    print(
                        f"Handle turn {'on' if self.light_state else 'off'} light request from "
                        f"{address[0]}:{address[1]}"
                    )
                    connection.send(self.get_state_data().encode("utf8"))
                elif SET_FILTRATION_STATUS_MESSAGE_KEY in message:
                    self.filtration_state = bool(message[SET_FILTRATION_STATUS_MESSAGE_KEY])
                    print(
                        f"Handle turn {'on' if self.filtration_state else 'off'} filtration "
                        f"request from {address[0]}:{address[1]}"
                    )
                    connection.send(self.get_state_data().encode("utf8"))
                elif SET_FILTRATION_PROG_THERMOREGULATED_STATUS_MESSAGE_KEY in message:
                    self.thermoregulated_filtration_state = bool(
                        message[SET_FILTRATION_STATUS_MESSAGE_KEY]
                    )
                    print(
                        f"Handle turn {'on' if self.thermoregulated_filtration_state else 'off'} "
                        f"thermoregulated filtration request from {address[0]}:{address[1]}"
                    )
                    connection.send(self.get_state_data().encode("utf8"))
                elif SET_LIGHT_COLOR_MESSAGE_KEY in message:
                    color = message[SET_LIGHT_COLOR_MESSAGE_KEY]
                    print(
                        f"Handle set light color request to '{color}' from "
                        f"{address[0]}:{address[1]}"
                    )
                    if color not in LIGHT_COLORS_CODES:
                        print(f"Invalid color '{color}'")
                        connection.send(b"ERROR: Invalid color")
                    else:
                        print(f"Light color set to {LIGHT_COLORS_CODES[color]} ({color})")
                        self.light_color_code = color
                        connection.send(self.get_state_data().encode("utf8"))
                elif SET_LIGHT_INTENSITY_MESSAGE_KEY in message:
                    intensity = message[SET_LIGHT_INTENSITY_MESSAGE_KEY]
                    print(
                        f"Handle set light intensity request to '{intensity}' from "
                        f"{address[0]}:{address[1]}"
                    )
                    if intensity not in LIGHT_INTENSITY_CODES:
                        print(f"Invalid intensity '{intensity}'")
                        connection.send(b"ERROR: Invalid intensity")
                    else:
                        print(
                            f"Light intensity set to {LIGHT_INTENSITY_CODES[intensity]} "
                            f"({intensity})"
                        )
                        self.light_intensity_code = intensity
                        connection.send(self.get_state_data().encode("utf8"))
                elif SET_LIGHT_TIMER_DURATION_MESSAGE_KEY in message:
                    duration = message[SET_LIGHT_TIMER_DURATION_MESSAGE_KEY]
                    print(
                        f"Handle set light timer duration request to '{duration}' from "
                        f"{address[0]}:{address[1]}"
                    )
                    if duration not in DURATION_CODES:
                        print(f"Invalid duration '{duration}'")
                        connection.send(b"ERROR: Invalid duration")
                    else:
                        print(
                            f"Light timer duration set to {DURATION_CODES[duration]} ({duration})"
                        )
                        self.light_timer_duration_code = duration
                        connection.send(self.get_state_data().encode("utf8"))
                else:
                    print(
                        f"Handle unknown JSON request from {address[0]}:{address[1]}: '{message}'"
                    )
                    connection.send(b"ERROR: unknown JSON request")
            print(f"Close connection from {address[0]}:{address[1]}")
            connection.close()
