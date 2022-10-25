# pylint: disable=missing-function-docstring, missing-class-docstring, missing-module-docstring

import discord


class CustomBot(discord.Client):
    async def on_ready(self):
        print(f"We have logged in as {self.user}")

    async def on_message(self, msg: discord.Message):
        print(
            f"{msg.created_at}[{msg.guild.name}-{msg.channel.name}]{msg.author.name}: {msg.content}"
        )
