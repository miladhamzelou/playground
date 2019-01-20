from telethon import TelegramClient
import socks
from telethon import types
import unittest
import io
import yaml
import os
import logging
# import _thread
import asyncio
import functools

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

    def test_download_urugang(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.download_dialogs("urugang", "+8613588178587"))


    def test_download_u(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.download_dialogs("u", "+8613588034774"))

    def test_download_v(self):
        asyncio.run_until_complete(self.download_dialogs("v", "+8613732215927"))

    def test_download_w(self):
        asyncio.run_until_complete(self.download_dialogs("w", "+8613868136443"))

    async def download_dialog(self, account, client, dialog):
        try:
            key = account + "-" + dialog.name.replace("/", "_")
            if key not in self.config:
                self.config[key] = 0
            with io.open('logs/' + key + ".log", 'a', encoding='utf8') as log:
                print(dialog.name, ": ",self.config[key])
                lastId = None
                tasks = []
                while True:
                    if lastId == self.config[key]:
                        break
                    lastId = self.config[key]
                    async for message in client.iter_messages(dialog.entity, limit=10, min_id=self.config[key], reverse=True):
                        print("\n", message.date, ":", message.id, ":", message.message)
                        if not isinstance(message, types.Message):
                            self.config[key]= message.id
                            continue
                        media = message.media
                        if not isinstance(media, (types.MessageMediaDocument)):
                            self.config[key]= message.id
                            continue
                        for attr in media.document.attributes:
                            if not isinstance(attr, (types.DocumentAttributeFilename)):
                                self.config[key]= message.id
                                continue
                            file_size = 0
                            while [ True ]:
                                file_name = "downloads/" + attr.file_name
                                if os.path.exists(file_name):
                                    stat = os.stat(file_name)
                                    if isinstance(media, types.MessageMediaDocument):
                                        file_size = stat.st_size
                                        if file_size == media.document.size:
                                            break
                                print("\n", attr.file_name, "(", media.document.size, "):", file_size, file=log)
                                print("\n", attr.file_name, "(", media.document.size, "):", file_size)
                                tasks.append(asyncio.create_task(self.download_media(client, message, file_name)))
                                break
                        self.config[key]= message.id

                    for task in tasks:
                        await task
        finally:
            # 3) update config file
            with io.open(self.configFile, 'w', encoding='utf8') as outfile:
                yaml.dump(self.config, outfile, default_flow_style=False, allow_unicode=True)

    async def download_media(self, client, message, file_name):
        print("========", file_name)
        await client.download_media(message, file_name)
        print("--------", file_name)

    async def download_dialogs(self, account, phone):
        # 0) setup
        api_id = 478514
        api_hash = '6e152cff4b48d83171b509923667ed47'
        # proxy = (socks.SOCKS5, 'localhost', 1080)
        proxy = (socks.SOCKS5, 'phobos.public.opennetwork.cc', 1090, False,
         '353916769', 'dN2TTGIm')

        # proxy = None
        client = TelegramClient(account, api_id, api_hash, proxy=proxy)
        # client.session.set_dc(2, '149.154.167.50', 443) # urugang
        # 1) start client
        await client.start(max_attempts=1, phone=phone)
        # # 2) iterate all dialogs
        for dialog in await client.get_dialogs():
            await self.download_dialog(account, client, dialog)
