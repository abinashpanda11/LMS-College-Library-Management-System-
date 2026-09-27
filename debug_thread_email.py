from app import app, send_email, mail
import time
import os

print("--- TESTING THREADED EMAIL ---")
recipient = os.getenv('MAIL_USERNAME')
print(f"Recipient: {recipient}")

# Mimic the registration call exactly
# send_email(subject, recipient, body) -> internal wrapper
# app context is passed inside send_email -> send_async_email

print("Calling send_email...")
with app.app_context():
    send_email(
        'Debug Registration', 
        recipient, 
        "This is a threaded test.\nIf you see this, the code matches app.py logic."
    )

print("Main thread sleeping for 5 seconds to allow thread to finish...")
time.sleep(5)
print("Main thread exiting.")
print("--- END ---")
