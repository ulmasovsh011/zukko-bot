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

TOKEN = '8755692281:AAHTLqoV3K6GoGPH9BZO_G95i-OknzwbOMA'

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
dp = Dispatcher(storage=MemoryStorage())

class StudyState(StatesGroup):
    solving_task = State()

CLASS_DATA = {
    "1-4": {
        "🔢 Arifmetika": (
            "🔢 **Boshlang'ich matematika:**\n\n"
            "• **Qo'shish:** a + b = c\n"
            "• **Ayirish:** a - b = d\n"
            "• **Ko'paytirish:** a * b = p\n"
            "• **Bo'lish:** a : b = q\n\n"
            "**Qoldiqli bo'lish:**\n"
            "a = b * c + r (r < b)"
        ),
        "📐 Geometriya": (
            "📐 **Geometriya asoslari:**\n\n"
            "**Kvadrat:**\n"
            "• P = 4 * a\n"
            "• S = a * a\n\n"
            "**To'g'ri to'rtburchak:**\n"
            "• P = 2 * (a + b)\n"
            "• S = a * b"
        )
    },
    "5-8": {
        "🔢 Algebra": (
            "🔢 **Qisqa ko'paytirish formulalari:**\n\n"
            "1. a² - b² = (a-b)(a+b)\n"
            "2. (a+b)² = a² + 2ab + b²\n"
            "3. (a-b)² = a² - 2ab + b²\n"
            "4. a³ + b³ = (a+b)(a² - ab + b²)\n"
            "5. a³ - b³ = (a-b)(a² + ab + b²)\n\n"
            "**Viyet teoremasi:**\n"
            "• x₁ + x₂ = -b/a\n"
            "• x₁ * x₂ = c/a"
        ),
        "🍕 Kasrlar va EKUB": (
            "🍕 **Kasrlar va EKUB:**\n\n"
            "• **EKUB:** Berilgan sonlarning har birini bo'ladigan eng katta son.\n"
            "• **EKUK:** Berilgan sonlarning har biriga bo'linadigan eng kichik son.\n"
            "• a * b = EKUB(a,b) * EKUK(a,b)"
        ),
        "📐 Geometriya": (
            "📐 **Geometriya (7-8 sinf):**\n\n"
            "• Pifagor teoremasi: a² + b² = c²\n"
            "• Uchburchak yuzi: S = (a * h) / 2\n"
            "• Aylana uzunligi: L = 2πr"
        )
    },
    "9-11": {
        "📐 Trigonometriya": (
            "📐 **Trigonometriya:**\n\n"
            "• sin²α + cos²α = 1\n"
            "• tgα = sinα / cosα\n"
            "• sin(2α) = 2sinαcosα\n"
            "• cos(2α) = cos²α - sin²α"
        ),
        "🧬 Progressiya": (
            "🧬 **Progressiyalar:**\n\n"
            "**Arifmetik:**\n"
            "• aₙ = a₁ + (n-1)d\n"
            "• Sₙ = (a₁+aₙ)*n / 2\n\n"
            "**Geometrik:**\n"
            "• bₙ = b₁ * qⁿ⁻¹"
        ),
        "♾ Analiz": (
            "♾ **Analiz asoslari:**\n\n"
            "• (xⁿ)' = nxⁿ⁻¹\n"
            "• (sin x)' = cos x\n"
            "• logₐ b = x  => aˣ = b\n"
            "• ∫ xⁿ dx = (xⁿ⁺¹) / (n+1) + C"
        ),
        "📦 Stereometriya": (
            "📦 **Fazoviy shakllar:**\n\n"
            "• Prizma: V = S_asos * h\n"
            "• Shar: V = 4/3 * πr³\n"
            "• Silindr: V = πr²h"
        )
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
async def start_solving(message: types.Message):
    builder = InlineKeyboardBuilder()
    for i in range(1, 12):
        builder.button(text=f"{i}-sinf", callback_data=f"solve_{i}")
    builder.adjust(3)
    await message.answer("Qaysi sinf misolini yechasiz?", reply_markup=builder.as_markup())

@dp.callback_query(F.data.startswith("solve_"))
async def generate_problem(callback: types.CallbackQuery, state: FSMContext):
    grade = int(callback.data.split("_")[1])
    task, ans = "", 0
    if grade == 1:
        a, b = random.randint(1, 15), random.randint(1, 15)
        task, ans = f"{a} + {b} = ?", a + b
    elif grade == 2:
        a, b = random.randint(2, 9), random.randint(2, 9)
        task, ans = f"{a} * {b} = ?", a * b
    elif grade == 3:
        a, b = random.randint(20, 50), random.randint(2, 6)
        task, ans = f"{a} : {b} qoldig'i?", a % b
    elif grade == 5:
        task, ans = "EKUB(12, 18) = ?", 6
    elif grade == 8:
        task, ans = "x² - 5x + 6 = 0. Katta ildizini toping.", 3
    elif grade == 10:
        task, ans = "sin²(45°) + cos²(45°) = ?", 1
    elif grade == 11:
        task, ans = "log₂(32) = ?", 5
    else:
        a, b = random.randint(10, 100), random.randint(10, 100)
        task, ans = f"{a} + {b} = ?", a + b

    await state.update_data(correct_ans=ans)
    await callback.message.edit_text(f"📝 {grade}-sinf misoli:\n\n`{task}`")
    await state.set_state(StudyState.solving_task)

@dp.message(StudyState.solving_task)
async def check_answer(message: types.Message, state: FSMContext):
    data = await state.get_data()
    try:
        if int(message.text) == data['correct_ans']:
            await message.answer("✅ To'g'ri! Barakalla!", reply_markup=main_menu())
        else:
            await message.answer(f"❌ Xato. To'g'ri javob: {data['correct_ans']}", reply_markup=main_menu())
    except:
        await message.answer("⚠️ Faqat son yozing.")
    await state.clear()

@dp.message(F.text == "📞 Aloqa")
async def contact(message: types.Message):
    await message.answer("🆘 Savollar bo'lsa admin @UlmasovSh011 ga murojaat qiling.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
