from typing import Union
from aiogram.types import CallbackQuery, Message
from create_bot import admins


async def ensure_admin(context: Union[Message, CallbackQuery]) -> bool:
    if context.from_user.id not in admins:
        await context.answer("🚫 Недостаточно прав!")
        return False
    return True