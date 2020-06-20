from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from app import app

db = SQLAlchemy(app)


class ModelMixin(db.Model):
    """
    Base model that contains save and delete methods, and common field
    attributes in the models
    """

    __abstract__ = True

    def save(self):
        """
        Save an instance of the model to the database.
        """
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except SQLAlchemyError:
            db.session.rollback()
            return False

    def delete(self):
        """
        Delete an instance of the model from the database.
        """
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except SQLAlchemyError:
            db.session.rollback()
            return False

    @classmethod
    def get(cls, *args):
        """
        Return data filtered by the id.
        """
        return cls.query.get(*args)

    @classmethod
    def order_by(cls, *args):
        """
        Query and order the data of the model by the given args.
        """
        return cls.query.order_by(*args)

    @classmethod
    def find_first(cls, **kwargs):
        """
        Query and filter the data of a model, returning the first result.
        """
        return cls.query.filter_by(**kwargs).first()

