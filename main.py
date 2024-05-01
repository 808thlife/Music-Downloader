from blessings import Terminal
from shazamio import Shazam, Serialize
import asyncio
import yt_dlp 
import warnings
import eyed3
from eyed3.id3.frames import ImageFrame
import requests
import urllib
import os

#temporrary
warnings.filterwarnings("ignore")

t = Terminal()

def download_audio(url):
    """
    Downloads an audio from youtube
    """
    
    ydl_opts = {
        'format': 'bestaudio/beyst',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': '%(title)s.%(ext)s',
    }
    filename = None
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        video_title = info_dict.get('title', None)
        print(video_title)
        filename = f"{video_title}.mp3"
        edit_metadata(filename)
        print(t.green+"Successfully Downloaded - check the local folder")
    return filename

async def recognize_audio(audio):
    shazam = Shazam()
    out = await shazam.recognize(audio)
    song_info = {}
    track_info = out["track"]
    song_info["title"] = track_info["title"]
    song_info["artist"] = track_info["subtitle"]
    song_info["img"] = track_info["images"]["coverart"]
    return song_info

def get_image(url):

    response = urllib.request.urlopen(url)
    imagedata = response.read()
    return imagedata

def edit_metadata(audio):
    songinfo = asyncio.run(recognize_audio(audio))
    img_data = get_image(songinfo["img"])
    

    audiofile = eyed3.load(audio)
    audiofile.tag.artist = songinfo["artist"]
    audiofile.tag.title = songinfo["title"]
    #audiofile.tag.images.set(type_=3, img_data=img_data, mime_type="images/jpeg", description=u"Cover art", img_url= u""+songinfo["img"])
    audiofile.tag.images.set(ImageFrame.FRONT_COVER, img_data, 'image/jpeg')

    #renaming the file
    #os.rename(audio, f'{songinfo["title"]}.mp3')

    audiofile.tag.save()
    return songinfo["title"]

def main():
    url = input("Paste a link from YouTube to the song you want to download: ")
    #getting filename of the download
    f = download_audio(url)
    print(f)
    title = edit_metadata(f)
    os.rename(f, title + ".mp3")

if __name__ == "__main__":
    main()