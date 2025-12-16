from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from typing import Union

from keyboards.inline_keyboard import home_kb, wiki_open_kb, wiki_approval_kb, wiki_show_kb, wiki_show_page_kb, wiki_show_empty_db_kb
from states import WikiStates

from create_bot import db

# TODO: use certain types instead of Union[Message, CallbackQuery] to reduce code implicity (?)

async def wiki_open(context: Union[Message, CallbackQuery], state: FSMContext):
    await context.answer()
    await context.message.answer("Меню управления статьями:", reply_markup=await wiki_open_kb())


async def wiki_add_page(context: Union[Message, CallbackQuery], state: FSMContext):
    await context.answer()
    await context.message.answer("✒️ Отправьте название статьи. /cancel для отмены")

    await state.set_state(WikiStates.waiting_for_title)
    await state.update_data(title="", content="")


async def wiki_add_page_title_got(context: Union[Message, CallbackQuery], state: FSMContext):
    # TODO: handle empty text (e.g sticker, video, photo, ..)
    # TODO: don't allow multiline title (?)
    title = context.text

    await context.answer(f'📄 Выбранное название: "{title}"')
    await context.answer("✒️ Отправьте содержимое статьи. /cancel для отмены")

    await state.set_state(WikiStates.waiting_for_content)
    await state.update_data(title=title)


async def wiki_add_page_content_got(context: Union[Message, CallbackQuery], state: FSMContext):
    data = await state.get_data()
    title = data["title"]
    # TODO: handle empty text (e.g sticker, video, photo, ..)
    content = context.text
    await state.set_state(WikiStates.waiting_for_approval)
    await state.update_data(content=content)
    await context.answer(f'📖 "{title}"\n\n{content}')
    await context.answer("Добавить статью в базу?", reply_markup=await wiki_approval_kb())


async def wiki_add_page_approve(context: Union[Message, CallbackQuery], state: FSMContext, approved: bool):
    data = await state.get_data()
    title, content = (data["title"], data["content"])

    if approved:
        # TODO: get the result (e.g updated, created, ..); error handling
        await db.add_page(title, content)

    await state.clear()
    text = "✅ Статья добавлена" if approved else "❌ Статья отклонена"
    await context.message.answer(text, reply_markup=await home_kb())


async def wiki_show(context: Union[Message, CallbackQuery], state: FSMContext):
    await context.answer()
    await state.clear()

    pages = await db.get_all_pages()
    if len(pages) == 0:
        await context.message.answer("❌ База пуста!", reply_markup=await wiki_show_empty_db_kb())
        return

    await context.message.answer("📃 Сохраненные статьи:", reply_markup=await wiki_show_kb(pages))


async def wiki_show_page(context: Union[Message, CallbackQuery], state: FSMContext, page_id: int):
    page = await db.get_page_by_id(page_id)
    if not page:
        # TODO: implement
        pass

    title, content = (page["title"], page["content"])
    text = f'📖 "{title}"\n\n{content}'

    await context.answer()
    await state.set_state(WikiStates.waiting_for_action_with_page)
    await state.update_data(page_id=page_id)
    await context.message.answer(text=text, reply_markup=await wiki_show_page_kb())


async def wiki_remove_page(context: Union[Message, CallbackQuery], state: FSMContext):
    data = await state.get_data()
    page_id = data["page_id"]

    # TODO: retrieve removal result
    await db.delete_page(page_id)

    await context.answer()
    await context.message.answer("❌ Статья удалена!")
    await wiki_show(context, state)
