# pylint: disable=missing-function-docstring, missing-class-docstring, missing-module-docstring

from time import strptime
import requests
from bs4 import BeautifulSoup


class Channel():
    def __init__(
        self,
        title: str,
        description: str,
        last_build_date: str,
        link: str,
        atom_link: str
    ):
        self.title = title
        self.description = description
        self.last_build_date = last_build_date
        self.link = link
        self.atom_link = atom_link

    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "last_build_date": self.last_build_date,
            "link": self.link,
            "atom_link": self.atom_link
        }

    def to_str(self):
        return str(self.to_dict())


class Item():
    def __init__(
        self,
        title: str,
        description: str,
        link: str,
        guid: str,
        category: list,
        creator: str,
        pub_date: str,
    ):
        self.title = title
        self.description = description
        self.link = link
        self.guid = guid
        self.category = category
        self.creator = creator
        self.pub_date = pub_date

    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "link": self.link,
            "guid": self.guid,
            "category": self.category,
            "creator": self.creator,
            "pub_date": self.pub_date
        }

    def to_str(self):
        return str(self.to_dict())


class Feed():
    def __init__(
        self,
        channel: Channel,
        items: list[Item]
    ):
        self.channel = channel
        self.items = items

    def to_dict(self):
        return {
            "channel": self.channel.to_dict(),
            "items": [item.to_dict() for item in self.items]
        }

    def to_str(self):
        return str(self.to_dict())


async def fetch(url: str, timeout=300):
    return requests.get(url, timeout=timeout).text


async def parse(xml: str) -> Feed:
    raw = BeautifulSoup(xml, 'lxml-xml')
    atom_link = raw.find("atom:link")
    return Feed(
        Channel(
            _parse(raw.find("title")),
            _parse(raw.find("description")),
            _parse(raw.find("lastBuildDate")),
            _parse(raw.find("link")),
            atom_link["href"] if not atom_link is None else ""
        ),
        [
            Item(
                _parse(item.find("title")),
                _parse(item.find("description")),
                _parse(item.find("link")),
                _parse(item.find("guid")),
                [_parse(j) for j in item.find_all("category")],
                _parse(item.find("dc:creator")),
                _parse(item.find("pubDate"))
            )
            for item in raw.find_all("item")
        ]
    )

def _parse(s):
    return s.text if not s is None else ""

def timeparse(time: str):
    if time.endswith("+0000"):
        # Example: Sat, 23 Apr 2022 20:04:56 +0000
        return strptime(time, "%a, %d %b %Y %H:%M:%S +0000")
    elif time.endswith("GMT"):
        # Example: Wed, 05 Oct 2022 17:08:00 GMT
        return strptime(time, "%a, %d %b %Y %H:%M:%S GMT")
