import json
import discord

dataFile: str = "data.json"

async def update_new_account(member: discord.Member) -> bool:
    """
    Add new user to *.json file when not in this
    """
    with open(dataFile, "r") as file:
        users = json.load(file)

        if str(member.id) in users:
            return False
        
        else:
            users[str(member.id)] = {"wallet": 0, "bank": 0, "isAdmin": False}

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

    with open(dataFile, "w") as f:
        json.dump(users, f)

async def get_bank(member: discord.Member) -> dict:
    """
    Return bank data of user
    """
    users = await get_data()
    return users[str(member.id)]["wallet"], users[str(member.id)]["bank"]