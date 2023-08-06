import logging
import asyncio

import aiosmtplib


class Notifier:
    def notify_failure(self, exception):
        raise RuntimeError('no implementation')

    def notify_success(self):
        raise RuntimeError('no implementation')


class NoopNotifier(Notifier):

    def notify_failure(self, exception):
        pass

    def notify_success(self):
        pass


class ClientFactory:
    def __init__(self, username, password, **options):
        self.username = username
        self.password = password
        self.options = options

    async def new_client(self, notifier, id_):
        return await Client.create(self.username, self.password, notifier=notifier, id_=id_, **self.options)


class Client:
    def __init__(self):
        self.id = None
        self.username = None
        self.password = None

        self.retry = 0
        self.backoff = 0
        self.backoff_limit = 0
        self.notifier = None

        self.conn = None

    @classmethod
    async def create(
            cls, username, password,
            retry=10,
            backoff=30,
            backoff_limit=600,
            notifier=NoopNotifier(),
            id_=''
    ):
        self = cls()
        self.id = id_ if id_ else id(self)
        logging.debug('%s: create a create', self.id)

        self.username = username
        self.password = password

        self.retry = retry
        self.backoff = backoff
        self.backoff_limit = backoff_limit
        self.notifier = notifier

        await self.connect()
        return self

    async def send(self, message):
        retry = self.retry
        backoff = self.backoff

        while True:
            try:
                if not self.conn.is_connected:
                    await self.connect()
                logging.debug('%s: try to send a message (%s)', self.id, message['Subject'])
                result = await self.conn.send_message(message)
                self.notifier.notify_success()
                logging.debug('%s: successfully sent a message (%s)', self.id, message['Subject'])

                return result
            except aiosmtplib.errors.SMTPServerDisconnected as e:
                self.notifier.notify_failure(e)

                if retry == 0:
                    self._raise(e)
                logging.debug('%s: SMTP server is disconnected', self.id)
                logging.debug('%s: retry (%s left)', self.id, retry - 1)
                retry -= 1

            except (aiosmtplib.errors.SMTPDataError, aiosmtplib.errors.SMTPSenderRefused) as e:
                self.notifier.notify_failure(e)
                if e.code == 550:
                    logging.debug('%s: 550 occurred while sending email: username=%s', self.id, self.username)

                if e.code != 421:
                    self._raise(e)
                if retry == 0:
                    self._raise(e)
                logging.debug('%s: 421 occurred while sending email: %s', self.id, e.args)
                logging.debug('%s: sleep (%s seconds) and retry (%s left)', self.id, backoff, retry - 1)
                await asyncio.sleep(backoff)

                retry -= 1
                backoff *= 2
                if self.backoff_limit < backoff:
                    backoff = self.backoff_limit

            except Exception as e:
                self._raise(e)

    async def connect(self):
        logging.debug('%s: try to connect', self.id)
        conn = aiosmtplib.SMTP(hostname='smtp.gmail.com', port=587, start_tls=True)
        await conn.connect()
        await conn.login(self.username, self.password)
        self.conn = conn

    def __del__(self):
        if self.conn is not None:
            self.conn.close()

    def _raise(self, e):
        if self.conn is not None:
            self.conn.close()

        self.conn.close()
        raise e
