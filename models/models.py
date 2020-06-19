import jwt
from datetime import datetime, timedelta
from flask_bcrypt import Bcrypt
import logging
from .model_mixin import app, db, ModelMixin


class User(ModelMixin):
    """
    The user model. This represents the holder of the bank account
    """
    __tablename__ = 'user'

    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    name = db.Column(db.String(120), nullable=False)

    def __init__(self, username, password, name):
        """
        Initialize the user instance
        """
        self.username = username
        self.password = Bcrypt().generate_password_hash(password).decode()
        self.name = name

    def is_password_valid(self, password):
        """
        Check the password provided against the hash we have stored to validate it
        """
        return Bcrypt().check_password_hash(self.password, password)

    @staticmethod
    def generate_token(user_id):
        """
        Generates the access token
        """
        try:
            # set up a payload with an expiration time to 4 hours
            payload = {
                'exp': datetime.utcnow() + timedelta(hours=4),
                'iat': datetime.utcnow(),
                'sub': user_id
            }
            # create the byte string token using the payload and the SECRET key
            jwt_string = jwt.encode(
                payload,
                app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
            return jwt_string

        except Exception as e:
            logging.error(f"An error while generating a token - {e}")
            # return an error in string format if an exception occurs
            return str(e)

    @staticmethod
    def decode_token(token):
        """
        Decodes the access token from the Authorization header.
        """
        try:
            # decode the token using the SECRET environment variable
            payload = jwt.decode(token, app.config.get('SECRET_KEY'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            # the token is expired, return an error string
            return "Expired token. Please login to get a new token"
        except jwt.InvalidTokenError:
            # the token is invalid, return an error string
            return "Invalid token. Please register or login"

