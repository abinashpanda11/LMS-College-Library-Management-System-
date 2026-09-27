import os
import time
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

print("--- STARTING MANUAL DB INIT ---")

app = Flask(__name__)
# Load config
app.config.from_object(Config)

# Force print URI (mask password)
uri = app.config['SQLALCHEMY_DATABASE_URI']
masked_uri = uri.split('@')[-1] if '@' in uri else 'LOCAL'
print(f"Target DB Host: {masked_uri}")

db = SQLAlchemy(app)

# Define User model just to ensure SQLAlchemy knows what to create
# (Copying minimal definition or importing from app if possible, but importing app might trigger other side effects)
# Better to import from app to get all models
try:
    from app import db, User, Book, Transaction
    print("Models imported successfully.")
except Exception as e:
    print(f"CRITICAL ERROR importing models: {e}")
    exit(1)

def manual_init():
    with app.app_context():
        print("1. Testing connection...")
        try:
            # Try a simple select
            db.session.execute(text('SELECT 1'))
            print("   Connection Successful!")
        except Exception as e:
            print(f"   CONNECTION FAILED: {e}")
            return

        print("2. Reseting tables...")
        try:
            db.drop_all()
            print("   db.drop_all() executed.")
            db.create_all()
            print("   db.create_all() executed.")
        except Exception as e:
            print(f"   TABLE CREATION FAILED: {e}")
            return

        print("3. Checking if tables exist...")
        try:
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"   Tables found: {tables}")
            
            if 'user' in tables:
                print("   'user' table exists.")
                # user_count = User.query.count()
                # print(f"   User count: {user_count}")
            else:
                print("   WARNING: 'user' table NOT found after creation attempt.")
                
        except Exception as e:
            print(f"   INSPECTION FAILED: {e}")

        print("--- FINISHED ---")

if __name__ == '__main__':
    manual_init()
