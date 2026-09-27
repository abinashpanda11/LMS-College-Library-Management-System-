from app import app, db, User

print("--- CLEARING STUDENTS ---")
with app.app_context():
    # Count before
    count_before = User.query.count()
    print(f"Total Users Before: {count_before}")
    
    # Delete non-admin
    # Assuming 'admin' is the username of the administrator
    deleted = User.query.filter(User.username != 'admin').delete()
    
    db.session.commit()
    print(f"Deleted {deleted} students.")
    
    # Count after
    remaining = User.query.all()
    print(f"Remaining Users: {[u.username for u in remaining]}")

print("--- END ---")
