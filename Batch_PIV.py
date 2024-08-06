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
    # with open('prep_analyzed.txt') as f:
        for line in f:
            analyzed.append(line.strip())

    videos = []
    for month in MONTHS: # MONTHS[::-1]:
        for video in sorted(glob.glob("*.mp4", root_dir=f"{month}/videos/")):
            video not in analyzed and videos.append(video)
    # for video in sorted(glob.glob("*.mp4", root_dir="CLAHE/videos/")):
        # video not in analyzed and videos.append(video)

    # preprocessing videos
    # videos = [
    #     'video_capture_2024-02-06_17-39-44.mp4',
    #     # 'video_capture_2024-03-01_13-09-44.mp4',
    #     # 'video_capture_2024-05-18_07-36-00.mp4',
    #     # 'video_capture_2024-05-19_07-20-48.mp4',
    #     # 'video_capture_2024-07-01_09-08-21.mp4',
    # ]
    # videos = []
    # with open('prep.txt') as f:
    #     for line in f:
    #         line.strip() not in analyzed and videos.append(line.strip())

    # videos = [ 
    #     # 'video_capture_2024-06-04_13-06-48.mp4'
    #     'video_capture_2024-07-17_14-30-04.mp4'
    # ]

    # videos = [
    #     'video_capture_2024-07-01_09-08-21_highpass6.mp4'
    # ]

    videos = ['video_capture_2024-06-02_13-56-10.mp4']

    # for v in videos: print(v); print()

    vid_length = len(videos)
    i = 0
    for video in videos:
        i += 1
        print(f"Video {i} of {vid_length}")
        print(f"{video}")

        # write_todo(video)
        PyCam_Implementation(video)

        with open('analyzed_videos.txt', "a") as f:
        # with open('prep_analyzed.txt', "a") as f:
            f.write(f"{video}\n")

        print()


batch()
