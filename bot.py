import os
import asyncio
from aiohttp import web

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton


# =========================================================
# SOZLAMALAR
# =========================================================

TOKEN = os.getenv("BOT_TOKEN")
PORT = int(os.getenv("PORT", 10000))

if not TOKEN:
    raise ValueError("BOT_TOKEN topilmadi!")

bot = Bot(token=TOKEN)
dp = Dispatcher()


# =========================================================
# HOLATLAR
# =========================================================

class Registration(StatesGroup):
    name = State()
    grade = State()


class StudentState(StatesGroup):
    menu = State()
    subject = State()


# =========================================================
# TUGMALAR
# =========================================================

start_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🚀 Boshlash")]
    ],
    resize_keyboard=True
)


grade_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="2-sinf"),
            KeyboardButton(text="3-sinf")
        ],
        [
            KeyboardButton(text="4-sinf")
        ]
    ],
    resize_keyboard=True
)


subject_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🇬🇧 Ingliz tili")],
        [KeyboardButton(text="🔢 Matematika")],
        [KeyboardButton(text="🧠 Tanqidiy fikrlash")],
        [KeyboardButton(text="🧩 Muammoli masalalar")]
    ],
    resize_keyboard=True
)


back_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="⬅️ Fanlarga qaytish")]
    ],
    resize_keyboard=True
)


# =========================================================
# 8 OYLIK DASTUR
# =========================================================

PROGRAMS = {

    # =====================================================
    # INGLIZ TILI
    # =====================================================

    "🇬🇧 Ingliz tili": {

        "2-sinf": [
            "1-oy — Alphabet, numbers, colors, family",
            "2-oy — School, animals, body parts",
            "3-oy — am / is / are",
            "4-oy — have / has, this / that",
            "5-oy — There is / There are",
            "6-oy — Basic verbs va everyday actions",
            "7-oy — Simple reading va vocabulary",
            "8-oy — Yakuniy test va Prezident maktabi mashqlari"
        ],

        "3-sinf": [
            "1-oy — Vocabulary va Present Simple",
            "2-oy — Present Continuous",
            "3-oy — Past Simple",
            "4-oy — Can / Can't, have / has",
            "5-oy — Comparatives va Superlatives",
            "6-oy — Question words va Prepositions",
            "7-oy — Reading comprehension",
            "8-oy — Grammar + Reading yakuniy testlari"
        ],

        "4-sinf": [
            "1-oy — Present Simple / Present Continuous",
            "2-oy — Past Simple",
            "3-oy — Future va Modal verbs",
            "4-oy — Articles, Pronouns, Prepositions",
            "5-oy — Comparatives / Superlatives",
            "6-oy — Vocabulary in context",
            "7-oy — Murakkab Reading comprehension",
            "8-oy — Prezident maktabi formatidagi English testlar"
        ]
    },


    # =====================================================
    # MATEMATIKA
    # =====================================================

    "🔢 Matematika": {

        "2-sinf": [
            "1-oy — Sonlar va taqqoslash",
            "2-oy — Qo‘shish va ayirish",
            "3-oy — Ko‘paytirish va bo‘lish",
            "4-oy — Vaqt, pul va o‘lchov birliklari",
            "5-oy — Geometrik shakllar",
            "6-oy — Perimetr va sodda masalalar",
            "7-oy — Sonli ketma-ketliklar",
            "8-oy — Murakkab aralash masalalar"
        ],

        "3-sinf": [
            "1-oy — Ko‘p xonali sonlar",
            "2-oy — 4 amalni mustahkamlash",
            "3-oy — Kasr tushunchasi",
            "4-oy — Perimetr va yuza",
            "5-oy — Tenglamalar",
            "6-oy — Jadval va diagrammalar",
            "7-oy — 2–3 bosqichli masalalar",
            "8-oy — Murakkab aralash testlar"
        ],

        "4-sinf": [
            "1-oy — Murakkab arifmetik amallar",
            "2-oy — Kasrlar va ulushlar",
            "3-oy — Tenglamalar va noma’lum son",
            "4-oy — Perimetr va yuza",
            "5-oy — Vaqt, masofa va tezlik",
            "6-oy — Ketma-ketliklar va sonli mantiq",
            "7-oy — Kombinatorika va nostandart masalalar",
            "8-oy — Prezident maktabi darajasidagi matematika"
        ]
    },


    # =====================================================
    # TANQIDIY FIKRLASH
    # =====================================================

    "🧠 Tanqidiy fikrlash": {

        "2-sinf": [
            "1-oy — O‘xshashlik va farq",
            "2-oy — Ortiqchasini topish",
            "3-oy — Ketma-ketlik",
            "4-oy — Tasniflash",
            "5-oy — Shakllar va naqshlar",
            "6-oy — Oddiy kodlar",
            "7-oy — Sabab va oqibat",
            "8-oy — Mantiqiy yakuniy test"
        ],

        "3-sinf": [
            "1-oy — Qoidani aniqlash",
            "2-oy — Murakkab ketma-ketlik",
            "3-oy — Jadval bilan ishlash",
            "4-oy — Kodlash va belgilar",
            "5-oy — Taqqoslash",
            "6-oy — Sabab–oqibat",
            "7-oy — Xulosa chiqarish",
            "8-oy — Aralash Critical Thinking testi"
        ],

        "4-sinf": [
            "1-oy — Murakkab ketma-ketliklar",
            "2-oy — Mantiqiy jadval",
            "3-oy — Kodlash",
            "4-oy — Rost / yolg‘on",
            "5-oy — Dalil va xulosa",
            "6-oy — Bir nechta shartli masalalar",
            "7-oy — Strategik fikrlash",
            "8-oy — Prezident maktabi Reasoning testi"
        ]
    },


    # =====================================================
    # MUAMMOLI MASALALAR
    # =====================================================

    "🧩 Muammoli masalalar": {

        "2-sinf": [
            "1-oy — Oddiy hayotiy masalalar",
            "2-oy — Ko‘p va kam",
            "3-oy — Qancha qoldi?",
            "4-oy — 1–2 bosqichli masalalar",
            "5-oy — Rasm asosidagi masalalar",
            "6-oy — Vaqt va pul masalalari",
            "7-oy — Noodatiy savollar",
            "8-oy — Challenge masalalar"
        ],

        "3-sinf": [
            "1-oy — 2–3 bosqichli masalalar",
            "2-oy — Orqaga qarab yechish",
            "3-oy — Jadval yordamida yechish",
            "4-oy — Chizma yordamida yechish",
            "5-oy — Yetishmayotgan ma’lumot",
            "6-oy — Eng kam / eng ko‘p",
            "7-oy — Yosh, vaqt va masofa masalalari",
            "8-oy — Murakkab muammoli masalalar"
        ],

        "4-sinf": [
            "1-oy — Murakkab shartli masalalar",
            "2-oy — Orqaga yurib yechish",
            "3-oy — Jadval va chizma",
            "4-oy — Bir nechta yechimli masalalar",
            "5-oy — Minimal / maksimal",
            "6-oy — Kombinatorik masalalar",
            "7-oy — Geometrik muammolar",
            "8-oy — Prezident maktabi + Olimpiada Challenge"
        ]
    }
}


# =========================================================
# START
# =========================================================

@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):

    await state.clear()

    await message.answer(
        "🇺🇿 ASSALOMU ALAYKUM!\n\n"
        "🎓 IMA PREZIDENT SCHOOL AI\n\n"
        "🏫 Prezident maktabiga tayyorlov platformasi.\n\n"
        "👦 2–4-sinf o‘quvchilari uchun.\n\n"
        "⭐ ASOSIY YO‘NALISHLAR:\n\n"
        "🇬🇧 Ingliz tili\n"
        "🔢 Matematika\n"
        "🧠 Tanqidiy fikrlash\n"
        "🧩 Muammoli masalalar\n\n"
        "🚀 Tayyorgarlikni boshlash uchun tugmani bosing.",
        reply_markup=start_keyboard
    )


# =========================================================
# BOSHLASH
# =========================================================

@dp.message(F.text == "🚀 Boshlash")
async def begin(message: Message, state: FSMContext):

    await message.answer(
        "👤 O‘QUVCHI PROFILI\n\n"
        "✍️ Ism va familiyangizni kiriting:"
    )

    await state.set_state(Registration.name)


# =========================================================
# ISM
# =========================================================

@dp.message(Registration.name)
async def get_name(message: Message, state: FSMContext):

    name = (message.text or "").strip()

    if len(name) < 3:
        await message.answer(
            "❗ Iltimos, ism va familiyani to‘liqroq kiriting."
        )
        return

    await state.update_data(name=name)

    await message.answer(
        "🎒 O‘quvchi nechanchi sinfda o‘qiydi?\n\n"
        "Faqat 2–4-sinf.",
        reply_markup=grade_keyboard
    )

    await state.set_state(Registration.grade)


# =========================================================
# SINF
# =========================================================

@dp.message(Registration.grade)
async def get_grade(message: Message, state: FSMContext):

    grade = (message.text or "").strip()

    if grade not in ["2-sinf", "3-sinf", "4-sinf"]:
        await message.answer(
            "❗ Faqat 2-, 3- yoki 4-sinfni tanlang.",
            reply_markup=grade_keyboard
        )
        return

    await state.update_data(grade=grade)

    data = await state.get_data()

    await state.set_state(StudentState.menu)

    await message.answer(
        "✅ PROFIL TAYYOR!\n\n"
        f"👤 O‘quvchi: {data['name']}\n"
        f"🎒 Sinf: {grade}\n\n"
        "🏆 Endi o‘zingizga kerakli yo‘nalishni tanlang:",
        reply_markup=subject_keyboard
    )


# =========================================================
# FAN TANLASH
# =========================================================

@dp.message(
    StudentState.menu,
    F.text.in_([
        "🇬🇧 Ingliz tili",
        "🔢 Matematika",
        "🧠 Tanqidiy fikrlash",
        "🧩 Muammoli masalalar"
    ])
)
async def choose_subject(message: Message, state: FSMContext):

    subject = message.text

    await state.update_data(subject=subject)

    data = await state.get_data()

    grade = data.get("grade")

    lessons = PROGRAMS[subject][grade]

    text = (
        f"{subject}\n"
        f"🎒 {grade}\n\n"
        "🏆 8 OYLIK O‘QUV DASTURI\n\n"
    )

    for lesson in lessons:
        text += f"📌 {lesson}\n"

    text += (
        "\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "🎯 MAQSAD\n"
        "━━━━━━━━━━━━━━━━━━\n\n"
        "Bolani bosqichma-bosqich "
        "Prezident maktabi imtihoniga tayyorlash.\n\n"
        "📚 Keyingi bosqichda har bir oy ichida:\n"
        "• Dars\n"
        "• Tushuntirish\n"
        "• Mashqlar\n"
        "• Test\n"
        "• Natija\n"
        "• Xatolar tahlili\n"
        "• Keyingi daraja\n"
        "\n"
        "bo‘ladi."
    )

    await state.set_state(StudentState.subject)

    await message.answer(
        text,
        reply_markup=back_keyboard
    )


# =========================================================
# FANLARGA QAYTISH
# =========================================================

@dp.message(
    StudentState.subject,
    F.text == "⬅️ Fanlarga qaytish"
)
async def back_to_subjects(message: Message, state: FSMContext):

    await state.set_state(StudentState.menu)

    await message.answer(
        "📚 YO‘NALISHNI TANLANG:\n\n"
        "Qaysi fan bo‘yicha ishlamoqchisiz?",
        reply_markup=subject_keyboard
    )


# =========================================================
# NOTO‘G‘RI FAN TUGMASI
# =========================================================

@dp.message(StudentState.menu)
async def menu_help(message: Message):

    await message.answer(
        "❗ Iltimos, quyidagi bo‘limlardan birini tanlang:",
        reply_markup=subject_keyboard
    )


# =========================================================
# RENDER HEALTH SERVER
# =========================================================

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


# =========================================================
# MAIN
# =========================================================

async def main():

    await start_web_server()

    print("====================================")
    print("IMA PREZIDENT SCHOOL AI BOT")
    print("Telegram bot started successfully!")
    print("====================================")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
