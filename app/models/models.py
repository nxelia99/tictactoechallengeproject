from datetime import datetime
from app.database.db import db
import pytz

# Match model creation to commit to the db
class Match(db.Model):
    __tablename__ = 'matches'
    id = db.Column(db.String(36), primary_key=True)
    board = db.Column(db.String(9), nullable=False)
    current_turn = db.Column(db.String(1), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='In progress')
    # Obtain Spain's timezone and save it to the db
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(pytz.timezone('Europe/Madrid')))

    def __init__(self, id, board, current_turn, status='In progress'):
        self.id = id
        self.board = board
        self.current_turn = current_turn
        self.status = status

    # Display the assignated match id.
    def __repr__(self):
        return f'<Match {self.id}>'
