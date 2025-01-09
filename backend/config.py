import os 
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'secret-key')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI', 'sqlite:///db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key', )
    # expire token in 7 days
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=7)
    