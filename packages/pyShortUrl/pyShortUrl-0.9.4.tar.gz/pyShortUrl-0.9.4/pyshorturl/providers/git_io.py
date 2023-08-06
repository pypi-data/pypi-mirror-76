
import random

from .base import BaseShortener, ShortenerServiceError


GITIO_SERVICE_URL = 'https://git.io'


class GitioError(ShortenerServiceError):
    pass


class Gitio(BaseShortener):

    exception_class = GitioError
    service_url = GITIO_SERVICE_URL

    def __init__(self, api_key=None, logger=None):
        super().__init__(api_key, logger=logger)

    def _construct_request(self, long_url):  # pylint: disable=no-self-use
        """Construct the request body as multipart/form-data"""

        boundary = '-----------------------------' + str(int(random.random()*1e10))
        parts = []

        parts.append('--' + boundary)
        parts.append('Content-Disposition: form-data; name="url"')
        parts.append('')
        parts.append(str(long_url))

        parts.append('--' + boundary + '--')
        parts.append('')

        body = '\r\n'.join(parts)
        headers = {'content-type': 'multipart/form-data; boundary=' + boundary}

        return (headers, body)

    def shorten_url(self, long_url):
        request_url = self.service_url
        headers, body = self._construct_request(long_url)
        headers, response = self._do_http_request(request_url, data=body, headers=headers)  # pylint: disable=unused-variable

        short_url = headers.get('Location')

        if not short_url:
            raise self.exception_class('Unable to get short url for %s.' % long_url)

        return short_url
