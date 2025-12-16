from aiogram.fsm.state import StatesGroup, State

class ConsultationStates(StatesGroup):
    in_progress = State()

class WikiStates(StatesGroup):
    waiting_for_title = State()
    waiting_for_content = State()
    waiting_for_approval = State()
    waiting_for_action_with_page = State()
