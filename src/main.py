# pylint: disable=missing-function-docstring, missing-class-docstring, missing-module-docstring

import discord

TOKEN = ""
GUILDs = []

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


@client.event
async def on_message(msg: discord.Message):
    print(
        f"{msg.created_at}[{msg.guild.name}-{msg.channel.name}]{msg.author.name}: {msg.content}")


@client.tree.command()
async def rss(interaction: discord.Interaction):
    """顯示已經訂閱的RSS列表"""
    await interaction.response.send_message("已經訂閱的RSS列表")


@client.tree.command()
@discord.app_commands.describe(
    rss_url="RSS URL"
)
async def sub(interaction: discord.Interaction, rss_url: str):
    """新訂閱"""
    await interaction.response.send_message(f"{rss_url} 訂閱成功")


@client.tree.command()
@discord.app_commands.describe(
    rss_url="RSS URL"
)
async def unsub(interaction: discord.Interaction, rss_url: str):
    """取消訂閱"""
    await interaction.response.send_message(f"{rss_url} 取消訂閱成功")


@client.tree.command()
async def export(interaction: discord.Interaction):
    """輸出OPML"""
    await interaction.response.send_message("TODO")


client.run(TOKEN)
