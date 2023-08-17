import sqlite3
import discord

databaseFile = "data.sqlite3"

async def createDB():
    """"
    Create a new table in the database if it doesnt exist yet
    """
    connection = sqlite3.connect(databaseFile)
    cursor = connection.cursor()

    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS balance (
            userID INTEGER,
            wallet INTEGER,
            bank INTEGER
        )""")
    
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS admin (
            isAdmin BOOLEAN,
            isOwner BOOLEAN
        )""")


async def open_account(user: discord.Member):
    """
    Insert user to database if it doesnt exist yey
    """
    connection = sqlite3.connect(databaseFile)
    cursor = connection.cursor()

    cursor.execute(f"SELECT userID FROM balance WHERE userID = {user.id}")
    result = cursor.fetchone()
    exists = result is not None

    if not exists:
        cursor.execute(
            f"INSERT INTO balance (userID, wallet, bank) VALUES ({user.id}, {0}, {0})")
        connection.commit()
        connection.close()
        return True

    else:
        return False


async def get_balance(user: discord.Member):
    connection = sqlite3.connect(databaseFile)
    cursor = connection.cursor()

    cursor.execute(f"SELECT wallet, bank FROM balance WHERE userID = {user.id}")
    result = cursor.fetchone()
    balance = result

    connection.close()

    return balance


async def update_balance(user: discord.Member, change: int = 0, mode: str = "wallet"):
    connection = sqlite3.connect(databaseFile)
    cursor = connection.cursor()

    cursor.execute(f"""
        UPDATE balance
        SET {mode} = {change}
        WHERE userID = {user.id}""")

    connection.commit()
    connection.close()
