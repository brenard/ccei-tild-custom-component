"""CCEI Tild client"""
import asyncio
import json
import logging
import random
import socket
from datetime import datetime

from .const import (
    FILTRATION_ENABLED,
    FILTRATION_EXPECTED_DURATION,
    FILTRATION_STATUS_CODE,
    LIGHT_COLOR,
    LIGHT_COLOR_CODE,
    LIGHT_ENABLED,
    LIGHT_INTENSITY,
    LIGHT_INTENSITY_CODE,
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
    TOGGLES_STATUS_CODE,
    TREATMENT_ENABLED,
    TREATMENT_STATUS_CODE,
    WATER_RAW_TEMPERATURE,
    WATER_TEMPERATURE,
    WATER_TEMPERATURE_OFFSET,
    WATER_TEMPERATURE_OFFSET_CODE,
)

LOGGER = logging.getLogger(__name__)

COLORS = {
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

TOGGLE_STATUS_CODES = {
    "0": {"light": False, "filtration": False},
    "1": {"light": False, "filtration": True},
    "2": {"light": True, "filtration": False},
    "3": {"light": True, "filtration": True},
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
    TOGGLES_STATUS_CODE: [34],
    LIGHT_COLOR_CODE: [64, 65],
    LIGHT_INTENSITY_CODE: [71],
    WATER_TEMPERATURE: [66, 67],
    WATER_TEMPERATURE_OFFSET_CODE: [155],
    FILTRATION_STATUS_CODE: [32],
    FILTRATION_EXPECTED_DURATION: [33],
    TREATMENT_STATUS_CODE: [69],
}

GET_SENSORS_DATA_MESSAGE = "Begin"
LIGHT_MESSAGE_KEY = "sprj"
FILTRATION_MESSAGE_KEY = "sfil"
SET_LIGHT_COLOR_MESSAGE_KEY = "prcn"
SET_LIGHT_INTENSITY_MESSAGE_KEY = "plum"


def parse_sensors_data(data):
    """Parse sensors state data"""
    state = {}
    for key, fields in IDENTIFIED_FIELDS.items():
        state[key] = "".join(map(lambda x: data[x], fields))

    state[SYSTEM_DATE] = datetime(
        int(state[SYSTEM_DATE_YEAR]) + 2000,
        int(state[SYSTEM_DATE_MONTH]) - 1,
        int(state[SYSTEM_DATE_DAY]),
        int(state[SYSTEM_DATE_HOUR]),
        int(state[SYSTEM_DATE_MINUTE]),
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
    state[LIGHT_ENABLED] = TOGGLE_STATUS_CODES.get(state[TOGGLES_STATUS_CODE], {}).get("light")
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
    state[LIGHT_COLOR] = COLORS.get(state[LIGHT_COLOR_CODE])
    state[LIGHT_INTENSITY] = LIGHT_INTENSITY_CODES.get(state[LIGHT_INTENSITY_CODE])
    return state


class CceiTildClient:
    """CCEI Tild client"""

    host = None
    port = None
    encoding = "utf8"

    def __init__(self, host, port=None):
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
        state = parse_sensors_data(data)
        state[SYSTEM_HOST] = self.host
        state[RAW_DATA] = data
        LOGGER.debug(
            "State:%s",
            "\n - {}".format("\n - ".join([f"{key}={value}" for key, value in state.items()])),
        )
        return state

    async def toggle_light(self, state=None):
        """Turn on the Tild light"""
        if state is None:
            LOGGER.debug("Ask for toogling the light, call Tild to retreive it current state")
            sensors_data = await self.get_sensors_data()
            if not sensors_data:
                LOGGER.warning("Fail to retreive current light state, cant't toggling it.")
                return False
            state = ON if sensors_data[LIGHT_ENABLED] else ON
        assert state in [ON, OFF], f"Invalid light state '{state}'"
        LOGGER.debug("Call Tild to turn %s the light", state)
        data = await self._call_tild({LIGHT_MESSAGE_KEY: 1 if state == ON else 0}, False)
        if not data:
            LOGGER.debug("Fail to turn %s the light", state)
            return False
        return True

    async def toggle_filtration(self, state=None):
        """Turn on the Tild filtration"""
        if state is None:
            LOGGER.debug("Ask for toogling the filtration, call Tild to retreive it current state")
            sensors_data = await self.get_sensors_data()
            if not sensors_data:
                LOGGER.warning("Fail to retreive current filtration state, cant't toggling it.")
                return False
            state = ON if sensors_data[FILTRATION_ENABLED] else ON
        assert state in [ON, OFF], f"Invalid filtration state '{state}'"
        LOGGER.debug("Call Tild to turn %s the filtration", state)
        data = await self._call_tild({FILTRATION_MESSAGE_KEY: 1 if state == ON else 0}, False)
        if not data:
            LOGGER.debug("Fail to turn %s the filtration", state)
            return False
        return True

    async def set_light_color(self, color):
        """Set the light color"""
        if color in COLORS:
            color_code = color
            color = COLORS[color]
        else:
            assert color in COLORS.values(), f"Invalid light color '{color}'"
            color_idx = list(COLORS.values()).index(color)
            color_code = list(COLORS.keys())[color_idx]
        data = await self._call_tild({SET_LIGHT_COLOR_MESSAGE_KEY: color_code}, False)
        if not data:
            LOGGER.debug("Fail to set light color to %s (%s)", color, color_code)
            return False
        return True

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
        data = await self._call_tild({SET_LIGHT_INTENSITY_MESSAGE_KEY: intensity_code}, False)
        if not data:
            LOGGER.debug("Fail to set light intensity to %s (%s)", intensity, intensity_code)
            return False
        return True


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
        self.light_color_code = random.choice(list(COLORS.keys()))
        self.light_intensity_code = random.choice(list(LIGHT_INTENSITY_CODES.keys()))
        self.filtration_state = random.choice([True, False])

    def get_toggle_status_code(self):
        """Retrieve toggle status code according current light & filtration state"""
        for code, state in TOGGLE_STATUS_CODES.items():
            if state["light"] == self.light_state and state["filtration"] == self.filtration_state:
                return code
        LOGGER.warning(
            "No toggle status code found for light %s and filtration %s",
            "on" if self.light_state else "off",
            "on" if self.filtration_state else "off",
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

    def get_random_state_data(self):
        """Generate random state data string"""

        now = datetime.now()

        # temperature (base 16, eg. 17 mean 23°C)
        temp = random.randrange(20, 30)
        temp = hex(temp).replace("0x", "")
        temp = f"0{temp}" if len(temp) == 1 else temp

        fields = {
            SYSTEM_DATE_YEAR: f"{now.year-2000:02}",
            SYSTEM_DATE_MONTH: f"{now.month+1:02}",
            SYSTEM_DATE_DAY: f"{now.day:02}",
            SYSTEM_DATE_HOUR: f"{now.hour:02}",
            SYSTEM_DATE_MINUTE: f"{now.minute:02}",
            WATER_TEMPERATURE: temp,
            TOGGLES_STATUS_CODE: self.get_toggle_status_code(),
            LIGHT_COLOR_CODE: self.light_color_code,
            LIGHT_INTENSITY_CODE: str(self.light_intensity_code),
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
                connection.send(self.get_random_state_data().encode("utf8"))
            else:
                try:
                    message = json.loads(message)
                    if not isinstance(message, dict):
                        raise ValueError("Unexpected JSON message, must be a dict")
                except json.decoder.JSONDecodeError:
                    print(f"Fail to decode JSON message '{message}' from {address[0]}:{address[1]}")
                    connection.send(b"ERROR: fail to decode JSON message")
                except ValueError:
                    print(f"Unexpected JSON message '{message}' from {address[0]}:{address[1]}")
                    connection.send(b"ERROR: unexcepected JSON message")
                if LIGHT_MESSAGE_KEY in message:
                    print(
                        f"Handle turn {'on' if message[LIGHT_MESSAGE_KEY] else 'off'} light "
                        f"request from {address[0]}:{address[1]}"
                    )
                    self.light_state = bool(message[LIGHT_MESSAGE_KEY])
                elif FILTRATION_MESSAGE_KEY in message:
                    print(
                        f"Handle turn {'on' if message[FILTRATION_MESSAGE_KEY] else 'off'} "
                        f"filtration request from {address[0]}:{address[1]}"
                    )
                    self.filtration_state = bool(message[FILTRATION_MESSAGE_KEY])
                    # No expected answer
                elif SET_LIGHT_COLOR_MESSAGE_KEY in message:
                    color = message[SET_LIGHT_COLOR_MESSAGE_KEY]
                    print(
                        f"Handle set light color request to '{color}' from "
                        f"{address[0]}:{address[1]}"
                    )
                    if color not in COLORS:
                        print(f"Invalid color '{color}'")
                        connection.send(b"ERROR: Invalid color")
                    self.light_color_code = color
                    # No expected answer
                elif SET_LIGHT_INTENSITY_MESSAGE_KEY in message:
                    intensity = message[SET_LIGHT_INTENSITY_MESSAGE_KEY]
                    print(
                        f"Handle set light intensity request to '{intensity}' from "
                        f"{address[0]}:{address[1]}"
                    )
                    if intensity not in LIGHT_INTENSITY_CODES:
                        print(f"Invalid intensity '{intensity}'")
                        connection.send(b"ERROR: Invalid intensity")
                    self.light_intensity_code = intensity
                    # No expected answer
                else:
                    print(
                        f"Handle unknown JSON request from {address[0]}:{address[1]}: '{message}'"
                    )
                    connection.send(b"ERROR: unknown JSON request")
            print(f"Close connection from {address[0]}:{address[1]}")
            connection.close()
