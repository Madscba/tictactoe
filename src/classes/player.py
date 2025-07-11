from pydantic import BaseModel
from abc import abstractmethod
from enum import Enum
from classes.player_move import Move
import typing as T


class PlayerValue(Enum):
    cross = 1
    nought = -1




class Player(BaseModel):
    symbol: str
    active_pieces: int = 0

    @property
    def symbol_val(self) -> PlayerValue:
        return PlayerValue[self.symbol.lower()].value

    def play_turn(self) -> Move:
        if self.active_pieces < 3:
            return self.place_piece()
        else:
            return self.move_piece()

    def increment_active_pieces(self) -> None:
        if self.active_pieces < 3:
            self.active_pieces += 1

    def place_piece(self) -> Move:
        to_row, to_col = self.get_player_move(move_existing_piece=True)

        return Move(to_row=to_row, to_col=to_col, move_existing_piece=False)

    def move_piece(self) -> Move:
        from_row, from_col = self.get_player_move(move_existing_piece=False)
        to_row, to_col = self.get_player_move(move_existing_piece=True)
        return Move(
            to_row=to_row,
            to_col=to_col,
            from_row=from_row,
            from_col=from_col,
            move_existing_piece=True,
        )

    @abstractmethod
    def get_player_move(self, move_existing_piece=True) -> T.Tuple[int, int]:
        pass

class HumanPlayer(Player):
    def get_player_move(self, move_existing_piece=True) -> T.Tuple[int, int]:
        action = "place" if move_existing_piece else "remove"
        preposition = "on" if move_existing_piece else "from"

        def prompt(position: str) -> str:
            return int(
                input(
                    f"What {position} would you like to {action} the piece {preposition}? "
                )
            )

        row = prompt("row")
        assert row in [0, 1, 2], f"row value {row} not valid"
        col = prompt("col")
        assert col in [0, 1, 2], f"col value {col} not valid"

        return row, col

class MockPlayer(Player):
    moves: T.List[T.Tuple[int,int]]
    turn_idx: int = 0
    def get_player_move(self, move_existing_piece=True) -> T.Tuple[int,int]:
        next_move = self.moves[self.turn_idx]
        self.turn_idx += 1
        return next_move

