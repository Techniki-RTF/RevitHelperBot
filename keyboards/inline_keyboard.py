from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def main_menu_kb():
    inline_kb_list = [
        [InlineKeyboardButton(text="🔎 Начать консультацию", callback_data="start_consult")],
        [InlineKeyboardButton(text="ℹ️ О боте", callback_data="about")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)


async def consult_step_kb():
    inline_kb_list = [
        [
            InlineKeyboardButton(text="✅ Сделано", callback_data="consult_done"),
            InlineKeyboardButton(text="⏭️ Пропустить", callback_data="consult_skip"),
        ],
        [InlineKeyboardButton(text="🏠 В главное меню", callback_data="home")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)


async def home_kb():
    inline_kb_list = [[InlineKeyboardButton(text="Главное меню", callback_data="home")]]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)


async def back_kb(callback: str):
    inline_kb_list = [[InlineKeyboardButton(text="Назад", callback_data=f"{callback}")]]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)
