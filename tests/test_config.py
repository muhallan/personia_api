import unittest
from app import app, config_dict
from flask_testing import TestCase


class TestProductionConfig(TestCase):
    """
    Test the production configuration
    """
    def create_app(self):
        app.config.from_object(config_dict['production'])
        return app

    def test_app_is_running_on_production(self):
        self.assertFalse(app.config['DEBUG'])
        self.assertFalse(app.config['SECRET_KEY'] is
                         'randomnessshouldbereplaced')


class TestTestingConfig(TestCase):
    """
    Test the testing configuration
    """
    def create_app(self):
        app.config.from_object(config_dict['testing'])
        return app

    def test_app_is_testing(self):
        self.assertTrue(app.config['SECRET_KEY'] is
                         'anotherrandomstringfortesting')
        self.assertTrue(app.config['DEBUG'])
        self.assertTrue(app.config['TESTING'])
        self.assertTrue(
            app.config['SQLALCHEMY_DATABASE_URI'] ==
            'sqlite:///personio_testing.db'
        )


class TestDevelopmentConfig(TestCase):
    """
    Test the development configuration
    """
    def create_app(self):
        app.config.from_object(config_dict['development'])
        return app

    def test_app_is_running_on_development(self):
        self.assertTrue(app.config['DEBUG'])
        self.assertFalse(app.config['SECRET_KEY'] is
                         'randomnessshouldbereplaced')
        self.assertTrue(app.config['SQLALCHEMY_TRACK_MODIFICATIONS'])
        self.assertTrue(app.config['SQLALCHEMY_ECHO'])


class TestStagingConfig(TestCase):
    """
    Test the production configuration
    """
    def create_app(self):
        app.config.from_object(config_dict['staging'])
        return app

    def test_app_is_running_on_production(self):
        self.assertTrue(app.config['DEBUG'])
        self.assertFalse(app.config['SECRET_KEY'] is
                         'randomnessshouldbereplaced')


if __name__ == '__main__':
    unittest.main()
