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


async def fetch(url: str, timeout=60):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.35",
    }
    response = requests.get(
        url,
        timeout=timeout,
        headers=headers,
        allow_redirects=True
    )

    if response.status_code in range(200, 300):
        return response.text

    return response.raise_for_status()


async def parse(xml: str) -> Feed:
    raw = BeautifulSoup(xml, 'lxml-xml')
    atom_link = raw.find("atom:link")
    return Feed(
        Channel(
            _soup2text(raw.find("title")),
            _soup2text(raw.find("description")),
            _soup2text(raw.find("lastBuildDate")),
            _soup2text(raw.find("link")),
            atom_link["href"] if not atom_link is None else ""
        ),
        [
            Item(
                _soup2text(item.find("title")),
                _soup2text(item.find("description")),
                _soup2text(item.find("link")),
                _soup2text(item.find("guid")),
                [_soup2text(j) for j in item.find_all("category")],
                _soup2text(item.find("dc:creator")),
                _soup2text(item.find("pubDate"))
            )
            for item in raw.find_all("item")
        ]
    )


def _soup2text(soup):
    return soup.text if not soup is None else ""


async def is_rss(url: str):
    return len(BeautifulSoup(await fetch(url), 'lxml-xml').find_all("rss")) != 0


async def get_rss(url: str):
    return await parse(
        await fetch(url)
    )


def timeparse(time: str):
    if time.endswith("+0000"):
        # Example: Sat, 23 Apr 2022 20:04:56 +0000
        return strptime(time, "%a, %d %b %Y %H:%M:%S +0000")
    if time.endswith("GMT"):
        # Example: Wed, 05 Oct 2022 17:08:00 GMT
        return strptime(time, "%a, %d %b %Y %H:%M:%S GMT")

    return ""
