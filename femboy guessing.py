# imports
import os
import discord
from discord import app_commands
from discord.ext import commands
from discord.app_commands import AppCommandError
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
import csv

#discord stuff
TOKEN = open(Path("apikeys/discordkey.txt"), "r").read()

intents = discord.Intents.all()

client = discord.Client(intents=intents)

bot = commands.Bot(command_prefix='!', intents=intents)

#variables
feeds = ['hot', 'top', 'rising']
IsFemboy = False
points=0
theLastTime = datetime.now()

a=""    
listofalreadysentimages = []
factualstatement = True
listofalreadysentimages1 = []
factualstatement1 = True
count = 0
count1 = 0

for root_dir, cur_dir, files in os.walk(r'images/'):
    count += len(files)

for root_dir, cur_dir, files in os.walk(r'bimages/boys/'):
    count1 += len(files)

#functions
def reset_imagegetter():
    global theLastTime
    now = datetime.now()
    if (now-theLastTime) > timedelta(hours=1):
        theLastTime = now
        importlib.reload(imagegetter)
        print("It happened frfr", now)
reset_imagegetter()

def deletingtheaudio():
    for filename in os.listdir("music"):
        os.remove("music/"+filename)

fieldnames = ["content","author","time"]
async def download_messages(inter):
    try:
        with open((Path("messages/"+ str(inter.guild.id) +".csv")), newline="", encoding="utf-8") as f:
            pass
    except:
        with open((Path("messages/"+ str(inter.guild.id) +".csv")),"a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=",")
            writer.writeheader()
            
            async for message in inter.channel.history(limit=None):
                content = message.content
                author = message.author
                time = message.created_at
                values = [content, author, time]

                res = {fieldnames[i]: values[i] for i in range(len(fieldnames))}

                writer.writerow(res)

                values = []
    
    time_list = []
    with open((Path("messages/"+ str(inter.guild.id) +".csv")), newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            time_list.append(row["time"])
    
    datetime_list = [datetime.fromisoformat(time) for time in time_list]
    
    most_recent_time = max(datetime_list)

    async for message in inter.channel.history(limit=1):
        last_message_time = message.created_at

    if last_message_time > most_recent_time:
        with open((Path("messages/"+ str(inter.guild.id) +".csv")) ,"a", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=",")
        
            async for message in inter.channel.history(after=most_recent_time, limit=None):
                content = message.content
                author = message.author
                time = message.created_at
                values = [content, author, time]

                res = {fieldnames[i]: values[i] for i in range(len(fieldnames))}

                writer.writerow(res)

                values = []

#on ready
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('Femboys'))
    try:
        synced = await bot.tree.sync()
        print(f"synced {len(synced)} commands")
    except Exception as e:
        print(e)

#global check
@app_commands.check
def check_blacklist(ctx):
    with open("blacklist.txt", "r") as f:
        if str(ctx.user.id) in f.read():
            raise BlacklistError()
    return True

#defining errors
class BlacklistError(discord.app_commands.AppCommandError):
    pass

#error handling
@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: discord.app_commands.AppCommandError):
    if isinstance(error, BlacklistError):
        await interaction.response.send_message("wowzers, it appears you are on the blacklist")
    else:
        await interaction.response.send_message(f"An error occurred: {str(error)}")

# all the actual commands
@bot.tree.command(name="send_image", description="Sends a random image/video from the ones i gave it")
@check_blacklist
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
@check_blacklist
async def send_femboy(ctx, place : str):
    await ctx.response.defer()
    try:
        reset_imagegetter()
        link = imagegetter.function(feed=place, subreddit="femboy")
        await ctx.followup.send(link)
    except Exception as e:
        response="Something went wrong.\nError message: "+str(e)
        await ctx.followup.send(response)


@bot.tree.command(name="send_reddit", description="Sends an image from a subreddit that you provide")
@app_commands.describe(place="The type of feed you want your image from (new, hot, top or rising)")
@app_commands.describe(subreddit="The subreddit you want the image to come from")
@check_blacklist
async def send_reddit(ctx, subreddit:str, place:str):
    try:
        reset_imagegetter()
        link = imagegetter.function(feed=place, subreddit=subreddit)
        await ctx.response.defer()
        await ctx.followup.send(link)
    except Exception as e:
        response="Something went wrong.\nError message: "+str(e)
        await ctx.response.send_message(response)


@bot.tree.command(name="help", description="Describes what each command does")
@check_blacklist
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
@check_blacklist
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
        response="Something went wrong.\nError message: "+str(e)
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
@check_blacklist
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
@check_blacklist
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
@check_blacklist
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
@check_blacklist
async def word_leaderboard(inter: discord.Interaction, word: str):
    await inter.response.defer()
    await download_messages(inter)

    allmsg = {}
    authorlst =[]
    word_counts = {}
    num=0
    
    with open((Path("messages/"+ str(inter.guild.id) +".csv")), newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["author"] not in word_counts:
                word_counts[row["author"]] = 0
            
            for words in row["content"].split(" "):
                if word.lower() == words.lower():
                    word_counts[row["author"]] += 1

    word_counts = {name: count for name, count in word_counts.items() if count != 0}
    
    sorted_members = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)

    embed = discord.Embed(title=f'Leaderboard for "{word}"', color=discord.Color.blue())
    for idx, (name, count) in enumerate(sorted_members):
        member = name
        if member:
            embed.add_field(name=f'{idx + 1}. {member}', value=f'Count: {count}', inline=False)
    
    await inter.followup.send(embed=embed)

@bot.tree.command(name="phrase_leaderboard", description="A leaderboard for singular word usage")
@app_commands.describe(phrase="The phrase you want to see the leaderboard of")
@check_blacklist
async def phrase_leaderboard(inter: discord.Interaction, phrase: str):
    await inter.response.defer()
    await download_messages(inter)

    allmsg = {}
    authorlst =[]
    word_counts = {}
    num=0
    
    with open((Path("messages/"+ str(inter.guild.id) +".csv")), newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["author"] not in word_counts:
                word_counts[row["author"]] = 0
            
            if phrase.lower() in row["content"].lower():
                word_counts[row["author"]] += 1

    word_counts = {name: count for name, count in word_counts.items() if count != 0}
    
    sorted_members = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)

    embed = discord.Embed(title=f'Leaderboard for "{phrase}"', color=discord.Color.blue())
    for idx, (name, count) in enumerate(sorted_members):
        member = name
        if member:
            embed.add_field(name=f'{idx + 1}. {member}', value=f'Count: {count}', inline=False)
    
    await inter.followup.send(embed=embed)

@bot.tree.command(name="word_count_leaderboard", description="A leaderboard for singular word usage")
@check_blacklist
async def word_count_leaderboard(inter: discord.Interaction):
    await inter.response.defer()
    await download_messages(inter)

    allmsg = {}
    authorlst =[]
    word_counts = {}
    num=0
    
    with open((Path("messages/"+ str(inter.guild.id) +".csv")), newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["author"] not in word_counts:
                word_counts[row["author"]] = 0
            
            for words in row["content"].split(" "):
                word_counts[row["author"]] += 1

    word_counts = {name: count for name, count in word_counts.items() if count != 0}
    
    sorted_members = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)

    embed = discord.Embed(title=f'Leaderboard for most words said:', color=discord.Color.blue())
    for idx, (name, count) in enumerate(sorted_members):
        member = name
        if member:
            embed.add_field(name=f'{idx + 1}. {member}', value=f'Count: {count}', inline=False)
    
    await inter.followup.send(embed=embed)

@bot.tree.command(name="top_words", description="A leaderboard for all word usage")
@check_blacklist
async def top_words(inter: discord.Interaction):
    combined_message = ""
    await download_messages(inter)
    await inter.response.defer()

    with open((Path("messages/"+ str(inter.guild.id) +".csv")), newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            combined_message += row["content"].lower() + " "

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
@check_blacklist
async def send_astolfo(ctx):
    await ctx.response.defer()

    numba = (requests.get("https://astolfo.rocks/api/images/random?rating=safe")).json()
    
    mes = "https://astolfo.rocks/astolfo/"+str(numba["id"])+"."+str(numba["file_extension"])

    await ctx.followup.send(mes)

vc = {}
@bot.tree.command(name="join_voice", description="Joins a Voice call")
@check_blacklist
async def join_voice(ctx: discord.Interaction):
    global vc
    await ctx.response.defer()

    try:    
        channel = ctx.user.voice.channel
        
        vc[ctx.guild.id] = await channel.connect()
        
        await ctx.followup.send("Joined")
    except Exception as e:
        await ctx.followup.send("Something went wrong.\nError message: "+str(e))
        

@bot.tree.command(name="play", description="Play audio from a youtube link")
@app_commands.describe(link="The Youtube link of what you want to play")
@check_blacklist
async def play(ctx, link: str):
    await ctx.response.defer()

    try:
        deletingtheaudio()
    except:
        await ctx.followup.send("Could not delete the previous audio")

    try:
        vidtitle, linkthing = youtubedown.download(link)

        audiosources = discord.FFmpegPCMAudio(executable="C:/FFmpeg/bin/ffmpeg.exe", source=linkthing)

        vc[ctx.guild.id].play(discord.PCMVolumeTransformer(audiosources, volume=0.5))
        
        await ctx.followup.send("Playing "+ vidtitle)

    except Exception  as e:
        await ctx.followup.send("Wrong link \nError message:"+str(e))

@bot.tree.command(name="stop", description="Stops playing audio")
@check_blacklist
async def stop(ctx: discord.Interaction):
    await ctx.response.send_message("Stopped")
    vc[ctx.guild.id].stop()


@bot.tree.command(name="leave_voice", description="Leaves a Voice call")
@check_blacklist
async def leave_voice(ctx: discord.Interaction):
    await ctx.response.send_message("Left")
    await vc[ctx.guild.id].disconnect()


bot.run(TOKEN)






