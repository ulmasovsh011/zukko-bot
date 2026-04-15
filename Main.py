import random
import math
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

# TOKENNI O'ZGARINGIZ
TOKEN = '8755692281:AAHTLqoV3K6GoGPH9BZO_G95i-OknzwbOMA'

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
dp = Dispatcher(storage=MemoryStorage())

class StudyState(StatesGroup):
    choosing_class = State()
    choosing_specific_class = State()
    solving_task = State()

CLASS_DATA = {
    "1-4": {
        "🔢 Arifmetika": "🔢 **Boshlang'ich matematika:**\n\n• Qo'shish: a+b=c\n• Ayirish: a-b=d\n• Ko'paytirish: a*b=p\n• Bo'lish: a:b=q\n\n**Qoldiqli bo'lish:**\na = b*c + r (r < b)",
        "📐 Geometriya": "📐 **Geometriya asoslari:**\n\n**Kvadrat:**\n• P = 4*a\n• S = a*a\n\n**To'rtburchak:**\n• P = 2*(a+b)\n• S = a*b"
    },
    "5-8": {
        "🔢 Algebra": "🔢 **Qisqa ko'paytirish formulalari:**\n\n1. a²-b²=(a-b)(a+b)\n2. (a+b)²=a²+2ab+b²\n3. (a-b)²=a²-2ab+b²\n\n**Viyet teoremasi:**\n• x₁+x₂ = -b/a\n• x₁*x₂ = c/a",
        "📐 Geometriya": "📐 **Geometriya (7-8 sinf):**\n\n• Pifagor teoremasi: a²+b²=c²\n• Uchburchak yuzi: S=(a*h)/2\n• Aylana uzunligi: L=2πr"
    },
    "9-11": {
        "📐 Trigonometriya": "📐 **Trigonometriya:**\n\n• sin²α + cos²α = 1\n• tgα = sinα/cosα\n• sin(2α) = 2sinαcosα",
        "♾ Analiz": "♾ **Analiz asoslari:**\n\n• (xⁿ)' = nxⁿ⁻¹\n• logₐ b = x => aˣ = b\n• ∫ xⁿ dx = (xⁿ⁺¹)/(n+1) + C"
    }
}

def main_menu():
    builder = ReplyKeyboardBuilder()
    builder.button(text="📚 Formulalar")
    builder.button(text="➕ Misol yechish")
    builder.button(text="📞 Aloqa")
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(f"Salom {message.from_user.full_name}! Zukko Ustoz botiga xush kelibsiz.", reply_markup=main_menu())

@dp.message(F.text == "📞 Aloqa")
async def contact(message: types.Message):
    await message.answer("🆘 Savollar bo'lsa admin @UlmasovSh011 ga murojaat qiling.")

@dp.message(F.text == "📚 Formulalar")
async def show_categories(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.button(text="👶 1-4 sinflar", callback_data="cat_1-4")
    builder.button(text="👦 5-8 sinflar", callback_data="cat_5-8")
    builder.button(text="🎓 9-11 sinflar", callback_data="cat_9-11")
    builder.adjust(1)
    await message.answer("Sinfni tanlang:", reply_markup=builder.as_markup())

@dp.callback_query(F.data.startswith("cat_"))
async def show_topics(callback: types.CallbackQuery):
    cat = callback.data.split("_")[1]
    builder = InlineKeyboardBuilder()
    for topic in CLASS_DATA[cat].keys():
        builder.button(text=topic, callback_data=f"topic_{cat}_{topic}")
    builder.button(text="⬅️ Orqaga", callback_data="back_to_cats")
    builder.adjust(1)
    await callback.message.edit_text(f"{cat}-sinflar uchun mavzular:", reply_markup=builder.as_markup())

@dp.callback_query(F.data.startswith("topic_"))
async def show_formula(callback: types.CallbackQuery):
    _, cat, topic = callback.data.split("_")
    text = CLASS_DATA[cat][topic]
    builder = InlineKeyboardBuilder()
    builder.button(text="⬅️ Orqaga", callback_data=f"cat_{cat}")
    await callback.message.edit_text(text, reply_markup=builder.as_markup())

@dp.callback_query(F.data == "back_to_cats")
async def back_cats(callback: types.CallbackQuery):
    await show_categories(callback.message)

@dp.message(F.text == "➕ Misol yechish")
async def start_solving(message: types.Message, state: FSMContext):
    builder = InlineKeyboardBuilder()
    builder.button(text="1-4 sinf", callback_data="math_1-4")
    builder.button(text="5-8 sinf", callback_data="math_5-8")
    builder.button(text="9-11 sinf", callback_data="math_9-11")
    builder.adjust(1)
    await message.answer("Qiyinchilik darajasini tanlang:", reply_markup=builder.as_markup())

@dp.callback_query(F.data.startswith("math_"))
async def choose_specific_grade(callback: types.CallbackQuery, state: FSMContext):
    level = callback.data.split("_")[1]
    builder = InlineKeyboardBuilder()
    grades = {"1-4": ["1", "2", "3", "4"], "5-8": ["5", "6", "7", "8"], "9-11": ["9", "10", "11"]}[level]
    for g in grades:
        builder.button(text=f"{g}-sinf", callback_data=f"level_{g}")
    builder.adjust(2)
    await callback.message.edit_text("Aniq sinfni tanlang:", reply_markup=builder.as_markup())
    await state.set_state(StudyState.choosing_specific_class)

@dp.callback_query(F.data.startswith("level_"))
async def generate_problem(callback: types.CallbackQuery, state: FSMContext):
    grade = callback.data.split("_")[1]
    task, ans = "", 0
    if grade == "1":
        a, b = random.randint(1, 20), random.randint(1, 20)
        task, ans = f"{a} + {b} = ?", a + b
    elif grade == "2":
        a, b = random.randint(2, 9), random.randint(2, 9)
        task, ans = f"{a} * {b} = ?", a * b
    elif grade == "3":
        a, b = random.randint(20, 50), random.randint(3, 7)
        task, ans = f"{a} : {b} qoldig'ini toping", a % b
    elif grade == "4":
        a, b = random.randint(5, 12), random.randint(5, 12)
        task, ans = f"Tomonlari {a} va {b} bo'lgan to'rtburchak yuzi?", a * b
    elif grade == "5":
        a, b = random.choice([12, 18, 24]), random.choice([30, 36, 48])
        task, ans = f"EKUB({a}, {b}) ni toping", math.gcd(a, b)
    elif grade == "6":
        x = random.randint(2, 10)
        task, ans = f"Proporsiya: x:10 = {x*2}:20. x = ?", x
    elif grade == "7":
        a = random.randint(2, 5)
        task, ans = f"(x - {a})(x + {a}) - x² + 30 ifodani hisoblang", 30 - a**2
    elif grade == "8":
        x1, x2 = random.randint(1, 5), random.randint(6, 10)
        b, c = -(x1+x2), x1*x2
        task, ans = f"x² {b if b<0 else '+'+str(b)}x + {c} = 0. Katta ildizi?", x2
    elif grade == "9":
        a1, d = random.randint(1, 5), random.randint(2, 4)
        task, ans = f"Arifmetik progressiya: a1={a1}, d={d}. a4 = ?", a1 + 3*d
    elif grade == "10":
        task, ans = "5 * (sin²(25°) + cos²(25°)) + 2 = ?", 7
    elif grade == "11":
        vals = {8:3, 16:4, 32:5, 64:6}
        x, a = random.choice(list(vals.items()))
        task, ans = f"log₂({x}) = ?", a

    await state.update_data(correct_ans=ans)
    await callback.message.edit_text(f"📝 {grade}-sinf misoli:\n\n`{task}`")
    await state.set_state(StudyState.solving_task)

@dp.message(StudyState.solving_task)
async def check_answer(message: types.Message, state: FSMContext):
    data = await state.get_data()
    try:
        user_ans = int(message.text)
        if user_ans == data['correct_ans']:
            await message.answer("✅ To'g'ri! Barakalla!", reply_markup=main_menu())
        else:
            await message.answer(f"❌ Noto'g'ri. Javob: {data['correct_ans']}", reply_markup=main_menu())
    except:
        await message.answer("⚠️ Iltimos, faqat son yozing.")
    await state.clear()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
