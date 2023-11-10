"""Fake Tild box implementation"""

import json
import queue
import random
import select
import socket
from datetime import datetime

from .const import (
    SYSTEM_DATE_DAY,
    SYSTEM_DATE_HOUR,
    SYSTEM_DATE_MINUTE,
    SYSTEM_DATE_MONTH,
    SYSTEM_DATE_YEAR,
    WATER_TEMPERATURE,
)
from .tild import (
    DISCOVER_DATA_MESSAGE,
    GET_SENSORS_DATA_MESSAGE,
    IDENTIFIED_PROPERTIES_BIN_POSITIONS,
    IDENTIFIED_PROPERTIES_POSITIONS,
    PROPERTIES_CODES,
    PROPERTIES_MESSAGE_KEY,
)


class FakeTildBox:
    """Fake Tild box"""

    host = "0.0.0.0"
    port = 30302
    discover_port = 30303
    sock = None

    message_key_to_property = {
        message_key: prop for prop, message_key in PROPERTIES_MESSAGE_KEY.items()
    }

    def __init__(self, host=None, port=None, discover_port=None):
        if host:
            self.host = host
        if port:
            self.port = port if isinstance(port, int) else int(port)
        if discover_port:
            self.discover_port = (
                discover_port if isinstance(discover_port, int) else int(discover_port)
            )
        print(
            f"Start fake Tild service on {self.host}:{self.port} and discovering service on "
            f"{self.host}:{self.discover_port}"
        )

        self.name = f"TILD{random.randrange(1000,9999):04}"
        print(f"Tild device name: {self.name}")

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
                bin_code = (
                    f"{self.properties_state[prop]:b}"
                    if len(pos) == 1
                    else f"{self.properties_state[prop]:02b}"
                )
                bin_status_code[pos[0] : pos[-1] + 1] = list(bin_code)
                print(f"- {prop}: {bin_code} ({self.properties_state[prop]})")
            bin_status_code = "".join(bin_status_code)

            data[bit] = f"{int(bin_status_code, 2):x}".upper()
            print(f" => binary properties bit {bit} = {data[bit]} ({bin_status_code})")

        return "".join(data)

    def handle_set_property_request(self, connection, code, prop):
        """Handle a request to set an Tild property"""
        print(f"Handle set {prop} request to '{code}'")
        if code not in PROPERTIES_CODES[prop]:
            print(f"Invalid {prop} code '{code}'")
            self.reply(connection, f"ERROR: Invalid {prop} code '{code}'")
        else:
            print(f"{prop} set to {PROPERTIES_CODES[prop][code]} ({code})")
            self.properties_state[prop] = code
            self.reply(connection, self.get_state_data())

    def run(self):
        """Run service"""
        print(f"Fake Tild service on {self.host}:{self.port} is running")
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.sock.listen(5)

        self.discover_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.discover_sock.bind((self.host, self.discover_port))

        print(
            f"Fake Tild service on {self.host}:{self.port} and discovering service on "
            f"{self.host}:{self.discover_port} are running"
        )

        self.inputs = [self.sock, self.discover_sock]
        self.outputs = []
        self.message_queues = {}

        while self.inputs:
            readable, writable, exceptional = select.select(self.inputs, self.outputs, self.inputs)
            for s in readable:
                if s is self.sock:
                    # for new connections
                    connection, client_address = s.accept()
                    connection.setblocking(0)
                    self.inputs.append(connection)
                    print(
                        f"Received connection request from {client_address[0]}:{client_address[1]}"
                    )
                    # creating a message queue for each connection
                    self.message_queues[connection] = queue.Queue()

                elif s is self.discover_sock:
                    # if data received on discover UDP service
                    self.handle_discover_request(s)

                else:
                    # if some data has been received on TCP connection
                    message = s.recv(1024)
                    if message:
                        self.handle_request(s, message)

            for s in writable:
                # If something has to be sent - send it. Else, remove connection from output queue
                if not self.message_queues[s].empty():
                    # if some item is present - send it
                    next_msg = self.message_queues[s].get()
                    s.send(next_msg)
                else:
                    # indicate that server has nothing to send
                    self.outputs.remove(s)

            for s in exceptional:
                # remove this connection and all its existences
                self.inputs.remove(s)
                if s in self.outputs:
                    self.outputs.remove(s)
                s.close()
                del self.message_queues[s]

    def handle_discover_request(self, connection):
        """Handle request on discover service"""
        message, remote = connection.recvfrom(1024)
        message = message.decode()
        print(f"Message received on discover service: '{message}' from {remote[0]}:{remote[1]}")
        if message == DISCOVER_DATA_MESSAGE:
            connection.sendto(self.name.encode(), remote)
        else:
            self.reply(connection, "ERROR: unknown message")

    def handle_request(self, connection, message):
        """Handle Tild request"""
        message = message.decode("utf-8").strip()
        if message == GET_SENSORS_DATA_MESSAGE:
            print(f"Handle a {GET_SENSORS_DATA_MESSAGE} request")
            self.reply(connection, self.get_state_data())
        else:
            try:
                message = json.loads(message)
                if not isinstance(message, dict):
                    self.reply(connection, "ERROR: Unexpected JSON message, must be a dict")
                    return
            except json.decoder.JSONDecodeError:
                print(f"Fail to decode JSON message '{message}'")
                self.reply(connection, "ERROR: fail to decode JSON message")
                return
            except ValueError:
                print(f"Unexpected JSON message '{message}'")
                self.reply(connection, "ERROR: fail to decode JSON message")
                return

            for key, value in message.items():
                if key in self.message_key_to_property:
                    self.handle_set_property_request(
                        connection, value, self.message_key_to_property[key]
                    )
                else:
                    print(
                        connection, f"Handle unknown JSON message key '{key}' => '{value}' request"
                    )
                    self.reply(
                        connection, f"ERROR: unknown JSON message key '{key}' => '{value}' request"
                    )

                self.reply(connection, "ERROR: unknown JSON request")

    def reply(self, connection, message):
        """Schedule to send a message on client connection"""
        self.message_queues[connection].put(message.encode("utf8"))
        if connection not in self.outputs:
            self.outputs.append(connection)
