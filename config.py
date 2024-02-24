import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    if SQLALCHEMY_DATABASE_URI is None:
        raise Exception('DATABASE_URL environment variable not set')
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("://", "ql://", 1)

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    FLASK_SECRET_KEY = os.getenv('FLASK_SECRET_KEY')
    if FLASK_SECRET_KEY is None:
        raise Exception('FLASK_SECRET_KEY environment variable not set')

class LocalTestConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('LOCAL_TEST_DATABASE_URL')
    if SQLALCHEMY_DATABASE_URI is None:
        raise Exception('LOCAL_TEST_DATABASE_URL environment variable not set')
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("://", "ql://", 1)
