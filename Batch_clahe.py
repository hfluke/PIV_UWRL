from CLAHE import alter_video

def batch():

    video = 'July/videos/video_capture_2024-07-01_09-08-21.mp4'

    for clip in [0.5, 0.75, 1, 2, 2.5, 3, 4, 7, 10]:
        for tile in [4, 6, 8, 12, 16, 24, 32]:
            print(f"clip: {clip}    tile: {tile}")

            alter_video(video, clip, tile)

            print()


batch()
