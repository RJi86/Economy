import discord
from discord.ext import commands
import json
import os
import random

#os.chdir("C:/Users/richardji/Desktop/Economy")

client = commands.Bot(command_prefix = "e!")

mainshop = [{"name": "Watch", "price":100, "description":"Tell the time"},
            {"name": "Laptop", "price":1000, "description":"Work"}]

@client.event
async def on_ready():
    print("Ready")

@client.command()
async def balance(ctx):
    user = ctx.author
    a = await open_account(ctx.author) #Open an account for the user

    users = await get_bank_data()
    wallet_amt = users[str(user.id)]["wallet"] 
    bank_amt = users[str(user.id)]["bank"]

    em = discord.Embed(title = f"{ctx.author.name}'s balance", color = discord.Color.blue())
    em.add_field(name = "Wallet Balance", value = wallet_amt)
    em.add_field(name = "Bank Balance", value = bank_amt)

    await ctx.send(embed = em)


@client.command()
async def shop(ctx):
    em = discord.Embed(title = "Shop")

    for item in mainshop:
        name = item["name"]
        price = item["price"]
        description = item["description"]
        em.add_field(name = name, value = f"price : {price} | description: {description}")

    await ctx.send(embed = em)


@client.command()
async def beg(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()

    earnings = random.randrange(100, 1000)

    await ctx.send(f"Someone gave you {earnings} coins!!")

    users[str(user.id)]["wallet"] += earnings

    with open("mainbank.json", "w") as f:
        json.dump(users,f)
    


@client.command() #Not finished
async def buy(ctx, item, amount = 1):
    await open_account(ctx.author)

    result = await buy_this(ctx.author, item, amount)
    

async def open_account(user):

    users = await get_bank_data()

    with open("mainbank.json", "r") as f:
        users = json.load(f) #Give us data of users

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 0
        users[str(user.id)]["bank"] = 0

    with open("mainbank.json", "w") as f:
        json.dump(users,f) #Create new account if user does not already have one
    
    return True

async def get_bank_data():
    with open("mainbank.json", "r") as f:
        users = json.load(f)

    return users

async def update_bank(user, change = 0, mode = "wallet"):
    users = await get_bank_data()

    users[str(user.id)][mode] += change   

    with open("mainbank.json", "w") as f:
        json.dump(users,f)

    balance = [users[str(user.id)]["wallet"],users[str(user.id)]["bank"]]
    return balance


@client.command()
async def withdraw(ctx, amount = None):
    await open_account(ctx.author)
    if amount == None:
        await ctx.send("Please enter the amount")
        return

    balance = await update_bank(ctx.author)

    amount = int(amount)
    if amount > balance[1]:
        await ctx.send("You Don't enough money!")
        return 

    if amount < 0:
        await ctx.send("Amount must be positive")
        return


    await update_bank(ctx.author, amount)
    await update_bank(ctx.author, -1*amount, "bank")

    await ctx.send(f"You Withdrew {amount} coins!")

@client.command()
async def deposit(ctx, amount = None):
    await open_account(ctx.author)
    if amount == None:
        await ctx.send("Please enter the amount")
        return

    balance = await update_bank(ctx.author)

    amount = int(amount)
    if amount > balance[0]:
        await ctx.send("You Don't enough money!")
        return 

    if amount < 0:
        await ctx.send("Amount must be positive")
        return


    await update_bank(ctx.author, -1*amount)
    await update_bank(ctx.author, amount, "bank")

    await ctx.send(f"You Deposited {amount} coins!")


client.run("OTg4OTkxMzg4MDYwMzg1MzEw.GlwJTM.eIhDivbXNTOaP8tGd_wZJxvhMwOSm-FK7-sqFc")
