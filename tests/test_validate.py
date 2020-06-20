import unittest
import uuid
from helpers.validate import validate_json, validate_uuid, check_json_contains_loop


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


class TestValidateJSON(unittest.TestCase):

    def test_validate_correct_json(self):
        data = """
        {
            "user": "joker",
            "password": "batman",
            "user": "man"
        }
        """
        self.assertTrue(validate_json(data))

    def test_validate_incorrect_json(self):
        data = "just a string"
        self.assertFalse(validate_json(data))
        data2 = 6789
        self.assertFalse(validate_json(data2))
        data3 = {'one': 1, "two": 2}
        self.assertFalse(validate_json(data3))
        data4 = [5, 2, 2, 4, 6]
        self.assertFalse(validate_json(data4))
        data5 = "{'color': 'white', 'size': '46'}"
        self.assertFalse(validate_json(data5))


class TestCheckJsonContainsLoop(unittest.TestCase):

    def test_check_json_contains_loop_gets_duplicates(self):
        with_loop = """
            {
                "Pete": "Nick",
                "Barbara": "Nick",
                "Nick": "Sophie",
                "Sophie": "Jonas",
                "Jane": "Reenah",
                "Barbara": "Sophie",
                "Nick": "Dre"
            }
        """
        duplicates = check_json_contains_loop(with_loop)
        self.assertListEqual(duplicates, ['Barbara', 'Nick'])

    def test_check_json_contains_loop_no_duplicates(self):
        with_loop = """
            {
                "Pete": "Nick",
                "Barbara": "Nick",
                "Nick": "Sophie",
                "Sophie": "Jonas",
                "Jane": "Reenah"
            }
        """
        duplicates = check_json_contains_loop(with_loop)
        self.assertListEqual(duplicates, [])


if __name__ == '__main__':
    unittest.main()
