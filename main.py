import sys

import usb.core

"""
This sample demonstrates how to use the pyusb to read data from a PX4 (CubeOrange)
Vendor Id: 0x2dae
Product Id: 0x1016

Interface 1 and 3 has out data
Interface 1 has out data on endpoint 0x2: Bulk OUT
Interface 1 has out data on endpoint 0x82: Bulk IN
Interface 3 has out data on endpoint 0x4: Bulk OUT

These ofcause comes out as a byte array

    INTERFACE 1: CDC Data ==================================
     bLength            :    0x9 (9 bytes)
     bDescriptorType    :    0x4 Interface
     bInterfaceNumber   :    0x1
     bAlternateSetting  :    0x0
     bNumEndpoints      :    0x2
     bInterfaceClass    :    0xa CDC Data
     bInterfaceSubClass :    0x0
     bInterfaceProtocol :    0x0
     iInterface         :    0x0
     ENDPOINT 0x2: Bulk OUT ===============================
       bLength          :    0x7 (7 bytes)
       bDescriptorType  :    0x5 Endpoint
       bEndpointAddress :    0x2 OUT
       bmAttributes     :    0x2 Bulk
       wMaxPacketSize   :   0x40 (64 bytes)
       bInterval        :    0x0 
     ENDPOINT 0x82: Bulk IN ===============================
       bLength          :    0x7 (7 bytes)
       bDescriptorType  :    0x5 Endpoint
       bEndpointAddress :   0x82 IN
       bmAttributes     :    0x2 Bulk
       wMaxPacketSize   :   0x40 (64 bytes)
       bInterval        :    0x0 

    INTERFACE 3: CDC Data ==================================
     bLength            :    0x9 (9 bytes)
     bDescriptorType    :    0x4 Interface
     bInterfaceNumber   :    0x3
     bAlternateSetting  :    0x0
     bNumEndpoints      :    0x2
     bInterfaceClass    :    0xa CDC Data
     bInterfaceSubClass :    0x0
     bInterfaceProtocol :    0x0
     iInterface         :    0x0 
     ENDPOINT 0x4: Bulk OUT ===============================
       bLength          :    0x7 (7 bytes)
       bDescriptorType  :    0x5 Endpoint
       bEndpointAddress :    0x4 OUT
       bmAttributes     :    0x2 Bulk
       wMaxPacketSize   :   0x40 (64 bytes)
       bInterval        :    0x0 
"""

# The Cube
device: usb.core.Device = usb.core.find(idVendor=0x2dae, idProduct=0x1016)
interfaces: usb.core.Interface = device[0].interfaces()
# i = interfaces.bInterfaceNumber
device.reset()

for interface in [interfaces[1], interfaces[3]]:
    # print(interface)
    endpoints = interface.endpoints()
    i = interface.bInterfaceNumber
    if device.is_kernel_driver_active(i):
        try:
            device.detach_kernel_driver(i)
        except usb.core.USBError as e:
            sys.exit("Could not detatch kernel driver from interface({0}): {1}".format(i, str(e)))
    for endpoint in endpoints:
        address = endpoint.bEndpointAddress

        try:
            # Read the 64 bytes from the endpoint
            print(device.read(address, 0x40), f"address: {endpoint}")

            # byte_arr = bytearray(device.read(address, 0x40))
            # print(byte_arr)
        except Exception:
            pass

while True:
    try:
        # Continuously read 64 (40 hex) bytes from endpoint 130 (82 hex)
        print(bytearray(device.read(0x82, 0x40).tobytes()))
    except usb.core.USBError as e:
        print(e)
        pass
