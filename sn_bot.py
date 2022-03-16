import logging
import os
import time
import asyncio
from dotenv import load_dotenv
from aiogram import Bot#, Dispatcher, executor
#from aiogram.contrib.fsm_storage.memory import MemoryStorage

from lxml import html
import requests
import json

load_dotenv()

logging.basicConfig(level=logging.INFO)

user_id = os.environ.get('UID')

bot = Bot(token=os.environ.get('TELEGRAM_API_TOKEN'))

#storage = MemoryStorage()
#dp = Dispatcher(bot, storage=storage)

async def handle_entry(conf_entry):
    page = requests.get(conf_entry['url'])
    tree = html.fromstring(page.content)
    res = tree.xpath(conf_entry['selector'])
    if str(res) == conf_entry['expect']:
        #print('no change')
        await bot.send_message(user_id, 'no change')
    else:
        await bot.send_message(user_id, conf_entry['message'])
        #print(conf_entry['message'])

async def handle_config():
    try: 
        with open('conf.json') as json_file:
            json_conf = json.load(json_file)
            for entry in json_conf: 
                await handle_entry(entry)
    except IOError:
        print('no config file found')

async def run_loop():
    while True:
        await handle_config()
        time.sleep(60 * 60 * 24)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_loop())

#@dp.message_handler()
#async def echo(message):
#    await message.answer(message.from_user.id)    

#if __name__ == '__main__':
#    executor.start_polling(dp, skip_updates=True)