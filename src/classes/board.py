import numpy as np
from pydantic import BaseModel, Field

from src.classes.game_status import GameStatus
from src.classes.player import Player
from src.classes.player_move import Move


class Board(BaseModel):
    board_cells: np.ndarray = Field(default_factory=lambda: np.zeros((3, 3), dtype=int))

    class Config:
        arbitrary_types_allowed = True

    def __str__(self):
        symbol_map = {0: " ", 1: "X", -1: "O"}
        rows = []
        for row in self.board_cells:
            formatted_row = " | ".join(symbol_map.get(cell, "?") for cell in row)
            rows.append(formatted_row)
        return "\n---------\n".join(rows)

    def is_valid_move(self, move: Move, player: Player) -> bool:
        conditions = [move.isInValidRange(), self.is_cell_free(move)]
        if move.move_existing_piece:
            conditions.append(
                self.matching_player_symbol_and_board_cell_symbol(player, move)
            )
        return all(conditions)

    def matching_player_symbol_and_board_cell_symbol(self, player, move) -> bool:
        return player.symbol_val == self.board_cells[move.from_row, move.from_col]

    def is_cell_free(self, move: Move) -> bool:
        return self.board_cells[move.to_row, move.to_col] == 0

    def reset_game(self) -> None:
        self.clear_board()

    def _clear_board(self) -> None:
        self.board_cells = np.zeros((3, 3))

    def update_board(self, move: Move, player: Player) -> None:
        if move.move_existing_piece:
            self.board_cells[move.from_row, move.from_col] = 0
        self.board_cells[move.to_row, move.to_col] = player.symbol_val

    def check_for_winning_pos(self) -> GameStatus:
        if (
            self.check_vertical_win_pos()
            | self.check_horizontal_win_pos()
            | self.check_diagonal_win_pos()
        ):
            return GameStatus.FINISHED
        else:
            return GameStatus.ACTIVE

    def check_vertical_win_pos(self) -> bool:
        for i in range(3):
            identical_pieces_in_pos = abs(sum(self.board_cells[i, :]))
            if identical_pieces_in_pos == 3:
                return True
        else:
            return False

    def check_horizontal_win_pos(self) -> bool:
        for i in range(3):
            identical_pieces_in_pos = abs(sum(self.board_cells[:, i]))
            if identical_pieces_in_pos == 3:
                return True
        else:
            return False

    def check_diagonal_win_pos(self) -> bool:
        upper_left_to_lower_right_diag = abs(
            self.board_cells[0, 0] + self.board_cells[1, 1] + self.board_cells[2, 2]
        )
        upper_right_to_lower_left_diag = abs(
            self.board_cells[2, 0] + self.board_cells[1, 1] + self.board_cells[0, 2]
        )
        if (upper_left_to_lower_right_diag == 3) | (
            upper_right_to_lower_left_diag == 3
        ):
            return True
        else:
            return False
