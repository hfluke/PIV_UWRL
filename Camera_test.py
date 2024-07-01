import pyorc
import xarray as xr
import pandas as pd
from matplotlib import patches
import matplotlib.pyplot as plt
import glob
import os

# def clear_terminal():
#     # For Windows
#     if os.name == 'nt':
#         os.system('cls')
#     # For macOS and Linux
#     else:
#         os.system('clear')

months = ['January', 'February', 'March', 'April', 'May', 'June']
videos = []
for month in months:
    for video in sorted(glob.glob("*.mp4", root_dir=f"{month}/")):
        videos.append(
            {
                'video': f'{month}/{video}',
                'name': video.split('.')[0]
            }
        )

i = 0
l = len(videos)
for v in videos:

    os.system('clear')
    i += 1; print(f'video {i} of {l}. {i/l:.2%} complete') 

    video_file = v['video']
    video_name = v['name']
    video = pyorc.api.video.Video(video_file, start_frame=0, end_frame=125)
    frame = video.get_frame(0, method="rgb")

    # plt.imshow(frame)
    # # plt.savefig(f"Camera_test/Building/{video_name}_building.png", bbox_inches="tight", dpi=600)
    # plt.savefig(f"Camera_test/test.png", bbox_inches="tight", dpi=600)
    # plt.clf()

    gcps = dict(
        src=[
            [2434, 1397], #Blue
            [2304, 1001], #Green
            [525, 879],   #Orange
            [77, 1779]    #Purple
        ]
    )

    plt.plot(1613, 40, "o", color="#FF0000", markersize=1)
    plt.imshow(frame)
    plt.plot(*zip(*gcps["src"]), "o", color="#FF0000", markersize=3, markeredgewidth=0.4, markeredgecolor="#FFFFFF") # , label="Control points")
    # plt.legend()
    plt.savefig(f"Camera_test/Control/{video_name}_control.png", bbox_inches="tight", dpi=600)
    # plt.savefig(f"Camera_test/test.png", bbox_inches="tight", dpi=600)
    plt.clf()

    # gcps["dst"] = [
    #     [13.633,6.171],  # Blue
    #     [15.307,9.675],   # Green
    #     [3.412,15.957],  # Orage
    #     [5.747,4.855]    # Purple    
    # ]

    # gcps["z_0"] = 0.00

    # height, width = frame.shape[0:2]

    # cam_config = pyorc.CameraConfig(height=height, width=width, gcps=gcps)

    # corners = [
    #     [2559, 1919],
    #     [1752, 680],
    #     [940, 680],
    #     [200, 1919]
    # ]
    # cam_config.set_bbox_from_corners(corners)
    # cam_config.resolution = 0.01
    # cam_config.window_size = 25

    # plt.imshow(frame)
    # plt.plot(*zip(*gcps["src"]), "rx", markersize=20, label="Control points")
    # plt.plot(*zip(*corners), "co", label="Corners of AOI")
    # plt.legend()
    # plt.savefig(f"Camera_test/Corners/{video_name}_corners.png", bbox_inches="tight", dpi=600)
    # plt.close()

    # ax2 = plt.axes()
    # ax2.imshow(frame)
    # cam_config.plot(ax=ax2, camera=True)
    # plt.savefig(f"Camera_test/Cam_config/{video_name}_cam_config.png", bbox_inches="tight", dpi=600)
    # plt.close()
  
    # print()
