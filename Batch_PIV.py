import glob
from PyCam_Implementation import PyCam_Implementation

def batch():

    # months = ['January', 'February', 'March', 'April', 'May']
    months = ['May']

    analyzed = []
    with open('analyzed_videos.txt') as f:
        for line in f:
            analyzed.append(line.strip())

    videos = []
    for month in months:
        for video in glob.glob("*.mp4", root_dir=f"{month}/"):
            video not in analyzed and videos.append(video)

    vid_length = len(videos)

    waterlab = videos[0:(vid_length//2)]
    hfluke = videos[(vid_length//2):vid_length]

    for video in waterlab:
        with open('waterlab.txt', 'a') as f:
            f.write(f'{video}\n')

    for video in hfluke:
        with open('hfluke.txt', 'a') as f:
            f.write(f'{video}\n')

    # i = 0
    # for video in videos:
    #     i += 1
    #     print(f"Analyzing video {i} of {vid_length}")
    #     print(f"{video}")

    #     PyCam_Implementation(video)
        
    #     with open('analyzed_videos.txt', "a") as f:
    #         f.write(f"{video}\n")

    #     print()

batch()
