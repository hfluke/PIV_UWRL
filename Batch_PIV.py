import glob
# from PyCam_Implementation import PyCam_Implementation
from UWRL_sun import UWRL_sun

def batch():

    months = ['January', 'February', 'March', 'April', 'May']

    analyzed = []
<<<<<<< HEAD
    with open('analyzed_videos.txt') as f:
        for line in f:
            analyzed.append(line.strip())
    with open('hfluke.txt') as f:
        for line in f:
            analyzed.append(line.strip())
    with open('waterlab.txt') as f:
        for line in f:
            analyzed.append(line.strip())
=======
    # with open('analyzed_videos.txt') as f:
    #     for line in f:
    #         analyzed.append(line.strip())
>>>>>>> 841c8287994580e84a1f86f7347ae0d5d8af005d

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
        UWRL_sun(video)

        with open('analyzed_videos.txt', "a") as f:
            f.write(f"{video}\n")

        print()

batch()
