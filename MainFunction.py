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
            pass

    if str(member.id) not in users:
        users[str(member.id)] = {
            "wallet": 0,
            "bank": 0,
            "isAdmin": False
        }

    with open(dataFile, "w") as file:
        json.dump(users, file)

    return True


async def update_inventory(member: discord.Member) -> bool:
    """
    Add new user to inventory.json when not in this
    """

    users = {}
    with open("inventory.json", "r") as file:
        try:
            users = json.load(file)

        except FileNotFoundError:
            pass

        if str(member.id) not in users:
            weapons = ["pistol", "cross_bow", "sniper"]
            for weapon in weapons:
                users[str(member.id)][weapon] = {
                    "ammo": 0,
                    "own": False,
                    "equip": False,
                }

    with open("inventory.json", "w") as file:
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

    with open(dataFile, "w") as f:
        json.dump(users, f)


async def get_bank(member: discord.Member) -> dict:
    """
    Return bank data of user
    """
    users = await get_data()
    return users[str(member.id)]["wallet"], users[str(member.id)]["bank"]
