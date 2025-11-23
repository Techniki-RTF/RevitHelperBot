from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from services.menu_services import handle_start_command, show_about

start_cmd_router = Router()

@start_cmd_router.message(CommandStart())
async def cmd_start(message: Message):
    await handle_start_command(message)

@start_cmd_router.message(Command("about"))
async def cmd_about(message: Message):
    await show_about(message)