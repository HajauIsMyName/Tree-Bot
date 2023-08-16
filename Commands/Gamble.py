import os
import random
import discord

from discord.ext import commands
from MainFunction import *


class Gamble(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["cf", "flip"])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def coinflip(self, ctx, amount=1, user_choice="h"):
        balance = await get_bank(ctx.author)

        if amount == "max" or amount == "all":
            amount = balance[0]

        try:
            amount = int(amount)

        except ValueError:
            raise commands.BadArgument

        if amount <= 0:
            raise commands.BadArgument

        elif amount > balance[0]:
            await ctx.send(f"**:no_entry_sign: {ctx.author}**, you don't have that much money!")
            return

        user_choice = user_choice.lower()

        if user_choice in ["h", "heads"]:
            user_choice = 0

        elif user_choice in ["t", "tails"]:
            user_choice = 1

        else:
            raise commands.BadArgument

        random.seed(int(os.getenv("SEED")))

        bot_choice = random.randrange(2)

        if bot_choice == user_choice:
            desc = f"You bet :coin: {amount} on {user_choice}.\nIt was {bot_choice}. **YOU WIN**\n+ :coin: {amount * 2}"
            await update_data(ctx.author, amount)

        else:
            desc = f"You bet :coin: {amount} on {user_choice}.\nIt was {bot_choice}. You lost all :C"
            await update_data(ctx.author, -amount)

        embed = discord.Embed(description=desc)
        embed.set_author(name="Coinflip")

        await ctx.send(embed=embed)


async def setup(client):
    await client.add_cog(Gamble(client))
