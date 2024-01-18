# import youtube_dl
import os
from pytube import Playlist, YouTube
from youtubesearchpython import VideosSearch

## TODO add support for youtube playlists
## TODO add search for youtube counterpart of spotify song
## TODO copy this code to scuffed groovy discord bot

query = input("what video shall I find?\n")

if not('://' in query): ## if the query is the title of the video
    # youtubesearchpython variables
    print("seaching video")
    search = VideosSearch(query, limit=1)

    url = search.result()['result'][0]['link']

    ## doing it the pytube way
    video = YouTube(url)
    audio = video.streams.filter(only_audio=False).first() ## download only the video's audio, but still as a mp4 file
    output = audio.download(output_path='./output') ## set the output destination

    ## change the file extension, ooga booga style
    name, ext = os.path.splitext(output)
    ext = '.mp3'
    os.rename(output, (name + ext))

else: ## if the query is a link
    print("using link")
    if "playlist" in query: ## if the link is a playlist
        playlist = Playlist(query)
        print(f"Number of videos in plalist: {len(playlist.video_urls)}")
        
        for i in range(len(playlist.video_urls)):
            url = playlist.video_urls[i]    

            ## doing it the pytube way
            video = YouTube(url)
            audio = video.streams.filter(only_audio=False).first() ## download only the video's audio, but still as a mp4 file
            output = audio.download(output_path=f'./output') ## set the output destination
        
            ## change the file extension, ooga booga style
            name, ext = os.path.splitext(output)
            ext = '.mp3'
            os.rename(output, (name + ext))
    else:
        url = query

        ## doing it the pytube way
        video = YouTube(url)
        mp4 = video.streams.filter(progressive=True, file_extension='mp4').order_by('resolutionl').first()
        output = video.download(output_path='./') ## set the output destination
    
        ## change the file extension, ooga booga style
        # name, ext = os.path.splitext(output)
        # ext = '.mp3'
        # os.rename(output, (name + ext))



# doing it the youtube_dl way
# youtube_dl variables
# info = youtube_dl.YoutubeDL().extract_info(url = url, download=False) ## set download to True to download default quality video, no bueno quality
# filename = "{}.mp3".format(info['title'])
# 
# 
# print(info)
# 
# options = {
    # 'format':'bestaudio/best',
    # 'keepvideo':False, ## set to true to use 'format' settings and get desired quality video/audio
    # 'outtmpl':filename
# }
# 
# with youtube_dl.YoutubeDL(options) as ydl:
    # ydl.download([info['webpage_url']])
# 
    # print("\nDownload complete: {}".format(filename))