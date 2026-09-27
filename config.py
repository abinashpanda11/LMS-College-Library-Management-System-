import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Security
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-fallback')
    
    # Database
    # This prioritizes the environment variable (External DB) over the local file
    _db_uri = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///library.db')
    # Auto-fix: ensure SQLAlchemy uses psycopg2 driver (not psycopg v3) for PostgreSQL
    if _db_uri.startswith('postgresql://'):
        _db_uri = _db_uri.replace('postgresql://', 'postgresql+psycopg2://', 1)
    SQLALCHEMY_DATABASE_URI = _db_uri
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Uploads
    UPLOAD_FOLDER = 'static/uploads'
    
    # Email Configuration
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_USERNAME')
