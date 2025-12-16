from aiogram.fsm.context import FSMContext
from aiogram import Router
from aiogram.types import Message
from states import WikiStates

from services.wiki import wiki_add_page_title_got, wiki_add_page_content_got

start_msg_router = Router()

@start_msg_router.message(WikiStates.waiting_for_title)
async def handle_wiki_add_page_title(message: Message, state: FSMContext):
    await wiki_add_page_title_got(message, state)

@start_msg_router.message(WikiStates.waiting_for_content)
async def handle_wiki_add_page_title(message: Message, state: FSMContext):
    await wiki_add_page_content_got(message, state)
