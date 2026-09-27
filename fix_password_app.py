from app import app, db, User

print("--- FIXING PASSWORD (VIA APP) ---")
with app.app_context():
    user = User.query.filter_by(username='section_user').first()
    if user:
        print(f"Old Hash: {user.password_hash}")
        user.set_password('password123')
        db.session.commit()
        print(f"New Hash: {user.password_hash}")
        print("Updated!")
    else:
        print("User not found via App Context")
print("--- END ---")
