from app.models.models import Match
from app.database.db import db

class MatchService:
    @staticmethod
    def make_move(match_id, player, x, y, session=None):
        """Make a move if it's valid"""
        if session is None:
            session = db.session # Start a session if there's none
        
        match = session.get(Match, match_id)

        # Handle exception if the match isn't found
        if not match:
            raise ValueError("Match not found.")

        square = int(x) * 3 + int(y)  # Convert x, y coordinates to square index

        # Check game status first
        if match.status != 'In progress':
            raise ValueError("The game is over.")

        # Check if the cell is empty
        if match.board[square] != ' ':
            raise ValueError("This cell is already taken.")

        # Then check if it's the player's turn
        if match.current_turn != player:
            raise ValueError("It's not the player's turn.")

        # Update the board
        board_list = list(match.board)
        board_list[square] = player
        match.board = ''.join(board_list)

        # Change turn
        match.current_turn = 'O' if player == 'X' else 'X'

        # Check if there's a winner
        MatchService.check_game_status(match)

        # Commit to db
        session.commit()
        return match

    @staticmethod
    def check_game_status(match):
        """Check the game status to see if there's a winner or a draw."""
        winning_combinations = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
        (0, 4, 8), (2, 4, 6)              # Diagonals
    ]

    # Iteration through each possible winning combo 
        for combo in winning_combinations:
            # Check if the symbols at the three positions of the current combination are the same
            # and not empty
            if match.board[combo[0]] == match.board[combo[1]] == match.board[combo[2]] != ' ':
                # If we find a winning combination, update the match status to indicate the winner
                match.status = f'Finished, {match.board[combo[0]]} wins'
                return

    # If we've checked all combinations and found no winner, check for a draw
        if ' ' not in match.board:
        # If the board is full, set the match status to 'Draw'
            match.status = 'Draw'