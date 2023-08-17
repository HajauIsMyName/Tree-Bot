import random

from discord.ext import commands
from MainFunction import *


class Gamble(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["cf", "flip"])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def coinflip(self, ctx, *messages):
        balance = await get_balance(ctx.author)
        messages = [message.lower() for message in messages]

        userChoice = "heads"
        amount = 1

        if len(messages) == 1:
            try:
                amount = int(messages)

            except:
                if messages == "max" or messages == "all":
                    amount = balance[0]

                elif messages in ["t", "tails"]:
                    userChoice = "tails"

        elif len(messages) == 2:
            for message in messages:
                if message == "max" or message == "all":
                    amount = balance[0]

                else:
                    try:
                        amount = int(message)

                    except:
                        if message in ["t", "tails"]:
                            userChoice = "tails"

        if amount <= 0:
            raise commands.BadArgument
        
        elif amount > balance[0]:
            await ctx.send(f"**:no_entry_sign: {ctx.author}**, you don't have that much money!")
            return

        botChoice = random.randrange(2)
        userChoice = 0 if userChoice == "heads" else 1

        choice = {0: "heads", 1: "tails"}
        desc = desc = f"You bet :coin: {amount} on {choice[userChoice]}.\n"

        if botChoice == userChoice:
            desc += f"It was {choice[botChoice]}. **YOU WIN**\n+ :coin: {amount * 2}"
            await update_balance(ctx.author, balance[0] + amount)

        else:
            desc += f"It was {choice[botChoice]}. You lost all :<"
            await update_balance(ctx.author, balance[0] - amount)

        embed = discord.Embed(description=desc)
        embed.set_author(name="Coinflip")

        await ctx.send(embed=embed)

async def setup(client):
    await client.add_cog(Gamble(client))