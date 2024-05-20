import os
import discord
from discord import app_commands
from discord.ext import commands
import random as randomn
import time
import imagegetter
from pathlib import Path
from datetime import timedelta
from datetime import datetime
import importlib
import requests
import json
import youtubedown

TOKEN = open(Path("apikeys/discordkey.txt"), "r").read()

intents = discord.Intents.all()

client = discord.Client(intents=intents)

bot = commands.Bot(command_prefix='!', intents=intents)

feeds = ['hot', 'top', 'rising']
IsFemboy = False
points=0
theLastTime = datetime.now()

def reset_imagegetter():
    global theLastTime
    now = datetime.now()
    if (now-theLastTime) > timedelta(hours=1):
        theLastTime = now
        importlib.reload(imagegetter)
        print("It happened frfr", now)
reset_imagegetter()

a=""    
listofalreadysentimages = []
factualstatement = True
listofalreadysentimages1 = []
factualstatement1 = True
count = 0
count1 = 0

def gen_numbers(ranger, amoun):
    global a
    a=""
    for i in range(amoun):
        a +="\n"+str(randomn.randint(0,int(ranger)))

for root_dir, cur_dir, files in os.walk(r'images/'):
    count += len(files)

for root_dir, cur_dir, files in os.walk(r'bimages/boys/'):
    count1 += len(files)


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('Femboys'))
    try:
        synced = await bot.tree.sync()
        print(f"synced {len(synced)} commands")
    except Exception as e:
        print(e)

@bot.tree.command(name="send_image", description="Sends a random image/video from the ones i gave it")
async def send_image(ctx):
    global factualstatement
    global listofalreadysentimages
    
    await ctx.response.defer()
    
    if len(listofalreadysentimages) == count:
        listofalreadysentimages = []
    
    while factualstatement == True:
        d = randomn.randint(1,len(next(os.walk('images'))[1]))
        response = randomn.choice(os.listdir(Path("images/"+str(d))))
        response = Path("images/"+str(d)+"/"+response)
        if response not in listofalreadysentimages:
            factualstatement=False
    
    await ctx.followup.send(file=discord.File(response))
    listofalreadysentimages.append(response)
    factualstatement=True

@bot.tree.command(name="send_femboy", description="Sends a random picture of a femboy")
@app_commands.describe(place="The type of feed you want your image from (new, hot, top or rising)")
async def send_femboy(ctx, place : str):
    await ctx.response.defer()
    try:
        reset_imagegetter()
        link = imagegetter.function(feed=place, subreddit="femboy")
        await ctx.followup.send(link)
    except Exception as e:
        response="Something went wrong."+str(e)
        await ctx.followup.send(response)


@bot.tree.command(name="send_reddit", description="Sends an image from a subreddit that you provide")
@app_commands.describe(place="The type of feed you want your image from (new, hot, top or rising)")
@app_commands.describe(subreddit="The subreddit you want the image to come from")
async def send_reddit(ctx, subreddit:str, place:str):
    try:
        reset_imagegetter()
        link = imagegetter.function(feed=place, subreddit=subreddit)
        await ctx.response.defer()
        await ctx.followup.send(link)
    except:
        response="Something went wrong."
        await ctx.response.send_message(response)


@bot.tree.command(name="help", description="Describes what each command does")
async def help(ctx):
    embed1 = discord.Embed(title="Femboy Bot",
                           description="These are all the commands and what they do",
                           color=discord.Color.from_rgb(66, 135, 245))
    
    with open("help.txt","r") as f:
        flines = f.readlines()

        for i in range(len(flines)):
            if "/" in flines[i]:
                embed1.add_field(name=str(flines[i]), value=str(flines[i+1]), inline=False)

    await ctx.response.send_message(embed=embed1)


@bot.tree.command(name="guess_femboy", description="Starts the Femboy Guessing game")
async def guess_femboy(ctx):
    global IsFemboy
    await ctx.response.defer()
    try:
        reset_imagegetter()
        h = randomn.randint(1,2)
        if h == 1:
            link = imagegetter.function(feed=feeds[randomn.randint(0,2)], subreddit="femboy")
            IsFemboy = True
        else:
            link = imagegetter.function(feed=feeds[randomn.randint(0,2)], subreddit="prettygirls")
            IsFemboy = False

        await ctx.followup.send(link, view=Buttons())

    except Exception as e:
        print(e)
        response="Something went wrong."
        await ctx.followup.send(response)



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

@bot.tree.command(name="guessing_points", description="Shows the amount of points you have in the Femboy Guessing game")
async def guessing_points(interaction: discord.Interaction, member: discord.Member=None):
    if member is None:
        try:
            path = Path('scores/'+str(interaction.user.id)+'.txt')
            with open(path, "r") as f:
                
                gh = (f.readlines()[0])
                await interaction.response.send_message("You have "+gh+" points!")
        except:
            await interaction.response.send_message("You havent played the guessing game yet.")

    else:
        try:
            path = Path('scores/'+str(member.id)+'.txt')
            with open(path, "r") as f:
                    
                gh = (f.readlines()[0])
                await interaction.response.send_message(str(member)+" has "+gh+" points!")
        except:
            await interaction.response.send_message("They havent played the guessing game yet.")


@bot.tree.command(name="leaderboard", description="The leaderboard for the Femboy guessing game points.")
async def leaderboard(inter: discord.Interaction):
    scores = os.listdir(Path('scores/'))
    fn = []
    userthing = []
    pointerz = []
    response = ""
    new_list = []

    await inter.response.defer()

    for i in range(len(scores)):
        with open(Path('scores/'+str(scores[i])), "r") as f:
            pointerz.append(int(f.read()))
            
        fn.append(os.path.splitext(scores[i])[0])

    for i in range(len(fn)):
        userthing.append(inter.client.get_user(int(fn[i])))

    for i in range(len(userthing)):
        new_list.append([userthing[i], pointerz[i]])

    users = new_list
    users.sort(key=lambda a: a[1], reverse=True)
    leaderboard = map(lambda user: str(user[0]) + " | " + str(user[1]) + " points", users)
    leaderboard = list(leaderboard)

    embed2 = discord.Embed(title="Femboy Guessing Game Leaderboard",
                           description="The leaderboard for the points from the Femboy Guessing game",
                           color=discord.Color.from_rgb(66, 135, 245))

    for i in range(len(leaderboard)):
        embed2.add_field(name="#"+str(i+1), value=leaderboard[i], inline=False)
    
    await inter.followup.send(embed=embed2)

@bot.tree.command(name="send_boys", description="Sends a random pic of boys")
async def send_boys(ctx):
    global factualstatement1
    global listofalreadysentimages1
    
    await ctx.response.defer()
    
    if len(listofalreadysentimages1) == count1:
        listofalreadysentimages1 = []

    while factualstatement1 == True:
        response = randomn.choice(os.listdir(Path("bimages/boys")))
        response = Path("bimages/boys/"+response)
        if response not in listofalreadysentimages1:
            factualstatement1=False
    
    await ctx.followup.send(file=discord.File(response))
    listofalreadysentimages1.append(response)
    factualstatement1=True


@bot.tree.command(name="word_leaderboard", description="A leaderboard for singular word usage")
@app_commands.describe(word="The word you want to see the leaderboard of")
async def word_leaderboard(inter: discord.Interaction, word: str):
    print("start ", datetime.now())

    members = inter.guild.members
    word_counts = {}
    fullmsgl=[]
    messagelist=[]
    await inter.response.defer()

    async for message in inter.channel.history(limit=None):
        fullmsgl.append(message)


    for message in fullmsgl:
        if word.lower() in message.content.lower():
            messagelist.append(message)

    print("after first thing", datetime.now())
    for member in members:
        word_counts[member.id] = 0
        for message in messagelist:
            if message.author == member:
                word_counts[member.id] += 1
    print("after second thing", datetime.now())

    word_counts = {member_id: count for member_id, count in word_counts.items() if count != 0}
    
    
    sorted_members = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)

    embed = discord.Embed(title=f'Leaderboard for "{word}"', color=discord.Color.blue())
    for idx, (member_id, count) in enumerate(sorted_members):
        member = inter.guild.get_member(member_id)
        if member:
            embed.add_field(name=f'{idx + 1}. {member.display_name}', value=f'Count: {count}', inline=False)
    
    await inter.followup.send(embed=embed)
    print("fin", datetime.now())

@bot.tree.command(name="top_words", description="A leaderboard for all word usage")
async def top_words(inter: discord.Interaction):
    combined_message = ""
    await inter.response.defer()
    
    async for message in inter.channel.history(limit=None):
        combined_message += message.content.lower() + " "

    counts = dict()
    words = combined_message.split()

    for word in words:
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1
            
    sortedlist = sorted(counts.items(), key=lambda x: x[1], reverse=True)[:10]

    embed = discord.Embed(title='Top 10 Most Used Words', color=discord.Color.blue())
    for idx, (word, count) in enumerate(sortedlist):
        embed.add_field(name=f'{idx + 1}. {word}', value=f'Count: {count}', inline=False)

    await inter.followup.send(embed=embed)


@bot.tree.command(name="send_astolfo", description="Sends a random image the best boy, astolfo")
async def send_astolfo(ctx):
    await ctx.response.defer()

    numba = (requests.get("https://astolfo.rocks/api/images/random?rating=safe")).json()
    
    mes = "https://astolfo.rocks/astolfo/"+str(numba["id"])+"."+str(numba["file_extension"])

    await ctx.followup.send(mes)


@bot.tree.command(name="join_voice", description="Joins a Voice call")
async def join_voice(ctx: discord.Interaction):
    global vc
    await ctx.response.defer()
    channel = ctx.user.voice.channel
    print(channel)
    vc = await channel.connect()
    await ctx.followup.send("Joined")
    
def deletingtheaudio():
    for filename in os.listdir("music"):
        os.remove("music/"+filename)
        
    
@bot.tree.command(name="play", description="Play audio from a youtube link")
@app_commands.describe(link="The Youtube link of what you want to play")
async def play(ctx, link: str):
    await ctx.response.defer()
    try:
        deletingtheaudio()
    except:
        print("hi")
    vidtitle, linkthing = youtubedown.download(link)

    audiosources = discord.FFmpegPCMAudio(executable="C:/FFmpeg/bin/ffmpeg.exe", source=linkthing)

    vc.play(discord.PCMVolumeTransformer(audiosources, volume=0.5))
    
    await ctx.followup.send("Playing "+ vidtitle)

@bot.tree.command(name="stop", description="Stops playing audio")
async def stop(ctx: discord.Interaction):
    global vc
    await ctx.response.send_message("Stopped")
    vc.stop()


@bot.tree.command(name="leave_voice", description="Leaves a Voice call")
async def leave_voice(ctx: discord.Interaction):
    global vc
    await ctx.response.send_message("Left")
    await vc.disconnect()


bot.run(TOKEN)






