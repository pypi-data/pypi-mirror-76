# The following import is to let tests run in Python 2.7 which does not have
# unittest.mocks which was introduced in Python 3.3. Some of our projects still run
# Python 2.7 so support is necessary for now
try:
    from unittest import mock
except ImportError:
    import mock
from unittest import TestCase

from mercuryclient.api import MercuryApi


class SMSMixinTest(TestCase):
    def setUp(self):
        self.post_api_mock = mock.patch(
            "mercuryclient.api.MercuryApi._post_json_http_request"
        ).start()
        self.addCleanup(self.post_api_mock.stop)

    def test_sending_sms_calls_sms_api(self):
        client = MercuryApi(
            {
                "username": "username",
                "password": "password",
                "url": "https://mercury-dev.esthenos.in",
            }
        )
        mock_response = mock.MagicMock()
        mock_response.status_code = 201
        self.post_api_mock.return_value = ("random_string", mock_response)
        client.send_sms("9876543210", "Some message", "kaleyra", "some_profile")

        self.post_api_mock.assert_called_with(
            "https://mercury-dev.esthenos.in/api/v1/sms/",
            data={
                "provider": "kaleyra",
                "profile": "some_profile",
                "recipient": "9876543210",
                "message": "Some message",
            },
            send_request_id=True,
            add_bearer_token=True,
        )

    def test_exception_raised_if_status_code_error(self):
        client = MercuryApi(
            {
                "username": "username",
                "password": "password",
                "url": "https://mercury-dev.esthenos.in",
            }
        )
        mock_response = mock.MagicMock()
        mock_response.status_code = 401
        self.post_api_mock.return_value = ("random_string", mock_response)
        with self.assertRaises(Exception):
            client.send_sms("9876543210", "Some message", "kaleyra", "some_profile")

    def test_api_succeeds_if_status_code_success(self):
        client = MercuryApi(
            {
                "username": "username",
                "password": "password",
                "url": "https://mercury-dev.esthenos.in",
            }
        )
        mock_response = mock.MagicMock()
        mock_response.status_code = 201
        self.post_api_mock.return_value = ("random_string", mock_response)

        response = client.send_sms(
            "9876543210", "Some message", "kaleyra", "some_profile"
        )
        self.assertEqual(response["request_id"], "random_string")
        self.assertEqual(response["status"], "Success")
