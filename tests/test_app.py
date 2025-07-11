from classes.engine import GameEngine
from classes.game_status import GameStatus


class TestGameEngine():
    def test_three_move_winning_sequence(self):
        game_engine = GameEngine(mock_players=True,mock_moves=[[(0,0),(0,1),(0,2)],[(1,0),(1,1),(1,2)]])
        game_engine.main()
        assert (game_engine.game_status == GameStatus.FINISHED)
