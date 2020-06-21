from flask import request, jsonify, make_response
from functools import wraps
import logging
from helpers.validate import validate_uuid
from models.user import User


def authorization(func):
    @wraps(func)
    def check_authorization(*args, **kwargs):
        # check if the header with key is present
        if 'Authorization' not in request.headers:
            response = {
                'status': 'fail',
                'message': 'Header with key Authorization missing.'
            }
            return make_response(jsonify(response)), 401

        # Get the access token from the header
        auth_header = request.headers.get('Authorization').strip()

        # check for when authorization was not provided in header
        if not auth_header:
            response = {
                'status': 'fail',
                'message': ('Token not provided in the header with key '
                            'Authorization.')
            }
            return make_response(jsonify(response)), 401

        # validate that the word bearer is in the token
        if 'bearer ' not in auth_header.lower():
            response = {
                "status": "fail",
                "message": "Invalid Token. The token should begin with the word 'Bearer '."
            }
            return make_response(jsonify(response)), 401

        auth_strings = auth_header.split(" ")
        if len(auth_strings) != 2:
            response = {
                'status': 'fail',
                'message': 'Invalid token format.'
            }
            return make_response(jsonify(response)), 401

        access_token = auth_header.split(" ")[1]

        if access_token:
            # Attempt to decode the token and get the user ID
            user_id = User.decode_token(access_token)
            # check whether the user_id is a valid UUID
            try:
                is_valid = validate_uuid(user_id)
                if is_valid:
                    # user_id is valid. Allow the function to continue
                    kwargs['user_id'] = user_id

                    return func(*args, **kwargs)
                else:
                    # something is wrong
                    logging.error(f"Invalid user_id: {user_id}")
                    response = {
                        'status': 'fail',
                        'message': "Failed to authenticate. Please try again."
                    }
                    return make_response(jsonify(response)), 401

            except (ValueError, TypeError):
                # we have an error message. Display it to the caller
                message = user_id
                response = {
                    'status': 'fail',
                    'message': message
                }
                return make_response(jsonify(response)), 401
        else:
            response = {
                'message': 'Empty token string'
            }
            return make_response(jsonify(response)), 401

    check_authorization.__doc__ = func.__doc__
    return check_authorization
