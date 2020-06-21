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


def post_hierarchy(self, data=None, access_token=""):
    """
    Helper method to help post hierarchy data to the endpoint
    """
    return self.client.post(
        '/api/v1/hierarchy/structure',
        headers=dict(Authorization="Bearer " + access_token),
        data=data,
        content_type='application/json'
    )


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
        data = json.dumps(single_root_json)
        # make a POST request to structure JSON
        response = post_hierarchy(self, data, "rubbishtoken")
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
        response = post_hierarchy(self, data, access_token)
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
        response = post_hierarchy(self, access_token=access_token)
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
        response = post_hierarchy(self, data="just a string", access_token=access_token)
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
        response = post_hierarchy(self, with_loop_json, access_token)
        res = json.loads(response.data.decode())
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
        response = post_hierarchy(self, multiple_roots_json, access_token)
        res = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertTrue(res['status'] == 'fail')
        self.assertTrue(res['message'] == "There are multiple roots in the hierarchy: ['Jonas', 'Reenah']")


class TestTwoImmediateSupervisors(BaseTestCase):

    def test_unauthenticated_user_fails(self):
        """
        Test that a user who is not authenticated gets an error message on accessing the endpoint
        """
        with self.client:
            response = self.client.get('/api/v1/hierarchy/two_supervisors/bigman')
            res = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 401)
            self.assertTrue(res['status'] == 'fail')
            self.assertTrue(res['message'] == 'Header with key Authorization missing.')

    def test_unauthorized_user_with_bad_token_is_rejected(self):
        """
        Test that a user who accesses this endpoint with a bad token gets an error message
        """
        response = self.client.get(
            '/api/v1/hierarchy/two_supervisors/bigman',
            headers=dict(Authorization="Bearer badtoken"),
        )
        res = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 401)
        self.assertTrue(res['status'] == 'fail')
        self.assertTrue(res['message'] == 'Invalid token. Please register or login')

    def test_get_supervisors_for_non_existent_employee_fails(self):
        """
        Test that a when a employee who is not in the database is sent, an error message is returned
        """
        register_user(self)
        result = login_user(self)
        access_token = json.loads(result.data.decode())['auth_token']
        response = self.client.get(
            '/api/v1/hierarchy/two_supervisors/pokeman',
            headers=dict(Authorization="Bearer " + access_token),
        )
        res = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 404)
        self.assertTrue(res['status'] == 'fail')
        self.assertTrue(res['message'] == "The requested employee: 'pokeman' doesn't exist")

    def test_get_supervisors_for_existent_employee_is_successful(self):
        """
        Test that when a logged in user sends a request with an existent employee, a successful response
        is given
        """
        register_user(self)
        result = login_user(self)
        access_token = json.loads(result.data.decode())['auth_token']
        data = json.dumps(single_root_json)
        post_hierarchy(self, data, access_token)
        response = self.client.get(
            '/api/v1/hierarchy/two_supervisors/Pete',
            headers=dict(Authorization="Bearer " + access_token),
        )
        res = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertTrue(res['status'] == 'success')
        self.assertTrue(res['message'] == "Both supervisors are available")
        supervisors = {'supervisor': 'Nick', 'supervisor_of_supervisor': 'Sophie'}
        self.assertDictEqual(res['supervisors'], supervisors)

    def test_get_supervisors_for_the_top_most_employee(self):
        """
        Test that no supervisor is returned for an employee who has no supervisor
        """
        register_user(self)
        result = login_user(self)
        access_token = json.loads(result.data.decode())['auth_token']
        data = json.dumps(single_root_json)
        post_hierarchy(self, data, access_token)
        response = self.client.get(
            '/api/v1/hierarchy/two_supervisors/Jonas',
            headers=dict(Authorization="Bearer " + access_token),
        )
        res = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertTrue(res['status'] == 'success')
        self.assertTrue(res['message'] == "This employee has no supervisor")
        supervisors = {'supervisor': None, 'supervisor_of_supervisor': None}
        self.assertDictEqual(res['supervisors'], supervisors)

    def test_get_supervisors_for_an_employee_with_one_supervisor(self):
        """
        Test that only one immediate supervisor is returned for an employee who is second in rank
        """
        register_user(self)
        result = login_user(self)
        access_token = json.loads(result.data.decode())['auth_token']
        data = json.dumps(single_root_json)
        post_hierarchy(self, data, access_token)
        response = self.client.get(
            '/api/v1/hierarchy/two_supervisors/Sophie',
            headers=dict(Authorization="Bearer " + access_token),
        )
        res = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertTrue(res['status'] == 'success')
        self.assertTrue(res['message'] == 'Only the immediate supervisor is available')
        supervisors = {'supervisor': 'Jonas', 'supervisor_of_supervisor': None}
        self.assertDictEqual(res['supervisors'], supervisors)


if __name__ == '__main__':
    unittest.main()
