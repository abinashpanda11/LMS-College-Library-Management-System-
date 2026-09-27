from app import app, db, User
from werkzeug.security import generate_password_hash
from datetime import datetime

def seed():
    with app.app_context():
        # Check if user exists
        user = User.query.filter_by(email='librarysystem55@gmail.com').first()
        if user:
            print("User already exists.")
            # Ensure password is known
            user.set_password('test1234')
            db.session.commit()
            print("Password reset to 'test1234'.")
            return

        print("Creating user...")
        new_user = User(
            username='emailtest',
            email='librarysystem55@gmail.com',
            full_name='Email Test User',
            role='student',
            registration_number='ET001',
            dob=datetime(1990, 1, 1).date(),
            section='1A1',
            semester=1,
            mobile_number='1234567890',
            photo_filename='default.png' # Dummy
        )
        new_user.set_password('test1234')
        db.session.add(new_user)
        db.session.commit()
        print("User 'emailtest' created successfully.")

if __name__ == '__main__':
    seed()
