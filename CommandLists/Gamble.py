import json
import random

import discord
from discord.ext import commands


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


class Gamble( commands.Cog ):
    def __init__(self, client):
        self.client = client

    @commands.command( aliases=["cf", "flip"] )
    @commands.cooldown( 1, 10, commands.BucketType.user )
    async def coinflip(self, ctx, amount=None, user_choice=None):
        await open_account( ctx.author )
        bal = await update_bank( ctx.author )

        if amount == "max" or amount == "all":
            amount = bal[0]

        elif amount is None:
            amount = 1

        try:
            amount = int( amount )

        except ValueError:
            raise commands.BadArgument

        if amount <= 0:
            raise commands.BadArgument

        elif amount > bal[0]:
            await ctx.send( f"**:no_entry_sign: {ctx.author.name}**, you don't have that much money!'" )
            return

        user_choice = user_choice.lower()

        if user_choice.startswith( "h" ):
            user_choice = "heads"

        elif user_choice.startswith( "t" ):
            user_choice = "tails"

        else:
            user_choice = "heads"

        bot_choice = random.randrange( 2 )

        if bot_choice == 0:
            bot_choice = "heads"

        else:
            bot_choice = "tails"

        if bot_choice == user_choice:
            desc = f"You bet :coin: {amount} on {user_choice}.\nIt was {bot_choice}. **YOU WIN**\n+ :coin: {amount * 2}"
            await update_bank( ctx.author, amount )

        else:
            desc = f"You bet :coin: {amount} on {user_choice}.\nIt was {bot_choice}. You lost all :C"
            await update_bank( ctx.author, -1 * amount )

        embed = discord.Embed( description=desc )
        embed.set_author( name="Coinflip" )

        await ctx.send( embed=embed )


async def setup(client):
    await client.add_cog( Gamble( client ) )
