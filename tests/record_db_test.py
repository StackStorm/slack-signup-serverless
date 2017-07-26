import unittest
import mock
import os
from testfixtures import log_capture

context = {}
env = {"DYNAMODB_TABLE": "mytable"}


class RecordDBTest(unittest.TestCase):
    @mock.patch.dict(os.environ, env)
    @mock.patch("boto3.resource")
    @log_capture()
    def test_handler_ok(self, mock_resource, log):
        event = {'email': 'my@email.com', 'first_name': "Yuri", 'last_name': "Gagarin"}
        from record_db import handler
        res = handler.endpoint(event, context)
        self.assertEqual(res['statusCode'], 200)
        print(log)

    @mock.patch.dict(os.environ, env)
    @mock.patch("boto3.resource")
    @log_capture()
    def test_handler_no_lastname(self, mock_resource, log):
        event = {'email': 'my@email.com', 'first_name': "Yuri", 'last_name': ""}
        from record_db import handler
        res = handler.endpoint(event, context)
        self.assertEqual(res['statusCode'], 200)
        print(log)

    @mock.patch.dict(os.environ, env)
    @mock.patch("boto3.resource")
    @log_capture()
    def test_handler_missed_keys(self, mock_resource, log):
        event = {'email': 'my@email.com', 'first_name': "Yuri"}
        from record_db import handler
        with self.assertRaises(KeyError):
            handler.endpoint(event, context)
        print(log)
