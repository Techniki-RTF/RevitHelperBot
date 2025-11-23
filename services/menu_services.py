from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from typing import Union

from keyboards.inline_keyboard import main_menu_kb

async def show_main_menu(context: Union[Message, CallbackQuery]):
    await context.answer()
    await context.message.answer(
        f"Привет, {context.from_user.full_name}!\nМеню:",
        reply_markup=await main_menu_kb()
    )
    
async def handle_start_command(user_id: int, context: Union[Message, CallbackQuery], state: FSMContext, bot: Bot = None):
    await show_main_menu(context)