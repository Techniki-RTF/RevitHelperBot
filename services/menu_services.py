from aiogram.types import Message, CallbackQuery
from typing import Union

from keyboards.inline_keyboard import main_menu_kb, home_kb


async def handle_start_command(context: Union[Message, CallbackQuery]):
    await show_main_menu(context)

async def show_main_menu(context: Union[Message, CallbackQuery]):
    text = f"Привет, {context.from_user.full_name}!\nМеню:"
    if isinstance(context, CallbackQuery):
        await context.answer()
        await context.message.answer(text, reply_markup=main_menu_kb())
        return
    await context.answer(text, reply_markup=await main_menu_kb())
    await context.answer(text, reply_markup=main_menu_kb())

async def show_about(context: Union[Message, CallbackQuery]):
    text = "Разработчики:\nt.me/renamq\nt.me/Blueberry_Roulette\n\nКоманда: Techniki"
    if isinstance(context, CallbackQuery):
        await context.answer()
        await context.message.answer(text, reply_markup=home_kb())
        return
    await context.answer(text, reply_markup=await home_kb())
