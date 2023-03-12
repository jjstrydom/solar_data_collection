import asyncio

from weather.client import WeatherClient
from datetime import date

async def main():

    async with WeatherClient() as client:
        weather = await client.get_data(date(2023,3,11),date(2023,3,13))
        
    print('Done!')

asyncio.run(main())