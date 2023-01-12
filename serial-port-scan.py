import serial.tools.list_ports


def list_open_serial_ports():
    """ Lists serial port names with description """
    serial_ports = []
    for port in list(serial.tools.list_ports.comports()):
        serial_ports.append({"port": port.name, "desc": port.description})
    return serial_ports


if __name__ == '__main__':
    print(list_open_serial_ports())
