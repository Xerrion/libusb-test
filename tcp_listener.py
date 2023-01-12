import socket
import pymavlink
import serial
from pymavlink import mavutil

# RTK IP address
TCP_IP = 'rtk2go.com'
# RTK Base mode port
TCP_PORT = 2101

# Set up the TCP socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Read the RTCM3 messages
master = mavutil.mavlink_connection('COM3', baud=57600)
# Wait a heartbeat before sending commands
master.wait_heartbeat()

# Open a serial connection to COM6
# ser = serial.Serial("COM6", "115200", timeout=1)

master.param_set_send(
    'GPS_RTK_BASE',
    3,
    mavutil.mavlink.MAV_PARAM_TYPE_UINT8,
)

master.mav.command_long_send(
    master.target_system,
    master.target_component,
    mavutil.mavlink.MAV_CMD_SET_MESSAGE_INTERVAL,
    0,
    mavutil.mavlink.MAVLINK_MSG_ID_GPS_RTK,
    10000000,
    0,
    0,
    0,
    0,
    1,
)
master.mav.command_long_send(
    master.target_system,
    master.target_component,
    mavutil.mavlink.MAV_CMD_SET_MESSAGE_INTERVAL,
    0,
    mavutil.mavlink.MAVLINK_MSG_ID_GPS2_RTK,
    10000000,
    0,
    0,
    0,
    0,
    1,
)


def request_message_interval(message_id: int, frequency_hz: float) -> None:
    """
    Request MAVLink message in a desired frequency,
    documentation for SET_MESSAGE_INTERVAL:
        https://mavlink.io/en/messages/common.html#MAV_CMD_SET_MESSAGE_INTERVAL

    Args:
        message_id (int): MAVLink message ID
        frequency_hz (float): Desired frequency in Hz
    """
    frequency = 1e6 / frequency_hz

    return master.mav.command_long_send(
        master.target_system,
        master.target_component,
        mavutil.mavlink.MAV_CMD_SET_MESSAGE_INTERVAL,
        0,
        message_id,  # The MAVLink message ID
        frequency,  # The interval in hertz
        0,  # Unused, but required
        0,  # Unused, but required
        0,  # Unused, but required
        0,  # Unused, but required
        0,  # Unused, but required
    )


request_message_interval(mavutil.mavlink.MAVLINK_MSG_ID_GPS_RAW_INT, 2)
request_message_interval(mavutil.mavlink.MAVLINK_MSG_ID_GPS_RTK, 1)
request_message_interval(mavutil.mavlink.MAVLINK_MSG_ID_GPS_RTCM_DATA, 3)
request_message_interval(mavutil.mavlink.MAVLINK_MSG_ID_GPS_RTK, 100)


def send_rtcm_msg(data):
    msglen = 180

    if len(data) > msglen * 4:
        return

    # How many messages will we send?
    msgs = 0
    if len(data) % msglen == 0:
        msgs = len(data) // msglen
    else:
        msgs = (len(data) // msglen) + 1

    for a in range(0, msgs):

        flags = 0

        # Set the fragment flag if we're sending more than 1 packet.
        if msgs > 1:
            flags = 1

        # Set the ID of this fragment
        flags |= (a & 0x3) << 1

        # Set an overall sequence number
        flags |= (0 & 0x1f) << 3

        amount = min(len(data) - a * msglen, msglen)
        datachunk = data[a * msglen:a * msglen + amount]

        master.mav.gps_rtcm_data_send(flags, len(datachunk),
                                      bytearray(datachunk.ljust(180, b'\0')))


while True:
    msg = master.recv_match()
    data = s.recv(1024)
    print(data)

    if not data:  # Stop reading when the connection is closed
        break

    # Process the RTCM3 message here
    # Split the data into chunks of 255 bytes or smaller
    send_rtcm_msg(data)
    if not msg:
        continue
    print(msg)
