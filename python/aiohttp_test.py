import aiohttp
import asyncio
import unittest
import asynctest
from aioresponses import aioresponses


SERVER_URL = "http://localhost"
async def get_username(loop):
    async with aiohttp.ClientSession(loop=loop) as session:
        async with session.get(f"{SERVER_URL}/profile") as response:
            data = await response.json()
            return data["user"]

class AiohttpTest(asynctest.TestCase):
    remote_content = {
        "/profile": {
            "user": "Ada"
        }
    }

    def setUp(self):
        mocked = aioresponses()
        mocked.start()
        for url, payload in self.remote_content.items():
            mocked.get(SERVER_URL + url, payload=payload)
        self.addCleanup(mocked.stop)

    async def test_get_username(self):
        u = await get_username(self.loop)
        assert( u == "Ada")


