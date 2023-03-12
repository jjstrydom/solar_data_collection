import aiohttp

from weather.weather import Weather

class  WeatherClient:

    def __init__(self, base_url=None):
        self.base_url = 'https://api.open-meteo.com' if base_url is None else base_url
        self.session = aiohttp.ClientSession()

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        await self.close()

    async def close(self):
        await self.session.close()
    
    async def get_data(self,from_date,to_date,lat=-25.89,lon=28.22):
        resp = await self.__get(f'v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m,precipitation,cloudcover,cloudcover_low,cloudcover_mid,cloudcover_high,windspeed_10m,soil_temperature_0cm&start_date={from_date}&end_date={to_date}&timezone=Africa%2FCairo')
        body = await resp.json()
        data = body['hourly']
        return Weather(data)

    async def __get(self, path, attempts=1):
        print(self.__url(path))
        resp = await self.session.get(self.__url(path), headers=self.__headers(), timeout=20)
        if resp.status == 401 and attempts == 1:
            await self.login()
            return await self.__get(path, attempts=attempts+1)
        return resp

    def __headers(self):
        headers = {
            "Content-Type": "application/json"
        }
        # if self.access_token:
        #     headers['Authorization'] = f"Bearer {self.access_token}"
        return headers
    
    def __url(self, path):
        return f'{self.base_url}/{path}'
    

