from discord.ext import commands
from MainFunction import *

class Events(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Logged in as {self.client.user} (ID: {self.client.user.id})")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        
        await update_new_account(message.author)
        await update_inventory(message.author)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            cooldown = error.retry_after

            if cooldown >= 3600:
                cooldownTime = f"**{cooldown // 3600}**h **{int( (cooldown % 3600) // 60 )}**m"

            elif cooldown >= 60:
                cooldownTime = f"**{int( (cooldown % 3600) // 60 )}**m **{round( cooldown % 60, 2 )}**s"

            else:
                cooldownTime = f"**{round(error.retry_after % 60, 2)}**"

            await ctx.send(f"**:stopwatch: | {ctx.author.name}**! Please wait {cooldownTime} and try again!")

        elif isinstance(error, commands.BadArgument):
            await ctx.send(f"**:no_entry_sign: | {ctx.author.name}**, Invalid arguments! :c")

        else:
            print(error)


async def setup(client):
    await client.add_cog(Events(client))
