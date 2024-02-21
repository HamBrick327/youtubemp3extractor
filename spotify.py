import spotipy
import os
from pytube import Playlist, YouTube
from youtubesearchpython import VideosSearch
from spotipy.oauth2 import SpotifyClientCredentials
import subprocess
import eyed3

spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="e1ca0e54413443109ff7eb696827389c",
                                                           client_secret="f12b6a6d37ed499fa9660a9716756971"))

playlistLink = "https://open.spotify.com/playlist/7s0hReCIRegs9Q2QrsVgC9?si=2e91b220db3643d0"



def searchYoutube(query: str, output_path: str="./output"):
    ## search for song on youtube
    
    # youtubesearchpython variables
    print("seaching video " + query)
    ## adding 'lyrics' tends to give the streaming/radio versions of the song, remove if you want
    search = VideosSearch((query + "lyrics"), limit=1)
    
    url = search.result()['result'][0]['link']
    title = search.result()['result'][0]['title']
    print("found: ", title)
    
    
    ## this library donwloads a .webm file
    video = YouTube(url)
    audio = video.streams.filter(only_audio=True).first() ## download only the video's audio, but still as a mp4 file
    output = audio.download(output_path=output_path) ## change to audio.download() when above line is being used
    
    ## change the file extension, ooga booga style
    name, ext = os.path.splitext(output)
    track, artist = query.split(" : ")
    print("converting " + name)
    try:
        ## uses python built in subprocess to use ffmpeg to convert the .webp audio file with a .mp4 extension to a .mp3
        subprocess.run(['ffmpeg', '-i', (name + '.mp4'), '-vn', '-acodec', 'libmp3lame', '-y', (name + ".mp3")])

    except:
        print("file already exists, skipping")
    ## remove the .mp4 file regardless of if the .mp3 file existed
    os.remove(f"{name}.mp4")

    ## update the metadata a little, so vlc and other things will know what's going on
    audioFile = eyed3.load((name + ".mp3"))
    audioFile.tag.title = track
    audioFile.tag.artist = artist
    audioFile.tag.save()
    
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

    ## get the playlist ID from the playlist link
    id = link.split("/")[-1].split("?")[0] ## list[-1] prints the last item of the list
    ## I learned now that you can just use the playlist link directly as the playlist_id so this is technically not needed.

    tracks = []
    
    offset = 0

    # ouput.write(str(response))

    offset = 0
    while True:
        ## only using this to get playlist name
        playlist = spotify.playlist(playlist_id=id)
        '''
        so what this does basically is force the spotify api to grab more than 100 tracks from the playlist by setting 
        the offset to whatever the length was for the `all_tracks` calling, 100 max, then gets the extra 60 off the end of 
        the playlist that wasn't grabbed by the first function call
        '''
        response = spotify.playlist_tracks(f"spotify:playlist:{id}", offset=offset) 
        tracks = response['items']
        
        # If there are no more tracks, break the loop
        if len(tracks) == 0:
            break

        # Append the tracks to the all_tracks list
        all_tracks.extend(tracks)

        ## increasing the offset to for the api call to grab the next 100 from the playlist
        offset += len(tracks)

    # You can access track information using the all_tracks list
    output = []
    for track in all_tracks:
        # print(f"Track Name: {track['track']['name']} - Artist: {track['track']['artists'][0]['name']}")
        # track = str(track['track']['name'])
        output.append(f"{track['track']['name']} : {track['track']['artists'][0]['name']}")

        # track = f"{track['track']['name']} : {track['track']['artists'][0]['name']}"
    try:
        os.mkdir(playlist['name'])
    except: 
        print("playlist filder already exists, continuing on")
    return output, playlist['name']

print(greaterThan100(playlistLink)[1])
# print(type(greaterThan100(playlistLink)))

tracks = greaterThan100(playlistLink)
playlistName = tracks[1]
for track in tracks[0]:
    searchYoutube(track, f"./{playlistName}")

# greaterThan100(playlistLink)
