from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from typing import Union

from keyboards.inline_keyboard import home_kb, consult_step_kb
from states import ConsultationStates
from .consultation_steps import CONSULT_STEPS, format_step


async def start_consultation(context: Union[Message, CallbackQuery], state: FSMContext):
    await state.set_state(ConsultationStates.in_progress)
    await state.update_data(step=0, answers=[])
    await show_consultation_step(context, state)

async def show_consultation_step(context: Union[Message, CallbackQuery], state: FSMContext):
    data = await state.get_data()
    step = data.get("step", 0)
    if step >= len(CONSULT_STEPS):
        await show_consultation_summary(context, state)
        return
    text = format_step(step)
    if isinstance(context, CallbackQuery):
        await context.answer()
        await context.message.edit_text(text, reply_markup=consult_step_kb())
        return
    await context.answer(text, reply_markup=consult_step_kb())

async def handle_consultation_action(context: CallbackQuery, state: FSMContext, action: str):
    data = await state.get_data()
    step = data.get("step", 0)
    answers = data.get("answers", [])
    if step < len(CONSULT_STEPS):
        answers.append({"key": CONSULT_STEPS[step]["key"], "title": CONSULT_STEPS[step]["title"], "action": action})
    step += 1
    await state.update_data(step=step, answers=answers)
    await show_consultation_step(context, state)


async def show_consultation_summary(context: Union[Message, CallbackQuery], state: FSMContext):
    data = await state.get_data()
    answers = data.get("answers", [])
    lines = ["Итоги консультации:"]
    for idx, ans in enumerate(answers, 1):
        mark = "✅" if ans["action"] == "done" else "⏭️"
        lines.append(f"{mark} {idx}) {ans['title']}")
    text = "\n".join(lines)
    await state.clear()
    if isinstance(context, CallbackQuery):
        await context.answer()
        await context.message.edit_text(text, reply_markup=home_kb())
        return
    await context.answer(text, reply_markup=home_kb())