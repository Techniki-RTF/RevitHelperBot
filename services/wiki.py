from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from typing import Union

from keyboards.inline_keyboard import home_kb, wiki_open_kb, wiki_approval_kb, wiki_show_kb, wiki_show_page_kb, \
    wiki_show_empty_db_kb, cancel_kb
from states import WikiStates

from create_bot import db
from utils.permissions import ensure_admin


# TODO: use certain types instead of Union[Message, CallbackQuery] to reduce code implicity (?)

async def wiki_open(context: Union[Message, CallbackQuery]):
    await context.answer()
    await context.message.edit_text("Меню действий со статьями:", reply_markup=wiki_open_kb(context.from_user.id))


async def wiki_add_page(context: Union[Message, CallbackQuery], state: FSMContext):
    if not await ensure_admin(context): return

    await context.answer()
    await context.message.edit_text("✒️ Отправьте название статьи", reply_markup=cancel_kb())

    await state.set_state(WikiStates.waiting_for_title)
    await state.update_data(title="", content="")


async def wiki_add_page_title_got(context: Union[Message, CallbackQuery], state: FSMContext):
    # TODO: handle empty text (e.g sticker, video, photo, ..)
    # TODO: don't allow multiline title (?)
    if not await ensure_admin(context): return

    title = context.text

    await context.answer(f'📄 Выбранное название: "{title}"\n\n✒️ Отправьте содержимое статьи', reply_markup=cancel_kb())

    await state.set_state(WikiStates.waiting_for_content)
    await state.update_data(title=title)


async def wiki_add_page_content_got(context: Union[Message, CallbackQuery], state: FSMContext):
    if not await ensure_admin(context): return
    data = await state.get_data()
    title = data["title"]
    # TODO: handle empty text (e.g sticker, video, photo, ..)
    content = context.text
    await state.set_state(WikiStates.waiting_for_approval)
    await state.update_data(content=content)
    await context.answer(f'📖 "{title}"\n\n{content}Добавить статью в базу?', reply_markup=wiki_approval_kb())


async def wiki_add_page_approve(context: Union[Message, CallbackQuery], state: FSMContext, approved: bool):
    if not await ensure_admin(context): return
    data = await state.get_data()
    title, content = (data["title"], data["content"])

    if approved:
        # TODO: get the result (e.g updated, created, ..); error handling
        await db.add_page(title, content)

    await context.answer()
    await state.clear()
    text = "✅ Статья добавлена" if approved else "❌ Статья отклонена"
    await context.message.edit_text(text, reply_markup=home_kb())


async def wiki_show(context: Union[Message, CallbackQuery], state: FSMContext):
    await context.answer()
    await state.clear()

    pages = await db.get_all_pages()
    if len(pages) == 0:
        await context.message.edit_text("❌ База пуста!", reply_markup=wiki_show_empty_db_kb())
        return

    await context.message.edit_text("📃 Сохраненные статьи:", reply_markup=wiki_show_kb(pages))


async def wiki_show_page(context: Union[Message, CallbackQuery], state: FSMContext, page_id: int):
    page = await db.get_page_by_id(page_id)
    if not page:
        await context.answer()
        await context.message.edit_text("Ошибка!\n\nСтатья не найдена!", reply_markup=wiki_show_empty_db_kb())
        pass

    title, content = (page["title"], page["content"])
    text = f'📖 "{title}"\n\n{content}'

    await context.answer()
    await state.set_state(WikiStates.waiting_for_action_with_page)
    await state.update_data(page_id=page_id)
    await context.message.edit_text(text=text, reply_markup=wiki_show_page_kb())


async def wiki_remove_page(context: Union[Message, CallbackQuery], state: FSMContext):
    if not await ensure_admin(context): return

    data = await state.get_data()
    page_id = data["page_id"]

    # TODO: retrieve removal result
    await db.delete_page(page_id)

    await context.answer()
    await context.message.edit_text("❌ Статья удалена!")
    await wiki_show(context, state)
