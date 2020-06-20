import unittest
import uuid
from helpers.validate import validate_uuid


class TestValidateUUID(unittest.TestCase):

    def test_validate_uuid_with_none_id(self):
        self.assertTrue(validate_uuid(None))

    def test_validate_uuid_with_non_string_id(self):
        with self.assertRaisesRegex(TypeError, 'Id should be of type string'):
            validate_uuid(768902)

    def test_validate_uuid_with_empty_string_id(self):
        with self.assertRaisesRegex(ValueError, 'Id should not be empty'):
            validate_uuid("")

    def test_validate_uuid_with_invalid_uuid_string_id(self):
        with self.assertRaisesRegex(ValueError, 'Id is not a valid UUID'):
            validate_uuid("dfwsdfh27482")

    def test_validate_uuid_with_valid_uuid_string_id(self):
        valid_uuid = uuid.uuid4().hex
        self.assertTrue(valid_uuid)
        uuid_with_dashes = "49f5a90b-0d67-49a1-ac55-7cdf3a0a4d7c"
        self.assertTrue(uuid_with_dashes)
        uuid_without_dashes = "3a08649d324845e299f4c227eb01428e"
        self.assertTrue(uuid_without_dashes)
        uppercase_uuid = "3DC908713E2F4FA2B1B2132E8717B394"
        self.assertTrue(uppercase_uuid)
