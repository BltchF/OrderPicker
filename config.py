import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL').replace("://", "ql://", 1)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
