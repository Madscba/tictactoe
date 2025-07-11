from distutils.command.install import value

from src.classes.board import Board
from src.classes.player import Player, HumanPlayer, MockPlayer
from src.classes.game_status import GameStatus
from src.classes.player_move import Move
from src.visualization.visualize_board import VisualizeBoardInTerminal
import typing as T



class GameEngine:
    def __init__(self, mock_players:bool=False, mock_moves:T.List[T.List[T.Tuple[int,int]]]=[[(0,0)],[(1,0)]]):
        self.board = Board()
        self.board_visualizer = VisualizeBoardInTerminal()
        self.players = [HumanPlayer(symbol="nought"), HumanPlayer(symbol="cross")] if not mock_players else [MockPlayer(symbol="nought",moves=mock_moves[0]), MockPlayer(symbol="cross", moves=mock_moves[1])]
        self.game_status = GameStatus.ACTIVE
        self.active_player_idx = 0

    def main(self):
        while self.game_status == GameStatus.ACTIVE:
            self.board_visualizer.visualize(self.board)
            cur_player = self.players[self.active_player_idx]
            move = self.get_valid_move(cur_player)
            cur_player.increment_active_pieces()
            self.board.update_board(move, cur_player)
            self.game_status = self.board.check_for_winning_pos()
            if self.game_status == GameStatus.FINISHED:
                self.board_visualizer.visualize(self.board)
                print(f"A winner has been found! Congratulations player {self.active_player_idx}")
            else:
                self.active_player_idx = (self.active_player_idx + 1) % 2

    def get_valid_move(self, player:Player)->Move:
        attempts = 0
        valid_move = False
        print("symbol to be placed:", player.symbol)
        while not valid_move:
            try:
                move = player.play_turn()
                valid_move = self.board.is_valid_move(move, player)
                if valid_move:
                    return move
                else:
                    print("Invalid move")
            except ValueError as ve:
                print(f"Input error: {ve}")
            except EOFError:
                print("\nKeyboard interrupt (EOF) received, exiting program.")
                exit()
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
            attempts += 1
            if attempts > 3:
                raise RuntimeError("Too many invalid attempts from player.")
        return None




