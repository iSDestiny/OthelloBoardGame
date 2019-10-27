# ICS 32 Project 5
# Jason Bugallon 85806059
# MENU_MODULE

import tkinter

DEFAULT_FONT = ('Helvetica', 15)


class OthelloMenu:
    def __init__(self):
        self._user_input = {}

        self._root_window = tkinter.Tk()
        self._root_window.title("Othello Menu")

        tkinter.Label(master=self._root_window, text='Number of Rows (Even 4-16):',
                      font=DEFAULT_FONT).grid(
            row=0, sticky=tkinter.W, pady=10, padx=10)
        tkinter.Label(master=self._root_window, text='Number of Columns (Even 4-16):',
                      font=DEFAULT_FONT).grid(
            row=1, sticky=tkinter.W, pady=10, padx=10)
        tkinter.Label(master=self._root_window, text='Initial Player: ', font=DEFAULT_FONT).grid(
            row=2, sticky=tkinter.W, pady=10, padx=10)
        tkinter.Label(master=self._root_window, text='Win Conditions: ', font=DEFAULT_FONT).grid(
            row=3, sticky=tkinter.W, pady=10, padx=10)

        self._rows_mb = tkinter.Menubutton(master=self._root_window, text='Rows', relief='raised',
                                           font=DEFAULT_FONT)
        self._columns_mb = tkinter.Menubutton(master=self._root_window, text='Columns', relief='raised',
                                              font=DEFAULT_FONT)

        self._rows_mb.grid(row=0, column=1, sticky=tkinter.E + tkinter.W, pady=10, padx=10, columnspan=2)
        self._columns_mb.grid(row=1, column=1, sticky=tkinter.E + tkinter.W, pady=10, padx=10, columnspan=2)

        self._rows_menu = tkinter.Menu(self._rows_mb, tearoff=0, font=DEFAULT_FONT)
        self._columns_menu = tkinter.Menu(self._columns_mb, tearoff=0, font=DEFAULT_FONT)

        self._rows_mb['menu'] = self._rows_menu
        self._columns_mb['menu'] = self._columns_menu

        column_commands = {
            4: self._get_column_4, 6: self._get_column_6, 8: self._get_column_8,
            10: self._get_column_10, 12: self._get_column_12, 14: self._get_column_14, 16: self._get_column_16
        }

        row_commands = {
            4: self._get_row_4, 6: self._get_row_6(), 8: self._get_row_8,
            10: self._get_row_10, 12: self._get_row_12, 14: self._get_row_14, 16: self._get_row_16
        }
        for i in range(4, 17, 2):
            self._rows_menu.add_command(label=i, command=row_commands[i])
            self._columns_menu.add_command(label=i, command=column_commands[i])

        self._rows_mb.grid(row=0, column=1, sticky=tkinter.E + tkinter.W, pady=10, padx=10, columnspan=2)
        self._columns_mb.grid(row=1, column=1, sticky=tkinter.E + tkinter.W, pady=10, padx=10, columnspan=2)

        player_control_variable = tkinter.StringVar()
        player_control_variable.set('B')

        self._initial_player1 = tkinter.Radiobutton(
            master=self._root_window, font=DEFAULT_FONT, text='Black', command=self._on_black_checked,
            variable=player_control_variable, value='B', indicatoron=0
        )
        self._initial_player2 = tkinter.Radiobutton(
            master=self._root_window, font=DEFAULT_FONT, text='White', command=self._on_white_checked,
            variable=player_control_variable, value='W', indicatoron=0
        )

        self._initial_player1.grid(row=2, column=1, sticky=tkinter.E + tkinter.W, pady=10, padx=10)
        self._initial_player2.grid(row=2, column=2, sticky=tkinter.E + tkinter.W, pady=10, padx=10)

        win_condition_control_variable = tkinter.StringVar()
        win_condition_control_variable.set('>')

        self._win_condition1 = tkinter.Radiobutton(
            master=self._root_window, font=DEFAULT_FONT, text='Highest Score', indicatoron=0,
            variable=win_condition_control_variable, value='>', command=self._on_higher_checked
        )
        self._win_condition2 = tkinter.Radiobutton(
            master=self._root_window, font=DEFAULT_FONT, text='Lowest Score', indicatoron=0,
            variable=win_condition_control_variable, value='<', command=self._on_lower_checked
        )

        self._win_condition1.grid(row=3, column=1, sticky=tkinter.E + tkinter.W, pady=10, padx=10)
        self._win_condition2.grid(row=3, column=2, sticky=tkinter.E + tkinter.W, pady=10, padx=10)

        self._start_button = tkinter.Button(
            master=self._root_window, command=self._on_button_pressed,
            text='START', font=DEFAULT_FONT
        )

        self._start_button.grid(row=4, column=0, columnspan=3, sticky=tkinter.E + tkinter.W, pady=10, padx=10)

    def run(self):
        self._root_window.mainloop()

    def all_user_input(self) -> dict:
        return self._user_input

    def _on_button_pressed(self) -> None:
        self._root_window.destroy()

    def _on_black_checked(self) -> None:
        self._user_input['first_player'] = 'B'

    def _on_white_checked(self) -> None:
        self._user_input['first_player'] = 'W'

    def _on_higher_checked(self) -> None:
        self._user_input['win_condition'] = '>'

    def _on_lower_checked(self) -> None:
        self._user_input['win_condition'] = '<'

    def _get_row_4(self) -> None:
        self._user_input['rows'] = 4

    def _get_row_6(self) -> None:
        self._user_input['rows'] = 6

    def _get_row_8(self) -> None:
        self._user_input['rows'] = 8

    def _get_row_10(self) -> None:
        self._user_input['rows'] = 10

    def _get_row_12(self) -> None:
        self._user_input['rows'] = 12

    def _get_row_14(self) -> None:
        self._user_input['rows'] = 14

    def _get_row_16(self) -> None:
        self._user_input['rows'] = 16

    def _get_column_4(self) -> None:
        self._user_input['columns'] = 4

    def _get_column_6(self) -> None:
        self._user_input['columns'] = 6

    def _get_column_8(self) -> None:
        self._user_input['columns'] = 8

    def _get_column_10(self) -> None:
        self._user_input['columns'] = 10

    def _get_column_12(self) -> None:
        self._user_input['columns'] = 12

    def _get_column_14(self) -> None:
        self._user_input['columns'] = 14

    def _get_column_16(self) -> None:
        self._user_input['columns'] = 16
