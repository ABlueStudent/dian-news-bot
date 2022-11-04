# pylint: disable=missing-function-docstring, missing-class-docstring, missing-module-docstring

import sqlite3


class DBControl():
    def __init__(self, db_path: str):
        self.connect = sqlite3.connect(db_path)
        self.cursor = self.connect.cursor()

    async def list_tables(self):
        return self.cursor.execute(
            """
            SELECT name FROM sqlite_schema
            WHERE type='table'
            ORDER BY name;
            """
        )

    async def init_table(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS discord (id INTEGER PRIMARY KEY ASC, guild TEXT NOT NULL, channel  TEXT NOT NULL, feed TEXT NOT NULL);
            """
        )
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS feeds (feed TEXT PRIMARY KEY NOT NULL, title TEXT, time TEXT, url TEXT) WITHOUT ROWID;
            """
        )

    async def add_subscribe(self, guild, channel, feed):
        self.cursor.execute(
            "INSERT INTO discord(guild, channel, feed) VALUES(?, ?, ?);",
            (guild, channel, feed)
        )

    async def del_subscribe(self, guild, channel, feed):
        self.cursor.execute(
            "DELETE FROM discord WHERE guild=? AND channel=? AND feed=?;",
            (guild, channel, feed)
        )

    async def list_subscribe(self, guild, channel, feed):
        return self.cursor.execute(
            "SELECT * FROM discord WHERE guild=? AND channel=? AND feed=?;",
            (guild, channel, feed)
        )

    async def get_feed_cache(self, feed):
        self.cursor.execute(
            "SELECT * FROM feeds WHERE feed=?;",
            (feed)
        )

    async def set_feed_cache(self, feed, title, time, url):
        self.cursor.execute(
            "INSERT OR REPLACE INTO feeds(feed, title, time, url) VALUES (?, ?, ?, ?);",
            (feed, title, time, url)
        )
