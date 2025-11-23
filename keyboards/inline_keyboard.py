from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

async def main_menu_kb():
    inline_kb_list = [
        [InlineKeyboardButton(text="О боте", callback_data='about')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)

async def home_kb():
    inline_kb_list = [
        [InlineKeyboardButton(text="Главное меню", callback_data='home')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)

async def back_kb(callback):
    inline_kb_list = [[InlineKeyboardButton(text="Назад", callback_data=f'{callback}')]]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)
