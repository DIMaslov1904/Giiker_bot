# победные комбинации
victories = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]


class TicTacToePlayer:
    def __init__(self, symbol: str, name: str | None = None, player_id: int = None, is_current: bool = False) -> None:
        self.symbol = symbol
        self.history_steps = []
        self.id = player_id
        self.name = name
        self.is_current = is_current

    def get_deleted(self) -> None | int:
        if len(self.history_steps) > 2:
            return self.history_steps[0]

    def step(self, index: int) -> None | int:
        self.history_steps.append(index)
        if len(self.history_steps) > 3:
            return self.history_steps.pop(0)

    def change(self, player_id: int, name: str | None) -> None:
        self.id = player_id
        self.name = name


class TicTacToe:
    _player1 = None
    _player2 = None
    user_id = None
    _winner = -1

    def __init__(self, mode: int = 0) -> None:
        """
        Giiker Крестики-нолики
        :param mode:
            0 - игрок против игрока || 1 - игрок против бота
        """
        self.board = list(range(9))  # Игровое поле (список от 0 до 8)
        self._mode = mode

    def _validate_init(self, symbol: str) -> None:
        if self._player2 and self._player2.name:
            raise ValueError('Игроки уже заданы')
        if symbol not in ('X', 'O'):
            raise ValueError(
                "Не верный символ пользователя. Выберите либо 'X' либо 'O'"
            )

    def set_player(self, symbol: str, player_id: int, name: str = 'Игрок') -> None:
        """
        Установка игрока в игре против бота
        :param symbol: Символ игрока
        :param player_id: Ид игрока
        :param name: имя игрока
        """
        self._validate_init(symbol)

        self._player1 = TicTacToePlayer(symbol, player_id=player_id, name=name)

        symbol_player2 = "O" if symbol == "X" else "X"
        self._player2 = TicTacToePlayer(symbol_player2)
        self._init_current_player()
        if self._mode == 1:
            self.set_player2(player_id=0, name='Бот')
            self._check_step_bot()

    def set_player2(self, player_id: int, name: str) -> None:
        self._player2.change(name=name, player_id=player_id)

    def _set_current_player(self, player: TicTacToePlayer) -> None:
        self._current_player = player
        player.is_current = True
        if player == self._player1:
            self._player2.is_current = False
        else:
            self._player1.is_current = False

    def _init_current_player(self) -> TicTacToePlayer:
        """Инициализация игрока делающего первый ход"""
        if self._player1.symbol == 'X':
            self._set_current_player(self._player1)
        else:
            self._set_current_player(self._player2)
        return self._current_player

    def _change_current_player(self) -> TicTacToePlayer:
        """Изменение текущего игрока"""
        if self._current_player == self._player1:
            self._set_current_player(self._player2)
        else:
            self._set_current_player(self._player1)
        return self._current_player

    def _check_step_bot(self):
        if (self._mode == 1) and (self._winner == -1) and (self._current_player == self._player2):
            step_bot = self._bot()
            self.step(step_bot)

    def _check_employment(self, step: int) -> bool:
        return isinstance(self.board[step], str)

    def get_deleted(self) -> None | int:
        current_player = self._current_player
        return current_player.get_deleted()

    def step(self, step: int) -> int:
        """
        Сделать ход
        :param step: индекс позиции хода
        :return:
            -2 - ошибка, ячейка уже занята
            -1 - следующий ход
            0 - ничья
            1 - победа первого игрока
            2 - победа второго игрока

        """
        if self._check_employment(step):
            return -2

        delete_step = self._current_player.step(step)
        if delete_step is not None:
            self.board[delete_step] = delete_step

        self.board[step] = self._current_player.symbol
        self._winner = self._get_result()

        self._change_current_player()

        self._check_step_bot()
        return self._winner

    def _get_victories_line(self, victory_line: list[int], symbol: str) -> bool:
        return (
                self.board[victory_line[0]] == symbol and
                self.board[victory_line[1]] == symbol and
                self.board[victory_line[2]] == symbol
        )

    def _get_result(self) -> int:
        """Проверка результатов"""
        if all(isinstance(x, str) for x in self.board):
            return 0
        for victory_line in victories:
            if self._get_victories_line(victory_line, self._player1.symbol):
                return 1
            if self._get_victories_line(victory_line, self._player2.symbol):
                return 2
        return -1

    def _check_line(self, sum_o: int, sum_x: int) -> int:
        """Проверка победных линий. Отдает правильный ход"""
        for line in victories:
            o = 0
            x = 0
            for j in range(0, 3):
                if self.board[line[j]] == self._player1.symbol:
                    o = o + 1
                if self.board[line[j]] == self._player2.symbol:
                    x = x + 1
            if o == sum_o and x == sum_x:
                for j in range(0, 3):
                    if self.board[line[j]] != self._player1.symbol and self.board[line[j]] != self._player2.symbol:
                        return line[j]

    def _bot(self) -> int:
        """Бот"""
        # Если этим ходом можем выиграть — выигрываем (уже 2 нолика стоят на одной из линий)
        if step := self._check_line(2, 0):
            return step
        # Если можем помешать выиграть человеку — мешаем (у человека уже 2 крестика на линии — ставим на нее нолик)
        if step := self._check_line(0, 2):
            return step
        # Если на линии одна наша фигура — ставим вторую
        if step := self._check_line(1, 0):
            return step
        # Если центр не занят ставим нолик в центр
        if self.board[4] != self._player2.symbol and self.board[4] != self._player1.symbol:
            return 4
        # Ставим в левый верхний угол
        return 0

    def get_winner(self) -> int:
        return self._winner

    def get_players(self) -> tuple[TicTacToePlayer, 2]:
        return self._player1, self._player2

    def get_current_player(self) -> TicTacToePlayer:
        return self._current_player

    def print_board(self):
        """Вывод игрового поля"""
        for i, item in enumerate(self.board):
            print(item, end="\n" if (i + 1) % 3 == 0 else " ")
