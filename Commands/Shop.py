import discord
import random

from discord.ext import commands
from MainFunction import *


class Shop(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.equipped_weapon = None
        self.cooldowns = commands.CooldownMapping.from_cooldown(
            1, 1800, commands.BucketType.user)
        self.dm_notifications = True

    async def notify_user(self, user, stolen_coins):
        try:
            await user.send(f"You have been hit! The criminal stole {stolen_coins} coins!")
        except discord.Forbidden:
            pass

    @commands.command()
    async def shop(self, ctx):
        embed = discord.Embed(title="Welcome to the Shop",
                              color=discord.Color.red())
        embed.add_field(
            name="1. Pistol",
            value="Cost: 50 coins\nDamage: 1-20\nHit Chance: 5/7\nAmmo: 10",
            inline=False)
        embed.add_field(
            name="2. Crossbow",
            value="Cost: 200 coins\nDamage: 20-100\nHit Chance: 3/6\nAmmo: 5",
            inline=False)
        embed.add_field(
            name="3. Sniper",
            value="Cost: 1000 coins\nDamage: 100-200\nHit Chance: 1/10\nAmmo: 2",
            inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    async def buy(self, ctx, item_number: int):
        user_bal = await update_data(ctx.author)

        if item_number == 1:  # pistol
            cost = 500
            damage_range = (1, 20)
            hit_chance = 5 / 7
        elif item_number == 2:  # cros sbow
            cost = 1000
            damage_range = (20, 100)
            hit_chance = 3 / 6
        elif item_number == 3:  # sniper
            cost = 5000
            damage_range = (100, 200)
            hit_chance = 1 / 10
        else:
            await ctx.send("Invalid item number.")
            return

        if user_bal[0] < cost:
            await ctx.send("You don't have enough coins to buy this item.")
            return

        await update_data(ctx.author, -cost)
        await ctx.send(
            f"You bought the item! Use it with `breh!equip {item_number}`.")

    @commands.command()
    async def buyammo(self, ctx, item_number: int):
        user_bal = await update_data(ctx.author)

        if item_number == 1:  # pistol
            cost = 10
            ammo = 10
        elif item_number == 2:  # cross bow
            cost = 50
            ammo = 5
        elif item_number == 3:  # sniper
            cost = 200
            ammo = 2
        else:
            await ctx.send("Invalid item number.")
            return

        if user_bal[0] < cost:
            await ctx.send("You don't have enough coins to buy ammo.")
            return

        await update_data(ctx.author, -cost)
        await ctx.send(f"You bought {ammo} ammo for item {item_number}.")

    @commands.command()
    async def equip(self, ctx, item_number: int):
        if item_number in [1, 2, 3]:
            self.equipped_weapon = item_number
            await ctx.send(f"You have equipped item {item_number}.")
        else:
            await ctx.send("Invalid item number. Choose an item from 1 to 3.")

    @commands.command()
    async def shoot(self, ctx, target_id: int):
        try:
            target_user = await self.client.fetch_user(target_id)
        except discord.NotFound:
            await ctx.send("User not found.")
            return
        if self.cooldowns.update_rate_limit(ctx.message):
            time_left = round(
                self.cooldowns.get_cooldown_retry_after(ctx.message), 2)
            await ctx.send(f"You need to wait {time_left} seconds before shooting again")
            return
        if self.equipped_weapon is None:
            await ctx.send(
                "You need to equip a weapon first. Use `breh!equip <item_number>`."
            )
            return

        item_number = self.equipped_weapon

        if item_number == 1:  # pistol
            damage_range = (1, 20)
            hit_chance = 5 / 7
            ammo_cost = 1
            min_steal = 1
            max_steal = 20
        elif item_number == 2:  # cross bow
            damage_range = (20, 100)
            hit_chance = 3 / 6
            ammo_cost = 20
            min_steal = 20
            max_steal = 100
        elif item_number == 3:  # sniper
            damage_range = (100, 200)
            hit_chance = 1 / 10
            ammo_cost = 100
            min_steal = 100
            max_steal = 200
        else:
            await ctx.send("Invalid item number.")
            return

        user_bal = await update_data(ctx.author)

        if user_bal[0] < ammo_cost:
            await ctx.send("You don't have enough coins to shoot.")
            return

        if random.random() <= hit_chance:
            damage = random.randint(*damage_range)
            coins_stolen = random.randint(min_steal, max_steal)
            await self.notify_user(ctx.author, coins_stolen)
            await update_data(ctx.author, -ammo_cost)
            await update_data(ctx.author, coins_stolen)
            await ctx.send(
                f"You hit your target and gained {damage} coins! You also stole {coins_stolen} coins."
            )
        else:
            await update_data(ctx.author, -ammo_cost)
            await ctx.send("You missed your target.")

    @commands.command()
    async def toggle_notifications(self, ctx):
        self.dm_notifications = not self.dm_notifications
        status = "enabled" if self.dm_notifications else "disabled"
        await ctx.send(f"Notifications have been {status}.")

    @commands.Cog.listener()
    async def on_shoot(self, user, stolen_coins):
        if not self.dm_notifications:
            return

        try:
            await user.send(f"You have been hit! The criminal stole {stolen_coins} coins!")
        except discord.Forbidden:
            pass

async def setup(client):
    await client.add_cog(Shop(client))