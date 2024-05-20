from aiogram.types import CallbackQuery, ChosenInlineResult
from game import TicTacToe
from storage import storage


class StorageControl:
    @classmethod
    def get_key(cls, call: CallbackQuery | ChosenInlineResult) -> tuple[int, int] | str:
        if call.inline_message_id:
            return call.inline_message_id
        return call.message.chat.id, call.message.message_id

    @classmethod
    def set_game_storage(cls, game: TicTacToe, call: CallbackQuery | ChosenInlineResult) -> None:
        storage[cls.get_key(call)] = {'game': game}

    @classmethod
    def get_game_storage(cls, call: CallbackQuery | ChosenInlineResult) -> TicTacToe | None:
        key = cls.get_key(call)
        if key in storage:
            return storage.setdefault(key, 'game')['game']

    @classmethod
    def delete_game_storage(cls, call: CallbackQuery | ChosenInlineResult) -> None:
        del storage[cls.get_key(call)]
