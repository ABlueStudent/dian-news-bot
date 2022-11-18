# pylint: disable=missing-function-docstring, missing-class-docstring, missing-module-docstring

import asyncio
import re
from time import strptime
import feedparser


async def fetch_rss(url: str):
    return feedparser.parse(url)


async def fetch_timeout(url: str, timeout=10):
    return await asyncio.wait_for(fetch_rss(url), timeout=timeout)


def timeparse(time: str):
    if re.match(r"\w{3}, \d{2} \w{3} \d{4} \d{2}:\d{2}:\d{2} (\+|\-)\d{4}", time) is not None:
        # Example: Sat, 23 Apr 2022 20:04:56 +0000
        return strptime(time, "%a, %d %b %Y %H:%M:%S %z")
    if re.match(r"\w{3}, \d{2} \w{3} \d{4} \d{2}:\d{2}:\d{2} \w{3}", time) is not None:
        # Example: Wed, 05 Oct 2022 17:08:00 GMT
        return strptime(time, "%a, %d %b %Y %H:%M:%S %Z")

    return
