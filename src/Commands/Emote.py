import os
import discord
import giphy_client
import random

from discord.ext import commands


class Emote(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.api_key = os.getenv("GIPHY_KEY")
        self.limit = 10

    @commands.command()
    async def kiss(self, ctx, member: discord.Member = None):
        if member is None:
            raise commands.BadArgument

        query = "anime-kiss"
        api_response = giphy_client.DefaultApi().gifs_search_get(
            api_key=self.api_key, q=query, limit=self.limit)
        listGif = api_response.data

        embed = discord.Embed(
            title=f"{ctx.author.name} kissed {member.name}!!", color=discord.Color.red())
        embed.set_image(url=random.choice(listGif).images.downsized.url)

        await ctx.send(embed=embed)

    @commands.command()
    async def hug(self, ctx, member: discord.Member = None):
        if member is None:
            raise commands.BadArgument

        query = "anime-hug"
        api_response = giphy_client.DefaultApi().gifs_search_get(
            api_key=self.api_key, q=query, limit=self.limit)
        listGif = api_response.data

        embed = discord.Embed(
            title=f"{ctx.author.name} hugged {member.name}!!", color=discord.Color.red())
        embed.set_image(url=random.choice(listGif).images.downsized.url)

        await ctx.send(embed=embed)

    @commands.command()
    async def slap(self, ctx, member: discord.Member = None):
        if member is None:
            raise commands.BadArgument

        query = "anime-slap"
        api_response = giphy_client.DefaultApi().gifs_search_get(
            api_key=self.api_key, q=query, limit=self.limit)
        listGif = api_response.data

        embed = discord.Embed(
            title=f"{ctx.author.name} slapped {member.name}!!", color=discord.Color.red())
        embed.set_image(url=random.choice(listGif).images.downsized.url)

        await ctx.send(embed=embed)


async def setup(client):
    await client.add_cog(Emote(client))