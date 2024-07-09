import os
import asyncio
from telegram import Bot
from dotenv import load_dotenv


load_dotenv()


BOT_API_TOKEN = os.getenv("BOT_API_TOKEN")
bot = Bot(token=BOT_API_TOKEN)


async def async_send_message(message, chat_id=1053260869):
    await bot.send_message(chat_id=chat_id, text=message)


def send_telegram_message(message):
    asyncio.run(async_send_message(message))
