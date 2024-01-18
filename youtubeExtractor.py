import youtube_dl
import os
import time
from pytube import Playlist, YouTube
from youtubesearchpython import VideosSearch
import pafy

## TODO add support for youtube playlists
## TODO add search for youtube counterpart of spotify song
## TODO copy this code to scuffed groovy discord bot


funeralThing = ["Hey good lookin-Hank Williams ", "Blue-Leann Rimes", "Lover come back-city and Colour", "Neon moon-Kacey musgraves with brooks and Dunn", "Pretty little angel eyes-Curtis lee", "Body in a box-City and Colour", "Good hearted woman- Waylon Jennings", "Can't help falling in love-Kacey musgraves", "I'm into something good-Herman's Hermits", "If Heaven ain't a lot like Dixie-hank Williams jr", "Secret love-Doris day", "Elvis-don't be cruel", "If I should go before you-city and Colour"]

begin = time.time()

def pytubeWay(url):
    ## doing it the pytube way
    video = YouTube(url)
    audio = video.streams.filter(only_audio=True).first() ## download only the video's audio, but still as a mp4 file
    output = audio.download(output_path='./output') ## set the output destination

    ## change the file extension, ooga booga style
    name, ext = os.path.splitext(output)
    ext = '.mp3'
    os.rename(output, (name + ext))

def youtubeDLway(url):
    ## doing it the youtube_dl way
    info = youtube_dl.YoutubeDL().extract_info(url = url, download=False) ## set download to True to download default quality video, no bueno quality
    filename = "{}.mp3".format(info['title'])

    print(info)

    options = {
        'format':'bestaudio/best',
        'keepvideo':False, ## set to true to use 'format' settings and get desired quality video/audio
        'outtmpl':filename
    }

    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download([info['webpage_url']])

        print("\nDownload complete: {}".format(filename))

def pafyWay(url):
    ## doing it the pafy way
    video = pafy.new(url)
    audio = video.getbestaudio()
    audio.download(filepath='./output')

def main(query):

    if not('://' in query): ## if the query is the title of the video
        # youtubesearchpython variables
        print("seaching video")
        search = VideosSearch(query, limit=1)

        url = search.result()['result'][0]['link']
        pytubeWay(url)
        
    else: ## if the query is a link
        print("using link")
        if "playlist" in query: ## if the link is a playlist
            print("playlist detected")
            playlist = Playlist(query)
            print(f"Number of videos in plalist: {len(playlist.video_urls)}")
            
            for i in range(len(playlist.video_urls)):
                url = playlist.video_urls[i]    

                pytubeWay(url)
        else:
            url = query

            pytubeWay(url)

    end = time.time()

    print("downloaded song in " + str(end - begin) + "seconds")

for i in funeralThing:
    main(i)
# query = input("what video shall I find?\n") <-- remember to change this when using the program normally


