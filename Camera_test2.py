import pyorc
import xarray as xr
import pandas as pd
from matplotlib import patches
import matplotlib.pyplot as plt
import glob
import concurrent.futures

def process_video(v):
    video_file = v['video']
    video_name = v['name']
    video = pyorc.api.video.Video(video_file, start_frame=0, end_frame=125)
    frame = video.get_frame(0, method="rgb")

    gcps = dict(
        src=[
            [2434, 1397], # Blue
            [2304, 1001], # Green
            [525, 879],   # Orange
            [77, 1779]    # Purple
        ]
    )

    plt.imshow(frame)
    plt.plot(*zip(*gcps["src"]), "rx", markersize=20, label="Control points")
    plt.legend()
    plt.savefig(f"Camera_test/Control/{video_name}_control.png", bbox_inches="tight", dpi=600)
    plt.clf()

    gcps["dst"] = [
        [13.633, 6.171],  # Blue
        [15.307, 9.675],  # Green
        [3.412, 15.957],  # Orange
        [5.747, 4.855]    # Purple    
    ]

    gcps["z_0"] = 0.00

    height, width = frame.shape[0:2]

    cam_config = pyorc.CameraConfig(height=height, width=width, gcps=gcps)

    corners = [
        [2559, 1919],
        [1752, 680],
        [940, 680],
        [200, 1919]
    ]
    cam_config.set_bbox_from_corners(corners)
    cam_config.resolution = 0.01
    cam_config.window_size = 25

    plt.imshow(frame)
    plt.plot(*zip(*gcps["src"]), "rx", markersize=20, label="Control points")
    plt.plot(*zip(*corners), "co", label="Corners of AOI")
    plt.legend()
    plt.savefig(f"Camera_test/Corners/{video_name}_corners.png", bbox_inches="tight", dpi=600)
    plt.clf()

    ax2 = plt.axes()
    ax2.imshow(frame)
    cam_config.plot(ax=ax2, camera=True)
    plt.savefig(f"Camera_test/Cam_config/{video_name}_cam_config.png", bbox_inches="tight", dpi=600)
    plt.clf()

def main():
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

    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(process_video, videos))

if __name__ == "__main__":
    main()
