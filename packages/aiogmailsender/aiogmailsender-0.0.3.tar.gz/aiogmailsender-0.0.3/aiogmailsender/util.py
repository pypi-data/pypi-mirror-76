import asyncio


class IdGenerator:
    def __init__(self, prefix):
        self.id = 0
        self.prefix = prefix
        self.lock = asyncio.Lock()

    async def generate(self):
        async with self.lock:
            self.id += 1
            return f'{self.prefix}{self.id}'
