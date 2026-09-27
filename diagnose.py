from app import app, db
from sqlalchemy import text
import traceback

print("--- DIAGNOSING ---")
with app.app_context():
    try:
        # Check connection details
        result = db.session.execute(text("SELECT current_database(), current_user"))
        row = result.fetchone()
        print(f"CONNECTED TO: Database='{row[0]}', User='{row[1]}'")
        
        db.session.execute(text('SELECT 1'))
        print("Connection Success!")
        
        # Check user table
        from app import User
        count = User.query.count()
        print(f"User count: {count}")
        
    except Exception as e:
        print(f"ERROR: {e}")
print("--- END ---")
