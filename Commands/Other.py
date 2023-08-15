import contextlib
import io

import discord
from discord.ext import commands
from discord_buttons_plugin import *


class Other(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.buttons = ButtonsClient(client)

    @commands.command(aliases=["av"])
    async def avatar(self, ctx, member: discord.Member = None):
        if member == None:
            member = ctx.author

        embed = discord.Embed(color=discord.Color.red())
        embed.set_author(name=f"{member.name}'s avatar")
        embed.set_image(url=member.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    async def echo(self, ctx, *, msg=None):
        if msg is None:
            return

        await ctx.send(msg)

    @commands.command()
    async def emojify(self, ctx, *, text=None):
        emojis = []

        for x in text.lower():
            if x.isdecimal():
                num2emo = {'0': 'zero', '1': 'one', '2': 'two', '3': 'three', '4': 'four', '5': 'five', '6': 'six',
                           '7': 'seven', '8': 'eight', '9': 'nine'}
                emojis.append(f':{num2emo.get( x )}:')

            elif x.isalpha():
                emojis.append(f':regional_indicator_{x}:')

            else:
                emojis.append(x)

        await ctx.send(''.join(emojis))

    @commands.command()
    async def invite(self, ctx):
        embed = discord.Embed(
            title=f"Invite {self.client.user.name}",
            color=discord.Color.red(),
            description=f"Wanna invite {self.client.user.name}, then [click here](https://discord.com/api/oauth2/authorize?client_id={self.client.user.id}&permissions=8&scope=bot)")

        await self.buttons.send(
            embed=embed,
            channel=ctx.channel.id,
            components=[ActionRow([Button(style=ButtonType().Link, label="Invite", url=f"https://discord.com/api/oauth2/authorize?client_id={self.client.user.id}&permissions=8&scope=bot")])])

    @commands.command(aliases=["calc", "eval", "calculator"])
    async def math(self, ctx, *, equation=None):
        if equation is None:
            return

        await ctx.send(f"**{ctx.author.name}**, the answer is: **{eval( equation )}**")

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'Pong! In **{round( self.client.latency * 1000 )}**ms')

    @commands.command(aliases=["py"])
    async def python(self, ctx, *, code):
        str_obj = io.StringIO()

        try:
            with contextlib.redirect_stdout(str_obj):
                exec(code)

        except Exception as e:
            return await ctx.send(f"```{e.__class__.__name__}: {e}```")

        await ctx.send(f"""{ctx.author.mention}\n```\n{str_obj.getvalue()}\n```""")

    @commands.command(aliases=["guildlink"])
    async def server(self, ctx):
        url = "https://discord.gg/YWXNzxJAxz"
        await ctx.send(f"Here's an invite for BrehServer's support guild: {url}")


async def setup(client):
    await client.add_cog(Other(client))
