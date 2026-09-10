import os
import asyncio
from aiohttp import web

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton


TOKEN = os.getenv("BOT_TOKEN")
PORT = int(os.getenv("PORT", 10000))

bot = Bot(token=TOKEN)
dp = Dispatcher()


# =========================
# O'QUVCHI HOLATLARI
# =========================

class Registration(StatesGroup):
    name = State()
    grade = State()
    goal = State()


# =========================
# TUGMALAR
# =========================

start_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🚀 Boshlash")]
    ],
    resize_keyboard=True
)


grade_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="1-sinf"),
            KeyboardButton(text="2-sinf"),
            KeyboardButton(text="3-sinf")
        ],
        [
            KeyboardButton(text="4-sinf"),
            KeyboardButton(text="5-sinf"),
            KeyboardButton(text="6-sinf")
        ],
        [
            KeyboardButton(text="7-sinf"),
            KeyboardButton(text="8-sinf"),
            KeyboardButton(text="9-sinf")
        ],
        [
            KeyboardButton(text="10-sinf"),
            KeyboardButton(text="11-sinf")
        ]
    ],
    resize_keyboard=True
)


goal_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🏫 Prezident maktabi")],
        [KeyboardButton(text="🏆 Olimpiada")],
        [KeyboardButton(text="📚 Bilimimni oshirish")],
        [KeyboardButton(text="🎯 Boshqa maqsad")]
    ],
    resize_keyboard=True
)


# =========================
# START
# =========================

@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await state.clear()

    await message.answer(
        "🇺🇿 Assalomu alaykum!\n\n"
        "🎓 IMA Prezident School AI Bot'iga xush kelibsiz!\n\n"
        "Bu bot sizni 8 oy davomida Prezident maktabi "
        "imtihoniga bosqichma-bosqich tayyorlaydi.\n\n"
        "🇬🇧 English\n"
        "➗ Matematika\n"
        "🧠 Mantiq\n"
        "🤖 AI tahlil\n\n"
        "Tayyorgarlikni boshlash uchun quyidagi tugmani bosing:",
        reply_markup=start_keyboard
    )


# =========================
# BOSHLASH
# =========================

@dp.message(F.text == "🚀 Boshlash")
async def begin_registration(message: Message, state: FSMContext):

    await message.answer(
        "👤 Ajoyib!\n\n"
        "Avval siz haqingizda ma'lumot olamiz.\n\n"
        "✍️ Ism va familiyangizni kiriting:"
    )

    await state.set_state(Registration.name)


# =========================
# ISM-FAMILIYA
# =========================

@dp.message(Registration.name)
async def get_name(message: Message, state: FSMContext):

    name = message.text.strip()

    if len(name) < 3:
        await message.answer(
            "❗ Ism va familiyangizni to'liqroq kiriting.\n"
            "Masalan: Ali Valiyev"
        )
        return

    await state.update_data(name=name)

    await message.answer(
        "🎒 Nechanchi sinfda o'qiysiz?",
        reply_markup=grade_keyboard
    )

    await state.set_state(Registration.grade)


# =========================
# SINF
# =========================

@dp.message(Registration.grade)
async def get_grade(message: Message, state: FSMContext):

    grade = message.text.strip()

    valid_grades = [
        "1-sinf", "2-sinf", "3-sinf",
        "4-sinf", "5-sinf", "6-sinf",
        "7-sinf", "8-sinf", "9-sinf",
        "10-sinf", "11-sinf"
    ]

    if grade not in valid_grades:
        await message.answer(
            "❗ Iltimos, pastdagi tugmalardan o'zingizga mos sinfni tanlang.",
            reply_markup=grade_keyboard
        )
        return

    await state.update_data(grade=grade)

    await message.answer(
        "🎯 Asosiy maqsadingiz nima?",
        reply_markup=goal_keyboard
    )

    await state.set_state(Registration.goal)


# =========================
# MAQSAD
# =========================

@dp.message(Registration.goal)
async def get_goal(message: Message, state: FSMContext):

    goal = message.text.strip()

    valid_goals = [
        "🏫 Prezident maktabi",
        "🏆 Olimpiada",
        "📚 Bilimimni oshirish",
        "🎯 Boshqa maqsad"
    ]

    if goal not in valid_goals:
        await message.answer(
            "❗ Iltimos, maqsadingizni tugmalardan tanlang.",
            reply_markup=goal_keyboard
        )
        return

    await state.update_data(goal=goal)

    data = await state.get_data()

    await message.answer(
        "✅ RO'YXATDAN O'TISH YAKUNLANDI!\n\n"
        f"👤 Ism: {data['name']}\n"
        f"🎒 Sinf: {data['grade']}\n"
        f"🎯 Maqsad: {data['goal']}\n\n"
        "🚀 Endi siz uchun individual diagnostika tayyorlaymiz.\n\n"
        "📊 Diagnostika orqali sizning hozirgi "
        "bilim darajangiz aniqlanadi.\n\n"
        "Keyingi bosqich:\n"
        "📝 40 ta diagnostik savol\n"
        "📈 Natijalar tahlili\n"
        "🤖 AI tavsiyasi\n"
        "🗓 8 oylik individual reja"
    )

    await state.clear()


# =========================
# RENDER WEB SERVER
# =========================

async def health(request):
    return web.Response(
        text="IMA Prezident School AI Bot is running!"
    )


async def start_web_server():

    app = web.Application()

    app.router.add_get("/", health)

    runner = web.AppRunner(app)

    await runner.setup()

    site = web.TCPSite(
        runner,
        "0.0.0.0",
        PORT
    )

    await site.start()

    print(f"Web server started on port {PORT}")


# =========================
# MAIN
# =========================

async def main():

    await start_web_server()

    print("Telegram bot started!")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
