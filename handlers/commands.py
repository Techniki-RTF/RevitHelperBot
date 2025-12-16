from aiogram.fsm.context import FSMContext
from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from services.menu_services import handle_start_command, show_about

start_cmd_router = Router()

@start_cmd_router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await handle_start_command(message)

@start_cmd_router.message(Command("about"))
async def cmd_about(message: Message):
    await show_about(message)

@start_cmd_router.message(Command("cancel"))
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("❌ Операция отменена")
    await cmd_start(message, state)