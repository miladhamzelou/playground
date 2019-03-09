import asynctest
from aioresponses import aioresponses


class AsyncTest(asynctest.TestCase):

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
        assert u == "Ada"
