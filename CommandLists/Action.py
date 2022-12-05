import random

import discord
from discord.ext import commands


class Action( commands.Cog ):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def hug(self, ctx, member: discord.Member = None):
        if member == None:
            return

        embed = discord.Embed(
            title=f"{ctx.author.name} hugged {member.name}!!",
            color=discord.Color.red()
        )

        embed.set_image(
            url=random.choice( [
                "https://c.tenor.com/0T3_4tv71-kAAAAM/anime-happy.gif",
                "https://c.tenor.com/3mr1aHrTXSsAAAAC/hug-anime.gif",
                "https://c.tenor.com/8Jk1ueYnyYUAAAAM/hug.gif"
            ] )
        )

        await ctx.send( embed=embed )

    @commands.command()
    async def kiss(self, ctx, member: discord.Member = None):
        if member == None:
            return

        embed = discord.Embed(
            title=f"{ctx.author.name} kissed {member.name}!!",
            color=discord.Color.red()
        )

        embed.set_image(
            url=random.choice( [
                "https://c.tenor.com/yoMKK29AMQsAAAAM/kiss-toradora.gif",
                "https://c.tenor.com/5iiiF4A7KI0AAAAM/anime-cry-anime.gif",
                "https://c.tenor.com/I8kWjuAtX-QAAAAM/anime-ano.gif"
            ] )
        )

        await ctx.send( embed=embed )

    @commands.command()
    async def slap(self, ctx, member: discord.Member = None):

        if member == None:
            return

        embed = discord.Embed(
            title=f"{ctx.author.name} slapped {member.name}!!",
            color=discord.Color.red()
        )

        embed.set_image(
            url=random.choice( [
                "https://c.tenor.com/eU5H6GbVjrcAAAAM/slap-jjk.gif",
                "https://c.tenor.com/XiYuU9h44-AAAAAC/anime-slap-mad.gif",
                "https://c.tenor.com/Ws6Dm1ZW_vMAAAAC/girl-slap.gif"
            ] )
        )

        await ctx.send( embed=embed )


async def setup(client):
    await client.add_cog( Action( client ) )
