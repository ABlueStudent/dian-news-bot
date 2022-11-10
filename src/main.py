# pylint: disable=missing-function-docstring, missing-class-docstring, missing-module-docstring

import discord
import provider
from database import DBControl

TOKEN = ""
GUILDs = []
db = DBControl(":memory:")

with open("./config", "r", encoding="utf-8") as file:
    for line in file.readlines():
        if line.strip() != "":
            tmp = line.split("=")
            if tmp[0] == "TOKEN":
                TOKEN = tmp[1]
            elif tmp[0] == "GUILD":
                GUILDs.append(discord.Object(id=tmp[1]))


class CustomBot(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = discord.app_commands.CommandTree(self)

    async def setup_hook(self) -> None:
        for guild in GUILDs:
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)
        return await super().setup_hook()


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
    feed = await provider.parse(
        await provider.fetch(rss_url)
    )

    if not (feed.channel.atom_link == "" or feed.channel.title == ""):
        await db.add_subscribe(interaction.guild_id, interaction.channel_id, rss_url)
        await interaction.response.send_message(f"《{feed.channel.title}》{rss_url} 訂閱成功")
    else:
        await interaction.response.send_message(f"{rss_url} 訂閱失敗")


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


async def update():
    subs = await db.list_subscribe()
    feeds = set(elem[3] for elem in subs.fetchall())

    for feed in feeds:
        content = await provider.parse(
            await provider.fetch(feed)
        )
        cached = await db.get_feed_cache(feed)

        if cached is None:
            new = content.items[0]
            await db.set_feed_cache(feed, new.title, new.pub_date, new.link)
            for s in filter(lambda elem: elem[3] == feed, subs):
                await client.get_channel(s[2]).send(f"{new.title}\n{new.link}")


@client.tree.command()
async def dup(interaction: discord.Interaction):
    """手動update"""
    await update()
    await interaction.response.send_message("Ok")


client.run(TOKEN)
