from telethon import TelegramClient, sync
import socks
from telethon import types
import unittest
import io
import yaml
import os
import logging

logging.basicConfig(level=logging.INFO)

class TelethonTestCase(unittest.TestCase):
    configFile = "telethon.yaml"
    config = {}


    def setUp(self):
        if not os.path.exists("logs"):
            os.mkdir("logs")
        if not os.path.exists("downloads"):
            os.mkdir("downloads")
        if os.path.exists(self.configFile):
            with open(self.configFile, 'r') as ymlfile:
                self.config = yaml.load(ymlfile)

    def test_download_urugang(self):
        self.download("urugang", "+8613588178587")

    def test_download_u(self):
        self.download("u", "+8613588034774")

    def test_download_v(self):
        self.download("v", "+8613732215927")

    def test_download_w(self):
        self.download("w", "+8613868136443")

    def download(self, account, phone):
        try:
            # 0) setup
            api_id = 478514
            api_hash = '6e152cff4b48d83171b509923667ed47'
            proxy = (socks.SOCKS5, 'localhost', 1080)
            # proxy = (socks.HTTP, '127.0.0.1', 8087)
            # proxy = None
            client = TelegramClient(account, api_id, api_hash, proxy=proxy)
            # client.session.set_dc(2, '149.154.167.50', 443) # urugang
            # client.session.set_dc(1, '149.154.175.50', 443)

            # 1) start client
            client.start(max_attempts=1, phone=phone)
            # # 2) iterate all dialogs
            for dialog in client.get_dialogs():
                print("===+++dialog")

                if dialog.name not in self.config:
                    self.config[account + "-" + dialog.name] = dialog.message.id-30
                with io.open('logs/' + account+ "-" + dialog.name.replace("/", "_")+ ".log",
                             'a', encoding='utf8') as log:
                    print(dialog.name, self.config[account + "-" + dialog.name])
                    lastId = None
                    while True:
                        if lastId == self.config[account + "-" + dialog.name]:
                            break
                        lastId = self.config[account + "-" + dialog.name]
                        for message in client.iter_messages(dialog.entity,
                                                                 limit=10,
                                                                 min_id=self.config[account + "-" + dialog.name],
                                                                 reverse=True):
                            print("\n", message.date, ":", message.message, file=log)
                            self.config[account + "-" + dialog.name]= message.id
                            if not isinstance(message, types.Message):
                                continue
                            media = message.media
                            if not isinstance(media, (types.MessageMediaDocument)):
                                continue
                            attrs = media.document.attributes
                            if not isinstance(attrs[0], (types.DocumentAttributeFilename)):
                                continue
                            for attr in attrs:
                                print("\n", attr.file_name, file=log)
                                print("\n", attr.file_name)
                                client.download_media(message, "downloads/" + attr.file_name)
            # 3) update config file
            with io.open(self.configFile, 'w', encoding='utf8') as outfile:
                yaml.dump(self.config, outfile, default_flow_style=False, allow_unicode=True)
        except RuntimeError as e:
            print("Unexpected error:", e.args)
