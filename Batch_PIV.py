import glob
from PyCam_Implementation import PyCam_Implementation
import tracemalloc # for memory tracking
# import gc # garbage collector
import sys
from memory_profiler import profile

@profile
def batch():
    tracemalloc.start()

    month = "February"

    analyzed = []
    with open('analyzed_videos.txt') as f:
        for line in f:
            analyzed.append(line.strip())

    videos = []
    for video in glob.glob("*.mp4", root_dir=f"{month}/"):
        if video not in analyzed:
            videos.append(video)

    # del analyzed
    # gc.collect()

    print(tracemalloc.get_traced_memory(), '\n')

    vid_length = 2 # len(videos)
    i = 1
    for video in videos:
        print(f"Analyzing video {i} of {vid_length}")
        print(f"{video}")

        PyCam_Implementation(video, month)
        
        with open('analyzed_videos.txt', "a") as f:
            f.write(f"{video}\n")

        i += 1

        # print('\n', tracemalloc.get_traced_memory())
        # gc.collect()
        print('\n', tracemalloc.get_traced_memory(), '\n')
        
        # current_vars.append(dir())
        # print(current_vars)

        # for var in current_vars:
        #     print(f'{var}: {sys.getsizeof(var)}')

        print('\n\n')

batch()
