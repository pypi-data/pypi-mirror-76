from aiohttp import ClientSession
from .exceptions import ResponseError


class HTTPClient:
    def __init__(self):
        self.url = 'https://opentdb.com/api.php'
        self.session = None

    async def set_session(self):
        self.session = ClientSession()

    async def get(self, url=None, params: dict = None):
        url = url or self.url
        params = params or {}
        if not self.session:
            await self.set_session()
        async with self.session.get(url, params=params) as r:
            res = await r.json()
        if res['response_code'] == 1:
            raise ResponseError()
        return res

    async def close(self):
        await self.session.close()
        self.session = None
