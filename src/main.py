# pylint: disable=missing-function-docstring, missing-class-docstring, missing-module-docstring

import socket
import discord
import provider
from discord.ext import tasks
from database import DBControl

TOKEN = ""
GUILDs = []
db = DBControl(":memory:")
socket.setdefaulttimeout(30)

with open("./config", "r", encoding="utf-8") as file:
    for line in file.readlines():
        striped = line.strip()
        if striped != "":
            splited = striped.split("=")
            if splited[0] == "TOKEN":
                TOKEN = splited[1]
            elif splited[0] == "GUILD":
                GUILDs.append(discord.Object(id=splited[1]))
            elif splited[0] == "DBLOC":
                db = DBControl(splited[1])


class CustomBot(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = discord.app_commands.CommandTree(self)

    async def setup_hook(self) -> None:
        self.news_update.start()  # pylint: disable=no-member
        for guild in GUILDs:
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)
        return await super().setup_hook()

    @tasks.loop(seconds=60)
    async def news_update(self):
        subs = (await db.list_subscribe()).fetchall()
        feeds = set(elem[3] for elem in subs)

        for feed in feeds:
            content = await provider.fetch_timeout(feed)
            cached = (await db.get_feed_cache(feed)).fetchone()

            if content == None:
                continue
            try:
                if content.version == "":
                    continue
            except AttributeError:
                continue

            if cached is None:
                new = content.entries[0]
                await db.set_feed_cache(feed, new.title, new.published, new.link)
                for sub in filter(lambda elem: elem[3] == feed, subs):
                    await client.get_channel(int(sub[2])).send(f"**{new.title}**\n{new.link}")

                return

            news = iter(content.entries[::-1])
            while True:
                try:
                    new = next(news)
                    if provider.timeparse(cached[2]) < provider.timeparse(new.published):
                        for sub in filter(lambda elem: elem[3] == feed, subs):
                            await client.get_channel(int(sub[2])).send(f"**{new.title}**\n{new.link}")
                except StopIteration:
                    if provider.timeparse(cached[2]) < provider.timeparse(new.published):
                        await db.set_feed_cache(feed, new.title, new.published, new.link)
                    break

    @news_update.before_loop
    async def update_before_loop(self):
        await self.wait_until_ready()


custom_intents = discord.Intents.default()
custom_intents.message_content = True  # pylint: disable=assigning-non-slot
client = CustomBot(intents=custom_intents)


@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    await db.init_table()


@client.event
async def on_message(msg: discord.Message):
    print(
        f"{msg.created_at}[{msg.guild.name}-{msg.channel.name}]{msg.author.name}: {msg.content}")


@client.tree.command()
async def rss(interaction: discord.Interaction):
    """顯示已經訂閱的RSS列表"""
    subs = await db.list_subscribe(interaction.guild_id, interaction.channel_id)
    await interaction.response.send_message(
        "已經訂閱的RSS列表\n" + "\n".join(map(lambda elem: elem[3], subs))
    )


@client.tree.command()
@discord.app_commands.describe(
    rss_url="RSS URL"
)
async def sub(interaction: discord.Interaction, rss_url: str):
    """新訂閱"""
    content = await provider.fetch_timeout(rss_url)
    try:
        if content.version == "":
            raise ValueError
    except (AttributeError, ValueError):
        await interaction.response.send_message(f"{rss_url} 訂閱失敗")
    else:
        await db.add_subscribe(interaction.guild_id, interaction.channel_id, rss_url)
        await interaction.response.send_message(f"《{content.feed.title}》{rss_url} 訂閱成功")


@client.tree.command()
@discord.app_commands.describe(
    rss_url="RSS URL"
)
async def unsub(interaction: discord.Interaction, rss_url: str):
    """取消訂閱"""
    await db.del_subscribe(interaction.guild_id, interaction.channel_id, rss_url)
    await interaction.response.send_message(f"{rss_url} 取消訂閱成功")


@client.tree.command()
async def export(interaction: discord.Interaction):
    """輸出OPML"""
    await interaction.response.send_message("TODO")


@client.tree.command()
async def dup(interaction: discord.Interaction):
    """手動update"""
    await interaction.response.send_message("Ok")
    await client.news_update()


client.run(TOKEN)
