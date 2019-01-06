from telethon import TelegramClient, sync
import socks
from telethon import types
import unittest
import io
import yaml
import os
import logging

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
            proxy = (socks.SOCKS5, 'localhost', 6153)
            # proxy = (socks.HTTP, '127.0.0.1', 8087)
            # proxy = None
            client = TelegramClient(account, api_id, api_hash, proxy=proxy)
            # client.session.set_dc(2, '149.154.167.50', 443) # urugang
            # client.session.set_dc(1, '149.154.175.50', 443)

            # 1) start client
            client.start(max_attempts=1, phone=phone)
            # # 2) iterate all dialogs
            for dialog in client.get_dialogs():
                key = account + "-" + dialog.name.replace("/", "_")
                print(self.config)
                if key not in self.config:
                    #self.config[key] = dialog.message.id-30000
                    self.config[key] = 0
                with io.open('logs/' + key + ".log", 'a', encoding='utf8') as log:
                    print(dialog.name, ": ",self.config[key])
                    lastId = None
                    while True:
                        if lastId == self.config[key]:
                            break
                        lastId = self.config[key]
                        for message in client.iter_messages(dialog.entity, limit=10, min_id=self.config[key], reverse=True):
                            print("\n", message.date, ":", message.id, ":", message.message, file=log)
                            if not isinstance(message, types.Message):
                                self.config[key]= message.id
                                continue
                            media = message.media
                            if not isinstance(media, (types.MessageMediaDocument)):
                                self.config[key]= message.id
                                continue
                            attrs = media.document.attributes
                            if not isinstance(attrs[0], (types.DocumentAttributeFilename)):
                                self.config[key]= message.id
                                continue
                            for attr in attrs:
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
                                    client.download_media(message, file_name)
                                    break
                            self.config[key]= message.id
        # except RuntimeError as e:
        #     print("Unexpected error:", e.args)
        finally:
            # 3) update config file
            with io.open(self.configFile, 'w', encoding='utf8') as outfile:
                yaml.dump(self.config, outfile, default_flow_style=False, allow_unicode=True)
