import unittest
from unittest.mock import patch, MagicMock
from flask import json
from app import create_app, db
from app.models.models import Match

class TestRoutes(unittest.TestCase):

    def setUp(self):

        # Configure the app and the db for the tests
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()
        
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    @patch('app.api.routes.Match.query')
    @patch('app.api.routes.MatchService.make_move')
    def test_move(self, mock_make_move, mock_query):
        mock_match = MagicMock()
        mock_match.board = 'X        '  # Mock the board state after the move
        mock_match.current_turn = 'O'  # Mock the next turn
        mock_match.status = 'In progress'  # Mock the game status
        mock_query.get.return_value = mock_match

        # Mock the make_move method to return the mock_match
        mock_make_move.return_value = mock_match

        data = {
            'matchId': '123',
            'playerId': 'X',
            'x': 0,
            'y': 0
        }

        response = self.client.post('/move', json=data)

        self.assertEqual(response.status_code, 200)
        self.assertIn('Move successful', response.get_json()['message'])
        mock_make_move.assert_called_with('123', 'X', 0, 0)

    @patch('app.api.routes.Match.query')
    def test_status(self, mock_query):
        mock_match = MagicMock()
        mock_match.board = ' ' * 9
        mock_match.current_turn = 'X'
        mock_match.status = 'In progress'
        mock_query.get.return_value = mock_match

        response = self.client.get('/status?matchId=123')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('board', data)
        self.assertIn('currentPlayer', data)
        self.assertIn('status', data)

    @patch('app.api.routes.render_template')
    def test_index(self, mock_render):
        mock_render.return_value = "Mocked template"
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    @patch('app.api.routes.uuid.uuid4')
    @patch('app.api.routes.db.session.add')
    @patch('app.api.routes.db.session.commit')
    def test_create_game(self, mock_commit, mock_add, mock_uuid):
        mock_uuid.return_value = '123'
        response = self.client.post('/create')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['matchId'], '123')

    @patch('app.api.routes.Match.query')
    def test_game_page(self, mock_query):
        mock_match = MagicMock()
        mock_query.get.return_value = mock_match

        response = self.client.get('/game/123')
        self.assertEqual(response.status_code, 200)

        mock_query.get.return_value = None
        response = self.client.get('/game/456')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()