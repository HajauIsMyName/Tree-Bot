import discord
import random

from discord.ext import commands
from MainFunction import *


class Economy(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["bal"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def balance(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author

        balance = await get_balance(member)

        if not balance:
            balance = (0, 0)

        embed = discord.Embed(color=discord.Color.red())
        embed.set_author(name=f"{member.name}'s balance",
                         icon_url=member.avatar.url)
        embed.add_field(name="Wallet: ", value=f":coin: {balance[0]}")
        embed.add_field(name="Bank:", value=f":coin: {balance[1]}")

        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def beg(self, ctx):
        balance = await get_balance(ctx.author)
        earnings = random.randrange(1, 51)

        await update_balance(ctx.author, balance[0] + earnings)

        await ctx.send(f"Someone gave you :coin: {earnings}")

    @commands.command()
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def work(self, ctx):
        balance = await get_balance(ctx.author)
        earnings = random.randrange(1, 201)

        await update_balance(ctx.author, balance[0] + earnings)

        await ctx.send(f"You worked for :coin: {earnings}")

    @commands.command(aliases=["dep"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def deposit(self, ctx, amount=None):
        balance = await get_balance(ctx.author)

        if amount == "max" or amount == "all":
            amount = balance[0]

        try:
            amount = int(amount)

        except:
            raise commands.BadArgument

        if amount > balance[0]:
            await ctx.send(f"**:no_entry_sign: {ctx.author.name}**, you don't have that much money!")
            return

        elif amount <= 0:
            raise commands.BadArgument

        await update_balance(ctx.author, balance[0] - amount)
        await update_balance(ctx.author, balance[1] + amount, "bank")

        await ctx.send(f"You deposited **:coin: {amount}**")

    @commands.command(aliases=["with"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def withdraw(self, ctx, amount=None):
        balance = await get_balance(ctx.author)

        if amount == "max" or amount == "all":
            amount = balance[1]

        try:
            amount = int(amount)

        except:
            raise commands.BadArgument

        if amount > balance[1]:
            await ctx.send(f"**:no_entry_sign: {ctx.author.name}**, you don't have that much money!")
            return

        elif amount <= 0:
            raise commands.BadArgument

        await update_balance(ctx.author, balance[1] - amount, "bank")
        await update_balance(ctx.author, balance[0] + amount)

        await ctx.send(f"You withdrew **:coin: {amount}**")

    @commands.command(aliases=["send", "sent"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def give(self, ctx, *messages):
        messages = [message.lower() for message in messages]

        if not messages:
            raise commands.BadArgument

        else:
            if len(messages) == 2:
                for message in messages:
                    try:
                        amount = int(message)

                    except:
                        member = discord.utils.get(
                            self.client.get_all_members(), id=int(message[2:-1]))

                        if member:
                            continue

                        else:
                            await ctx.send(f"**:no_entry_sign: {ctx.author.name}**, you can't give money to bot")
                            return

            else:
                raise commands.BadArgument

            authorBalance = await get_balance(ctx.author)
            memberBalance = await get_balance(member)

            if amount <= 0 or member is ctx.author:
                raise commands.BadArgument

            elif amount > authorBalance[0]:
                await ctx.send(f"**:no_entry_sign: {ctx.author}**, you don't have that much money!")
                return

            await update_balance(ctx.author, authorBalance[0] - amount)
            await update_balance(member, memberBalance[0] + amount)

            await ctx.send(f"**{ctx.author.name}** sent **:coin: {amount}** to **{member.name}**!")


async def setup(client):
    await client.add_cog(Economy(client))
