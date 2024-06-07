import glob
# from PyCam_Implementation import PyCam_Implementation
# from UWRL_sun import UWRL_sun
from UWRL_spacial_location import UWRL_spacial_location

def batch():

    months = ['January', 'February', 'March', 'April', 'May']

    analyzed = []
    # with open('analyzed_videos.txt') as f:
    #     for line in f:
    #         analyzed.append(line.strip())

    videos = []
    for month in months:
        for video in glob.glob("*.mp4", root_dir=f"{month}/"):
            video not in analyzed and videos.append(video)

    vid_length = len(videos)
    i = 0
    for video in videos:
        i += 1
        print(f"Analyzing video {i} of {vid_length}")
        print(f"{video}")

        # PyCam_Implementation(video)
        # UWRL_sun(video)
        UWRL_spacial_location(video)

        # with open('analyzed_videos.txt', "a") as f:
        #     f.write(f"{video}\n")

        print()

batch()
