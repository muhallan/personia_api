import os
import coverage
import unittest
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import app, db

migrate = Migrate(app, db)
manager = Manager(app)

# create a migration utility command
manager.add_command('db', MigrateCommand)

COV = coverage.coverage(config_file=True)
COV.start()


@manager.command
def create_db():
    """
    Creates the database tables
    """
    db.create_all()


@manager.command
def drop_db():
    """
    Drops the database tables
    """
    db.drop_all()


@manager.command
def test():
    """Runs the unit tests without test coverage."""
    tests = unittest.TestLoader().discover('./tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@manager.command
def cov():
    """Runs the unit tests with coverage."""
    cov = coverage.coverage(branch=True, source=['auth/', 'helpers/', 'hierarchy/', 'models/'])
    cov.start()
    tests = unittest.TestLoader().discover('./tests', pattern='test*.py')
    unittest.TextTestRunner(verbosity=2).run(tests)
    cov.stop()
    cov.save()
    print('Coverage Summary:')
    cov.report()
    basedir = os.path.abspath(os.path.dirname(__file__))
    covdir = os.path.join(basedir, 'tmp/coverage')
    cov.html_report(directory=covdir)
    print('HTML version: file://%s/index.html' % covdir)
    cov.erase()


if __name__ == '__main__':
    manager.run()
