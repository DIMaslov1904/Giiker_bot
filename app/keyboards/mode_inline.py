from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def mode_inline_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="🔄", switch_inline_query_current_chat='')
    kb.button(text='🤖', url='https://t.me/Giiker_bot?start')
    kb.adjust(2)
    return kb.as_markup()

