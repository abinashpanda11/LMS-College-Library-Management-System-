from app import app, User

with app.app_context():
    students = User.query.filter_by(role='student').all()
    print(f"Found {len(students)} students.")
    for s in students:
        print(f"- {s.username} ({s.email})")
