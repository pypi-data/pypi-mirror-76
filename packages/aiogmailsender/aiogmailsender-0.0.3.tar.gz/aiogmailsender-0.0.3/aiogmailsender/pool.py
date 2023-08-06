import asyncio
import logging

import aiosmtplib

from .client import Notifier
from .util import IdGenerator

ID_GENERATOR = IdGenerator('pool-')


class Pool(Notifier):
    def __init__(self):
        self.id = 0
        self.size = 0
        self.clients = None

        self.available = True
        self.wake_up_after_task = None

    @classmethod
    async def create(cls, size, client_factory):
        self = cls()
        self.id = await ID_GENERATOR.generate()
        logging.debug('%s: create a pool', self.id)

        self.size = size
        self.clients = asyncio.Queue()

        id_generator = IdGenerator(f'{self.id}-client-')

        async def _create_client():
            client = await client_factory.new_client(self, await id_generator.generate())
            self.clients.put_nowait(client)

        await asyncio.gather(*[_create_client() for _ in range(size)])
        return self

    def handle(self, task):
        async def _handle():
            client = await self.clients.get()
            try:
                result = await client.send(task.message)
                task.set_result(result)
            except Exception as exception:
                task.set_exception(exception)
            self.clients.put_nowait(client)

        asyncio.create_task(_handle())

    def notify_failure(self, exception):
        if not self.available:
            return

        if isinstance(exception, aiosmtplib.errors.SMTPSenderRefused):
            if exception.code == 421:
                logging.debug("%s: 421 occurred", self.id)
                self.available = False

        elif isinstance(exception, aiosmtplib.errors.SMTPDataError):
            if exception.code == 550:
                logging.error("%s: 550 occurred", self.id)
                self.available = False

                self.wake_up_after(3600)

    def wake_up_after(self, sleep):
        if self.wake_up_after_task is not None and not self.wake_up_after_task.done():
            self.wake_up_after_task.cancel()

        async def func():
            logging.debug('%s: sleep %s seconds and will wake up', self.id, sleep)
            await asyncio.sleep(sleep)
            self.available = True

        self.wake_up_after_task = asyncio.create_task(func())

    def notify_success(self):
        if self.available:
            return

        logging.debug('%s: back to available', self.id)
        self.available = True
