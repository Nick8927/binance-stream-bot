import asyncio
import random
import requests
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from config import TG_TOKEN, API_KEY

bot = Bot(token=TG_TOKEN)
dp = Dispatcher()

CHAT_ID = 7003041125
PIXABAY_API_KEY = API_KEY
PIXABAY_API_URL = "https://pixabay.com/api/"

params = {
    "key": PIXABAY_API_KEY,
    "q": "kids",
    "image_type": "photo",
    "orientation": "horizontal",
    "category": "people",
    "safesearch": "true",
    "per_page": 10,
}

@dp.message(Command("start"))
async def send_welcome(message: Message):
    await message.answer("Привет! Я буду присылать тебе изображения.")

async def fetch_image():
    response = requests.get(PIXABAY_API_URL, params=params)
    try:
        data = response.json()
    except Exception as e:
        print(f"Ошибка при парсинге JSON: {e}")
        print("Ответ сервера:", response.text)
        return None

    if data.get("hits"):
        image = random.choice(data["hits"])
        return image["webformatURL"]
    return None

async def send_daily_image():
    image_url = await fetch_image()
    if image_url:
        await bot.send_photo(CHAT_ID, photo=image_url)
    else:
        await bot.send_message(CHAT_ID, "Извините, изображения не найдены.")

async def daily_loop():
    while True:
        try:
            await send_daily_image()
        except Exception as e:
            print(f"Ошибка при отправке картинки: {e}")
        await asyncio.sleep(10)

async def main():
    await asyncio.gather(
        dp.start_polling(bot),
        daily_loop()
    )

if __name__ == "__main__":
    asyncio.run(main())
