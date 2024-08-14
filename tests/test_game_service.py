import unittest
from unittest.mock import patch, MagicMock
from app import create_app
from app.models.models import Match
from app.database.db import db
from app.static.services.game_services import MatchService

class TestGameService(unittest.TestCase):
    def setUp(self):
        # Create the Flask app and push the application context
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()

        # Create a mock match
        self.match = Match(id='test_match', board=' ' * 9, current_turn='X', status='In progress')
        
        # Create a mock session
        self.mock_session = MagicMock()
        self.mock_session.get.return_value = self.match

    def tearDown(self):
        # Pop the application context
        self.app_context.pop()

    def test_make_move_valid(self):
        MatchService.make_move(self.match.id, 'X', 0, 0, session=self.mock_session)
        self.assertEqual(self.match.board, 'X' + ' ' * 8)
        self.assertEqual(self.match.current_turn, 'O')

    def test_make_move_invalid_turn(self):
        self.match.current_turn = 'X'
        with self.assertRaises(ValueError) as context:
            MatchService.make_move(self.match.id, 'O', 0, 0, session=self.mock_session)
        self.assertEqual(str(context.exception), "It's not the player's turn.")

    def test_make_move_occupied_cell(self):
        self.match.board = 'X' + ' ' * 8
        with self.assertRaises(ValueError) as context:
            MatchService.make_move(self.match.id, 'O', 0, 0, session=self.mock_session)
        self.assertEqual(str(context.exception), "This cell is already taken.")

    def test_make_move_game_over(self):
        self.match.status = 'Finished, X wins'
        with self.assertRaises(ValueError) as context:
            MatchService.make_move(self.match.id, 'X', 0, 0, session=self.mock_session)
        self.assertEqual(str(context.exception), "The game is over.")

    def test_check_game_status_row_win(self):
        self.match.board = 'XXX' + ' ' * 6
        MatchService.check_game_status(self.match)
        self.assertEqual(self.match.status, 'Finished, X wins')

    def test_check_game_status_column_win(self):
        self.match.board = 'X  X  X  '
        MatchService.check_game_status(self.match)
        self.assertEqual(self.match.status, 'Finished, X wins')

    def test_check_game_status_diagonal_win(self):
        self.match.board = 'X   X   X'
        MatchService.check_game_status(self.match)
        self.assertEqual(self.match.status, 'Finished, X wins')

    def test_check_game_status_draw(self):
        self.match.board = 'XOXOXOOXO'
        MatchService.check_game_status(self.match)
        self.assertEqual(self.match.status, 'Draw')

    def test_check_game_status_in_progress(self):
        self.match.board = 'XOX   OXO'
        MatchService.check_game_status(self.match)
        self.assertEqual(self.match.status, 'In progress')

if __name__ == '__main__':
    unittest.main()