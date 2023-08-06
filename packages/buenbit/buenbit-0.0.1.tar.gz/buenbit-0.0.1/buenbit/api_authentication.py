import hashlib
import hmac
import time
from urllib.parse import urlparse

from requests.auth import AuthBase


class HttpSigningAuth(AuthBase):
    """Attaches HTTP Signing Authentication to the given Request object."""

    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret

    def __call__(self, r):
        expiration = self._expiration()
        auth_headers = {
            'api-key': self.api_key,
            'expires': str(expiration),
            'signature': self._generate_signature_for_request(r, expiration)
        }
        r.headers.update(auth_headers)
        return r

    def _expiration(self):
        grace_period = 5
        return round(time.time() + grace_period)

    def _generate_signature_for_request(self, request, expiration):
        """Generate a request signature compatible with Buenbit API."""

        parsedURL = urlparse(request.url)
        path = parsedURL.path
        if parsedURL.query:
            path = path + '?' + parsedURL.query

        body = request.body or ''
        if isinstance(body, (bytes, bytearray)):
            body = body.decode('utf8')

        message = f'{request.method}{path}{expiration}{body}'

        signature = hmac.new(bytes(self.api_secret, 'utf8'), bytes(message, 'utf8'),
                             digestmod=hashlib.sha256).hexdigest()
        return signature
