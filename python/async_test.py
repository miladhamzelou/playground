import unittest
import types
import asyncio
import random

# 1. 普通汉书
def function():
    return 1

# 2. 生成器函数
def generator():
    yield 1

# 3. 异步函数（协程）
async def async_function():
    return 1

# 4. 异步生成器
async def async_generator():
    yield 1


def run(coroutine):
    try:
        coroutine.send(None)
    except StopIteration as e:
        return e.value

async def await_coroutine():
    result = await async_function()

class Potato:
    @classmethod
    def make(cls, num, *args, **kws):
        potatos = []
        for i in range(num):
            potatos.append(cls.__new__(cls, *args, **kws))
        return potatos

all_potatos = Potato.make(5)

async def take_potatos(num):
    count = 0
    while True:
        if len(all_potatos) == 0:
            await ask_for_potato()
        potato = all_potatos.pop()
        yield potato
        count += 1
        if count == num:
            break

async def ask_for_potato():
    await asyncio.sleep(random.random())
    all_potatos.extend(Potato.make(random.randint(1, 10)))

async def buy_potatos():
    bucket = []
    async for p in take_potatos(3):
        bucket.append(p)

class AsyncTest(unittest.TestCase):
    """
    Test the add function from the mymath library
    """
    def test_async1(self):
        self.assertTrue(type(function) is types.FunctionType)
        self.assertTrue(type(generator()) is types.GeneratorType)
        self.assertTrue(type(async_generator()) is types.AsyncGeneratorType)
        # self.assertTrue(type(async_function()) is types.CoroutineType)
        run(await_coroutine())

    def test_async2(self):
        loop = asyncio.get_event_loop()
        res = loop.run_until_complete(buy_potatos())
        loop.close()

