from typing import Union

from .letterboxd import Letterboxd
from .lid import LID

__version__ = "1.0.0"

def new(api_key: str, secret: Union[str, bytes]) -> Letterboxd:
    """Create a new Letterboxd instance."""
    return Letterboxd(api_key, secret)