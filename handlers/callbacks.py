from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from services.menu_services import show_main_menu, show_about
from services.consultation import start_consultation, handle_consultation_action

start_callback_router = Router()

@start_callback_router.callback_query(F.data == "home")
async def home(callback: CallbackQuery):
    await show_main_menu(callback)

@start_callback_router.callback_query(F.data == "start_consult")
async def start_consult(callback: CallbackQuery, state: FSMContext):
    await start_consultation(callback, state)

@start_callback_router.callback_query(F.data == "consult_done")
async def consult_done(callback: CallbackQuery, state: FSMContext):
    await handle_consultation_action(callback, state, action="done")

@start_callback_router.callback_query(F.data == "consult_skip")
async def consult_skip(callback: CallbackQuery, state: FSMContext):
    await handle_consultation_action(callback, state, action="skip")

@start_callback_router.callback_query(F.data == "about")
async def about(callback: CallbackQuery):
    await show_about(callback)