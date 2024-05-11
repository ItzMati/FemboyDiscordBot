from pytube import YouTube
from pytube.cli import on_progress
import time
import random



def download(link):
    url = link

    try:
        yt = YouTube(url)
    except:
        print("wrong link")

    name = random.randint(100000,999999)

    vid = yt.streams.filter(only_audio=True).first()
    vid.download("music", str(name)+".mp3")

    return(str(vid.title), str("music/"+str(name)+".mp3"))
    
    


