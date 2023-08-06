
import json

from urllib.parse import urlencode
from .base import BaseShortener, ShortenerServiceError


VGD_SERVICE_URL = "http://v.gd/%s.php"


class VgdError(ShortenerServiceError):
    pass


class Vgd(BaseShortener):

    exception_class = VgdError
    service_url = VGD_SERVICE_URL

    def __init__(self, logger=None):
        super().__init__(None, logger=logger)
        self.default_request_params = {
            'format': 'json',
        }

    def _get_request_url(self, action, params):
        request_params = self.default_request_params
        request_params.update(params)
        request_params = request_params.items()

        encoded_params = urlencode(request_params)
        url = self.service_url %action

        return "%s?%s" % (url, encoded_params)

    def _get_error_from_response(self, response):  # pylint: disable=no-self-use
        """General syntax of the error response:

            { "errorcode": <error code>, "errormessage": "<error message>" }

        Specific error messages:
        Error code 1 - Please specify a URL to shorten.
        Error code 1 - there was a problem with the short URL provided (invalid/doesn't exist)
        Error code 2 - the requested short URL exists but has been disabled by us (perhaps due
                       to violation of our terms)
        Error code 3 - our rate limit was exceeded (your app should wait before trying again)
        Error code 4 - any other error (includes potential problems with our service such as a
                       maintenance period)
        """
        error = 'An error occured while executing this request.'
        error_code = response.get('errorcode')
        if error_code:
            error = str(error_code) + ': '
        error_message = response.get('errormessage')
        if error_message:
            error += error_message

        return error

    def shorten_url(self, long_url, logstats=False):  # pylint: disable=arguments-differ
        data = {'url': long_url}
        if logstats:
            data['logstats'] = 1
        request_url = self._get_request_url('create', data)
        headers, response = self._do_http_request(request_url)  # pylint: disable=unused-variable

        response = json.loads(response)
        short_url = response.get('shorturl')
        if not short_url:
            error = self._get_error_from_response(response)
            raise self.exception_class(error)

        return short_url

    def expand_url(self, short_url):
        data = {'shorturl': short_url}
        request_url = self._get_request_url('forward', data)
        headers, response = self._do_http_request(request_url)  # pylint: disable=unused-variable

        response = json.loads(response)
        long_url = response.get('url')
        if not long_url:
            error = self._get_error_from_response(response)
            raise self.exception_class(error)

        return long_url
