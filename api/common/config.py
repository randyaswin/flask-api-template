import os
import logging

basedir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig:
    """
    Base Configuration
    """
    # Base
    APP_NAME = os.environ.get('APP_NAME')
    DEBUG = False
    TESTING = False
    LOGGING_FORMAT = '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    LOGGING_LOCATION = 'logs/flask.log'
    LOGGING_LEVEL = logging.DEBUG
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Security
    BCRYPT_LOG_ROUNDS = 13
    TOKEN_EXPIRATION_DAYS = 30
    TOKEN_EXPIRATION_SECONDS = 0
    TOKEN_PASSWORD_EXPIRATION_DAYS = 1
    TOKEN_PASSWORD_EXPIRATION_SECONDS = 0
    TOKEN_EMAIL_EXPIRATION_DAYS = 1
    TOKEN_EMAIL_EXPIRATION_SECONDS = 0

    # Pagination
    POSTS_PER_PAGE = 10
    MAX_PER_PAGE = 100
    DATE_FORMAT = '%m-%d-%Y, %H:%M:%S'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f"postgresql://{os.environ.get('DB_USERNAME')}:{os.environ.get('DB_PASSWORD')}@{os.environ.get('DB_HOST')}/{os.environ.get('DB_NAME')}"
    CELERY_BROKER_URL = os.environ.get('BROKER_URL')
