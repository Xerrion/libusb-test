import serial


try:
    ser = serial.Serial("COM6", "9600", timeout=1)

except Exception as e:
    if "Access is denied" in str(e):
        print("Device probably already in use")
    if "The system cannot find the file specified" in str(e):
        print("Device probably not connected")
