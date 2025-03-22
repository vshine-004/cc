from app import app, db
from flask_migrate import Migrate, upgrade

def init_db():
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Run any pending migrations
        upgrade()
        
        print("Database initialized successfully!")

if __name__ == '__main__':
    init_db() 