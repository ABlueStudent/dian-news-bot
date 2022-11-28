# pylint: disable=missing-function-docstring, missing-class-docstring, missing-module-docstring

import asyncio
import re
from time import strptime
import feedparser


async def fetch_rss(url: str):
    feed = feedparser.parse(
        url,
        agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.35"
    )
    if feed.status in range(300, 400):
        return fetch_rss(feed.href)

    return feed


async def fetch_timeout(url: str, timeout=10):
    try:
        return await asyncio.wait_for(fetch_rss(url), timeout=timeout)
    except TimeoutError:
        print(f"{url} fetch timeout!")
        return  # TODO: 我先想想


def timeparse(time: str):
    if re.match(r"\w{3}, \d{2} \w{3} \d{4} \d{2}:\d{2}:\d{2} (\+|\-)\d{4}", time) is not None:
        # Example: Sat, 23 Apr 2022 20:04:56 +0000
        return strptime(time, "%a, %d %b %Y %H:%M:%S %z")
    if re.match(r"\w{3}, \d{2} \w{3} \d{4} \d{2}:\d{2}:\d{2} \w{3}", time) is not None:
        # Example: Wed, 05 Oct 2022 17:08:00 GMT
        return strptime(time, "%a, %d %b %Y %H:%M:%S %Z")

    return
