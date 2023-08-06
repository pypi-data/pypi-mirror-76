import requests
from requests_openapi import Client

from .api_authentication import HttpSigningAuth


class SpecificationUrl:
    LATEST = "https://customers.buenbit.com/api/v1/documentation"


class BuenbitApiClient:
    @classmethod
    def new_with(cls, api_key, api_secret, specification_url=SpecificationUrl.LATEST):
        requester = requests.Session()
        requester.auth = HttpSigningAuth(api_key, api_secret)

        client = Client(requester)
        client.load_spec(cls._get_openapi_specification(specification_url))

        return client

    @staticmethod
    def _get_openapi_specification(url):
        response = requests.get(url)
        response.raise_for_status()
        specification = response.json()["object"]
        return specification
