''' this is a proof of concept I think, idk I wrote this code a long time ago '''

# from moviepy.editor import VideoFileClip
import eyed3
import subprocess

inputFile = "/home/hambrick/youtubemp3extractor/output/freewill : rush.ogg"
output = "/home/hambrick/youtubemp3extractor/output/freewill : rush.mp3"

''' no longer needed, use ffmeg instead'''
# video = VideoFileClip("/home/hollajam000/programming/python/youtubemp3extractor/Dance Frog/Johnny B Goode.mp4")
# audio = video.audio
# audio.write_audiofile("/home/hollajam000/programming/python/youtubemp3extractor/Dance Frog/Johnny B Goode.mp3")
# video.close()
# audio.close()

## convert from whatever yt-dl downloaded (probably .webm) to .mp3 for optimal compatbility
subprocess.run(['ffmpeg', '-i', output, '-vn', '-acodec', 'libmp3lame', '-y', output])

## add metadata
audio = eyed3.load(output)
print(audio)
audio.tag.title = "Freewill"
audio.tag.artist = "Rush"

audio.tag.save()
print("did the metadata thign")