import os

os.chdir("./Dance\ Frog")
directory = os.listdir("./")

for item in directory:
    if item.endswith(".mp4"):
        os.remove(f"./{item}")