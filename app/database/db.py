from app import db

# DB shcema initialization
def init_db(app):
    with app.app_context():
        db.create_all()

