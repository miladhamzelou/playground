import asyncio
import aiohttp

async def fetch(url):
    """Perform an HTTP GET to the URL and print the response"""
    async with aiohttp.request('GET', url) as response:
        text = await response.text()
        return text

# Get a reference to the event loop
loop = asyncio.get_event_loop()

# Create the batch of requests we wish to execute
requests = [asyncio.ensure_future(fetch("https://baidu.com")),
            asyncio.ensure_future(fetch("https://baidu.com"))]

# Run the batch
responses = loop.run_until_complete(asyncio.gather(*requests))

# Examine responses
# for resp in responses:
#   print(resp)
