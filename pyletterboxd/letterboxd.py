from typing import Union

import requests

from .exceptions import *
from .lid import LID
from .session import Session


class Letterboxd:
    def __init__(self, api_key: str, secret: Union[str, bytes]) -> None:
        self.session = Session(api_key, secret)
        self.lid = LID(self.session)

    def call(self, url: str, method: str = "GET", **kwargs) -> requests.Response:
        """Make a request to the Letterboxd API."""
        return self.session.request(method, url, **kwargs).json()
