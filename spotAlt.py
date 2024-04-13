## I accidentally remade the same functionality in the orignal spotify.py file but it is done in a slightly different way so I wanted to add it still
import spotipy
import os
from pytube import Playlist, YouTube
from youtubesearchpython import VideosSearch
from spotipy.oauth2 import SpotifyClientCredentials
import music_tag
import subprocess

## god I love spaghetti code

spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="e1ca0e54413443109ff7eb696827389c",
                                                           client_secret="f12b6a6d37ed499fa9660a9716756971"))
## "https://open.spotify.com/playlist/7s0hReCIRegs9Q2QrsVgC9?si=633dd92ceda94787" <-- my spotify playlist
playlistLink = input("spotify playlist link: ")
playlist_id = playlistLink.split("/")[-1].split("?")[0]

playlist_tracks = spotify.playlist_tracks(playlist_id=playlist_id, fields='items,uri,name,id,total', market='us', limit=100)

def searchYoutube(query: str, output_path: str="./output"):
    ## search for song on youtube
    
    # youtubesearchpython variables
    print("seaching video " + query)
    search = VideosSearch(query, limit=1)
    
    url = search.result()['result'][0]['link']
    title = search.result()['result'][0]['title']
    print("found: ", title)
    
    
    ## doing it the pytube way
    video = YouTube(url)
    audio = video.streams.filter(only_audio=True).first() ## download only the video's audio, but still as a mp4 file
    output = audio.download(output_path=output_path) ## set the output destination
    
    ## convert the .webm file to a .mp3 using ffmpeg
    name, ext = os.path.splitext(output)
    subprocess.run(['ffmpeg', '-i', (name + ext), '-vn', '-acodec', 'libmp3lame', '-y', (name + ".mp3")])
    print('new file created: ' + name + ".mp3")
    os.remove((name + ext))

    fileName = name + ".mp3"
    artist = query.split(" : ")[-1]
    ## file is created now
    ## add simple metadata
    mp3 = music_tag.load_file(fileName)
    mp3['artist'] = artist
    mp3['title'] = query.split(" : ")[0]
    mp3.save()
    
def spotPlaylist(link):
    ## track URL https://open.spotify.com/playlist/6yHOBv1K6lvJHbAcr61SBB?si=30169aad79f04d6a

    playlist = spotify.playlist_tracks(playlist_id="6yHOBv1K6lvJHbAcr61SBB")
    # print each track in playlist
    for i in playlist["items"]:
        track = i["track"]["name"]
        artist = i["track"]["artists"][0]["name"]
        print(track, ':', artist)


def greaterThan100(link):
    ## initialize an empty list to return later as all of the tracks from the playlist
    all_tracks = []

    tracks = []
    
    offset = 0

    # ouput.write(str(response))

    offset = 0
    while True:
        ## this is only used for getting the name of the playlist
        playlist = spotify.playlist(playlist_id=playlist_id)
        '''
        so what this does basically is force the spotify api to grab more than 100 tracks from the playlist by setting 
        the offset to whatever the length was for the `all_tracks` calling, 100 max, then gets the extra 60 off the end of 
        the playlist that wasn't grabbed by the first function call
        '''
        response = spotify.playlist_tracks(f"spotify:playlist:{playlist_id}", offset=offset) 
        tracks = response['items']
        
        # If there are no more tracks, break the loop
        if len(tracks) == 0:
            break

        # Append the tracks to the all_tracks list
        all_tracks.extend(tracks)

        # Increment the offset to retrieve the next set of tracks
        '''increasing the offset to for the api call to grab the next 100 from the playlist'''
        offset += len(tracks)

    # You can access track information using the all_tracks list
    output = []
    for track in all_tracks:
        output.append(f"{track['track']['name']} : {track['track']['artists'][0]['name']}")
    try:
        os.mkdir(playlist['name'])
    except: 
        print("playlist folder already exists, continuing on")
    return output, playlist['name']

print(greaterThan100(playlistLink)[1])
# print(type(greaterThan100(playlistLink)))

tracks = greaterThan100(playlistLink)
playlistName = tracks[1]
for track in tracks[0]:
    searchYoutube(track, f"./{playlistName}")

# greaterThan100(playlistLink)
