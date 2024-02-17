from __future__ import annotations

import re
import requests

from .exceptions import *
from .session import Session


class LID:
    def __init__(self, session: Session = None, lid: str = None) -> None:
        self.id = lid
        self.session = session

    def __str__(self):
        return self.id if self.id else "No LID"

    def __eq__(self, other: LID) -> bool:
        return self.id == other.id if self.id and other.id else False

    def __ne__(self, other: LID) -> bool:
        return self.id != other.id

    @staticmethod
    def from_url(url: str, raw: bool = False) -> LID:
        """Get the Letterboxd ID (LID) from a URL."""
        if "boxd.it" in url:
            return LID(url.split("/")[-1])

        if url.startswith("letterboxd.com"):
            url = "https://" + url

        if not url.startswith("https://letterboxd.com") and not raw:
            if url.startswith("/film/"):
                url = "https://letterboxd.com" + url
            elif re.match(r"film/[a-zA-Z0-9-]+/?$", url):
                url = (
                    "https://letterboxd.com/"
                    + re.search(r"film/[a-zA-Z0-9-]+/?$", url).group()
                )
            else:
                url = f"https://letterboxd.com/film/{url}/"

        if not url.endswith("/"):
            url += "/"

        r = requests.head(url)

        if r.status_code == 404:
            raise TitleNotFound(url)
        elif not r.ok:
            raise RequestException(f"{r.status_code} {r.reason}")
        elif not r.headers.get("x-letterboxd-identifier"):
            raise Exception(f"Could not find LID in response headers: {r.headers}")

        return LID(lid=r.headers["x-letterboxd-identifier"])

    def from_imdb(self, imdb: str) -> LID:
        """session the Letterboxd ID (LID) from an IMDb ID."""
        return self._get_lid_from_external_id(imdb, "imdb")

    def from_tmdb(self, tmdb: str) -> LID:
        """Get the Letterboxd ID (LID) from a TMDb ID."""
        return self._get_lid_from_external_id(tmdb, "tmdb")

    def _get_lid_from_external_id(self, external_id: str, source: str) -> LID:
        """Helper function to get the LID from an external source like IMDb or TMDb."""
        r = self.session.get(
            "films",
            params={"filmId": f"{source}:{external_id}"},
        ).json()

        if "error" in r:
            raise Exception(f"{r['message']} [{r['code']}]")

        r = r["items"]

        if not r:
            raise TitleNotFound(external_id)

        return LID(r[0]["id"])
