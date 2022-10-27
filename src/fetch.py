# pylint: disable=missing-function-docstring, missing-class-docstring, missing-module-docstring

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

    def to_string(self):
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
            "channel": self.channel,
            "items": [item.to_dict() for item in self.items]
        }

    def to_string(self):
        return str(self.to_dict())


class Provider():
    async def fetch_stream(self, url: str):
        return requests.get(url, timeout=300)

    async def parse(self, xml: str) -> Feed:
        raw = BeautifulSoup(xml, 'lxml-xml')

