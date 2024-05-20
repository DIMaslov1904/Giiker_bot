from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def mode_kb(column: bool = False) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text='Игра с ботом 🤖', callback_data="select_mode_1")
    kb.button(text="Игра с другом 👥", switch_inline_query='')
    kb.adjust(1 if column else 2)
    return kb.as_markup()

