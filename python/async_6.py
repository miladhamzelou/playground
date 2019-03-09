import concurrent.futures
import asyncio
import time

def long_task(t):
    time.sleep(1)
    return len(t)

executor = concurrent.futures.ThreadPoolExecutor(max_workers=4)
inputs = ["a", "aa"]
loop = asyncio.get_event_loop()
futures = [loop.run_in_executor(executor, long_task, i) for i in inputs]
results = loop.run_until_complete( asyncio.gather(*futures))
for (i, result) in zip(inputs, results):
    print(i, result)
