import glob
from PyCam_Implementation import PyCam_Implementation, PyCam_Implementation2
from datetime import datetime
# import pandas as pd

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
    # with open('analyzed_videos.txt') as f:
    with open('analyzed_videos2.txt') as f:
        for line in f:
            analyzed.append(line.strip())

    videos = []
    for month in MONTHS:
        for video in sorted(glob.glob("*.mp4", root_dir=f"{month}/videos/")):
            # video not in analyzed and videos.append(video)
            videos.append(video)
    
    videos = videos[::37][len(analyzed):]

    # return

    vid_length = len(videos)
    i = 0
    for video in videos:
        i += 1
        print(f"Video {i} of {vid_length}")
        print(f"{video}")

        time_start = datetime.now()

        original_area = PyCam_Implementation(video)
        time_mid = datetime.now()
        elapsed_original = time_mid - time_start
        print('Elapsed: ', elapsed_original)

        new_area = PyCam_Implementation2(video)
        time_end = datetime.now()
        elapsed_bounded = time_end - time_mid
        print('Elapsed: ', elapsed_bounded)

        # with open('analyzed_videos.txt', "a") as f:
        with open('analyzed_videos2.txt', "a") as f:
            f.write(f"{video}\n")

        print(f'original AOI area: {original_area}')
        print(f'original AOI time: {elapsed_original}')
        print(f'new AOI area: {new_area}')
        print(f'new AOI time: {elapsed_bounded}')
        print(f'original to new area ratio: {original_area/new_area}')
        print(f'original to new time ratio: {elapsed_original/elapsed_bounded}')

        with open('AOI_analysis.csv', "a") as f:
            f.write(f"{video},{original_area},{elapsed_original},{new_area},{elapsed_bounded}\n")

        print()


batch()
