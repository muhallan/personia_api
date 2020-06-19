import os


class Config:
    """
    The base class configuration
    """
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'SQLALCHEMY_DATABASE_URI', 'sqlite:///personio.db')
    DEBUG = True
    SQLALCHEMY_ECHO = False
    SECRET_KEY = os.getenv('SECRET', 'randomnessshouldbereplaced')


class Production(Config):
    """
    Production configuration
    """
    DEBUG = False


class Testing(Config):
    """
    Testing configuration
    """
    SQLALCHEMY_DATABASE_URI = 'sqlite:///personio_testing_db'
    TESTING = True
    SECRET_KEY = 'anotherrandomstringfortesting'


class StagingConfig(Config):
    """Configurations for Staging."""
    DEBUG = True


class Development(Config):
    """
    Development configuration
    """
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ECHO = True


config_dict = {
    'production': Production,
    'development': Development,
    'staging': StagingConfig,
    'testing': Testing
}
