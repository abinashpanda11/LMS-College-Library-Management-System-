from app import app, db, User
import traceback

print("--- DIAGNOSING QUERY ---")
with app.app_context():
    try:
        print(f"URI from App Config: {app.config['SQLALCHEMY_DATABASE_URI']}")
        print("Attempting to query User table...")
        user = User.query.first()
        print(f"User found: {user}")
    except Exception as e:
        print("EXCEPTION CAUGHT:")
        traceback.print_exc()
print("--- END ---")
