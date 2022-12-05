import os
import sys
import discord
from discord.ext import commands
import json


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


def restart_bot():
    os.execv( sys.executable, ['python'] + sys.argv )


class Admin( commands.Cog ):
    def __init__(self, client):
        self.client = client
        self.ownerID = [899696290735210576, 923045277621968916]

    @commands.command()
    async def restart(self, ctx):
        if ctx.author.id in self.ownerID:
            await ctx.send( "Restarting bot..." )
            restart_bot()

    @commands.command()
    async def shutdown(self, ctx):
        if ctx.author.id in self.ownerID:
            await ctx.send( "Shutting down bot..." )
            print( "Bot is down" )
            exit()

    @commands.command()
    async def ak47(self, ctx, member: discord.Member = None):
        if ctx.author.id in self.ownerID:
            if member is None:
                raise commands.BadArgument

            if member.bot:
                return

            await open_account( member )

            bal = await update_bank( member )

            await ctx.send( f"You shot **{member.name}** and got :coin: **{bal[0] + bal[1]}**!" )

            await update_bank( member, -1 * bal[0], "wallet" )
            await update_bank( member, -1 * bal[1], "bank" )

            await update_bank( ctx.author, bal[0], "wallet" )
            await update_bank( ctx.author, bal[1], "bank" )

    @commands.command()
    async def givemoneyto(self, ctx, member: discord.Member = None, amount=None):
        if ctx.author.id in self.ownerID:
            if member is None or amount is None:
                raise commands.BadArgument

            try:
                amount = int(amount)

            except ValueError:
                raise commands.BadArgument

            await update_bank( member, amount )
            await ctx.send( f"You gave :coin: **{amount}** to **{member.name}**" )


async def setup(client):
    await client.add_cog( Admin( client ) )
