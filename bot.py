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
# HOLATLAR
# =========================

class Registration(StatesGroup):
    name = State()
    grade = State()
    goal = State()


class TestState(StatesGroup):
    answering = State()


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
# TEST SAVOLLARI
# =========================

questions = [

    # ===== MATEMATIKA 1-20 =====

    {
        "subject": "➗ MATEMATIKA",
        "question": "1. 48 + 27 = ?",
        "options": ["65", "75", "85", "70"],
        "answer": "75"
    },
    {
        "subject": "➗ MATEMATIKA",
        "question": "2. 96 - 38 = ?",
        "options": ["58", "68", "48", "62"],
        "answer": "58"
    },
    {
        "subject": "➗ MATEMATIKA",
        "question": "3. 7 × 8 = ?",
        "options": ["54", "56", "64", "48"],
        "answer": "56"
    },
    {
        "subject": "➗ MATEMATIKA",
        "question": "4. 81 ÷ 9 = ?",
        "options": ["7", "8", "9", "10"],
        "answer": "9"
    },
    {
        "subject": "➗ MATEMATIKA",
        "question": "5. 125 + 375 = ?",
        "options": ["400", "450", "500", "550"],
        "answer": "500"
    },
    {
        "subject": "➗ MATEMATIKA",
        "question": "6. 15 × 6 = ?",
        "options": ["80", "90", "100", "75"],
        "answer": "90"
    },
    {
        "subject": "➗ MATEMATIKA",
        "question": "7. 144 ÷ 12 = ?",
        "options": ["10", "11", "12", "14"],
        "answer": "12"
    },
    {
        "subject": "➗ MATEMATIKA",
        "question": "8. 3/4 ning 20 ga ko‘paytmasi nechaga teng?",
        "options": ["12", "15", "16", "18"],
        "answer": "15"
    },
    {
        "subject": "➗ MATEMATIKA",
        "question": "9. 2,5 + 3,7 = ?",
        "options": ["5,2", "6,2", "6,7", "5,7"],
        "answer": "6,2"
    },
    {
        "subject": "➗ MATEMATIKA",
        "question": "10. 200 ning 25% i nechaga teng?",
        "options": ["25", "40", "50", "75"],
        "answer": "50"
    },
    {
        "subject": "➗ MATEMATIKA",
        "question": "11. x + 17 = 42. x = ?",
        "options": ["15", "20", "25", "27"],
        "answer": "25"
    },
    {
        "subject": "➗ MATEMATIKA",
        "question": "12. 5x = 45. x = ?",
        "options": ["7", "8", "9", "10"],
        "answer": "9"
    },
    {
        "subject": "➗ MATEMATIKA",
        "question": "13. To‘g‘ri to‘rtburchakning tomonlari 8 sm va 5 sm. Yuzi?",
        "options": ["13", "26", "40", "45"],
        "answer": "40"
    },
    {
        "subject": "➗ MATEMATIKA",
        "question": "14. Kvadrat tomoni 7 sm. Perimetri?",
        "options": ["14", "21", "28", "49"],
        "answer": "28"
    },
    {
        "subject": "➗ MATEMATIKA",
        "question": "15. 1 soat 35 daqiqa necha daqiqa?",
        "options": ["85", "90", "95", "105"],
        "answer": "95"
    },
    {
        "subject": "➗ MATEMATIKA",
        "question": "16. Ketma-ketlikni davom ettiring: 3, 6, 12, 24, ...",
        "options": ["36", "42", "48", "54"],
        "answer": "48"
    },
    {
        "subject": "➗ MATEMATIKA",
        "question": "17. 450 ning 10% i?",
        "options": ["35", "40", "45", "50"],
        "answer": "45"
    },
    {
        "subject": "➗ MATEMATIKA",
        "question": "18. 2² + 3² = ?",
        "options": ["10", "11", "12", "13"],
        "answer": "13"
    },
    {
        "subject": "➗ MATEMATIKA",
        "question": "19. 72 ning 1/8 qismi?",
        "options": ["8", "9", "10", "12"],
        "answer": "9"
    },
    {
        "subject": "➗ MATEMATIKA",
        "question": "20. 4 ta daftar 28 000 so‘m. 1 ta daftar qancha?",
        "options": ["5 000", "6 000", "7 000", "8 000"],
        "answer": "7 000"
    },

    # ===== ENGLISH 21-30 =====

    {
        "subject": "🇬🇧 ENGLISH",
        "question": "21. Choose the correct answer: She ___ a student.",
        "options": ["am", "is", "are", "be"],
        "answer": "is"
    },
    {
        "subject": "🇬🇧 ENGLISH",
        "question": "22. I ___ football every Sunday.",
        "options": ["play", "plays", "playing", "played"],
        "answer": "play"
    },
    {
        "subject": "🇬🇧 ENGLISH",
        "question": "23. What is the opposite of 'big'?",
        "options": ["long", "small", "tall", "fast"],
        "answer": "small"
    },
    {
        "subject": "🇬🇧 ENGLISH",
        "question": "24. There ___ three books on the table.",
        "options": ["is", "am", "are", "be"],
        "answer": "are"
    },
    {
        "subject": "🇬🇧 ENGLISH",
        "question": "25. Yesterday I ___ to school.",
        "options": ["go", "goes", "went", "going"],
        "answer": "went"
    },
    {
        "subject": "🇬🇧 ENGLISH",
        "question": "26. Choose the correct plural: child → ?",
        "options": ["childs", "children", "childes", "childrens"],
        "answer": "children"
    },
    {
        "subject": "🇬🇧 ENGLISH",
        "question": "27. My brother is ___ than me.",
        "options": ["tall", "taller", "tallest", "more tall"],
        "answer": "taller"
    },
    {
        "subject": "🇬🇧 ENGLISH",
        "question": "28. We ___ watching TV now.",
        "options": ["is", "are", "am", "be"],
        "answer": "are"
    },
    {
        "subject": "🇬🇧 ENGLISH",
        "question": "29. What does 'beautiful' mean?",
        "options": ["chiroyli", "tez", "katta", "sovuq"],
        "answer": "chiroyli"
    },
    {
        "subject": "🇬🇧 ENGLISH",
        "question": "30. Choose the correct sentence.",
        "options": [
            "He don't like apples.",
            "He doesn't like apples.",
            "He doesn't likes apples.",
            "He not like apples."
        ],
        "answer": "He doesn't like apples."
    },

    # ===== MANTIQ 31-40 =====

    {
        "subject": "🧠 MANTIQ",
        "question": "31. 2, 4, 8, 16, ... Keyingi son?",
        "options": ["20", "24", "32", "36"],
        "answer": "32"
    },
    {
        "subject": "🧠 MANTIQ",
        "question": "32. 1, 4, 9, 16, ... Keyingi son?",
        "options": ["20", "24", "25", "36"],
        "answer": "25"
    },
    {
        "subject": "🧠 MANTIQ",
        "question": "33. Bir qatorda 5 bola turibdi. Aziz chapdan 2-o‘rinda. Bobur Azizning o‘ng tomonida. Bobur qaysi o‘rinda turishi mumkin?",
        "options": ["1-o‘rin", "2-o‘rin", "3-o‘rin", "Faqat 5-o‘rin"],
        "answer": "3-o‘rin"
    },
    {
        "subject": "🧠 MANTIQ",
        "question": "34. 5 ta olma bor. 5 bolaga bittadan berildi, lekin savatda 1 ta olma qoldi. Qanday?",
        "options": [
            "Olma yashirildi",
            "Oxirgi bolaga olma savati bilan berildi",
            "Bitta olma buzilgan",
            "Bu mumkin emas"
        ],
        "answer": "Oxirgi bolaga olma savati bilan berildi"
    },
    {
        "subject": "🧠 MANTIQ",
        "question": "35. Qaysi biri boshqalardan farq qiladi?",
        "options": ["2", "4", "8", "11"],
        "answer": "11"
    },
    {
        "subject": "🧠 MANTIQ",
        "question": "36. Bugun dushanba bo‘lsa, 10 kundan keyin qaysi kun?",
        "options": ["Chorshanba", "Payshanba", "Juma", "Shanba"],
        "answer": "Payshanba"
    },
    {
        "subject": "🧠 MANTIQ",
        "question": "37. 3 ta mushuk 3 daqiqada 3 ta sichqon tutadi. 1 mushuk 3 daqiqada nechta sichqon tutadi?",
        "options": ["1", "2", "3", "9"],
        "answer": "1"
    },
    {
        "subject": "🧠 MANTIQ",
        "question": "38. 10, 20, 40, 80, ...",
        "options": ["100", "120", "140", "160"],
        "answer": "160"
    },
    {
        "subject": "🧠 MANTIQ",
        "question": "39. Agar barcha A lar B bo‘lsa va barcha B lar C bo‘lsa, A lar nima bo‘ladi?",
        "options": ["C", "D", "A emas", "Aniqlab bo‘lmaydi"],
        "answer": "C"
    },
    {
        "subject": "🧠 MANTIQ",
        "question": "40. 1 kg paxta va 1 kg temirdan qaysi biri og‘ir?",
        "options": ["Paxta", "Temir", "Ikkalasi teng", "Sharoitga bog‘liq"],
        "answer": "Ikkalasi teng"
    }
]


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
        "Tayyorgarlikni boshlash uchun tugmani bosing:",
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
# ISM
# =========================

@dp.message(Registration.name)
async def get_name(message: Message, state: FSMContext):

    name = message.text.strip()

    if len(name) < 3:
        await message.answer(
            "❗ Ism va familiyangizni to‘liqroq kiriting."
        )
        return

    await state.update_data(name=name)

    await message.answer(
        "🎒 Nechanchi sinfda o‘qiysiz?",
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
            "❗ Iltimos, sinfni tugmalardan tanlang.",
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
            "❗ Iltimos, maqsadni tugmalardan tanlang.",
            reply_markup=goal_keyboard
        )
        return

    await state.update_data(goal=goal)

    data = await state.get_data()

    await message.answer(
        "✅ RO‘YXATDAN O‘TISH YAKUNLANDI!\n\n"
        f"👤 Ism: {data['name']}\n"
        f"🎒 Sinf: {data['grade']}\n"
        f"🎯 Maqsad: {data['goal']}\n\n"
        "📝 Endi diagnostika boshlanadi.\n\n"
        "📊 40 ta savol\n"
        "➗ 20 ta matematika\n"
        "🇬🇧 10 ta English\n"
        "🧠 10 ta mantiq\n\n"
        "Har bir savolga faqat bitta javob tanlang."
    )

    await asyncio.sleep(1)

    await state.update_data(
        question_index=0,
        score=0
    )

    await state.set_state(TestState.answering)

    await send_question(message, state)


# =========================
# SAVOL YUBORISH
# =========================

async def send_question(message: Message, state: FSMContext):

    data = await state.get_data()

    index = data["question_index"]

    if index >= len(questions):
        await finish_test(message, state)
        return

    q = questions[index]

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=q["options"][0])],
            [KeyboardButton(text=q["options"][1])],
            [KeyboardButton(text=q["options"][2])],
            [KeyboardButton(text=q["options"][3])]
        ],
        resize_keyboard=True
    )

    await message.answer(
        f"📊 SAVOL {index + 1} / {len(questions)}\n\n"
        f"{q['subject']}\n\n"
        f"❓ {q['question']}",
        reply_markup=keyboard
    )


# =========================
# JAVOBNI TEKSHIRISH
# =========================

@dp.message(TestState.answering)
async def check_answer(message: Message, state: FSMContext):

    data = await state.get_data()

    index = data["question_index"]

    if index >= len(questions):
        return

    selected = message.text.strip()

    q = questions[index]

    score = data["score"]

    if selected == q["answer"]:
        score += 1
        await message.answer("✅ To‘g‘ri!")
    else:
        await message.answer(
            f"❌ Noto‘g‘ri.\n"
            f"To‘g‘ri javob: {q['answer']}"
        )

    index += 1

    await state.update_data(
        question_index=index,
        score=score
    )

    await asyncio.sleep(0.3)

    await send_question(message, state)


# =========================
# NATIJA
# =========================

async def finish_test(message: Message, state: FSMContext):

    data = await state.get_data()

    score = data["score"]

    percentage = score / len(questions) * 100

    if percentage >= 90:
        level = "🏆 JUDA YUQORI"
    elif percentage >= 75:
        level = "🥇 YAXSHI"
    elif percentage >= 60:
        level = "🥈 O‘RTA"
    else:
        level = "📚 RIVOJLANTIRISH KERAK"

    await message.answer(
        "🎉 DIAGNOSTIKA YAKUNLANDI!\n\n"
        f"👤 O‘quvchi: {data['name']}\n"
        f"🎒 Sinf: {data['grade']}\n\n"
        f"📊 Natija: {score} / 40\n"
        f"📈 Foiz: {percentage:.0f}%\n\n"
        f"🏅 Daraja: {level}\n\n"
        "🤖 Keyingi bosqichda sizning xatolaringiz "
        "tahlil qilinadi va individual o‘quv reja tuziladi."
    )

    await state.clear()


# =========================
# RENDER SERVER
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
