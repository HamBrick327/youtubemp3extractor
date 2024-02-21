from moviepy.editor import VideoFileClip
import eyed3
import subprocess

path = "/home/hollajam000/programming/python/youtubemp3extractor/Dance Frog/Johnny B Goode.webm"
output = "/home/hollajam000/programming/python/youtubemp3extractor/Dance Frog/Johnny B Goode.mp3"

''' no longer needed, use ffmeg instead'''
# video = VideoFileClip("/home/hollajam000/programming/python/youtubemp3extractor/Dance Frog/Johnny B Goode.mp4")
# audio = video.audio
# audio.write_audiofile("/home/hollajam000/programming/python/youtubemp3extractor/Dance Frog/Johnny B Goode.mp3")
# video.close()
# audio.close()

subprocess.run(['ffmpeg', '-i', path, '-vn', '-acodec', 'libmp3lame', '-y', output])

audio = eyed3.load(output)
audio.tag.title = "Johnny B. Goode"
audio.tag.artist = "Chuck Berry"

audio.tag.save()