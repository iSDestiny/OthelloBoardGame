# ICS 32 Project 5
# Jason Bugallon 85806059
# USER_INTERFACE MODULE (GUI MODULE)

import game_logic
import tkinter
import point
import menu

NONE = 0
BLACK = 1
WHITE = 2
DEFAULT_FONT = ('Helvetica', 15)


# CLASSES


class OthelloApplication:
    def __init__(self, game_input: dict):
        self._turn = game_input['first_player']
        self._rows = game_input['rows']
        self._columns = game_input['columns']
        self._win_condition = game_input['win_condition']

        self._cells = []
        self._black_discs = []
        self._white_discs = []

        self._black_score_number = 0
        self._white_score_number = 0

        self._root_window = tkinter.Tk()
        self._root_window.title("Othello: Full")

        self._canvas = tkinter.Canvas(
            master=self._root_window, borderwidth=4,
            background='black')

        self._canvas.grid(
            row=0, padx=30, pady=30,
            sticky=tkinter.N + tkinter.S + tkinter.W + tkinter.E)

        self._canvas.bind('<Button-1>', self._on_canvas_clicked)
        self._canvas.bind('<Configure>', self._on_canvas_resized)

        self._info_frame = tkinter.Frame(master=self._root_window, border=1, background='green')
        self._info_frame.grid(
            row=0, column=1, padx=30, pady=30,
            sticky=tkinter.N + tkinter.S + tkinter.W + tkinter.E)

        self._black_score = tkinter.Label(master=self._info_frame, text='Black: {}'.format(self._black_score_number),
                                          font=DEFAULT_FONT)
        self._white_score = tkinter.Label(master=self._info_frame, text='White: {}'.format(self._white_score_number),
                                          font=DEFAULT_FONT)
        self._turn_status = tkinter.Label(master=self._info_frame, text='Turn: {}'.format(self._turn),
                                          font=DEFAULT_FONT)
        self._switch_color_button = tkinter.Button(
            master=self._info_frame, text='Switch Color',
            font=DEFAULT_FONT, command=self._on_next_pressed
        )
        self._start_button = tkinter.Button(
            master=self._info_frame, text='START',
            font=DEFAULT_FONT, command=self._start_button_pressed)

        self._black_score.grid(row=1, columnspan=1, padx=1, pady=10, sticky=tkinter.W + tkinter.E)
        self._white_score.grid(row=0, columnspan=1, padx=1, pady=10, sticky=tkinter.W + tkinter.E)
        self._turn_status.grid(row=2, columnspan=1, padx=1, pady=10, sticky=tkinter.W + tkinter.E)
        self._switch_color_button.grid(row=3, padx=1, pady=5, sticky=tkinter.E + tkinter.W)
        self._start_button.grid(row=4, padx=1, pady=5, sticky=tkinter.S + tkinter.W + tkinter.E)
        self._info_frame.rowconfigure(3, weight=1)
        self._root_window.rowconfigure(0, weight=10)
        self._root_window.columnconfigure(0, weight=10)

    def run(self) -> None:
        self._root_window.mainloop()

    def _on_canvas_clicked(self, event: tkinter.Event) -> None:
        width = self._canvas.winfo_width()
        height = self._canvas.winfo_height()

        click_point = point.from_pixel(
            event.x, event.y, width, height)

        self._handle_click(click_point)
        self._redraw_discs()

    def _on_canvas_resized(self, event: tkinter.Event) -> None:
        self._canvas.delete(tkinter.ALL)
        self._redraw_board()
        self._redraw_discs()

    def _redraw_discs(self) -> None:
        canvas_width = self._canvas.winfo_width()
        canvas_height = self._canvas.winfo_height()

        for disc in self._black_discs:
            center_x, center_y = disc.center().pixel(canvas_width, canvas_height)

            radius_x = disc.radius_x() * canvas_width
            radius_y = disc.radius_y() * canvas_height

            self._canvas.create_oval(
                center_x - radius_x, center_y - radius_y,
                center_x + radius_x, center_y + radius_y,
                fill='black', outline='black', width=2, tags=('discs', 'black'))

        for disc in self._white_discs:
            center_x, center_y = disc.center().pixel(canvas_width, canvas_height)

            radius_x = disc.radius_x() * canvas_width
            radius_y = disc.radius_y() * canvas_height

            self._canvas.create_oval(
                center_x - radius_x, center_y - radius_y,
                center_x + radius_x, center_y + radius_y,
                fill='white', outline='black', width=2, tags=('disc', 'white'))

    def _on_next_pressed(self) -> None:
        if self._turn == 'B':
            self._turn = 'W'
            self._turn_status['text'] = 'Turn: {}'.format(self._turn)
        else:
            self._turn = 'B'
            self._turn_status['text'] = 'Turn: {}'.format(self._turn)

    def _redraw_board(self) -> None:
        canvas_width = self._canvas.winfo_width()
        canvas_height = self._canvas.winfo_height()
        cell_width = canvas_width / self._columns
        cell_height = canvas_height / self._rows

        self._cells = []
        for row in range(self._rows):
            cell_list = []
            for column in range(self._columns):
                x1 = column * cell_width
                y1 = row * cell_height
                x2 = x1 + cell_width
                y2 = y1 + cell_height
                cell = self._canvas.create_rectangle(x1, y1, x2, y2, activeoutline='yellow',
                                                     fill='green', width=1, activewidth=3,
                                                     tags='cell')
                cell_list.append(cell)
            self._cells.append(cell_list)

    def _contains(self, click_point: point.Point, cell: int) -> bool:
        width = self._canvas.winfo_width()
        height = self._canvas.winfo_height()

        x1, y1, x2, y2 = self._canvas.coords(cell)
        x, y = click_point.pixel(width, height)
        return x1 < x < x2 and y1 < y < y2

    def _handle_click(self, click_point: point.Point) -> None:
        width = self._canvas.winfo_width()
        height = self._canvas.winfo_height()

        for cell_list in self._cells:
            for cell in cell_list:
                if self._contains(click_point, cell):
                    x1, y1, x2, y2 = self._canvas.coords(cell)
                    center_x = (x1+x2)/2
                    center_y = (y1+y2)/2

                    center_point = point.from_pixel(center_x, center_y, width, height)
                    radius_x = (((x2-x1)/2)/width) - 0.013
                    radius_y = (((y2-y1)/2)/height) - 0.013

                    if self._turn == 'B':
                        self._black_discs.append(OthelloDisc(center_point, radius_x, radius_y))
                    else:
                        self._white_discs.append(OthelloDisc(center_point, radius_x, radius_y))

    def _start_button_pressed(self) -> None:
        initial_board = self._create_initial_board()
        self._game_state = game_logic.GameState(game_input, initial_board)
        self._black_score_number, self._white_score_number = self._game_state.discs()
        self._black_score['text'] = 'Black: {}'.format(self._black_score_number)
        self._white_score['text'] = 'White: {}'.format(self._white_score_number)
        self._switch_color_button.destroy()
        self._start_button.destroy()
        self._canvas.bind('<Button-1>', self._on_canvas_clicked_b)
        self._turn = self._game_state.turn()
        self._turn_status['text'] = 'Turn: {}'.format(self._turn)
        self._display_winner()

    def _create_initial_board(self) -> [[int]]:
        initial_board = []

        for cell_list in self._cells:
            row = []
            for cell in cell_list:
                x1, y1, x2, y2 = self._canvas.coords(cell)
                overlapped = self._canvas.find_overlapping(x1, y1, x2, y2)
                if self._canvas.itemcget(overlapped[-1], 'fill') == 'black':
                    row.append(BLACK)
                elif self._canvas.itemcget(overlapped[-1], 'fill') == 'white':
                    row.append(WHITE)
                else:
                    row.append(NONE)
            initial_board.append(row)
        return initial_board

    def _on_canvas_clicked_b(self, event: tkinter.Event) -> None:
        width = self._canvas.winfo_width()
        height = self._canvas.winfo_height()
        click_point = point.from_pixel(event.x, event.y, width, height)
        user_input = self._get_row_on_click(click_point)
        try:
            self._game_state.skip_turn()
            self._game_state.move(user_input)

            self._turn = self._game_state.turn()
            self._black_score_number, self._white_score_number = self._game_state.discs()

            self._turn_status['text'] = 'Turn: {}'.format(self._turn)
            self._black_score['text'] = 'Black: {}'.format(self._black_score_number)
            self._white_score['text'] = 'White: {}'.format(self._white_score_number)

            self._move_label = tkinter.Label(master=self._info_frame, text='VALID MOVE', font=DEFAULT_FONT)
            self._move_label.grid(row=3, padx=1, pady=5, sticky=tkinter.E + tkinter.W)

            self._convert_board_to_discs()
            self._redraw_discs()
            self._display_winner()

        except (game_logic.InvalidMoveError, game_logic.GameOverError):
            self._move_label = tkinter.Label(master=self._info_frame, text='INVALID MOVE', font=DEFAULT_FONT)
            self._move_label.grid(row=3, padx=1, pady=5, sticky=tkinter.E + tkinter.W)
            self._display_winner()

    def _get_row_on_click(self, click_point: point.Point) -> list:
        for row in range(len(self._cells)):
            for column in range(len(self._cells[row])):
                if self._contains(click_point, self._cells[row][column]):
                    return [row+1, column+1]

    def _convert_board_to_discs(self) -> None:
        game_board = self._game_state.return_board()

        width = self._canvas.winfo_width()
        height = self._canvas.winfo_height()

        for row in range(len(game_board)):
            for column in range(len(game_board[row])):
                cell = self._cells[row][column]
                x1, y1, x2, y2 = self._canvas.coords(cell)

                center_x = (x1 + x2) / 2
                center_y = (y1 + y2) / 2

                center_point = point.from_pixel(center_x, center_y, width, height)
                radius_x = (((x2 - x1) / 2) / width) - 0.013
                radius_y = (((y2 - y1) / 2) / height) - 0.013

                self._delete_overlaying(center_point)

                if game_board[row][column] == BLACK:
                    self._black_discs.append(OthelloDisc(center_point, radius_x, radius_y))
                elif game_board[row][column] == WHITE:
                    self._white_discs.append(OthelloDisc(center_point, radius_x, radius_y))

    def _delete_overlaying(self, center_point: point.Point) -> None:
        for i in range(len(self._black_discs)):
            if self._black_discs[i].center().frac() == center_point.frac():
                del self._black_discs[i]
                return

        for i in range(len(self._white_discs)):
            if self._white_discs[i].center().frac() == center_point.frac():
                del self._white_discs[i]
                return

    def _display_winner(self) -> None:
        winner = self._game_state.winner()
        self._winner_label = tkinter.Label(master=self._info_frame, font=DEFAULT_FONT)
        if winner == BLACK:
            self._winner_label['text'] = 'Winner: Black'
        elif winner == WHITE:
            self._winner_label['text'] = 'Winner: White'
        elif winner == 3:
            self._winner_label['text'] = 'Winner: None'
        if winner != 0:
            self._winner_label.grid(row=4, padx=1, pady=5, sticky=tkinter.E + tkinter.W)


class OthelloDisc:
    def __init__(self, center_point: point.Point, radius_x: int, radius_y: int):
        self._center = center_point
        self._radius_x = radius_x
        self._radius_y = radius_y

    def center(self) -> point.Point:
        return self._center

    def radius_x(self) -> float:
        return self._radius_x

    def radius_y(self) -> int:
        return self._radius_y


# MAIN FUNCTION


def main():
    pass


if __name__ == '__main__':
    menu = menu.OthelloMenu()
    menu.run()
    game_input = menu.all_user_input()
    othello = OthelloApplication(game_input)
    othello.run()

