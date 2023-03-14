import asyncio
import os

from sunsynk.client import SunsynkClient
from datetime import date


async def main():
    sunsynk_username = os.getenv('SUNSYNK_USERNAME')
    sunsynk_password = os.getenv('SUNSYNK_PASSWORD')

    async with SunsynkClient(sunsynk_username, sunsynk_password) as client:
        plants = await client.get_plants()
        for plant in plants: 
            measurements = await client.get_historic_graph_data(plant.id,date(2023,3,11))

    battery = measurements.get_battery()
    consumption = measurements.get_consumption()
    grid_usage = measurements.get_grid_usage()
    solar_production = measurements.get_solar_production()
    state_of_charge = measurements.get_state_of_charge()
    print('Done!')

asyncio.run(main())