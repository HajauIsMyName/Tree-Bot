import json
import discord

dataFile: str = "data.json"


async def update_new_account(member: discord.Member) -> bool:
    """
    Add new user to data.json file when not in this
    """

    users = {}
    with open(dataFile, "r") as file:
        try:
            users = json.load(file)

        except FileNotFoundError:
            users = {
                str(member.id): {
                    "wallet": 0,
                    "bank": 0,
                    "isAdmin": False
                }
            }

    if str(member.id) not in users:
        users[str(member.id)] = {
            "wallet": 0,
            "bank": 0,
            "isAdmin": False,
            "inventory": {
                "pistol": {
                    "ammo": 0,
                    "own": False,
                    "equip": False,
                },
                "cross_bow": {
                    "ammo": 0,
                    "own": False,
                    "equip": False,
                },
                "sniper": {
                    "ammo": 0,
                    "own": False,
                    "equip": False,
                },
            }
        }

    with open(dataFile, "w") as file:
        json.dump(users, file)

    return True


async def get_data() -> dict:
    """
    Return data of users
    """
    with open(dataFile, "r") as file:
        users = json.load(file)

    return users


async def update_data(member: discord.Member, change: any = 0, mode: any = "wallet") -> None:
    """
    Update user with data
    """
    users = await get_data()
    users[str(member.id)][mode] = change

    with open(dataFile, "w") as file:
        json.dump(users, file)


async def update_weapon(member: discord.Member, weapon: str = None, mode: str = "own", change: any = True) -> None:
    """
    Update inventory of user
    """

    users = await get_data()
    users[str(member.id)]["inventory"][weapon][mode] = change

    with open(dataFile, "w") as file:
        json.dump(users, file)


async def get_bank(member: discord.Member) -> tuple:
    """
    Return bank data of user
    """
    users = await get_data()
    return users[str(member.id)]["wallet"], users[str(member.id)]["bank"]

async def get_inventory(member: discord.Member) -> tuple:
    users = await get_data()
    return users[str(member.id)]["inventory"]