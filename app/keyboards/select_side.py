from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def select_side_kb(mode: int = None) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text='❌', callback_data=f'select_side_X{'_0' if mode == 0 else ''}')
    kb.button(text='🔵', callback_data=f'select_side_O{'_0' if mode == 0 else ''}')
    kb.adjust(2)
    return kb.as_markup()
