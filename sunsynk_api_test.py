import asyncio
import os

from sunsynk.client import SunsynkClient
from datetime import date


async def main():
    sunsynk_username = os.getenv('SUNSYNK_USERNAME')
    sunsynk_password = os.getenv('SUNSYNK_PASSWORD')

    print('-'*52)
    print(sunsynk_username)
    print(sunsynk_password)
    print('-'*52)

    async with SunsynkClient(sunsynk_username, sunsynk_password) as client:
        plants = await client.get_plants()
        for plant in plants: 
            print(plant.id, plant.master_id)
            body = await client.get_historic_graph_data(plant.id,date(2023,3,11))
            
    print('Done!')

asyncio.run(main())