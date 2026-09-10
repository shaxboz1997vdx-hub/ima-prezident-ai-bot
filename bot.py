import os
import asyncio
from aiohttp import web

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message


TOKEN = os.getenv("BOT_TOKEN")
PORT = int(os.getenv("PORT", 10000))

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "🇺🇿 Assalomu alaykum!\n\n"
        "🎓 IMA Prezident School AI Bot'iga xush kelibsiz!\n\n"
        "Bu bot sizni 8 oy davomida Prezident maktabi "
        "imtihoniga bosqichma-bosqich tayyorlaydi.\n\n"
        "🇬🇧 English\n"
        "➗ Matematika\n"
        "🧠 Mantiq\n\n"
        "🤖 AI sizning natijalaringizni tahlil qiladi."
    )


async def health(request):
    return web.Response(text="IMA Prezident School AI Bot is running!")


async def start_web_server():
    app = web.Application()
    app.router.add_get("/", health)

    runner = web.AppRunner(app)
    await runner.setup()

    site = web.TCPSite(runner, "0.0.0.0", PORT)
    await site.start()

    print(f"Web server started on port {PORT}")


async def main():
    await start_web_server()

    print("Telegram bot started!")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
