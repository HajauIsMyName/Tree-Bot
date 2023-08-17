import os
import asyncio
import discord

from discord.ext import commands
from dotenv import load_dotenv

client = commands.Bot(
    command_prefix=commands.when_mentioned_or("breh!"),
    case_insensitive=True,
    strip_after_prefix=True,
    help_command=None,
    intents=discord.Intents.all()
)


async def load_source():
    for folder in os.listdir("./src"):
        for filename in os.listdir(f"./src/{folder}"):
            if filename.endswith(".py"):
                await client.load_extension(f"src.{folder}.{filename[:-3]}")


async def start_bot():
    load_dotenv()

    async with client:
        await load_source()
        await client.start(os.getenv("TOKEN"))

if __name__ == "__main__":
    asyncio.run(start_bot())
