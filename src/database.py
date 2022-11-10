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
            CREATE TABLE IF NOT EXISTS feeds (
                feed TEXT PRIMARY KEY NOT NULL,
                title TEXT,
                time TEXT,
                url TEXT
            ) WITHOUT ROWID;
            """
        )
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS discord (
                id INTEGER PRIMARY KEY ASC,
                guild TEXT NOT NULL,
                channel TEXT NOT NULL,
                feed TEXT NOT NULL,
                UNIQUE (guild, channel, feed)
            );
            """
        )

    async def add_subscribe(self, guild, channel, feed):
        self.cursor.execute(
            "INSERT OR IGNORE INTO discord(guild, channel, feed) VALUES(?, ?, ?);",
            (guild, channel, feed)
        )
        self.connect.commit()

    async def del_subscribe(self, guild, channel, feed):
        self.cursor.execute(
            "DELETE FROM discord WHERE guild=? AND channel=? AND feed=?;",
            (guild, channel, feed)
        )
        self.connect.commit()

    async def list_subscribe(self, guild=None, channel=None, feed=None):
        if not (guild is None or channel is None or feed is None):
            return self.cursor.execute(
                "SELECT * FROM discord WHERE guild=? AND channel=? AND feed=?;",
                (guild, channel, feed)
            )
        if not (guild is None or channel is None):
            return self.cursor.execute(
                "SELECT * FROM discord WHERE guild=? AND channel=?;",
                (guild, channel)
            )
        if not (guild is None):
            return self.cursor.execute(
                "SELECT * FROM discord WHERE guild=?;",
                (guild,)
            )

        return self.cursor.execute("SELECT * FROM discord;")

    async def get_feed_cache(self, feed):
        return self.cursor.execute(
            "SELECT * FROM feeds WHERE feed=?;",
            (feed,)
        )

    async def set_feed_cache(self, feed, title, time, url):
        self.cursor.execute(
            "INSERT OR REPLACE INTO feeds(feed, title, time, url) VALUES (?, ?, ?, ?);",
            (feed, title, time, url)
        )
        self.connect.commit()
