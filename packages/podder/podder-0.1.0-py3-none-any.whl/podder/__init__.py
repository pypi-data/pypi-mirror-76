__version__ = '0.1.0'

from .client import Client
from .services import APIService


def client(domain: str, access_token: str):
    api_service = APIService(domain, access_token)
    return Client(api_service)
