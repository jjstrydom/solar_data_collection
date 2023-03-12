import aiohttp

from sunsynk.plant import Plant
from sunsynk.day_graph import DayGraph


class InvalidCredentialsException(Exception):
    def __init__(self):
        super().__init__('Invalid username or password')


class SunsynkClient:

    @classmethod
    async def create(cls, username, password, base_url=None):
        self = SunsynkClient(username, password, base_url)
        return await self.login()

    def __init__(self, username, password, base_url=None):
        self.base_url = 'https://pv.inteless.com' if base_url is None else base_url
        self.session = aiohttp.ClientSession()
        self.access_token = None
        self.refresh_token = None
        self.username = username
        self.password = password

    async def __aenter__(self):
        await self.login()
        return self

    async def __aexit__(self, *args):
        await self.close()

    async def close(self):
        await self.session.close()

    async def get_plants(self):
        resp = await self.__get('api/v1/plants?page=1&limit=10&name=&status=')
        body = await resp.json()
        plants = body['data']['infos']
        return [Plant(data) for data in plants]
    
    async def get_historic_graph_data(self, plant_id, date):
        api_str = f'api/v1/plant/energy/{plant_id}/day?lan=en&date={date}&id={plant_id}'
        print(api_str)
        resp = await self.__get(api_str)
        body = await resp.json()
        graphs = body['data']['infos']
        return DayGraph(graphs, date)

    async def __get(self, path, attempts=1):
        resp = await self.session.get(self.__url(path), headers=self.__headers(), timeout=20)
        if resp.status == 401 and attempts == 1:
            await self.login()
            return await self.__get(path, attempts=attempts+1)
        return resp

    def __headers(self):
        headers = {
            "Content-Type": "application/json"
        }
        if self.access_token:
            headers['Authorization'] = f"Bearer {self.access_token}"
        return headers

    async def login(self):
        payload = {
            'username': self.username,
            'password': self.password,
            'grant_type': 'password',
            'client_id': 'csp-web'
        }
        resp = await self.session.post(self.__url('oauth/token'),
                                 headers={"Content-Type": "application/json"},
                                 timeout=20,
                                 json=payload)
        if resp.status == 200:
            resp_body = await resp.json()
            if resp_body['success']:
                self.access_token = resp_body['data']['access_token']
                self.refresh_token = resp_body['data']['refresh_token']
                return self
        raise InvalidCredentialsException()

    def __url(self, path):
        return f'{self.base_url}/{path}'
