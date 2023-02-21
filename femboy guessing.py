import os
import discord
from discord import app_commands
from discord.ext import commands
import random as randomn
#try:
import imagegetter
#except:
#    null
TOKEN = "MTA3NzMyNTY3OTExODUyNDUwOA.GV-A9B.0WbVrVdPg4Gg4URxmOhvM10JvqFqQ8ET9Sn8kw"

intents = discord.Intents.all()

client = discord.Client(intents=intents)

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    try:
        synced = await bot.tree.sync()
        print(f"synced {len(synced)} commands")
    except Exception as e:
        print(e)


@bot.tree.command(name="send_number", description="Sends back the number you give")
@app_commands.describe(number="The number that the bot will repeat back to you")
async def send_number(ctx, number : int):
    response = "the number you said was "+ str(number)
    await ctx.response.send_message(response)

a=""
def gen_numbers(ranger, amoun):
    global a
    a=""
    for i in range(amoun):
        a +="\n"+str(randomn.randint(0,int(ranger)))

@bot.tree.command(name = "random", description="Sends a defined amount of random numbers")
@app_commands.describe(high="The highest number you can generate", amount="The amount of numbers that will be generated")
async def random(ctx, high : int, amount : int):
    gen_numbers(high, amount)
    response = a
    await ctx.response.send_message(response)
    

@bot.tree.command(name="send_image", description="Sends an image")
async def send_image(ctx):
    await ctx.response.send_message(file=discord.File('meme.png'))

@bot.tree.command(name="send_femboy", description="Sends a random picture of a femboy")
@app_commands.describe(place="The type of feed you want your image from (new, hot, top or rising)")
async def send_femboy(ctx, place : str):
    try:
        imagegetter.function(feed=place)
        await ctx.response.send_message(file=discord.File('image_name0.jpg'))
    except:
        response="Something went wrong."
        await ctx.response.send_message(response)
    

bot.run(TOKEN)
