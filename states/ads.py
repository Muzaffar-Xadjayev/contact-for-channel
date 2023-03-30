from aiogram.dispatcher.filters.state import State, StatesGroup

class Advers(StatesGroup):
    text = State()

class One(StatesGroup):
    text=State()