"""CCEI Tild client"""
import asyncio
import logging
import random
import socket
from datetime import datetime

from .const import (
    FILTRATION_ENABLED,
    FILTRATION_STATUS_CODE,
    LIGHT_COLOR,
    LIGHT_COLOR_CODE,
    LIGHT_ENABLED,
    LIGHT_INTENSITY,
    LIGHT_INTENSITY_CODE,
    PUMP_ENABLED,
    RAW_DATA,
    SYSTEM_DATE,
    SYSTEM_HOST,
    TOGGLES_STATUS_CODE,
    TREATMENT_ENABLED,
    TREATMENT_STATUS_CODE,
    WATER_REAL_TEMPERATURE,
    WATER_TEMPERATURE,
    WATER_TEMPERATURE_OFFSET,
    WATER_TEMPERATURE_OFFSET_CODE,
)

LOGGER = logging.getLogger(__name__)

COLORS = {
    "01": "cold",
    "02": "bleu",
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
    "0": 0,
    "6": -3,
}

TOGGLE_STATUS_CODES = {
    "0": {"light": False, "pump": False},
    "2": {"light": True, "pump": False},
    "3": {"light": True, "pump": True},
}

FILTRATION_STATUS_CODES = {
    "8": True,
    "0": False,
}

TREATMENT_STATUS_CODES = {
    "7": True,
    "3": False,
}


class CceiTildClient:
    """CCEI Tild client"""

    host = None
    port = None

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

    async def get_sensors_data(self):
        """Async retrieve sensors state data"""
        return await self._get_sensors_data()

    async def _get_sensors_data(self):
        """Retrieve sensors state data"""
        LOGGER.debug("Start connection to tcp://%s:%d...", self.host, self.port)
        connect = asyncio.open_connection(self.host, self.port)
        reader, writer = await connect
        LOGGER.debug("Connection established")
        try:
            LOGGER.debug("Send begin and awaiting answer...")
            writer.write(b"Begin")
            data = await reader.read(256)
            data = data.decode("UTF-8")
            LOGGER.debug("Answer received: %s", data)
            if not data:
                return False
        finally:
            writer.close()

        LOGGER.debug("Parse answer and compute state")
        state = {
            SYSTEM_HOST: self.host,
            SYSTEM_DATE: datetime(
                int(data[132:134]) + 2000,
                int(data[130:132]) - 1,
                int(data[128:130]),
                int(data[124:126]),
                int(data[122:124]),
            ).isoformat(),
            TOGGLES_STATUS_CODE: data[34:35],
            LIGHT_COLOR_CODE: data[64:66],
            LIGHT_INTENSITY_CODE: data[71:72],
            WATER_TEMPERATURE: int(data[66:68], 16),
            WATER_TEMPERATURE_OFFSET_CODE: data[155:156],
            FILTRATION_STATUS_CODE: data[75:76],
            TREATMENT_STATUS_CODE: data[69:70],
            RAW_DATA: data,
        }

        state[LIGHT_ENABLED] = TOGGLE_STATUS_CODES.get(state[TOGGLES_STATUS_CODE], {}).get("light")
        state[TREATMENT_ENABLED] = TREATMENT_STATUS_CODES.get(state[TREATMENT_STATUS_CODE])
        state[FILTRATION_ENABLED] = FILTRATION_STATUS_CODES.get(state[FILTRATION_STATUS_CODE])
        state[PUMP_ENABLED] = TOGGLE_STATUS_CODES.get(state[TOGGLES_STATUS_CODE], {}).get("pump")
        state[WATER_TEMPERATURE_OFFSET] = WATER_TEMPERATURE_OFFSET_CODES.get(
            state[WATER_TEMPERATURE_OFFSET_CODE]
        )
        state[WATER_REAL_TEMPERATURE] = (
            state[WATER_TEMPERATURE] + state[WATER_TEMPERATURE_OFFSET]
            if state[WATER_TEMPERATURE_OFFSET] is not None
            else None
        )
        state[LIGHT_COLOR] = COLORS.get(state[LIGHT_COLOR_CODE])
        state[LIGHT_INTENSITY] = LIGHT_INTENSITY_CODES.get(state[LIGHT_INTENSITY_CODE])
        LOGGER.debug(
            "State:%s",
            "\n - {}".format("\n - ".join([f"{key}={value}" for key, value in state.items()])),
        )
        return state


class FakeTildBox:
    """Fake Tild box"""

    host = "0.0.0.0"
    port = 30302
    sock = None

    def __init__(self, host=None, port=None):
        if host:
            self.host = host
        if port:
            self.port = port

    @staticmethod
    def get_random_state_data():
        """Generate random state data string"""
        data = []
        for idx in range(0, 255):  # pylint: disable=unused-variable
            data.append("0")
        now = datetime.now()
        data[132:134] = list(f"{now.year-2000:02}")  # year
        data[130:132] = list(f"{now.month+1:02}")  # month
        data[128:130] = list(f"{now.day:02}")  # day
        data[124:126] = list(f"{now.hour:02}")  # hours
        data[122:124] = list(f"{now.minute:02}")  # minutes

        # temperature (base 16, eg. 17 mean 23°C)
        temp = random.randrange(20, 30)
        temp = hex(temp).replace("0x", "")
        temp = f"0{temp}" if len(temp) == 1 else temp
        data[66:68] = list(temp)

        data[34:35] = list(random.choice(list(TOGGLE_STATUS_CODES.keys())))
        data[64:66] = list(random.choice(list(COLORS.keys())))
        data[71:72] = list(random.choice(list(LIGHT_INTENSITY_CODES.keys())))
        data[75:76] = list(random.choice(list(FILTRATION_STATUS_CODES.keys())))
        data[69:70] = list(random.choice(list(TREATMENT_STATUS_CODES.keys())))
        data[155:156] = list(random.choice(list(WATER_TEMPERATURE_OFFSET_CODES.keys())))

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
            buf = connection.recv(1024).decode("utf-8").strip()
            if buf == "Begin":
                print(f"Handle a begin request from {address[0]}:{address[1]}")
                connection.send(self.get_random_state_data().encode("utf8"))
            else:
                connection.send(b"unknown")
            connection.close()
