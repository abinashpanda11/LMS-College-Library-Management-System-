from app import app, mail
from flask_mail import Message
from dotenv import load_dotenv
import os

load_dotenv()

print("--- TESTING EMAIL ---")
sender = os.getenv('MAIL_USERNAME')
print(f"Sender: {sender}")

with app.app_context():
    try:
        msg = Message("Test Email from Library System", recipients=[sender])
        msg.body = "This is a test email to verify the SMTP configuration."
        mail.send(msg)
        print("SUCCESS: Email sent!")
    except Exception as e:
        print(f"FAILURE: {e}")

print("--- END ---")
