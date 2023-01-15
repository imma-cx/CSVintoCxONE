import unittest
import json
import mock
from unittest.mock import MagicMock

class TestCreateGroupSet(unittest.TestCase):

    @mock.patch('requests.post')
    def test_create_group_set_success(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_post.return_value = mock_response

        group_data = {"name": "test_group"}
        __create_group_set(group_data)

        mock_post.assert_called_with(relative_url, json.dumps(group_data), headers=auth_headers)
        self.assertTrue(logger.info.called)

    @mock.patch('requests.post')
    def test_create_group_set_failure(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_post.return_value = mock_response

        group_data = {"name": "test_group"}
        __create_group_set(group_data)

        mock_post.assert_called_with(relative_url, json.dumps(group_data), headers=auth_headers)
        self.assertTrue(logger.error.called)

    @mock.patch('requests.post')
    def test_create_group_set_exception(self, mock_post):
        mock_post.side_effect = Exception("Error")

        group_data = {"name": "test_group"}
        __create_group_set(group_data)

        mock_post.assert_called_with(relative_url, json.dumps(group_data), headers=auth_headers)
        self.assertTrue(logger.exception.called)

