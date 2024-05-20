from game import TicTacToePlayer


def get_scoreboard_players(players: tuple[TicTacToePlayer, TicTacToePlayer]) -> str:
    if players[0].symbol == 'X':
        player_x, player_o = players
    else:
        player_o, player_x, = players

    result = f"""
❌ {player_x.name or '?'} {'👈' if player_x.is_current else ''}
⭕️ {player_o.name or '?'} {'👈' if player_o.is_current else ''}
        """
    return result
