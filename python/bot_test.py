from telethon import TelegramClient, sync, utils
import socks
import datetime
from telethon import types
import unittest
import asyncio
import io
import yaml
import sys
import os

class BotTestCase(unittest.TestCase):
    #def setup(self):
    configFile = "telethon.yaml"

    def test_bot(self):
        # cfg = {
        #     't.me/shuwu': datetime.date(2018,12,28),
        # }
        # with io.open('telethon.yaml', 'w', encoding='utf8') as outfile:
        #     yaml.dump(cfg, outfile, default_flow_style=False, allow_unicode=True)
        if os.path.exists(self.configFile):
            with open(self.configFile, 'r') as ymlfile:
                cfg = yaml.load(ymlfile)
        else:
            cfg = {}
        api_id = 478514
        api_hash = '6e152cff4b48d83171b509923667ed47'
        proxy = (socks.SOCKS5, 'localhost', 1080)
        client = TelegramClient('urugang', api_id, api_hash, proxy=proxy)
        try:
            client.start()
            for dialog in client.get_dialogs():
                print(dialog.name, dialog.date)
                if dialog.name in cfg:
                    timestamp = cfg[dialog.name]
                else:
                    timestamp = datetime.date(2018,12,28)
                with io.open('log/'+dialog.name+ ".log", 'a', encoding='utf8') as log:
                    for message in client.iter_messages(dialog.entity, limit=1, offset_date=timestamp):
                        print(message.message, file=log)
                        cfg[dialog.name]= message.date
            with io.open('telethon.yaml', 'w', encoding='utf8') as outfile:
                yaml.dump(cfg, outfile, default_flow_style=False, allow_unicode=True)
            return
        except RuntimeError as e:
            print("Unexpected error:", e.args)

        #print(client.get_me().stringify())
        #client.send_message('urugang', 'Hello! Talking to you from Telethon')
        #client.send_file('username', '/home/myself/Pictures/holidays.jpg')
        #client.download_profile_photo('urugang')
        # lastTimestamp = datetime.date(2018,12,20)
        # loop = asyncio.get_event_loop()
        # for url, timestamp in cfg.items():
        #     print("\n", url, timestamp)
        #     for message in client.iter_messages(url, limit=1000, offset_date=timestamp):
        #         if not isinstance(message, types.Message):
        #             continue
        #         media = message.media
        #         cfg[url] = message.date
        #         if not isinstance(media, (types.MessageMediaDocument)):
        #             continue
        #         attrs = media.document.attributes
        #         if not isinstance(attrs[0], (types.DocumentAttributeFilename)):
        #             continue
        #         for attr in attrs:
        #             print(attr.file_name)
        # with io.open('telethon.yaml', 'w', encoding='utf8') as outfile:
        #     yaml.dump(cfg, outfile, default_flow_style=False, allow_unicode=True)
