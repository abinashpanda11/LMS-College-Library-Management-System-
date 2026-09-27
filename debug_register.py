from app import app
from io import BytesIO
import traceback

# FORCE DEBUG MODE to propagate exceptions
app.config['DEBUG'] = True
app.config['TESTING'] = True

TEST_USER = {
    'full_name': 'Test User 2J3',
    'email': 'test2j3@library.com',
    'mobile': '9876543210',
    'reg_no': 'REG2J3',  # Ensure key matches form name in app.py
    'dob': '2005-05-20',
    'section': '2J3',
    'semester': '4',
    'username': 'section_user',
    'password': 'password123'
}

IMAGE_PATH = r'C:/Users/ASUS/.gemini/antigravity/brain/62044283-933a-41c2-ae77-375f4daf2715/test_profile_pic_1765571590403.png'

print("--- DEBUG REGISTRATION ---")
try:
    with app.test_client() as client:
        with open(IMAGE_PATH, 'rb') as f:
            img_data = f.read()
        
        data = TEST_USER.copy()
        data['photo'] = (BytesIO(img_data), 'profile.png', 'image/png')
        
        print("Posting...")
        # Note: keys in TEST_USER must match request.form.get keys
        # In app.py: reg_no = request.form.get('reg_no') -> Correct
        response = client.post('/register', data=data, content_type='multipart/form-data')
        
        if response.status_code == 200 or response.status_code == 302:
            print("Success!")
        else:
            print(f"Failed with status: {response.status_code}")
            # If exception happened, it might be printed by app due to DEBUG=True or accessible here?
            # Actually, with TESTING=True, the client might raise the exception directly.
            
except Exception:
    traceback.print_exc()

print("--- END ---")
