import asyncio

from weather.client import WeatherClient
from datetime import date

async def main():

    async with WeatherClient() as client:
        weather = await client.get_data(date(2023,3,11),date(2023,3,13))
    
    temperature_2m = weather.get_temperature_2m()
    relativehumidity_2m = weather.get_relativehumidity_2m()
    precipitation_probability = weather.get_precipitation_probability()
    precipitation = weather.get_precipitation()
    surface_pressure = weather.get_surface_pressure()
    cloudcover = weather.get_cloudcover()
    cloudcover_low = weather.get_cloudcover_low()
    cloudcover_mid = weather.get_cloudcover_mid()
    cloudcover_high = weather.get_cloudcover_high()
    windspeed_10m = weather.get_windspeed_10m()
    winddirection_10m = weather.get_winddirection_10m()
    soil_temperature_0cm = weather.get_soil_temperature_0cm()
    print('Done!')

asyncio.run(main())