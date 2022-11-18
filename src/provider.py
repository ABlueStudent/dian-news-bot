# pylint: disable=missing-function-docstring, missing-class-docstring, missing-module-docstring

import asyncio
from time import strptime
import feedparser


async def fetch_rss(url: str):
    return feedparser.parse(url)


async def fetch_timeout(url: str, timeout=10):
    return await asyncio.wait_for(fetch_rss(url), timeout=timeout)


def timeparse(time: str):
    if time.endswith("+0000"):
        # Example: Sat, 23 Apr 2022 20:04:56 +0000
        return strptime(time, "%a, %d %b %Y %H:%M:%S +0000")
    if time.endswith("GMT"):
        # Example: Wed, 05 Oct 2022 17:08:00 GMT
        return strptime(time, "%a, %d %b %Y %H:%M:%S GMT")

    return ""
