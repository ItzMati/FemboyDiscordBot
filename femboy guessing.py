import os
import discord
from discord import app_commands
from discord.ext import commands
import random as randomn
import time
import imagegetter
from pathlib import Path

TOKEN = "MTA3NzMyNTY3OTExODUyNDUwOA.GV-A9B.0WbVrVdPg4Gg4URxmOhvM10JvqFqQ8ET9Sn8kw"

intents = discord.Intents.all()

client = discord.Client(intents=intents)

bot = commands.Bot(command_prefix='!', intents=intents)

feeds = ['hot', 'top', 'rising']

IsFemboy = False

points=0

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
    

@bot.tree.command(name="send_image", description="Sends a random image/video from the ones i gave it")
async def send_image(ctx):
    await ctx.response.defer()
    d = randomn.randint(1,len(next(os.walk('images'))[1]))
    response = randomn.choice(os.listdir(Path("images/"+str(d))))
    response = Path("images/"+str(d)+"/"+response)
    await ctx.followup.send(file=discord.File(response))


@bot.tree.command(name="send_femboy", description="Sends a random picture of a femboy")
@app_commands.describe(place="The type of feed you want your image from (new, hot, top or rising)")
async def send_femboy(ctx, place : str):
    try:
        imagegetter.function(feed=place, subreddit="femboy")
        await ctx.response.defer()
        await ctx.followup.send(file=discord.File('image_name0.jpg'))
    except:
        response="Something went wrong."
        await ctx.response.send_message(response)


@bot.tree.command(name="send_reddit", description="Sends an image from a subreddit that you provide")
@app_commands.describe(place="The type of feed you want your image from (new, hot, top or rising)")
@app_commands.describe(subreddit="The subreddit you want the image to come from")
async def send_reddit(ctx, subreddit:str, place:str):
    try:
        imagegetter.function(feed=place, subreddit=subreddit)
        await ctx.response.defer()
        await ctx.followup.send(file=discord.File('image_name0.jpg'))
    except:
        response="Something went wrong."
        await ctx.response.send_message(response)


@bot.tree.command(name="help", description="Describes what each command does")
async def help(ctx):
    with open("help.txt","r") as f:
        response=f.read()
    response = "```"+response+"```"
    await ctx.response.send_message(response)


@bot.tree.command(name="guess_femboy", description="Starts the Femboy Guessing game")
async def guess_femboy(ctx):
    global IsFemboy
    try:
        h = randomn.randint(1,2)
        if h == 1:
            imagegetter.function(feed=feeds[randomn.randint(0,2)], subreddit="femboy")
            IsFemboy = True
        else:
            imagegetter.function(feed=feeds[randomn.randint(0,2)], subreddit="prettygirls")
            IsFemboy = False

        await ctx.response.defer()
        await ctx.followup.send(file=discord.File('image_name0.jpg'), view=Buttons())

    except:
        response="Something went wrong."
        await ctx.response.send_message(response)



class Buttons(discord.ui.View):
    global points
    def __init__(self):
        super().__init__(timeout=None) 

    @discord.ui.button(label="Femboy", style=discord.ButtonStyle.blurple)
    async def femboy(self, interaction: discord.Interaction, Button: discord.ui.Button):
        global points
        await interaction.response.defer()
        if IsFemboy == True:
            await interaction.followup.send("Correct")
            points+=1
        else:
            await interaction.followup.send("False")
            points-=1


        path = Path('scores/'+str(interaction.user.id)+'.txt')

        if path.is_file() == False:
            with open(path, "w") as f:
                f.write("0")

        with open(path, "r") as f:
            v = int(f.readline())


        with open(path, "w") as f:
            writing = int(v)+int(points)
            f.write(str(writing))

            points=0
            writing = 0
            v=0

        self.stop()
    
    @discord.ui.button(label="Woman", style=discord.ButtonStyle.blurple)
    async def woman(self, interaction: discord.Interaction, Button: discord.ui.Button):
        global points
        await interaction.response.defer()
        if IsFemboy == False:
            await interaction.followup.send("Correct")
            points+=1
        else:
            await interaction.followup.send("False")
            points-=1

        path = Path('scores/'+str(interaction.user.id)+'.txt')

        if path.is_file() == False:
            with open(path, "w") as f:
                f.write("0")
        
        with open(path, "r") as f:
            v = int(f.readline())


        with open(path, "w") as f:
            writing = int(v)+int(points)
            f.write(str(writing))

            points=0
            writing = 0
            v=0

        self.stop()

@bot.tree.command(name="guessing_points", description="shows the amount of points you have in the Femboy Guessing game")
async def guessing_points(interaction: discord.Interaction):
    try:
        path = Path('scores/'+str(interaction.user.id)+'.txt')
        with open(path, "r") as f:
            
            gh = (f.readlines()[0])
            await interaction.response.send_message("You have "+gh+" points!")
    except:
        await interaction.response.send_message("You havent played the guessing game yet.")

bot.run(TOKEN)






