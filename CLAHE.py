import cv2
import numpy as np
import matplotlib.pyplot as plt

def apply_clahe(frame, clahe):

    lab_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB) # Convert the image to LAB color space
    l_channel, a_channel, b_channel = cv2.split(lab_frame) # Split the LAB image into L, A, and B channels
    lab_image_clahe = cv2.merge((clahe.apply(l_channel), a_channel, b_channel)) # Merge the channels back together
    new_frame = cv2.cvtColor(lab_image_clahe, cv2.COLOR_LAB2BGR) # Convert back to BGR color space

    return new_frame


def alter_video(video, clip_lim, tile_size):

    # video in format month/videos/name.mp4
    name = video.split('/')[-1].split('.')[0]

    cap = cv2.VideoCapture(video)
    clahe = cv2.createCLAHE(clipLimit=clip_lim, tileGridSize=(tile_size, tile_size))

    # Get video properties
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    # Define the codec and create VideoWriter object
    output_video_path = f'CLAHE/videos/{name}_clahe#clip={clip_lim}#tile={tile_size}.mp4'
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # apply clahe
        new_frame = apply_clahe(frame, clahe)

        # Write the frame to the output video
        out.write(new_frame)

    # Release everything
    cap.release()
    out.release()
    cv2.destroyAllWindows()

    with open('clahe_vids.txt', 'a') as f:
        f.write(f'{output_video_path}\n')
