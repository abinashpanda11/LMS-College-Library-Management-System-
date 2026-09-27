import os
from app import app
from io import BytesIO

# Configuration for the test user
TEST_USER = {
    'full_name': 'Test User 2J3',
    'email': 'test2j3@library.com',
    'mobile': '9876543210',
    'registration_number': 'REG2J3',
    'dob': '2005-05-20',
    'section': '2J3',
    'semester': '4',
    'username': 'section_user',
    'password': 'password123'
}

IMAGE_PATH = r'C:/Users/ASUS/.gemini/antigravity/brain/62044283-933a-41c2-ae77-375f4daf2715/test_profile_pic_1765571590403.png'

print("--- STARTING REGISTRATION TEST ---")
print(f"Target: {app.config['SQLALCHEMY_DATABASE_URI'].split('@')[-1]}")

try:
    with app.test_client() as client:
        # Load image
        with open(IMAGE_PATH, 'rb') as f:
            img_data = f.read()
        
        # Prepare data with file
        data = TEST_USER.copy()
        data['photo'] = (BytesIO(img_data), 'profile.png', 'image/png')
        
        print("Sending POST request to /register...")
        response = client.post('/register', data=data, content_type='multipart/form-data', follow_redirects=True)
        
        print(f"Response Status: {response.status_code}")
        
        # Check if we landed on login page (Success) or are still on register (Error)
        # We can check prompt text
        if "Login" in response.text and "Sign In" in response.text:
             print("SUCCESS: Redirected to Login page.")
        elif "Registration Successful" in response.text:
             # Some implementations flash the message and redirect
             print("SUCCESS: Registration success message found.")
        else:
             print("POTENTIAL FAILURE. Checking page content snippets:")
             print(response.text[:500])
             
except Exception as e:
    print(f"EXCEPTION: {e}")

print("--- END ---")
