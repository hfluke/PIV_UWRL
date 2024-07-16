import glob
from PyCam_Implementation import PyCam_Implementation, PyCam_Implementation2, filter_explore
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
    with open('analyzed_videos.txt') as f:
        for line in f:
            analyzed.append(line.strip())

    all_videos = []
    with open('filter_explore.txt') as f:
        for line in f:
            all_videos.append(f"{line.strip()}.mp4")

    videos = []
    for month in MONTHS[::-1]:
        for video in sorted(glob.glob("*.mp4", root_dir=f"{month}/videos/")):
            video not in analyzed and video not in all_videos and videos.append(video)

    # with open('analyzed_videos.txt', "a") as f:
    #     f.write("\n\n")
    #     for video in sorted(analyzed):
    #         f.write(f"{video}\n")
    #         # print(video)
    # return


    # videos = all_videos[:]

    # videos = []
    # for video in all_videos:
    #     video not in analyzed and videos.append(video)

    # print(videos); return

    vid_length = len(videos)
    i = 0
    for video in videos:
        i += 1
        print(f"Video {i} of {vid_length}")
        print(f"{video}")

        # filter_explore(video)

        # time_start = datetime.now()

        PyCam_Implementation(video)

        # original_area = PyCam_Implementation(video)
        # time_mid = datetime.now()
        # elapsed_original = time_mid - time_start
        # print('Elapsed: ', elapsed_original)

        # new_area = PyCam_Implementation2(video)
        # time_end = datetime.now()
        # elapsed_bounded = time_end - time_mid
        # print('Elapsed: ', elapsed_bounded)

        with open('analyzed_videos.txt', "a") as f:
            f.write(f"{video}\n")

        # print(f'original AOI area: {original_area}')
        # print(f'original AOI time: {elapsed_original}')
        # print(f'new AOI area: {new_area}')
        # print(f'new AOI time: {elapsed_bounded}')
        # print(f'original to new area ratio: {original_area/new_area}')
        # print(f'original to new time ratio: {elapsed_original/elapsed_bounded}')

        # with open('AOI_analysis.csv', "a") as f:
        #     f.write(f"{video},{original_area},{elapsed_original},{new_area},{elapsed_bounded}\n")

        print()


batch()
