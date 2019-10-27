# ICS 32 Project 5
# Jason Bugallon 85806059
# GAME_LOGIC MODULE

from collections import namedtuple

NONE = 0
BLACK = 1
WHITE = 2

Coordinates = namedtuple('Coordinates', [
    'up', 'down', 'right', 'left',
    'up_right', 'up_left',
    'down_right', 'down_left'
])


# EXCEPTIONS

class InvalidMoveError(Exception):
    """ Raised whenever an invalid move is made """
    pass


class InvalidColumnError(Exception):
    """ Raised whenever an invalid column is entered """
    pass


class InvalidRowError(Exception):
    """ Raised whenever an invalid row is entered """
    pass


class GameOverError(Exception):
    """
    Raised whenever an attempt is made to make a move after the game is
    already over
    """
    pass


# CLASSES

class GameState:
    def __init__(self, game_input: dict, initial_board: [[int]]):
        self._board = initial_board
        self._turn = game_input['first_player']
        self._rows = game_input['rows']
        self._columns = game_input['columns']
        self._win_condition = game_input['win_condition']
        self._winner = NONE
        self._black = _check_discs(self._board)[0]
        self._white = _check_discs(self._board)[1]

    def winner(self) -> int:
        none_count = 0
        tie = 3

        for row in self._board:
            for column in row:
                if column == NONE:
                    none_count += 1

        if self._win_condition == '>':
            if none_count == 0 or not _check_if_any_valid(self._rows, self._columns, self._board):
                if self._black > self._white:
                    self._winner = BLACK
                elif self._white > self._black:
                    self._winner = WHITE
                else:
                    self._winner = tie

        elif self._win_condition == '<':
            if none_count == 0 or not _check_if_any_valid(self._rows, self._columns, self._board):
                if self._black > self._white:
                    self._winner = WHITE
                elif self._white > self._black:
                    self._winner = BLACK
                else:
                    self._winner = tie

        return self._winner

    def discs(self) -> (int, int):
        self._black = _check_discs(self._board)[0]
        self._white = _check_discs(self._board)[1]

        return self._black, self._white

    def turn(self) -> str:
        return self._turn

    def row(self) -> int:
        return self._rows

    def column(self) -> int:
        return self._columns

    def move(self, user_input: list) -> None:
        _require_valid_column_number(user_input[1]-1, self._columns)
        _require_valid_row_number(user_input[0]-1, self._rows)
        _require_game_not_over(self.winner())

        coordinates = _gather_coordinates(user_input[0]-1, user_input[1]-1,
                                          self._rows, self._columns, self._turn, self._board)

        _check_move(coordinates, self._board, self._turn)
        _check_if_empty(user_input, self._board)

        self._board = _flip_discs(coordinates, self._turn, self._board)
        self._board = _place_disc(user_input, self._board, self._turn)
        self._turn = _opposite_turn(self._turn)

    def skip_turn(self) -> None:
        valid_count = _check_if_any_valid_this_turn(self._rows, self._columns, self._turn, self._board)

        if valid_count == 0:
            self._turn = _opposite_turn(self._turn)

    def return_board(self) -> [[int]]:
        return self._board


# PRIVATE FUNCTIONS


def _check_discs(board: [[int]]) -> tuple:
    black_count = 0
    white_count = 0

    for row in board:
        for column in row:
            if column == BLACK:
                black_count += 1
            elif column == WHITE:
                white_count += 1

    return black_count, white_count


def _check_move(coordinates: Coordinates, board: [[int]], turn: str) -> None:
    disc_count = _check_for_valid_coordinate(coordinates, board, turn)

    if disc_count == 0:
        raise InvalidMoveError


def _check_for_valid_coordinate(coordinates: Coordinates, board: [[int]], turn: str) -> int:
    list_of_disc_lists = _separate_coordinates(coordinates, board)
    disc_count = 0

    for disc_list in list_of_disc_lists:
        if turn == 'B':
            if WHITE in disc_list and BLACK == disc_list[-1] and NONE not in disc_list:
                disc_count += 1

        elif BLACK in disc_list and WHITE == disc_list[-1] and NONE not in disc_list:
            disc_count += 1

    return disc_count


def _separate_coordinates(coordinates: Coordinates, board: [[int]]) -> list:
    reformed_list = []

    for direction in coordinates:
        disc_list = _convert_to_discs(direction, board)
        reformed_list.append(disc_list)

    return reformed_list


def _check_if_any_valid_this_turn(max_row: int, max_column: int, turn: str, board: [[int]]) -> int:
    valid_count = 0

    for row in range(len(board)):
        for column in range(len(board[row])):
            if board[row][column] == NONE:
                coordinates = _gather_coordinates(row, column, max_row, max_column, turn, board)
                disc_count = _check_for_valid_coordinate(coordinates, board, turn)

                if disc_count:
                    valid_count += 1

    return valid_count


def _check_if_any_valid(max_row: int, max_column: int, board: [[int]]) -> bool:
    valid_count_b = _check_if_any_valid_this_turn(max_row, max_column, 'B', board)
    valid_count_w = _check_if_any_valid_this_turn(max_row, max_column, 'W', board)

    if valid_count_b == 0 and valid_count_w == 0:
        return False
    return True


def _place_disc(user_input: list, board: [[int]], turn: str) -> [[int]]:
    row = int(user_input[0]) - 1
    column = int(user_input[1]) - 1

    if turn == 'B':
        board[row][column] += 1
    else:
        board[row][column] += 2
    return board


def _check_if_empty(user_input: list, board: [[int]]):
    row = int(user_input[0]) - 1
    column = int(user_input[1]) - 1

    if board[row][column] != 0:
        raise InvalidMoveError


def _convert_to_discs(direction: [tuple], board: [[int]]) -> list:
    reformed_list = []

    for coordinate in direction:
        disc = board[coordinate[0]][coordinate[1]]
        reformed_list.append(disc)

    return reformed_list


def _flip_discs(coordinates: Coordinates, turn: str, board: [[int]]) -> [[int]]:
    for direction in coordinates:
        if type(direction) is not None and len(direction) > 0:
            for coordinate in direction:
                row, column = coordinate
                last_row, last_column = direction[-1]
                discs = _convert_to_discs(direction, board)

                if turn == 'B':
                    if board[row][column] == WHITE and board[last_row][last_column] == BLACK and NONE not in discs:
                        board[row][column] -= 1
                elif board[row][column] == BLACK and board[last_row][last_column] == WHITE and NONE not in discs:
                    board[row][column] += 1
    return board


def _require_valid_column_number(column_number: int, max_column: int) -> None:
    if not _is_valid_column_number(column_number, max_column):
        raise InvalidColumnError()


def _require_valid_row_number(row_number: int, max_row: int) -> None:
    if not _is_valid_row_number(row_number, max_row):
        raise InvalidRowError()


def _require_game_not_over(winner: int) -> None:
    if winner != NONE:
        raise GameOverError()


def _is_valid_column_number(column_number: int, max_column: int) -> bool:
    return 0 <= column_number < max_column


def _is_valid_row_number(row_number: int, max_row: int) -> bool:
    return 0 <= row_number < max_row


def _gather_coordinates(row: int, column: int, max_row: int, max_column: int, turn: str, board: [[int]]) -> Coordinates:
    list_of_directions = ['UP', 'DOWN', 'RIGHT', 'LEFT', 'UP RIGHT', 'UP LEFT', 'DOWN RIGHT', 'DOWN LEFT']
    coordinate_list = []
    for direction in list_of_directions:
        coordinates = _find_coordinates(row, column, max_row, max_column, direction, turn, board)
        coordinate_list.append(coordinates)

    coordinate_object = Coordinates(
        coordinate_list[0], coordinate_list[1],
        coordinate_list[2], coordinate_list[3],
        coordinate_list[4], coordinate_list[5],
        coordinate_list[6], coordinate_list[7]
    )
    return coordinate_object


def _find_coordinates(row: int, column: int, max_row: int, max_column: int,
                      direction: str, turn: str, board: [[int]]) -> [tuple]:
    coordinates = []
    coordinate = (row, column)
    max_coordinate = (max_row, max_column)

    if direction == 'UP':
        while not _check_if_edge(row, max_row, column, max_column, direction) and not \
                _check_if_current(coordinate, turn, board, max_coordinate):
            row -= 1
            coordinate = (row, column)
            if _is_valid_row_number(row, max_row) and _is_valid_column_number(column, max_column):
                coordinates.append(coordinate)

    elif direction == 'DOWN':
        while not _check_if_edge(row, max_row, column, max_column, direction) and not \
                _check_if_current(coordinate, turn, board, max_coordinate):
            row += 1
            coordinate = (row, column)
            if _is_valid_row_number(row, max_row) and _is_valid_column_number(column, max_column):
                coordinates.append(coordinate)

    elif direction == 'RIGHT':
        while not _check_if_edge(row, max_row, column, max_column, direction) and not \
                _check_if_current(coordinate, turn, board, max_coordinate):
            column += 1
            coordinate = (row, column)
            if _is_valid_row_number(row, max_row) and _is_valid_column_number(column, max_column):
                coordinates.append(coordinate)

    elif direction == 'LEFT':
        while not _check_if_edge(row, max_row, column, max_column, direction) and not \
                _check_if_current(coordinate, turn, board, max_coordinate):
            column -= 1
            coordinate = (row, column)
            if _is_valid_row_number(row, max_row) and _is_valid_column_number(column, max_column):
                coordinates.append(coordinate)

    elif direction == 'UP RIGHT':
        while not _check_if_edge(row, max_row, column, max_column, direction) and not \
                _check_if_current(coordinate, turn, board, max_coordinate):
            column += 1
            row -= 1
            coordinate = (row, column)
            if _is_valid_row_number(row, max_row) and _is_valid_column_number(column, max_column):
                coordinates.append(coordinate)

    elif direction == 'UP LEFT':
        while not _check_if_edge(row, max_row, column, max_column, direction) and not \
                _check_if_current(coordinate, turn, board, max_coordinate):
            column -= 1
            row -= 1
            coordinate = (row, column)
            if _is_valid_row_number(row, max_row) and _is_valid_column_number(column, max_column):
                coordinates.append(coordinate)

    elif direction == 'DOWN RIGHT':
        while not _check_if_edge(row, max_row, column, max_column, direction) and not \
                _check_if_current(coordinate, turn, board, max_coordinate):
            column += 1
            row += 1
            coordinate = (row, column)
            if _is_valid_row_number(row, max_row) and _is_valid_column_number(column, max_column):
                coordinates.append(coordinate)

    elif direction == 'DOWN LEFT':
        while not _check_if_edge(row, max_row, column, max_column, direction) and not \
                _check_if_current(coordinate, turn, board, max_coordinate):
            column -= 1
            row += 1
            coordinate = (row, column)
            if _is_valid_row_number(row, max_row) and _is_valid_column_number(column, max_column):
                coordinates.append(coordinate)

    return coordinates


def _check_if_edge(row: int, max_row: int, column: int, max_column: int, direction: str) -> bool:
    if _is_valid_row_number(row, max_row) and _is_valid_column_number(column, max_column):
        if direction == 'UP':
            return row == 0
        elif direction == 'DOWN':
            return row == max_row
        elif direction == 'RIGHT':
            return column == max_column
        elif direction == 'LEFT':
            return column == 0
        elif direction == 'UP RIGHT':
            return row == 0 or column == max_column
        elif direction == 'UP LEFT':
            return row == 0 or column == 0
        elif direction == 'DOWN RIGHT':
            return row == max_row or column == max_column
        else:
            return row == max_row or column == 0


def _check_if_current(coordinate: tuple, turn: str, board: [[int]], max_coordinate: tuple) -> bool:
    row, column = coordinate
    max_row, max_column = max_coordinate
    if _is_valid_row_number(row, max_row) and _is_valid_column_number(column, max_column):
        if turn == 'B':
            return board[row][column] == BLACK

        else:
            return board[row][column] == WHITE
    else:
        return True


def _opposite_turn(turn: str) -> str:
    if turn == 'B':
        return 'W'
    else:
        return 'B'
