from app import app, User, mail, Message
import time

print("--- RESENDING WELCOME EMAILS ---")
with app.app_context():
    students = User.query.filter_by(role='student').all()
    count = 0
    for user in students:
        try:
            print(f"Sending to {user.email}...")
            msg = Message('Welcome to Library System', recipients=[user.email])
            msg.body = f"Hi {user.full_name},\n\nYour account has been created successfully.\nUsername: {user.username}\n\nHappy Reading!"
            
            # Using our HTML template manually since we are outside the route
            msg.html = f"""
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #e2e8f0; border-radius: 8px; background-color: #f8fafc;">
                <div style="text-align: center; margin-bottom: 20px;">
                    <h2 style="color: #1e293b; margin: 0;">Welcome to Library System</h2>
                    <p style="color: #64748b; font-size: 14px;">Library Management System</p>
                </div>
                <div style="background-color: #ffffff; padding: 20px; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                    <p style="color: #334155; font-size: 15px; line-height: 1.6; white-space: pre-line;">
                        Hi {user.full_name},

                        Your account has been created successfully.
                        Username: <strong>{user.username}</strong>

                        Happy Reading!
                    </p>
                    <p style="color: #94a3b8; font-size: 12px; margin-top: 20px; text-align: center; border-top: 1px solid #e2e8f0; padding-top: 20px;">
                        Library Management System Automation
                    </p>
                </div>
            </div>
            """
            
            mail.send(msg)
            print("SUCCESS.")
            count += 1
            time.sleep(1) # Polite delay
        except Exception as e:
            print(f"FAILED for {user.email}: {e}")

    print(f"Sent {count} emails.")
print("--- END ---")
