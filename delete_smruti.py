from app import app, db, User

print("--- DELETING USER 'smruti' ---")
with app.app_context():
    user = User.query.filter_by(username='smruti').first()
    if user:
        print(f"Found User ID: {user.id}, Email: {user.email}")
        db.session.delete(user)
        db.session.commit()
        print("SUCCESS: User deleted.")
    else:
        print("User 'smruti' not found.")

print("--- END ---")
