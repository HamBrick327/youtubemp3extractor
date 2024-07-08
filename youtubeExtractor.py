## import youtube_dl ## uses old version, didn't work for me
import eyed3
import os
import time
# from pytube import Playlist, YouTube ## <-- don't use this
from youtubesearchpython import VideosSearch ## old library, probably will stop working eventually
import subprocess

## TODO add support for youtube playlists
## TODO add search for youtube counterpart of spotify song
## TODO fix playlist clause in main()
## TODO find alternative for youtubesearchpython
## BUG yt-dl kinda hangs on my desktop for no apparent reason, seems to work fine on fedora but not my pop_os install

begin = time.time()

def metadata(file, track, artist): ## this needs the artist and track, so it will only be run if there is a passed artist/track name
    print("metadata: loading file", file)
    audio = eyed3.load(file)
    audio.tag.title = track
    audio.tag.artist = artist
    audio.tag.save()

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
    ## works now TODO get youtube to stop giving me the censored version of explicit songs. see if ChatGPT can help me search engineer that
    ## doing it the youtube_dl way
    if not os.path.isdir('./output'):
        os.mkdir("./output")
    ogDir = os.getcwd() ## kinda hacky but better than the other thing I was thinking of
    os.chdir("./output")
    if artist and track: ## if a track name and artist is passed, use it in the filename
        subprocess.run(['youtube-dl', '-o', f'./{track} : {artist}.%(ext)s', '-f', 'bestaudio', url])
        ## get newest file in the output direcotry
        outputDir = os.listdir("./")
        print("output dir", outputDir)
        newFile = os.path.abspath(max(outputDir, key=os.path.getctime))

        ## this is gross
        newFileExt = newFile.split('.')[-1]
        newFilemp3 = newFile.replace(newFileExt, 'mp3')
        print(newFilemp3)

        subprocess.run(['ffmpeg', '-i', newFile, '-vn', '-acodec', 'libmp3lame', '-y', newFilemp3])
        os.remove(newFile)

        metadata(newFilemp3, track, artist) ## under the clause there's a title and artist passed in, set the metadata, if not track and artist, no metadata
        os.chdir(ogDir)
    else: ## use title from youtube video
        subprocess.run(['youtube-dl', '-o', './output/%(title)s.%(ext)s', '--audio-format', 'mp3', '-f', 'bestaudio', url]) ## yt-dl just kinda hangs at the end, but only on my desktop rig, not my laptop, try using a differnt nightly version or just google it
        # os.system(f"youtube-dl -o ./%(title)s.%(ext)s -x --audio-format mp3 -f bestaudio {url}")


def main(query, track=None, artist=None):
    url = ''
    print('working directory: ', os.getcwd())
    if not('://' in query): ## if not link, assume title, get link from title
        try:
            track, artist = query.split(" : ")
        except:
            print("not formatted for proper metadata, skippping")
            track = query
            artist = '' ## trying to avoid an error with metadata
        print("seaching video")
        search = VideosSearch(query, limit=1)

        url = search.result()['result'][0]['link']

        
    else: ## if the query is a link
        print("using link")
        track = input("what is the track name? (leave blank to use default)\n")
        artist = input("who is the artist? (leave blank to use none)\n")

        ## TODO fix this
        ########### NOT WORKING ###############
        if "playlist" in query: ## if the link is a playlist
            print("playlist detected")
            playlist = Playlist(query)
            print(f"Number of videos in plalist: {len(playlist.video_urls)}")
            
            for i in range(len(playlist.video_urls)):
                url = playlist.video_urls[i]    
        else:
            url = query

    youtubeDLway(url, track, artist)
    end = time.time()


    print("downloaded song in " + str(end - begin) + "seconds")


query = input("what video shall I find?\n") ## <-- remember to change this when using the program normally
main(query)

