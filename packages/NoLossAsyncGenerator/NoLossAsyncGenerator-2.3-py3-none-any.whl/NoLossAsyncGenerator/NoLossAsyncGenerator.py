'''
Asynchronous generator without any data loss in case that handling one message costs too much time.
'''
import asyncio
from ensureTaskCanceled.ensureTaskCanceled import ensureTaskCanceled


class NoLossAsyncGenerator:
    def __init__(self, raw_async_iterater=None):
        self.q = asyncio.Queue()
        self.raw_async_iterater = raw_async_iterater
        self._activate_task = asyncio.create_task(self._activate())

    async def _activate(self):
        if self.raw_async_iterater:
            async for msg in self.raw_async_iterater:
                self.q.put_nowait(msg)

    def __aiter__(self):
        return self

    @property
    def left(self):
        return self.q.qsize()

    async def __anext__(self):
        try:
            return await self.q.get()
        finally:
            self.q.task_done()

    async def wait_empty(self):
        '''
        等待下一次空数据的机会

        :return:
        '''
        await self.q.join()

    async def close(self):
        await self.wait_empty()
        await ensureTaskCanceled(self._activate_task)


# def NoLossAsyncGenerator(raw_async_iterater):
#     async def no_data_loss_async_generator_wrapper(raw_async_iterater):
#         q = asyncio.Queue()
#
#         async def yield2q(raw_async_iterater, q: asyncio.Queue):
#             async for msg in raw_async_iterater:
#                 q.put_nowait(msg)
#
#         asyncio.create_task(yield2q(raw_async_iterater, q))
#         while True:
#             msg = await q.get()
#             # generator.left = q.qsize()
#             # generator.__dict__['left'] = q.qsize()
#             yield msg
#
#     generator = no_data_loss_async_generator_wrapper(raw_async_iterater)
#     return generator


def no_data_loss_async_generator_decorator(async_generator_function):
    async def g(*args, **kwargs):
        async for msg in NoLossAsyncGenerator(async_generator_function(*args, **kwargs)):
            yield msg

    return g


if __name__ == '__main__':

    async def test_no_data_loss_async_generator():
        async def g():
            n = 0
            while True:
                yield n
                n += 1
                await asyncio.sleep(1)

        m = 0
        g = NoLossAsyncGenerator(g())
        async for n in g:
            print(n)
            print(f'left:{g.left}')
            m += 1
            if m <= 5:
                await asyncio.sleep(2)


    async def test_no_data_loss_async_generator_decorator():
        @no_data_loss_async_generator_decorator
        async def g():
            n = 0
            while True:
                yield n
                n += 1
                await asyncio.sleep(1)

        m = 0
        async for n in g():
            print(n)
            m += 1
            if m <= 5:
                await asyncio.sleep(2)


    asyncio.run(test_no_data_loss_async_generator())
