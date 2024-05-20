from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from utils import get_marker
from game import TicTacToe


def board_kb(game: TicTacToe) -> InlineKeyboardMarkup:
    deleted_index = game.get_deleted()
    kb = InlineKeyboardBuilder()
    for i, value in enumerate(game.board):
        text = get_marker(value, deleted=(deleted_index == i))
        kb.button(text=text, callback_data=f"click_board_{i}")
    kb.adjust(3)
    return kb.as_markup()
