import os
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "🇺🇿 Assalomu alaykum!\n\n"
        "🎓 IMA Prezident School AI Bot'iga xush kelibsiz!\n\n"
        "Bu bot sizni 8 oy davomida Prezident maktabi imtihoniga "
        "bosqichma-bosqich tayyorlaydi.\n\n"
        "🇬🇧 English\n"
        "➗ Matematika\n"
        "🧠 Mantiq\n\n"
        "🤖 AI sizning natijalaringizni tahlil qiladi."
    )


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
