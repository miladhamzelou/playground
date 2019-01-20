from telethon import TelegramClient, types
import socks
import unittest
import io
import yaml
import os
import logging
import asyncio

logging.basicConfig(level=logging.ERROR)

class TelethonTestCase(unittest.TestCase):
    configFile = "telethon.yaml"
    config = None

    def setUp(self):
        if not os.path.exists("logs"):
            os.mkdir("logs")
        if not os.path.exists("downloads"):
            os.mkdir("downloads")
        if os.path.exists(self.configFile):
            with open(self.configFile, 'r') as ymlfile:
                self.config = yaml.load(ymlfile)
        if self.config == None:
            self.config = {}

    async def download_dialog(self, account, client, dialog):
        try:
            key = account + "-" + dialog.name.replace("/", "_")
            if key not in self.config:
                self.config[key] = 0
            with io.open('logs/' + key + ".txt", 'a', encoding='utf8') as log:
                min_id = self.config[key]
                print('dialog[{0}] = {1}'.format(dialog.name, min_id))
                while True:
                    tasks = []
                    async for message in client.iter_messages(dialog.entity, limit=200, min_id=min_id, reverse=True):
                        self.download_message(log, message)
                        tasks.append(self.download_media(client, message))
                        min_id = message.id
                    await asyncio.gather(*tasks)
                    if min_id == self.config[key]:
                        break
                    self.config[key] = min_id
        finally:
            with io.open(self.configFile, 'w', encoding='utf8') as outfile:
                yaml.dump(self.config, outfile, default_flow_style=False, allow_unicode=True)

    def download_message(self, log, message):
        print("\n", message.date, ":", message.id, ":", message.message, file=log)
        print("\n", message.date, ":", message.id, ":", message.message)

    async def download_media(self, client, message):
        if not isinstance(message, types.Message):
            return
        media = message.media
        if not isinstance(media, (types.MessageMediaDocument)):
            return
        for attr in media.document.attributes:
            if not isinstance(attr, (types.DocumentAttributeFilename)):
                continue
            file_size = 0
            while [ True ]:
                file_name = "downloads/" + attr.file_name
                file_size = 0
                if os.path.exists(file_name):
                    stat = os.stat(file_name)
                    file_size = stat.st_size
                    if file_size == media.document.size:
                        break
                print('\n downloading {0} {1} ({2}): {3}'.format(message.id, file_name, media.document.size, file_size))
                await client.download_media(message, file_name)
                stat = os.stat(file_name)
                print('\n downloaded {0} {1} ({2}): {3}'.format(message.id, file_name, media.document.size, stat.st_size))
                break

    async def download_dialogs(self, account, phone):
        api_id = 478514
        api_hash = '6e152cff4b48d83171b509923667ed47'
        proxy = (socks.SOCKS5, 'localhost', 1080)
        # proxy = (socks.SOCKS5, 'phobos.public.opennetwork.cc', 1090, False,
        #          '35316769', 'dN2TTGIm')
        client = TelegramClient(account, api_id, api_hash, proxy=proxy)
        await client.start(max_attempts=1, phone=phone)
        # tasks = []
        for dialog in await client.get_dialogs():
            await self.download_dialog(account, client, dialog)

    def test_download_urugang(self):
        asyncio.run(self.download_dialogs("urugang", "+8613588178587"))

    def test_download_u(self):
        asyncio.run(self.download_dialogs("u", "+8613588034774"))

    def test_download_v(self):
        asyncio.run(self.download_dialogs("v", "+8613732215927"))

    def test_download_w(self):
        asyncio.run(self.download_dialogs("w", "+8613868136443"))
