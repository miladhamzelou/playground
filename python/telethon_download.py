from telethon import TelegramClient, types
from concurrent.futures import ThreadPoolExecutor
import socks
import unittest
import io
import yaml
import os
import logging
import asyncio
import asynctest
import pickle


logging.basicConfig(level=logging.ERROR)

config = None
phone = '08613588178587'
filelist = []
def load_config():
    global config
    with open(phone + ".yml", 'r') as ymlfile:
        config = yaml.load(ymlfile)
    if config is None:
        config = {}

def save_config():
    global phone
    global config
    with open(phone + ".yml", 'w') as ymlfile:
        yaml.dump(config, ymlfile, default_flow_style=False, allow_unicode=True)

def load_filelist():
    global phone
    global filelist
    if os.path.exists(phone + "-filelist.log"):
        with open(phone + "-filelist.log", 'rb') as log:
            filelist = pickle.load(file=log)

def save_filelist():
    global phone
    global filelist
    with open(phone + "-filelist.log", 'wb') as log:
        pickle.dump(filelist, file=log)
    for f in filelist:
        print(f)

async def consumer(qout):
    while True:
        (dialog, id) = await qout.get()

async def worker(name, qin, qout):
    global filter
    global filelist
    file_name = None
    while True:
        try:
            (client, dialog, message) = await qin.get()
            while True:
                if not isinstance(message, types.Message):
                    break
                media = message.media
                if not isinstance(media, (types.MessageMediaDocument)):
                    break
                file_name = None
                for attr in media.document.attributes:
                    if not isinstance(attr, (types.DocumentAttributeFilename)):
                        continue
                    file_name = attr.file_name
                    break
                if file_name is None:
                    break

                if media.document.mime_type == 'image/png':
                    if ".png" not in file_name :
                        file_name += ".png"
                if media.document.mime_type == 'application/pdf':
                    if ".pdf" not in file_name :
                        file_name += ".pdf"
                if not(".pdf" in file_name.lower()  or \
                       ".mobi" in file_name.lower() or \
                       ".azw" in file_name.lower()  or \
                       ".epub" in file_name.lower() or \
                       ".txt" in file_name.lower()):
                       # ".zip" in file_name.lower()  or \
                       # ".rar" in file_name.lower()):
                    break
                if file_name in filter:
                    break
                file_name = 'downloads/' + file_name
                if os.path.exists(file_name):
                    stat = os.stat(file_name)
                    file_size = stat.st_size
                    if file_size == media.document.size:
                        filelist.append(file_name)
                        break
                print("\ndownloading ", message.id,file_name)
                await client.download_media(message, file_name)
                filelist.append(file_name)
                print("\ndownloaded ", message.id, file_name)
                break
            qin.task_done()
            qout.put_nowait((dialog, message.id))
        except:
            qin.put_nowait((client, dialog, message))
            print("put job to queue againt: {}".format(file_name))
        await asyncio.sleep(1)


async def main():
    global config
    global filelist
    load_config()
    load_filelist()
    api_id = 478514
    api_hash = '6e152cff4b48d83171b509923667ed47'
    proxy = (socks.SOCKS5, 'localhost', 6153)
    # proxy = (socks.SOCKS5, 'localhost', 1080)
    # proxy = (socks.SOCKS5, 'phobos.public.opennetwork.cc', 1090, False,
    #          '35316769', 'dN2TTGIm')
    client = TelegramClient('urugang', api_id, api_hash, proxy=proxy)
    qin = asyncio.Queue()
    qout = asyncio.Queue()
    tasks = []
    for i in range(10):
        task = asyncio.create_task(worker(f'worker-{i}', qin, qout))
        tasks.append(task)

    await client.start(max_attempts=1, phone='08613588178587')

    try:
        for dialog in await client.get_dialogs():
            # if 'KindleBot' not in dialog.name:
            #     continue

            if dialog.name not in config:
                min_id = 0
                config[dialog.name] = 0
            else:
                min_id = config[dialog.name]
            print("begin dialog: ", dialog.name, min_id)
            last_id = min_id
            while True:
                async for message in client.iter_messages(dialog.entity,
                                                          limit=200,
                                                          min_id=min_id,
                                                          reverse=True):
                    media = message.media
                    last_id = message.id
                    print('.', end='', flush=True)
                    if not isinstance(media, (types.MessageMediaDocument)):
                        continue
                    qin.put_nowait((client, dialog.name, message))
                if last_id == min_id:
                    break
                min_id = last_id
                if min_id > config[dialog.name] + 200:
                    print("last_id: ", last_id)
                    await qin.join()
                    config[dialog.name] = last_id
                    save_config()
            #await qin.join()
            print("\nend dialog: ", dialog.name, min_id)
            config[dialog.name] = last_id
            save_config()
        print("\njobs :", qin.qsize())
        await qin.join()
    finally:
        save_config()
        save_filelist()
        pass
    print("qout: {}".format(qout))
    for task in tasks:
        task.cancel()
    await asyncio.gather(*tasks, return_exceptions=True)
    await client.disconnect()

asyncio.run(main())
