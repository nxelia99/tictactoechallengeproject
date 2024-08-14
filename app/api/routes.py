from flask import Blueprint, jsonify, render_template, request
import logging
import uuid

from app.models.models import Match 
from app.database.db import db 
from app.static.services.game_services import MatchService


api = Blueprint('/', __name__)
logger = logging.getLogger(__name__)


# Endpoint for the move function
@api.route("/move", methods=['POST'])
def move():
    # Extract data from the JSON payload
    data = request.json
    match_id = data['matchId']
    player_id = data['playerId']
    x = data['x']
    y = data['y']

    try:
        # Try to make a move using the make_move function
        match = MatchService.make_move(match_id, player_id, x, y)
        logger.info(f"Move successful for match {match_id}")
        # Return a response with updated game state
        return jsonify({
            "message": "Move successful",
             # Convert the board to a 2D list
            "board": [list(match.board[i:i+3]) for i in range(0, 9, 3)],
            "currentTurn": match.current_turn,
            "status": match.status
        }), 200
    except ValueError as e:
        # Log and return an error if the move is invalid
        logger.warning(f"Invalid move for match {match_id}: {str(e)}")
        return jsonify({"error": str(e)}), 400
    
# Retrieves the current state of a game    
@api.route("/status", methods=['GET'])
def status():
    match_id = request.args.get('matchId')
    match = Match.query.get(match_id)

    # If no match is found with the given id
    if not match:
        logger.error(f"Match with id {match_id} not found")
        return jsonify({"error": "Match not found"}), 404

    logger.info(f"Status retrieved for match {match_id}")
     # Return a response with updated game details
    return jsonify({
        "board": [list(match.board[i:i+3]) for i in range(0, 9, 3)],
        "currentPlayer": match.current_turn,
        "status": match.status
    }), 200

# Saves the game state in case we refresh the page
@api.route("/game/<match_id>/state", methods=['GET'])
def game_state(match_id):
    match = Match.query.get(match_id)
    if not match:
        return jsonify({"error": "Match not found"}), 404

    return jsonify({
        "board": [list(match.board[i:i+3]) for i in range(0, 9, 3)],
        "currentTurn": match.current_turn,
        "status": match.status
    }), 200


# "Home" page for creating the first game
@api.route("/", methods=['GET'])
def index():
    return render_template('index.html')


# Endpoint for creating a new match
@api.route("/create", methods=['POST'])
def create_game():

    # MatchID generation
    short_uuid = lambda: str(uuid.uuid4())[:5] # MatchID is set to have 5 characters
    match_id = str(short_uuid())

    # Create a new match
    new_match = Match(
        id=match_id,
        board=" " * 9,  # Empty 3x3 board
        current_turn="X"  # X always starts
    )

    # Save the new match in the db
    db.session.add(new_match)
    db.session.commit()
    logger.debug(f'Created new match with ID: {match_id}')
    # Responder con el ID del nuevo partido
    return jsonify({"matchId": match_id}), 200

# Endpoint to display the game corresponding to its id
@api.route("/game/<match_id>", methods=['GET'])
def game_page(match_id):
    match = Match.query.get(match_id)
    if not match:
        return "Match not found", 404
    return render_template('game.html', match_id=match_id)
