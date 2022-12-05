import asyncio
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from app import keep_alive

client = commands.Bot( command_prefix=commands.when_mentioned_or( "breh!" ), case_insensitive=True,
                       strip_after_prefix=True, help_command=None, intents=discord.Intents.all(), )


async def load_extensions():
    for filename in os.listdir( "EventHandlers" ):
        if filename.endswith( ".py" ):
            await client.load_extension( f"EventHandlers.{filename[:-3]}" )

    for filename in os.listdir( "CommandLists" ):
        if filename.endswith( ".py" ):
            await client.load_extension( f"CommandLists.{filename[:-3]}" )


async def start_bot():
    keep_alive()
    load_dotenv()

    async with client:
        await load_extensions()
        await client.start( os.getenv( "TOKEN" ) )


if __name__ == "__main__":
    asyncio.run( start_bot() )