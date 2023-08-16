import discord
import random

from discord.ext import commands
from MainFunction import *

shopPrice = {
    "pistol": {
        "id": 1,
        "name": "pistol",
        "price": 500,
        "ammo": 10,
        "dame": (1, 20),
        "hit_chance": 5 / 7 * 100
    },
    "cross_bow": {
        "id": 2,
        "name": "cross_bow",
        "price": 1000,
        "ammo": 5,
        "dame": (20, 100),
        "hit_chance": 3 / 6 * 100
    },
    "sniper": {
        "id": 3,
        "name": "sniper",
        "price": 2000,
        "ammo": 2,
        "dame": (100, 200),
        "hit_chance": 1 / 10 * 100
    }
}


def returnVarItem(itemID: int = 0, itemVar: str = "name"):
    """
    Return variable in item
    """

    return next((shopPrice[item][itemVar] for item in shopPrice if shopPrice[item]["id"] == itemID), None)


def isHit(hit_chance: int = 0):
    trueList = [True] * (100 - hit_chance)
    falseList = [False] * hit_chance
    isHit = trueList + falseList

    return random.choice(isHit)


class Shop(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def shop(self, ctx):
        embed = discord.Embed(title="Welcome to the Shop",
                              color=discord.Color.red())

        for _ in shopPrice:
            embed.add_field(
                name=f"{shopPrice[_]['id']}. {shopPrice[_]['name'].replace('_', ' ').title()}",
                value=f"""
                    Cost: **:coin: {shopPrice[_]['price']}**
                    Damage: **{min(shopPrice[_]['dame'])}-{max(shopPrice[_]['dame'])}**
                    Hit chance: **{int(shopPrice[_]["hit_chance"])}%**
                    Ammo: **{shopPrice[_]["ammo"]}**
    """,
                inline=False)

        await ctx.send(embed=embed)

    @commands.command()
    async def buy(self, ctx, id: int = 0):
        balance = await get_bank(ctx.author)
        inventory = await get_inventory(ctx.author)

        if id in range(1, len(shopPrice) + 1):
            if inventory[returnVarItem(id)]["own"]:
                await ctx.send(f"You already own a {returnVarItem(id).replace('_', ' ').title()}")
                return

            cost = returnVarItem(id, "price")

        else:
            raise commands.BadArgument

        if balance[0] < cost:
            await ctx.send("You don't have enough coins to buy this item.")
            return

        await update_data(ctx.author, balance[0] - cost)
        await update_weapon(ctx.author, returnVarItem(id))
        await update_weapon(ctx.author, returnVarItem(id), "ammo", returnVarItem(id, "ammo"))

        await ctx.send(f"You bought the item! Use it with `breh!equip {id}`.")

    @commands.command()
    async def buyammo(self, ctx, id: int = 0):
        balance = await update_data(ctx.author)
        inventory = await get_inventory(ctx.author)

        if id in range(1, len(shopPrice) + 1):
            cost = returnVarItem(id, "price") / 10
            ammo = returnVarItem(id, "ammo")

        else:
            raise commands.BadArgument

        if balance[0] < cost:
            await ctx.send("You don't have enough coins to buy ammo.")
            return

        await update_data(ctx.author, balance[0] - cost)
        await update_weapon(ctx.author, returnVarItem(id), "ammo", inventory[returnVarItem(id)]["ammo"] + returnVarItem(id, ammo))

        await ctx.send(f"You bought {ammo} ammo for item {id}.")

    @commands.command()
    async def equip(self, ctx, id: int = 0):
        inventory = await get_inventory(ctx.author)

        if id in range(1, len(shopPrice) + 1):
            for _ in inventory:
                if inventory[_]["own"]:
                    inventory[_]["own"] = False

        else:
            raise commands.BadArgument

        inventory[returnVarItem(id)]["own"] = True
        await ctx.send(f"You equiped **{returnVarItem(id).replace('_', ' ').title()}**")

    @commands.command()
    async def shoot(self, ctx, member: discord.Member = None):
        if member is None:
            raise commands.BadArgument

        inventory = await get_inventory(ctx.author)

        for _ in inventory:
            if inventory[_]["equip"]:
                weapon = _
                authorBalance = await get_bank(ctx.author)
                memberBalance = await get_bank(member)

                if inventory[weapon]["ammo"] < 1:
                    await ctx.send("You don't have enough ammo to shoot.")
                    return


                dame = shopPrice[weapon]["dame"]
                hit_chance = shopPrice[weapon]["hit_chance"]

                damage = max(dame) if isHit(int(hit_chance)) else random.randint(dame[0], dame[-1])
                coins_stolen = random.randint(dame[0], dame[-1]) * damage

                await update_weapon(ctx.author, weapon, "ammo", inventory[weapon]["ammo"] - 1)
                await update_data(ctx.author, authorBalance[0] + coins_stolen)
                await update_data(member, memberBalance[0] - coins_stolen)

                await ctx.send(f"You also stole **{coins_stolen}** coins.")
                return

        await ctx.send("You need to equip a weapon first. Use `breh!equip <item_number>`.")


async def setup(client):
    await client.add_cog(Shop(client))
