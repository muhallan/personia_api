import uuid


def validate_uuid(id_string):
    """
    Validate the given string whether it is a valid UUID if it's not None
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
