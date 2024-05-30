import glob
from PyCam_Implementation import PyCam_Implementation

month = "February"

analyzed = []
with open('analyzed_videos.txt') as f:
    for line in f:
        analyzed.append(line.strip())

total_videos = glob.glob("*.mp4", root_dir=f"{month}/")
videos = []
for video in total_videos:
    if video not in analyzed:
        videos.append(video)

for i in range(len(videos)):
    print(f"Analyzing video {i+1} of {len(videos)+1}")
    print(f"{videos[i]}")

    PyCam_Implementation(videos[i], month)
    
    with open('analyzed_videos.txt', "a") as f:
        f.write(f"{videos[i]}\n")

    print()
    