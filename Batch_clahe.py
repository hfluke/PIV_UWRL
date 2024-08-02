from CLAHE import alter_video, alter_video2, alter_video3
# from highpass import alter_video

def batch():

    video = 'July/videos/video_capture_2024-07-01_09-08-21.mp4'
    # video = "CLAHE/videos/video_capture_2024-07-01_09-08-21_clahe#clip=4#tile=32.mp4"

    # for clip in [0.5, 0.75, 1, 2, 2.5, 3, 4, 7, 10]:
    #     for tile in [4, 6, 8, 12, 16, 24, 32]:
    for lower in [_ for _ in range(0, 128, 16)]:
        for upper in [_ for _ in range(255, 128, -16)]:

            # print(f"clip: {clip}    tile: {tile}")
            print(f"lower: {lower}    upper: {upper}")

            alter_video3(video, lower, upper)
            # alter_video(video)

            print()


batch()
