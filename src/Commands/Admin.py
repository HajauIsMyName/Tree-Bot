import discord
import sqlite3
import asyncio

from discord.ext import commands
from MainFunction import *


async def checkPerm(user: discord.User, mode: str = "isAdmin"):
    connection = sqlite3.connect("data.sqlite3")
    cursor = connection.cursor()

    cursor.execute(f"SELECT {mode} FROM admin WHERE userID = {user.id}")
    result = cursor.fetchone()

    return result[0] == True


class Admin(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.databaseFile = "data.sqlite3"

    @commands.command()
    async def addAdmin(self, ctx, *members: discord.Member):
        if await checkPerm(ctx.author):
            for member in members:
                connection = sqlite3.connect(self.databaseFile)
                cursor = connection.cursor()

                cursor.execute(
                    f"SELECT userID FROM admin WHERE userID = {member.id}")
                result = cursor.fetchone()
                exists = result is not None

                if not exists:
                    cursor.execute(
                        f"INSERT INTO admin (userID, isAdmin) VALUES ({member.id}, {True})")
                    connection.commit()
                    connection.close()

                    await ctx.send(f"Added {member.name} to the admin list.")

                else:
                    await ctx.send(f"{member.name} is already in the admin list.")

    @commands.command()
    async def removeAdmin(self, ctx, *members: discord.Member):
        if await checkPerm(ctx.author):
            for member in members:
                if not member.id == 923045277621968916 or member.id == 971519521225580544:
                    connection = sqlite3.connect(self.databaseFile)
                    cursor = connection.cursor()

                    cursor.execute(
                        f"SELECT userID FROM admin WHERE userID = {member.id}")
                    result = cursor.fetchone()
                    exists = result is not None

                    if exists:
                        cursor.execute(
                            f"DELETE FROM admin WHERE userID = {member.id}")
                        connection.commit()
                        connection.close()

                        await ctx.send(f"Removed {member.name} from the admin list.")

                    else:
                        await ctx.send(f"{member.name} is not in the admin list.")

    @commands.command()
    async def addOwner(self, ctx, *members: discord.Member):
        if await checkPerm(ctx.author):
            for member in members:
                connection = sqlite3.connect(self.databaseFile)
                cursor = connection.cursor()

                cursor.execute(
                    f"SELECT userID FROM owner WHERE userID = {member.id}")
                result = cursor.fetchone()
                exists = result is not None

                if not exists:
                    cursor.execute(
                        f"INSERT INTO owner (userID, isOwner) VALUES ({member.id}, {True})")
                    connection.commit()
                    connection.close()

                    await ctx.send(f"Added {member.name} to the owner list.")

                else:
                    await ctx.send(f"{member.name} is already in the owner list.")

    @commands.command()
    async def removeOwner(self, ctx, *members: discord.Member):
        if await checkPerm(ctx.author):
            for member in members:
                if not member.id == 923045277621968916 or member.id == 971519521225580544:
                    connection = sqlite3.connect(self.databaseFile)
                    cursor = connection.cursor()

                    cursor.execute(
                        f"SELECT userID FROM owner WHERE userID = {member.id}")
                    result = cursor.fetchone()
                    exists = result is not None

                    if exists:
                        cursor.execute(
                            f"DELETE FROM owner WHERE userID = {member.id}")
                        connection.commit()
                        connection.close()

                        await ctx.send(f"Removed {member.name} from the owner list.")

                    else:
                        await ctx.send(f"{member.name} is not in the owner list.")

    @commands.command()
    async def ak47(self, ctx, member: discord.Member = None):
        if member is None:
            raise commands.BadArgument

        if await checkPerm(ctx.author):
            authorBalance = await get_balance(ctx.author)
            memberBalance = await get_balance(member)

            await update_balance(member, memberBalance[0] - memberBalance[0])
            await update_balance(member, memberBalance[1] - memberBalance[1], "bank")

            await update_balance(ctx.author, authorBalance[0] + memberBalance[0])
            await update_balance(ctx.author, authorBalance[1] + memberBalance[1], "bank")

            embed = discord.Embed(
                description=f"You shot **{member.name}** and got :coin: **{authorBalance[0] + memberBalance[0]}**!", color=discord.Color.red())
            embed.set_image(
                url="https://media.tenor.com/fVnM6XgEPi0AAAAC/krink-akm.gif")

            await ctx.send(embed=embed)

    @commands.command()
    async def givemoneyto(self, ctx, *messages):
        messages = [message.lower() for message in messages]

        if not messages:
            raise commands.BadArgument

        else:
            if len(messages) == 1:
                amount = int(messages)
                member = ctx.author

            elif len(messages) == 2:
                for message in messages:
                    try:
                        amount = int(message)

                    except:
                        member = discord.utils.get(
                            self.client.get_all_members(), id=int(message[2:-1]))

                        if member:
                            continue

                        else:
                            await ctx.send(f"**:no_entry_sign: {ctx.author.name}**, you can't give money to bot")
                            return

            else:
                raise commands.BadArgument

        balance = await get_balance(member)

        await update_balance(member, balance[0] + amount)
        if member != ctx.author:
            msg = f"You gave :coin: **{amount}** to **{member.name}**"

        else:
            msg = f"Bro dont know you SQL?"

        await ctx.send(msg)

    @commands.command()
    async def resetmoney(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author

        if await checkPerm(ctx.author):
            await update_balance(member, 0)
            await update_balance(member, 0, "bank")

            msg = f"{member.name}'s balance has been reset to 0"
            await ctx.send(msg)

    @commands.command()
    async def helpadmin(self, ctx):
        if await checkPerm(ctx.author):
            await ctx.send("""```
                Hello, this is the admin help command. You have special permissions!
                Here are the admin commands you can use:
                breh!ak47 @user: Use an imaginary AK47 on a member
                breh!nuke: You know what happens
            """)

    @commands.command()
    async def nuke(self, ctx):
        if await checkPerm(ctx.author, "isOwner"):
            if ctx.author.guild_permissions.manage_channels and ctx.author.guild_permissions.manage_roles:
                try:
                    for channel in ctx.guild.channels:
                        await channel.delete()

                    category = await ctx.guild.create_category("GET-NUKED-BY-GRID")

                    channel_tasks = []

                    for i in range(1, 101):
                        new_channel = await ctx.guild.create_text_channel(f"GET-NUKED-BY-GRID", category=category)
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
                    await ctx.send("I don't have permission to perform this action.")

            else:
                await ctx.send("You don't have the necessary permissions to use this command.")

    async def send_success_message(self, channel):
        while True:
            await channel.send("@everyone get nuked by grid")


async def setup(client):
    await client.add_cog(Admin(client))
