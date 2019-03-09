import time
import asyncio
from threading import Thread

async def do_some_work(x):
    print("Waiting " + str(x))
    await asyncio.sleep(x)
    print("Finished " + str(x))

def start_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

loop = asyncio.get_event_loop()
tasks = [asyncio.ensure_future(do_some_work(2)),
         asyncio.ensure_future(do_some_work(5))]
#loop.run_until_complete(asyncio.gather(*tasks))

################################################################################

def more_work(x):
  print("More work %s" % x)
  time.sleep(x)
  print("Finished more work %s" % x)

new_loop = asyncio.new_event_loop()
new_loop.call_soon_threadsafe(more_work, 20)
asyncio.run_coroutine_threadsafe(do_some_work(5), new_loop)
asyncio.run_coroutine_threadsafe(do_some_work(10), new_loop)
