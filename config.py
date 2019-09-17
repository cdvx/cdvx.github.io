import os


class Config:
    # DEBUG = os.getenv("DEBUG")
    SECRET_KEY = os.urandom(24)
    TESTING = False
    # DATABASE_URL=postgresql://postgres@localhost:{port}/{dbname}
    # DB_USER = os.getenv("DB_USER")
    # DB_HOST = os.getenv("DB_HOST")
    # DB_PORT = os.getenv("DB_PORT")
    # DB_NAME = os.getenv("DB_NAME")
    # DB_PASS = os.getenv("DB_PASS")
    SQLALCHEMY_DATABASE_URI = 'postgresql://cdvx:@localhost/profile'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    pass


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'prof_test'


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://cdvx:@localhost/profile'


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
