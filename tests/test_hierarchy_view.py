import json
import unittest
from tests.base_test import BaseTestCase


def register_user(self, username="user@test", password="test1234", name="tester"):
    """
    Helper method to help register a test user
    """
    user_data = json.dumps({
        'username': username,
        'password': password,
        'name': name
    })
    return self.client.post(
        '/api/v1/auth/register', data=user_data,
        content_type='application/json')


def login_user(self, username="user@test", password="test1234"):
    """
    Helper method to help login a test user
    """
    user_data = json.dumps({
        'username': username,
        'password': password
    })
    return self.client.post(
        'api/v1/auth/login', data=user_data, content_type='application/json')


single_root_json = {
    "Pete": "Nick",
    "Barbara": "Nick",
    "Nick": "Sophie",
    "Sophie": "Jonas"
}

formatted_structure = {
    'Jonas': {
        'Sophie': {
            'Nick': {
                'Barbara': {},
                'Pete': {}
            }
        }
    }
}

with_loop_json = """
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

multiple_roots_json = """
            {
                "Pete": "Nick",
                "Barbara": "Nick",
                "Nick": "Sophie",
                "Sophie": "Jonas",
                "Jane": "Reenah"
            }
        """


class TestStructureHierarchy(BaseTestCase):

    def test_unauthenticated_user_fails_to_post_hierarchy(self):
        """
        Test that a user who tries to post a hierarchy without an authentication fails
        """
        with self.client:
            data = json.dumps(single_root_json)
            # make a POST request to structure JSON
            response = self.client.post(
                '/api/v1/hierarchy/structure',
                data=data,
                content_type='application/json'
            )
            res = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 401)
            self.assertTrue(res['status'] == 'fail')
            self.assertTrue(res['message'] == 'Header with key Authorization missing.')

    def test_unauthenticated_user_with_bad_token_fails_to_post_hierarchy(self):
        """
        Test that a user with an invalid token fails to post the hierarchy
        """
        with self.client:
            data = json.dumps(single_root_json)
            # make a POST request to structure JSON
            response = self.client.post(
                '/api/v1/hierarchy/structure',
                headers=dict(Authorization="Bearer rubbishtoken"),
                data=data,
                content_type='application/json'
            )
            res = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 401)
            self.assertTrue(res['status'] == 'fail')
            self.assertTrue(res['message'] == 'Invalid token. Please register or login')

    def test_authenticated_user_successfully_posts_hierarchy_json(self):
        """
        Test that a user with a valid token posts a hierarchy successfully and gets a response
        """
        register_user(self)
        result = login_user(self)
        access_token = json.loads(result.data.decode())['auth_token']
        data = json.dumps(single_root_json)
        # make a POST request to structure JSON
        response = self.client.post(
            '/api/v1/hierarchy/structure',
            headers=dict(Authorization="Bearer " + access_token),
            data=data,
            content_type='application/json'
        )
        res = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertTrue(res['status'] == 'success')
        self.assertEqual(res['employee_hierarchy'], formatted_structure)

    def test_authenticated_user_fails_to_post_empty_post_body(self):
        """
        Test that an empty post body fails
        """
        register_user(self)
        result = login_user(self)
        access_token = json.loads(result.data.decode())['auth_token']
        response = self.client.post(
            '/api/v1/hierarchy/structure',
            headers=dict(Authorization="Bearer " + access_token),
            content_type='application/json'
        )
        res = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertTrue(res['status'] == 'fail')
        self.assertTrue(res['message'] == 'No post body provided.')

    def test_that_invalid_post_json_gets_rejected(self):
        """
        Test that poorly formatted JSON fails to be processed
        """
        register_user(self)
        result = login_user(self)
        access_token = json.loads(result.data.decode())['auth_token']
        # make a POST request to structure JSON
        response = self.client.post(
            '/api/v1/hierarchy/structure',
            headers=dict(Authorization="Bearer " + access_token),
            data="just a string",
            content_type='application/json'
        )
        res = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertTrue(res['status'] == 'fail')
        self.assertTrue(res['message'] == 'Invalid JSON posted. Please check the format.')

    def test_that_hierarchy_containing_loops_fails(self):
        """
        Test that employee JSON with loops returns an error message
        """
        register_user(self)
        result = login_user(self)
        access_token = json.loads(result.data.decode())['auth_token']
        # make a POST request to structure JSON
        response = self.client.post(
            '/api/v1/hierarchy/structure',
            headers=dict(Authorization="Bearer " + access_token),
            data=with_loop_json,
            content_type='application/json'
        )
        res = json.loads(response.data.decode())
        print(res)
        self.assertEqual(response.status_code, 400)
        self.assertTrue(res['status'] == 'fail')
        self.assertTrue(res['message'] == "The posted JSON contains loops. These employees have more "
                                          "than one supervisor: ['Barbara', 'Nick']")

    def test_that_hierarchy_with_multiple_roots_fails(self):
        """
        Test that the employee JSON with more than one root fails
        """
        register_user(self)
        result = login_user(self)
        access_token = json.loads(result.data.decode())['auth_token']
        # make a POST request to structure JSON
        response = self.client.post(
            '/api/v1/hierarchy/structure',
            headers=dict(Authorization="Bearer " + access_token),
            data=multiple_roots_json,
            content_type='application/json'
        )
        res = json.loads(response.data.decode())
        print(res)
        self.assertEqual(response.status_code, 400)
        self.assertTrue(res['status'] == 'fail')
        self.assertTrue(res['message'] == "There are multiple roots in the hierarchy: ['Jonas', 'Reenah']")


if __name__ == '__main__':
    unittest.main()
