import json
import logging
import uuid


def validate_uuid(id_string):
    """
    Validates the given string whether it is a valid UUID if it's not None
    :param id_string: Id string to validate
    :return: Bool
    :raises: TypeError, ValueError
    """
    if id_string is None:
        return True
    if not isinstance(id_string, str):
        raise TypeError('Id should be of type string')
    if len(id_string) == 0:
        raise ValueError('Id should not be empty')
    try:
        id_uuid = uuid.UUID(id_string)
        return id_uuid.hex == id_string
    except ValueError:
        raise ValueError('Id is not a valid UUID')


def validate_json(json_data):
    """
    Checks whether the data provided is valid JSON or not
    :param json_data: data to validate. This is of any data type
    :return: Bool. Whether the data is valid or not
    """
    try:
        json.loads(json_data)
        return True
    except (ValueError, TypeError) as error:
        logging.error(f"Invalid JSON. Reason: {error}")
        return False


def check_json_contains_loop(json_data):
    """
    Checks the JSON data provided whether it contains a loop. This happens when there is a duplicate key in the JSON.
    This would imply that the employee has more than one supervisor.
    :param json_data: str JSON to check
    :return: List of duplicated keys
    """
    def find_duplicated_key(ordered_pairs):
        """
        Hook function used to check if the decoded pairs contain duplicate keys
        :param ordered_pairs: List of tuples which are key-value pairs
        :return: List of duplicated keys
        """
        correct_dict = {}
        duplicates = []
        for key, value in ordered_pairs:
            if key in correct_dict:
                duplicates.append(key)
            else:
                correct_dict[key] = value
        return duplicates
    return json.loads(json_data, object_pairs_hook=find_duplicated_key)
