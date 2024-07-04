## import youtube_dl ## uses old version, didn't work for me
import eyed3
import os
import time
from pytube import Playlist, YouTube ## <-- don't use this
from youtubesearchpython import VideosSearch ## old library, probably will stop working eventually
import subprocess

## TODO add support for youtube playlists
## TODO add search for youtube counterpart of spotify song
## TODO fix playlist clause in main()
## TODO find alternative for youtubesearchpython
## BUG yt-dl kinda hangs on my desktop for no apparent reason, seems to work fine on fedora but not my pop_os install

begin = time.time()

def metadata(file, track, artist): ## this needs the artist and track, so it will only be run if there is a passed artist/track name
    pass

def pytubeWay(url): ## not really working, and gets mad at age redstricted stuff
    ## doing it the pytube way
    video = YouTube(url)
    audio = video.streams.filter(only_audio=True).first() ## download only the video's audio, but still as a mp4 file
    output = audio.download(output_path='./output') ## set the output destination

    ## change the file extension, ooga booga style
    name, ext = os.path.splitext(output)
    ext = '.mp3'
    os.rename(output, (name + ext))

def youtubeDLway(url, track=None, artist=None): ## gets less mad at age restricted stuff
    ## doing it the youtube_dl way
    if artist and track: ## if a track name and artist is passed, use it in the filename
        ## TODO get filename after install
        subprocess.run(['youtube-dl', '-o', f'./output/{track : artist}.%(ext)s', '-x', '--audio-format', 'mp3', '-f', 'bestaudio', url])
        filename = os.listdir('./output').sort(key=os.path.getctime)
        metadata(filename, track, artist)
    else: ## use title from youtube video
        subprocess.run(['youtube-dl', '-o', './output/%(title)s.%(ext)s', '-x', '-f', 'bestaudio', url]) ## yt-dl just kinda hangs at the end, but only on my desktop rig, not my laptop, try using a differnt nightly version or just google it


def main(query, track=None, artist=None):

    if not('://' in query): ## if not link, assume title, get link from title
        track, artist = query.split(" : ")
        print("seaching video")
        search = VideosSearch(query, limit=1)

        url = search.result()['result'][0]['link']

        
    else: ## if the query is a link
        print("using link")
        track = input("what is the track name? (leave blank to use default)\n")
        artist = input("who is the artist? (leave blank to use none)\n")

        ## TODO fix this to not use pytube
        ########### NOT WORKING ###############
        if "playlist" in query: ## if the link is a playlist
            print("playlist detected")
            playlist = Playlist(query)
            print(f"Number of videos in plalist: {len(playlist.video_urls)}")
            
            for i in range(len(playlist.video_urls)):
                url = playlist.video_urls[i]    

                youtubeDLway(url)
        else:
            url = query


    ## add metadata
    audio = eyed3.load()## <-- add variable when I get to that part
    audio.tag.title = track ## track should exist at this point
    if artist: ## artist might not exist, make sure it does
        audio.tag.artist = artist
    else:
        print("no artist set, moving on")
    
    audio.tag.save()

    end = time.time()


    print("downloaded song in " + str(end - begin) + "seconds")


query = input("what video shall I find?\n") ## <-- remember to change this when using the program normally
main(query)

