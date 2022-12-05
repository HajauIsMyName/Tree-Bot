import json
import random

import discord
from discord.ext import commands


def checkDigits(string):
    for x in string:
        if not x.isdigit():
            raise commands.BadArgument

        continue


async def open_account(user):
    with open( "bank.json", "r" ) as f:
        users = json.load( f )

    if str( user.id ) in users:
        return False

    else:
        users[str( user.id )] = {}
        users[str( user.id )]["wallet"] = 0
        users[str( user.id )]["bank"] = 0

    with open( "bank.json", "w" ) as f:
        json.dump( users, f )

    return True


async def get_bank_data():
    with open( "bank.json", "r" ) as f:
        users = json.load( f )

    return users


async def update_bank(user, change=0, mode="wallet"):
    users = await get_bank_data()
    users[str( user.id )][mode] += change

    with open( "bank.json", "w" ) as f:
        json.dump( users, f )

    bal = [users[str( user.id )]["wallet"], users[str( user.id )]["bank"]]

    return bal


class Economy( commands.Cog ):
    def __init__(self, client):
        self.client = client

    @commands.command( aliases=["bal"] )
    @commands.cooldown( 1, 5, commands.BucketType.user )
    async def balance(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author

        if member.bot:
            return

        await open_account( member )

        bal = await update_bank( member )

        embed = discord.Embed( color=discord.Color.red() )
        embed.set_author( name=f"{member.name}'s balance", icon_url=member.avatar.url )

        embed.add_field( name="Wallet:", value=f":coin: {bal[0]}" )
        embed.add_field( name="Bank:", value=f":coin: {bal[1]}" )

        await ctx.send( embed=embed )

    @commands.command()
    @commands.cooldown( 1, 20, commands.BucketType.user )
    async def beg(self, ctx):
        await open_account( ctx.author )

        earnings = random.randrange( 51 )

        await update_bank( ctx.author, earnings )
        await ctx.send( f"Someone gave you :coin: {earnings}" )

    @commands.command( aliases=["dep"] )
    @commands.cooldown( 1, 5, commands.BucketType.user )
    async def deposit(self, ctx, amount=None):
        await open_account( ctx.author )
        bal = await update_bank( ctx.author )

        if amount == "max" or amount == "all":
            amount = bal[0]

        elif amount is None:
            raise commands.BadArgument

        try:
            amount = int( amount )

        except ValueError:
            raise commands.BadArgument

        if amount > bal[0]:
            await ctx.send( f"**:no_entry_sign: {ctx.author.name}**, you don't have that much money!" )
            return

        elif amount < 0:
            raise commands.BadArgument

        await update_bank( ctx.author, -1 * amount )
        await update_bank( ctx.author, amount, "bank" )

        await ctx.send( f"You deposited **:coin: {amount}**" )

    @commands.command( aliases=["send", "sent"] )
    @commands.cooldown( 1, 5, commands.BucketType.user )
    async def give(self, ctx, member: discord.Member = None, amount=None):
        if member.bot:
            return

        await open_account( ctx.author )

        bal = await update_bank( ctx.author )

        if amount == "max" or amount == "all":
            amount = bal[0]

        elif member is None or amount is None:
            raise commands.BadArgument

        try:
            amount = int( amount )


        except ValueError:
            raise commands.BadArgument

        await open_account( member )

        if amount > bal[0]:
            await ctx.send( f"**:no_entry_sign: {ctx.author.name}**, you don't have that much money!" )
            return

        elif amount < 0:
            raise commands.BadArgument

        await update_bank( ctx.author, -1 * amount )
        await update_bank( member, amount )

        await ctx.send( f"**{ctx.author.name}** sent **:coin: {amount}** to **{member.name}**!" )

    @commands.command( aliases=["with", "withdrew"] )
    @commands.cooldown( 1, 5, commands.BucketType.user )
    async def withdraw(self, ctx, amount=None):
        await open_account( ctx.author )
        bal = await update_bank( ctx.author )

        if amount == "max" or amount == "all":
            amount = bal[1]

        elif amount is None:
            raise commands.BadArgument

        try:
            amount = int( amount )


        except ValueError:
            raise commands.BadArgument

        if amount > bal[1]:
            await ctx.send( f"**:no_entry_sign: {ctx.author.name}**, you don't have that much money!" )
            return

        elif amount < 0:
            raise commands.BadArgument

        await update_bank( ctx.author, amount )
        await update_bank( ctx.author, -1 * amount, "bank" )

        await ctx.send( f"You withdrew **:coin: {amount}**" )

    @commands.command( aliases=["job"] )
    @commands.cooldown( 1, 20, commands.BucketType.user )
    async def work(self, ctx):
        await open_account( ctx.author )

        earnings = random.randrange( 201 )

        await update_bank( ctx.author, earnings )
        await ctx.send( f"Boss gave you :coin: {earnings}" )


async def setup(client):
    await client.add_cog( Economy( client ) )
