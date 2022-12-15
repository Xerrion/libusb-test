"""
Example of how to request a message in a desired interval
"""

# Disable "Bare exception" warning
# pylint: disable=W0702

# Import mavutil
from pymavlink import mavutil


class MAVLinkGPS:

    def __init__(self, com_port: str = "COM3"):
        self.master = mavutil.mavlink_connection(com_port)
        self.current_position = None

    def get_gps(self):
        while True:
            msg = self.master.recv_match(type="GPS_RAW_INT")
            if not msg:
                continue

            if msg.get_type() == 'GPS_RAW_INT':
                self.current_position = msg.to_dict()["lat"], msg.to_dict()["lon"], msg.to_dict()["alt"]

    def get_current_position(self):
        if self.get_gps():
            return self.current_position

    def request_message_interval(self, message_id: int, frequency_hz: float):
        """
        Request MAVLink message in a desired frequency,
        documentation for SET_MESSAGE_INTERVAL:
            https://mavlink.io/en/messages/common.html#MAV_CMD_SET_MESSAGE_INTERVAL

        Args:
            message_id (int): MAVLink message ID
            frequency_hz (float): Desired frequency in Hz
        """
        self.master.mav.command_long_send(
            self.master.target_system,
            self.master.target_component,
            mavutil.mavlink.MAV_CMD_SET_MESSAGE_INTERVAL,
            0,
            message_id,  # The MAVLink message ID
            1e6 / frequency_hz,
            # The interval between two messages in microseconds. Set to -1 to disable and 0 to request default rate.
            0,
            0,
            0,
            0,  # Unused parameters
            0,
            # Target address of message stream (if message has target address fields). 0: Flight-stack default (recommended), 1: address of requestor, 2: broadcast.
        )


gps = MAVLinkGPS("COM3")
gps.request_message_interval(mavutil.mavlink.MAVLINK_MSG_ID_GPS_RAW_INT, 3)

while True:
    try:
        print(gps.get_current_position())

    except Exception as e:
        pass
# lat, lon, alt = gps.get_current_position()
# print(lat, lon, alt)
