from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from services.menu_services import show_main_menu, show_about
from services.consultation import start_consultation, handle_consultation_action
from services.wiki import wiki_open, wiki_add_page, wiki_show, wiki_show_page, wiki_add_page_approve, wiki_remove_page

start_callback_router = Router()

# TODO: callback should be linked with current state
# if bot was restarted and user is trying to press buttons under previous messages
# it cause undefined behaviour
# so if current state isn't correct (or undefined) for retrieved callback data, then just drop this update

@start_callback_router.callback_query(F.data == "home")
async def home(callback: CallbackQuery):
    await show_main_menu(callback)

@start_callback_router.callback_query(F.data == "cancel")
async def cancel(callback: CallbackQuery):
    await show_main_menu(callback)

@start_callback_router.callback_query(F.data == "start_consult")
async def start_consult(callback: CallbackQuery, state: FSMContext):
    await start_consultation(callback, state)

@start_callback_router.callback_query(F.data == "wiki_open")
async def wiki_open_callback(callback: CallbackQuery):
    await wiki_open(callback)

@start_callback_router.callback_query(F.data == "wiki_add_page")
async def wiki_add_page_callback(callback: CallbackQuery, state: FSMContext):
    await wiki_add_page(callback, state)

@start_callback_router.callback_query(F.data.in_({"wiki_add_page_approve", "wiki_add_page_decline"}))
async def wiki_add_page_approve_callback(callback: CallbackQuery, state: FSMContext):
    await wiki_add_page_approve(callback, state, callback.data == "wiki_add_page_approve")

@start_callback_router.callback_query(F.data == "wiki_show")
async def wiki_show_callback(callback: CallbackQuery, state: FSMContext):
    await wiki_show(callback, state)

@start_callback_router.callback_query(F.data.startswith("wiki_show_page_id_"))
async def wiki_show_page_callback(callback: CallbackQuery, state: FSMContext):
    page_id = int(callback.data.split("_")[-1])
    await wiki_show_page(callback, state, page_id)

@start_callback_router.callback_query(F.data == "wiki_remove_page")
async def wiki_remove_page_callback(callback: CallbackQuery, state: FSMContext):
    await wiki_remove_page(callback, state)

@start_callback_router.callback_query(F.data == "consult_done")
async def consult_done(callback: CallbackQuery, state: FSMContext):
    await handle_consultation_action(callback, state, action="done")

@start_callback_router.callback_query(F.data == "consult_skip")
async def consult_skip(callback: CallbackQuery, state: FSMContext):
    await handle_consultation_action(callback, state, action="skip")

@start_callback_router.callback_query(F.data == "about")
async def about(callback: CallbackQuery):
    await show_about(callback)
