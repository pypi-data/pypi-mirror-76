import os


class BaseConfig:
    """Base configuration."""
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = \
        f"postgresql://{os.environ.get('PG_USER')}:{os.environ.get('PG_PASSWORD')}" \
        f"@{os.environ.get('PG_HOST')}:{os.environ.get('PG_PORT')}/{os.environ.get('PG_DB')}"


class InMemoryConfig(BaseConfig):
    """Development configuration."""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class TestingConfig(BaseConfig):
    """Testing configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = \
        f"postgresql://{os.environ.get('PG_USER')}:{os.environ.get('PG_PASSWORD')}" \
        f"@{os.environ.get('PG_HOST')}:{os.environ.get('PG_PORT')}/testing"


class ProductionConfig(BaseConfig):
    """Production configuration."""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = \
        f"postgresql://{os.environ.get('PG_USER')}:{os.environ.get('PG_PASSWORD')}" \
        f"@{os.environ.get('PG_HOST')}:{os.environ.get('PG_PORT')}/{os.environ.get('PG_DB')}"


config = {
    'development': DevelopmentConfig,
    'inmemory': InMemoryConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
}
