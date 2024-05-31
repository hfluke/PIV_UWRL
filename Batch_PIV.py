import glob
from PyCam_Implementation import PyCam_Implementation

def batch():

    month = "February"

    analyzed = []
    with open('analyzed_videos.txt') as f:
        for line in f:
            analyzed.append(line.strip())

    videos = []
    for video in glob.glob("*.mp4", root_dir=f"{month}/"):
        if video not in analyzed:
            videos.append(video)

    vid_length = len(videos)
    i = 0
    for video in videos:
        i += 1
        print(f"Analyzing video {i} of {vid_length}")
        print(f"{video}")

        PyCam_Implementation(video, month)
        
        with open('analyzed_videos.txt', "a") as f:
            f.write(f"{video}\n")

        print()

batch()
