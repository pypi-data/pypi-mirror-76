import asyncio
import types
import logging

from .pool import Pool
from .client import ClientFactory


class Task:
    def __init__(self, message):
        self.message = message
        self.event = asyncio.Event()
        self.result = None
        self.exception = None

    async def get_result(self):
        await self.event.wait()

        if self.exception:
            raise self.exception
        return self.result

    def set_result(self, result):
        self.result = result
        self.event.set()

    def set_exception(self, exception):
        self.exception = exception
        self.event.set()


class Scheduler:
    def __init__(self):
        self.rate_limit = None
        self.tasks = asyncio.Queue()

        self.pools = asyncio.Queue()
        self.pool_count = 0

    @classmethod
    async def create(cls, accounts, rate_limit=60, pool_size=2, **options):
        self = cls()
        self.rate_limit = rate_limit
        self.pool_count = len(accounts)

        async def _create_pool(username, password):
            pool = await Pool.create(pool_size, ClientFactory(username, password, **options))
            self.pools.put_nowait(pool)

        await asyncio.gather(*[_create_pool(username, password) for username, password in accounts])
        return self

    def schedule(self, task):
        self.tasks.put_nowait(task)

    async def start(self):
        logging.debug('scheduler start')
        while True:
            task = await self.tasks.get()
            pool = await self.pop_pool()

            pool.handle(task)
            self.pools.put_nowait(pool)

            if self.rate_limit > 0:
                await asyncio.sleep(60 / self.rate_limit)

    async def pop_pool(self):
        try_ = 0
        while True:
            pool = await self.pools.get()
            try_ += 1
            if pool.available:
                return pool

            if try_ % self.pool_count == 0:
                logging.debug('all pools are not available. sleep 1 second and retry')
                await asyncio.sleep(1)

            self.pools.put_nowait(pool)


NS = types.SimpleNamespace()


class Sender:
    def __init__(self):
        self.scheduler = None

    @classmethod
    async def create(cls, accounts, **options):
        self = cls()

        scheduler = await Scheduler.create(accounts, **options)
        asyncio.create_task(scheduler.start())
        self.scheduler = scheduler
        return self

    def send(self, message):
        task = Task(message)
        self.scheduler.schedule(task)

        return asyncio.create_task(task.get_result())
