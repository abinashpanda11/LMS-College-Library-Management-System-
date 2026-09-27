import os
from dotenv import load_dotenv
from flask import Flask
from config import Config

# Manually load to mimic app behavior
load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)

print(f"DEBUG_DB_URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
print(f"DEBUG_ENV_VAR: {os.getenv('SQLALCHEMY_DATABASE_URI')}")
