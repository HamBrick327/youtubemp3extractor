# import youtube_dl
import os
from pytube import Playlist, YouTube
from youtubesearchpython import VideosSearch

## TODO add support for youtube playlists
## TODO add search for youtube counterpart of spotify song
## TODO copy this code to scuffed groovy discord bot

query = input("what video shall I find?\n")

def findlink(query): ## will return two values, the string/list of link(s) and a boolean telling whether or not the first value is referring to a playlist
    if not('://' in query): ## if the query is the title of the video
        # youtubesearchpython variables
        print("seaching video")
        search = VideosSearch(query, limit=1)

        url = search.result()['result'][0]['link']
        return url, False

    else: ## if the query is a link
        print("using link")
        if "playlist" in query: ## if the link is a playlist
            playlist = Playlist(query)
            print(f"Number of videos in plalist: {len(playlist.video_urls)}")
            
            for i in range(len(playlist.video_urls)):
                url = playlist.video_urls[i]    

                return url, True
        else:
            return query, False

url, isPlaylist = findlink(query=query)
subprocess.run(['youtube-dl', '-o', './output/%(title)s.%(ext)s', '-x', '-f', 'bestaudio', url])