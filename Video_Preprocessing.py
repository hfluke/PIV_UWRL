import cv2
import numpy as np


def main():

    video = 'July/videos/video_capture_2024-07-01_09-08-21.mp4'
    name = video.split('/')[-1].split('.')[0]

    all_clahe(video, name)
    all_canny(video, name)
    all_intensity(video, name)
    apply_sobel(video, name)
    apply_scharr(video, name)
    apply_laplacian(video, name)


def alter_video(video, path_out, filter):

    print(path_out)

    cap = cv2.VideoCapture(video)

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(path_out, fourcc, fps, (frame_width, frame_height))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        out.write(filter(frame))

    cap.release()
    out.release()
    cv2.destroyAllWindows()


def all_clahe(video, name):

    for clip in [0.5, 0.75, 1, 2, 2.5, 3, 4, 7, 10]:
        for tile in [4, 6, 8, 12, 16, 24, 32]:

            path_out = f"Video_Preprocessing/test/{name}#clahe_clip={str(clip).replace('.', '_')}#clahe_tile={tile}.mp4"
            clahe = cv2.createCLAHE(clipLimit=clip, tileGridSize=(tile, tile))

            def filter(frame):
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                frame = clahe.apply(frame)
                return cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)

            alter_video(video, path_out, filter)

def all_canny(video, name):

    for lower in [_ for _ in range(0, 128, 16)]:
        for upper in [_ for _ in range(255, 128, -16)]:

            path_out = f"Video_Preprocessing/test/{name}#canny_lower={lower}#canny_upper={upper}.mp4"
            
            def filter(frame):
                return cv2.cvtColor(cv2.Canny(frame, lower, upper), cv2.COLOR_GRAY2BGR)

            alter_video(video, path_out, filter)

def all_intensity(video, name):

    for lower in [_ for _ in range(0, 128, 16)]:
        for upper in [_ for _ in range(255, 128, -16)]:

            path_out = f"Video_Preprocessing/test/{name}#intensity_lower={lower}#intensity_upper={upper}.mp4"
            
            def filter(frame):
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                frame = np.where(frame < lower, 0, np.where(frame > upper, 255, frame))
                return cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)

            alter_video(video, path_out, filter)


def apply_sobel(video, name):

    path_out = f"Video_Preprocessing/test/{name}#sobel.mp4"

    def filter(frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        sobel_x = cv2.Sobel(frame, cv2.CV_64F, 1, 0, ksize=3)
        sobel_y = cv2.Sobel(frame, cv2.CV_64F, 0, 1, ksize=3)
        frame = cv2.convertScaleAbs(cv2.magnitude(sobel_x, sobel_y))
        return cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)

    alter_video(video, path_out, filter)

    
def apply_scharr(video, name):

    path_out = f"Video_Preprocessing/test/{name}#scharr.mp4"

    def filter(frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        scharr_x = cv2.Scharr(frame, cv2.CV_64F, 1, 0)
        scharr_y = cv2.Scharr(frame, cv2.CV_64F, 0, 1)
        frame = cv2.convertScaleAbs(cv2.magnitude(scharr_x, scharr_y))
        return cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)

    alter_video(video, path_out, filter)


def apply_laplacian(video, name):

    path_out = f"Video_Preprocessing/test/{name}#laplacian.mp4"
    
    def filter(frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = cv2.Laplacian(frame, cv2.CV_64F)
        frame = cv2.convertScaleAbs(frame)
        return cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)

    alter_video(video, path_out, filter)


main()
