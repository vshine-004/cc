from app import app, db
from flask_migrate import Migrate, init, migrate, upgrade

def setup_database():
    with app.app_context():
        # Initialize migrations
        init()
        
        # Create initial migration
        migrate()
        
        # Apply migrations
        upgrade()
        
        # Create all tables
        db.create_all()
        
        print("Database setup completed successfully!")

if __name__ == '__main__':
    setup_database() 