import unittest
import mock
import put_projects
import auth.authHeaders_prod as authHeaders_prod

# Here we have created a test class TestMoveProjectFromGroup which is a subclass of unittest.TestCase. 
# The class has two test methods: test_move_project_success and test_move_project_failure.

# The setUp method is called before each test method, it sets up the initial state of the test.

# test_move_project_success test the successful scenario where the status code is 200 and the 
# json response is {"status":"success"}

# test_move_project_failure test the failure scenario where the status code is 400 and the 
# json response is {}

# The @mock.patch('requests.put') decorator is used to mock the requests.put() method, 
# so we can control its behavior in our tests.

# In test_move_project_success test, we set the status_code of the mock response 
# object to 200 and the json response to {"status":"success"}

# In test_move_project_failure test, we set the status_code of the mock response 
# object to 400

# Then we call the __move_project_from_group(self.src_prj_id, self.dst_group_id) function and assert 
# the returned value against the expected value


class TestMoveProjectFromGroup(unittest.TestCase):
    def setUp(self):
        self.src_prj_id = 'prj1'
        self.dst_group_id = 'grp1'
        self.mock_response = mock.Mock()
        authHeaders_prod.server_url_prod = "http://example.com"
        authHeaders_prod.tenant_prod = "tenant1"
        authHeaders_prod.auth_headers_prod = {"headers1": "header1"}

    @mock.patch('requests.put')
    def test_move_project_success(self, mock_put):
        self.mock_response.status_code = 200
        self.mock_response.json.return_value = {"status": "success"}
        mock_put.return_value = self.mock_response

        result = put_projects.move_project_from_group(self.src_prj_id, self.dst_group_id)
        self.assertEqual(result, {"status": "success"})

    @mock.patch('requests.put')
    def test_move_project_failure(self, mock_put):
        self.mock_response.status_code = 400
        mock_put.return_value = self.mock_response

        result = put_projects.move_project_from_group(self.src_prj_id, self.dst_group_id)
        self.assertEqual(result, {})

if __name__ == '__main__':
    unittest.main()

