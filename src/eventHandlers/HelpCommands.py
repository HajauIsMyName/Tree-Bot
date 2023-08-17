import discord

from discord.ext import commands
from src.Commands import Economy, Emote, Gamble, Other


class HelpCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(invoke_without_command=True, aliases=["commands", "info"])
    async def help(self, ctx):
        embed = discord.Embed(
            description="""
            Here is the list of commands!
            For more info For more info on a specific command, use `breh!help {command}`
            Need more help? Come join our [guild](https://discord.gg/YWXNzxJAxz)""",
            color=discord.Color.red())

        embed.set_author(name="Commands List",
                         icon_url=ctx.author.avatar.url)

        names = ["💸 Economy", "🎰 Gamble", "🎰 Gamble", "⚙️ Other"]
        allCommands = []

        commandsList = {command.name for command in self.client.commands}
        commandsClass = [Economy.Economy,
                         Emote.Emote, Gamble.Gamble, Other.Other]

        for Class in commandsClass:
            allCommands.append([method for method in dir(
                Class) if not method.startswith("___") and method in commandsList])

        for _ in range(4):
            embed.add_field(
                name=names[_],
                value=", ".join(sorted(allCommands[_])),
                inline=False)

        await ctx.send(embed=embed)

    @help.command(aliases=["av"])
    async def avatar(self, ctx):
        embed = discord.Embed(title="Avatar Command",
                              color=discord.Color.red())
        embed.add_field(name="Aliases", value="avatar, av", inline=False)
        embed.add_field(name="Description",
                        value="Check your or someone's avatar", inline=False)
        embed.add_field(name="Syntax", value="breh!avatar @user", inline=False)

        await ctx.send(embed=embed)

    @help.command(aliases=["bal"])
    async def balance(self, ctx):
        embed = discord.Embed(title="Balance Command",
                              color=discord.Color.red())
        embed.add_field(name="Aliases", value="balance, bal", inline=False)
        embed.add_field(name="Description",
                        value="Check your or someone's balance", inline=False)
        embed.add_field(name="Syntax", value="breh!balance", inline=False)

        await ctx.send(embed=embed)

    @help.command()
    async def beg(self, ctx):
        embed = discord.Embed(title="Beg Command", color=discord.Color.red())
        embed.add_field(name="Aliases", value="beg", inline=False)
        embed.add_field(
            name="Description", value="This commands is used to beg for coins", inline=False)
        embed.add_field(name="Syntax", value="breh!beg", inline=False)

        await ctx.send(embed=embed)

    @help.command(aliases=["cf", "flip"])
    async def coinflip(self, ctx):
        embed = discord.Embed(title="Coinflip Command",
                              color=discord.Color.red())
        embed.add_field(
            name="Aliases", value="coinflip, flip, cf", inline=False)
        embed.add_field(name="Description",
                        value="Flip a coin to earn some coins", inline=False)
        embed.add_field(
            name="Syntax", value="breh!coinflip <amount> <heads | tails>", inline=False)

        await ctx.send(embed=embed)

    @help.command()
    async def deposit(self, ctx):
        embed = discord.Embed(title="Deposit Command",
                              color=discord.Color.red())
        embed.add_field(name="Aliases", value="deposit, dep", inline=False)
        embed.add_field(
            name="Description", value="Deposit money from your wallet to the bank", inline=False)
        embed.add_field(
            name="Syntax", value="breh!deposit <amount>", inline=False)

        await ctx.send(embed=embed)

    @help.command()
    async def echo(self, ctx):
        embed = discord.Embed(title="Echo Command", color=discord.Color.red())
        embed.add_field(name="Aliases", value="echo", inline=False)
        embed.add_field(name="Description",
                        value="Repeat your message", inline=False)
        embed.add_field(
            name="Syntax", value="breh!echo <message>", inline=False)

        await ctx.send(embed=embed)

    @help.command()
    async def emojify(self, ctx):
        embed = discord.Embed(title="Emojify Command",
                              color=discord.Color.red())
        embed.add_field(name="Aliases", value="emojify", inline=False)
        embed.add_field(name="Description",
                        value="Repeat your message with emoji", inline=False)
        embed.add_field(
            name="Syntax", value="breh!emojify <message>", inline=False)

        await ctx.send(embed=embed)

    @help.command(aliases=["send"])
    async def give(self, ctx):
        embed = discord.Embed(title="Give Command", color=discord.Color.red())
        embed.add_field(name="Aliases", value="give, send", inline=False)
        embed.add_field(name="Description",
                        value="Give your money to someone", inline=False)
        embed.add_field(
            name="Syntax", value="breh!give @user <amount>", inline=False)

        await ctx.send(embed=embed)

    @help.command()
    async def hug(self, ctx):
        embed = discord.Embed(title="Hug Command", color=discord.Color.red())
        embed.add_field(name="Aliases", value="hug, kiss, slap", inline=False)
        embed.add_field(name="Description",
                        value="Express your emotions on others!", inline=False)
        embed.add_field(name="Syntax", value="breh!hug @user", inline=False)

        await ctx.send(embed=embed)

    @help.command()
    async def invite(self, ctx):
        embed = discord.Embed(title="Invite Command",
                              color=discord.Color.red())
        embed.add_field(name="Aliases", value="invite", inline=False)
        embed.add_field(
            name="Description", value="Want to invite this bot to another server? Use this command!", inline=False)
        embed.add_field(name="Syntax", value="breh!invite", inline=False)

        await ctx.send(embed=embed)

    @help.command()
    async def kiss(self, ctx):
        embed = discord.Embed(title="Kiss Command", color=discord.Color.red())
        embed.add_field(name="Aliases", value="hug, kiss, slap", inline=False)
        embed.add_field(name="Description",
                        value="Express your emotions on others!", inline=False)
        embed.add_field(name="Syntax", value="breh!kiss @user", inline=False)

        await ctx.send(embed=embed)

    @help.command()
    async def math(self, ctx):
        embed = discord.Embed(title="Math Command", color=discord.Color.red())
        embed.add_field(
            name="Aliases", value="math, calc, eval, calculator", inline=False)
        embed.add_field(
            name="Description",
            value="Let me do your math homework! More in-depth syntax can be found here: https://mathjs.org/docs/expressions/syntax.html",
            inline=False)
        embed.add_field(
            name="Syntax", value="breh!math <equation>", inline=False)

        await ctx.send(embed=embed)

    @help.command()
    async def ping(self, ctx):
        embed = discord.Embed(title="Ping Command", color=discord.Color.red())
        embed.add_field(name="Aliases", value="ping", inline=False)
        embed.add_field(name="Description",
                        value="Check bot's connection speed", inline=False)
        embed.add_field(name="Syntax", value="breh!ping", inline=False)

        await ctx.send(embed=embed)

    @help.command(aliases=["py"])
    async def python(self, ctx):
        embed = discord.Embed(title="Python Command",
                              color=discord.Color.red())
        embed.add_field(name="Aliases", value="py, python", inline=False)
        embed.add_field(name="Description",
                        value="Execute Python code", inline=False)
        embed.add_field(
            name="Syntax", value="breh!python <code>", inline=False)

        await ctx.send(embed=embed)

    @help.command(aliases=["guildlink"])
    async def server(self, ctx):
        embed = discord.Embed(title="Guildlink Command",
                              color=discord.Color.red())
        embed.add_field(name="Aliases", value="guildlink", inline=False)
        embed.add_field(
            name="Description", value="Come join our guild! You might be awarded with special gifts once in awhile",
            inline=False)
        embed.add_field(name="Syntax", value="breh!guildlink", inline=False)

        await ctx.send(embed=embed)

    @help.command()
    async def slap(self, ctx):
        embed = discord.Embed(title="Slap Command", color=discord.Color.red())
        embed.add_field(name="Aliases", value="hug, kiss, slap", inline=False)
        embed.add_field(name="Description",
                        value="Express your emotions on others!", inline=False)
        embed.add_field(name="Syntax", value="breh!slap @user", inline=False)

        await ctx.send(embed=embed)

    @help.command(aliases=["with"])
    async def withdraw(self, ctx):
        embed = discord.Embed(title="Withdraw Command",
                              color=discord.Color.red())
        embed.add_field(name="Aliases", value="withdraw, with", inline=False)
        embed.add_field(
            name="Description", value="Withdraw coins from your bank to wallet", inline=False)
        embed.add_field(name="Syntax", value="breh!slap @user", inline=False)

        await ctx.send(embed=embed)

    @help.command(aliases=["work"])
    async def job(self, ctx):
        embed = discord.Embed(title="Work Command", color=discord.Color.red())
        embed.add_field(name="Aliases", value="work, job", inline=False)
        embed.add_field(name="Description",
                        value="Work to get coins", inline=False)
        embed.add_field(name="Syntax", value="breh!work", inline=False)

        await ctx.send(embed=embed)


async def setup(client):
    await client.add_cog(HelpCommands(client))
