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


async def fetch_stream(url: str, timeout=300):
    return requests.get(url, timeout)


async def parse(xml: str) -> Feed:
    raw = BeautifulSoup(xml, 'lxml-xml')
    return Feed(
        Channel(
            raw.find("title").text,
            raw.find("description").text,
            raw.find("lastBuildDate").text,
            raw.find("link").text,
            raw.find("atom:link")["href"]
        ),
        map(
            lambda item: Item(
                item.find("title").text,
                item.find("description").text,
                item.find("link").text,
                item.find("guid").text,
                [j.text for j in item.find_all("category")],
                item.find("dc:creator").text,
                item.find("pubDate").text
            ),
            raw.find_all("item")
        )
    )
