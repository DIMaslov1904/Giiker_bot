from game import TicTacToe
from .get_marker import get_marker


def get_text_game_end(game: TicTacToe) -> str:
    winner_text_list = ('Ничья', 'Победил {pl1}', 'Победил {pl2}')
    pl1, pl2 = game.get_players()
    winner = game.get_winner()
    text = winner_text_list[winner].format(pl1=pl1.name, pl2=pl2.name) + '\n'
    for i, item in enumerate(game.board):
        text += get_marker(item)
        if (i + 1) % 3 == 0:
            text += '\n'
    return text
