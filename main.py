import asyncio
import json
import time

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
import websockets
from config import TG_TOKEN



bot = Bot(token=TG_TOKEN)
dp = Dispatcher()

binance_url = "wss://fstream.binance.com/ws/btcusdt@aggTrade"


subscribers: set[int] = set()

last_send_time = 0


@dp.message(CommandStart())
async def get_start(message: Message):
    """Добавляем пользователя в подписчики"""
    user_id = message.from_user.id
    subscribers.add(user_id)
    await message.answer(
        text=f"✅ Ты подписан на рассылку цен BTC/USDT.\n"
             f"({len(subscribers)} подписчиков всего)"
    )


async def fetch_binance_trades(url: str):
    """Слушаем Binance и шлём цены всем подписчикам"""
    global last_send_time
    async with websockets.connect(url) as ws:
        async for message in ws:
            data = json.loads(message)
            price = data['p']
            if time.time() - last_send_time > 5:
                await send_message_to_all(
                    msg=f"Последняя цена BTC / USDT: {price}"
                )
                last_send_time = time.time()


async def send_message_to_all(msg: str):
    """Отправляем сообщение всем подписчикам"""
    for user_id in list(subscribers):
        try:
            await bot.send_message(chat_id=user_id, text=msg)
        except Exception as e:
            print(f"Ошибка при отправке {user_id}: {e}")
            subscribers.discard(user_id)


async def main():
    await asyncio.gather(
        fetch_binance_trades(binance_url),
        dp.start_polling(bot, handle_unknown_updates=False)
    )


if __name__ == "__main__":
    asyncio.run(main())
