from aiogram.types import InputTextMessageContent
from game import TicTacToe
from .get_scoreboard_players import get_scoreboard_players


def set_user_symbol_inline_mode(symbol: str, game: TicTacToe, user) -> InputTextMessageContent:
    game.set_player(symbol=symbol, player_id=user.id, name=user.first_name)
    players = game.get_players()
    message_text = get_scoreboard_players(players)
    return InputTextMessageContent(message_text=message_text)
