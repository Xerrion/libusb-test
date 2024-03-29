#!/usr/bin/env python3

import asyncio
from mavsdk import System


async def run():
    # Init the drone
    drone = System(mavsdk_server_address='localhost', port=50051)
    await drone.connect(system_address="serial://COM3:9600")
    print("Waiting for drone to connect...")

    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"-- Connected to drone!")
            break
    async for position in drone.telemetry.position():
        print(position)

    # Start the tasks
    asyncio.ensure_future(print_battery(drone))
    asyncio.ensure_future(print_gps_info(drone))
    asyncio.ensure_future(print_in_air(drone))
    asyncio.ensure_future(print_position(drone))


async def print_battery(drone):
    async for battery in drone.telemetry.battery():
        print(f"Battery: {battery.remaining_percent}")


async def print_gps_info(drone):
    async for gps_info in drone.telemetry.gps_info():
        print(f"GPS info: {gps_info}")


async def print_in_air(drone):
    async for in_air in drone.telemetry.in_air():
        print(f"In air: {in_air}")


async def print_position(drone):
    async for position in drone.telemetry.position():
        print(position)


if __name__ == "__main__":
    # Start the main function
    asyncio.ensure_future(run())

    # Runs the event loop until the program is canceled with e.g. CTRL-C
    asyncio.get_event_loop().run_forever()
