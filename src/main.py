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

    async def on_ready(self):
        print(f"We have logged in as {self.user}")

    async def on_message(self, msg: discord.Message):
        print(
            f"{msg.created_at}[{msg.guild.name}-{msg.channel.name}]{msg.author.name}: {msg.content}"
        )


custom_intents = discord.Intents.default()
custom_intents.message_content = True  # pylint: disable=assigning-non-slot
client = CustomBot(intents=custom_intents)

client.run(TOKEN)
