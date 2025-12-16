from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from create_bot import admins


# TODO: why async?

async def main_menu_kb():
    inline_kb_list = [
        [InlineKeyboardButton(text="🔎 Начать консультацию", callback_data="start_consult")],
        [InlineKeyboardButton(text="📃 База знаний", callback_data="wiki_open")],
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


async def wiki_open_kb(user_id: int):
    inline_kb_list = [
        [InlineKeyboardButton(text="👀️ Посмотреть добавленные статьи", callback_data="wiki_show")],
        [InlineKeyboardButton(text="🏠 В главное меню", callback_data="home")],
    ]
    if user_id in admins:
        inline_kb_list.insert(1,
[InlineKeyboardButton(text="📄 Добавить статью", callback_data="wiki_add_page")])
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)


async def wiki_approval_kb():
    inline_kb_list = [
        [InlineKeyboardButton(text="✅ Добавить", callback_data="wiki_add_page_approve")],
        [InlineKeyboardButton(text="❌ Отменить", callback_data="wiki_add_page_decline")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)


async def wiki_show_kb(pages: list[dict[str, any]]):
    builder = InlineKeyboardBuilder()

    for page in pages:
        builder.button(text=page["title"], callback_data=f'wiki_show_page_id_{page["id"]}')

    builder.button(text="🏠 Главное меню", callback_data="home")
    builder.adjust(1)
    return builder.as_markup()


async def wiki_show_empty_db_kb():
    inline_kb_list = [
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="wiki_open")],
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="home")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)


async def wiki_show_page_kb():
    inline_kb_list = [
        [InlineKeyboardButton(text="⬅️ Назад к списку", callback_data="wiki_show")],
        [InlineKeyboardButton(text="❌️ Удалить", callback_data="wiki_remove_page")],
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="home")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)


async def home_kb():
    inline_kb_list = [[InlineKeyboardButton(text="🏠 Главное меню", callback_data="home")]]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)


async def back_kb(callback: str):
    inline_kb_list = [[InlineKeyboardButton(text="⬅️ Назад", callback_data=f"{callback}")]]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)
