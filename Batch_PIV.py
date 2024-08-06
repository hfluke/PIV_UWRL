import glob
from PyCam_Implementation import PyCam_Implementation
# from Pycam_Preprocessing import PyCam_Implementation, write_todo


MONTHS = [
    'January',
    'February',
    'March',
    'April',
    'May',
    'June',
    'July',
    # 'August',
    # 'September',
    # 'October',
    # 'November',
    # 'December'
]


def batch():

    analyzed = []
    with open('analyzed_videos.txt') as f:
        for line in f:
            analyzed.append(line.strip())

    videos = []
    for month in MONTHS:
        for video in sorted(glob.glob("*.mp4", root_dir=f"{month}/videos/")):
            video not in analyzed and videos.append(video)

    vid_length = len(videos)
    i = 0
    for video in videos:
        i += 1
        print(f"Video {i} of {vid_length}")
        print(f"{video}")

        PyCam_Implementation(video)

        with open('analyzed_videos.txt', "a") as f:
            f.write(f"{video}\n")

        print()


batch()
