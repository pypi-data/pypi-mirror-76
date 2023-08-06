
import json

from urllib.parse import urlencode
from .base import BaseShortener, ShortenerServiceError


BITLY_API_VERSION = '2.0.1'
BITLY_SERVICE_URL = 'http://api.bit.ly/'


class BitlyError(ShortenerServiceError):
    pass


class Bitly(BaseShortener):

    exception_class = BitlyError
    service_url = BITLY_SERVICE_URL

    def __init__(self, login, api_key, logger=None):
        super().__init__(api_key, logger=logger)
        self.login = login
        self.default_request_params = {
            'version': BITLY_API_VERSION,
            'format': 'json',
            'login':  self.login,
            'apiKey': self.api_key,
        }

    def _get_request_url(self, action, param_key, param_value):
        request_params = self.default_request_params
        request_params[param_key] = param_value
        request_params = request_params.items()

        encoded_params = urlencode(request_params)
        return "%s%s?%s" % (self.service_url, action, encoded_params)

    def _is_response_success(self, response):  # pylint: disable=no-self-use
        return response.get('statusCode') == 'OK'

    def _get_error_from_response(self, response):  # pylint: disable=no-self-use
        error_code = response.get('errorCode')
        error_message = response.get('errorMessage')

        error = 'Invalid Response. '
        if error_code:
            error = '%s: ' %error_code
        if error_message:
            error += error_message

        return error

    def shorten_url(self, long_url):
        request_url = self._get_request_url('shorten', 'longUrl', long_url)
        headers, response = self._do_http_request(request_url)  # pylint: disable=unused-variable

        response = json.loads(response)
        if not self._is_response_success(response):
            msg = self._get_error_from_response(response)
            raise self.exception_class(msg)

        results_dict = response.get('results')
        result = results_dict.get(long_url)
        return result.get('shortUrl')

    def expand_url(self, short_url):
        request_url = self._get_request_url('expand', 'shortUrl', short_url)
        headers, response = self._do_http_request(request_url)  # pylint: disable=unused-variable

        response = json.loads(response)
        if not self._is_response_success(response):
            msg = self._get_error_from_response(response)
            raise self.exception_class(msg)

        results_dict = response.get('results')
        return results_dict.values()[0].get('longUrl')


    def get_short_url_info(self, short_url):
        request_url = self._get_request_url('info', 'shortUrl', short_url)
        headers, response = self._do_http_request(request_url)  # pylint: disable=unused-variable

        response = json.loads(response)
        if not self._is_response_success(response):
            msg = self._get_error_from_response(response)
            raise self.exception_class(msg)

        results_dict = response.get('results')
        return results_dict.values()[0]

    def get_stats(self, short_url):
        request_url = self._get_request_url('stats', 'shortUrl', short_url)
        headers, response = self._do_http_request(request_url)  # pylint: disable=unused-variable

        response = json.loads(response)
        if not self._is_response_success(response):
            msg = self._get_error_from_response(response)
            raise self.exception_class(msg)

        results_dict = response.get('results')
        return results_dict
