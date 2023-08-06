import uuid

from .http_utils import get_session
from .mixins import AuthMixin, MailMixin, SMSMixin


class MercuryApi(AuthMixin, MailMixin, SMSMixin):
    """
    Mercury client to connect to the mercury service

    """

    def __init__(self, conn_params=None):
        self.username = conn_params["username"]
        self.password = conn_params["password"]
        self.host = conn_params["url"]
        self._access_token = None
        self._refresh_token = None
        self._session = None

    @property
    def session(self):
        if self._session is None:
            self._session = get_session()

        return self._session

    @staticmethod
    def _generate_mercury_request_id():
        """
        Generate Unique request id
        :return:
        """
        return uuid.uuid4().hex

    def _post_json_http_request(
        self, url, data, headers=None, send_request_id=True, add_bearer_token=True
    ):
        """

        :param url: URL to send the HTTP POST
        :param data: dict to be sent as JSON in the HTTP body
        :param headers: headers for the request
        :param send_request_id: Defaults to True. Indicates if a request Id has to generated for the request
        :param add_bearer_token: Defaults to True. If True, we will add the bearer token to the request
        :return: (request_id, response): The request id (if present) and the response
        """
        if headers is None:
            headers = dict()

        if send_request_id:
            headers["X-Mercury-Request-Id"] = self._generate_mercury_request_id()

        if add_bearer_token:
            headers["Authorization"] = "Bearer {}".format(self.access_token)

        r = self.session.post(url=url, data=data, headers=headers, timeout=10)

        return headers.get("X-Mercury-Request-Id"), r
