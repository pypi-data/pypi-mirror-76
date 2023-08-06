class SMSMixin:
    """
    Mixin for sending emails
    """

    def send_sms(self, recipient, message, provider, profile):
        """
        Send sms using the mercury service

        :param recipient: Phone number of recipients
        :param message: SMS message to be sent
        :param provider: SMS Provider. Currently 'kaleyra'
        :param profile: An existing profile in Mercury. The profile has to correspond
        to the provider.
        :return: (request_id, status)
        """
        api = "api/v1/sms/"
        url = "{}/{}".format(self.host, api)

        data = {
            "provider": provider,
            "profile": profile,
            "recipient": recipient,
            "message": message,
        }

        request_id, r = self._post_json_http_request(
            url, data=data, send_request_id=True, add_bearer_token=True
        )

        if r.status_code == 201:
            return {"request_id": request_id, "status": "Success"}

        raise Exception(
            "Error while sending SMS. Status: {}, Response is {}".format(
                r.status_code, r.json()
            )
        )
