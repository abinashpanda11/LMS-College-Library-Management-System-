from app import app, User
from werkzeug.security import check_password_hash

with app.app_context():
    user = User.query.filter_by(username='section_user').first()
    if not user:
        print("User NOT FOUND")
    else:
        print(f"User Found: {user.username}")
        print(f"Hash: {user.password_hash}")
        is_valid = user.check_password('password123')
        print(f"Password 'password123' Valid? {is_valid}")
