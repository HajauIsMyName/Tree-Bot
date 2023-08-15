import discord
import random

from discord.ext import commands
from MainFunction import *


class Economy(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["bal", "coin"])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def balance(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author

        balance = await get_bank(member)

        embed = discord.Embed(color=discord.Color.red())
        embed.set_author(
            name=f"{member.name}'s balance", icon_url=member.avatar.url)
        embed.add_field(name="Wallet:", value=f":coin: {balance[0]}")
        embed.add_field(name="Bank:", value=f":coin: {balance[1]}")

        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def beg(self, ctx):
        earnings = random.randrange(51)
        await update_data(ctx.author, earnings)

        await ctx.send(f"Someone gave you :coin: {earnings}")

    @commands.command(aliases=["dep"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def deposit(self, ctx, amount=None):
        balance = await update_data(ctx.author)

        if amount == "max" or amount == "all":
            amount = balance[0]

        elif amount is None:
            raise commands.BadArgument

        try:
            amount = int(amount)

        except ValueError:
            raise commands.BadArgument

        if amount > balance[0]:
            await ctx.send(f"**:no_entry_sign: {ctx.author.name}**, you don't have that much money!")
            return

        elif amount < 0:
            raise commands.BadArgument

        await update_data(ctx.author, -1 * amount)
        await update_data(ctx.author, amount, "bank")

        await ctx.send(f"You deposited **:coin: {amount}**")

    commands.command(aliases=["send", "sent"])

    @commands.cooldown(1, 5, commands.BucketType.user)
    async def give(self, ctx, member: discord.Member = None, amount=None):
        if member is None or amount is None:
            raise commands.BadArgument

        try:
            amount = int(amount)

        except ValueError:
            raise commands.BadArgument

        balance = await update_data(ctx.author)

        if amount == "max" or amount == "all":
            amount = balance[0]

        if amount > balance[0]:
            await ctx.send(f"**:no_entry_sign: {ctx.author.name}**, you don't have that much money!")
            return

        elif amount < 0:
            raise commands.BadArgument

        await update_data(ctx.author, -1 * amount)
        await update_data(member, amount)

        await ctx.send(f"**{ctx.author.name}** sent **:coin: {amount}** to **{member.name}**!")

    @commands.command(aliases=["with", "withdrew"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def withdraw(self, ctx, amount=None):
        balance = await update_data(ctx.author)

        if amount == "max" or amount == "all":
            amount = balance[1]

        elif amount:
            raise commands.BadArgument

        try:
            amount = int(amount)

        except ValueError:
            raise commands.BadArgument

        if amount > balance[1]:
            await ctx.send(f"**:no_entry_sign: {ctx.author.name}**, you don't have that much money!")
            return

        elif amount < 0:
            raise commands.BadArgument

        await update_data(ctx.author, amount)
        await update_data(ctx.author, -1 * amount, "bank")

        await ctx.send(f"You withdrew **:coin: {amount}**")

    @commands.command(aliases=["job"])
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def work(self, ctx):
        earnings = random.randrange(201)
        await update_data(ctx.author, earnings)

        await ctx.send(f"Boss gave you :coin: {earnings}")


async def setup(client):
    await client.add_cog(Economy(client))
