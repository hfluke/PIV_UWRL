import cv2


def apply_highpass(frame):

    # Split the image into its respective channels
    b_channel, g_channel, r_channel = cv2.split(frame) 

    # Apply the Sobel operator to each channel
    sobel_b_x = cv2.Sobel(b_channel, cv2.CV_64F, 1, 0, ksize=3)
    sobel_b_y = cv2.Sobel(b_channel, cv2.CV_64F, 0, 1, ksize=3)
    sobel_b = cv2.magnitude(sobel_b_x, sobel_b_y)

    sobel_g_x = cv2.Sobel(g_channel, cv2.CV_64F, 1, 0, ksize=3)
    sobel_g_y = cv2.Sobel(g_channel, cv2.CV_64F, 0, 1, ksize=3)
    sobel_g = cv2.magnitude(sobel_g_x, sobel_g_y)

    sobel_r_x = cv2.Sobel(r_channel, cv2.CV_64F, 1, 0, ksize=3)
    sobel_r_y = cv2.Sobel(r_channel, cv2.CV_64F, 0, 1, ksize=3)
    sobel_r = cv2.magnitude(sobel_r_x, sobel_r_y)

    # Convert back to an 8-bit image
    sobel_b = cv2.convertScaleAbs(sobel_b)
    sobel_g = cv2.convertScaleAbs(sobel_g)
    sobel_r = cv2.convertScaleAbs(sobel_r)

    # Merge the channels back together
    sobel_color = cv2.merge((sobel_b, sobel_g, sobel_r))

    # Blend the Sobel image with the original image
    alpha = 0.7  # Original image weight
    beta = 0.3   # Sobel edge weight
    new_frame = cv2.addWeighted(frame, alpha, sobel_color, beta, 0)

    return new_frame


def apply_highpass2(frame):

    # Convert to LAB color space
    lab_image = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
    l_channel, a_channel, b_channel = cv2.split(lab_image)

    # Apply Sobel to the Luminance channel
    sobel_l_x = cv2.Sobel(l_channel, cv2.CV_64F, 1, 0, ksize=3)
    sobel_l_y = cv2.Sobel(l_channel, cv2.CV_64F, 0, 1, ksize=3)
    sobel_l = cv2.magnitude(sobel_l_x, sobel_l_y)
    sobel_l = cv2.convertScaleAbs(sobel_l)

    # Merge back to LAB image
    enhanced_lab = cv2.merge((sobel_l, a_channel, b_channel))

    # Convert back to BGR color space
    new_frame = cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2BGR)

    return new_frame


def apply_Lap(frame):

    # Convert the image to grayscale
    gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply the Laplacian operator
    laplacian = cv2.Laplacian(gray_image, cv2.CV_64F, ksize=3)
    new_frame = cv2.convertScaleAbs(laplacian)

    return new_frame


def apply_Canny(frame):

    gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to reduce noise
    blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)

    # Apply Canny edge detector
    # Parameters: image, lower threshold, upper threshold
    edges = cv2.Canny(blurred_image, 100, 200)

    new_frame = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    return new_frame


def alter_video(video):

    # video in format month/videos/name.mp4
    name = video.split('/')[-1].split('.')[0]

    cap = cv2.VideoCapture(video)

    # Get video properties
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    # Define the codec and create VideoWriter object
    output_video_path = f'July/videos/{name}_highpass6.mp4'
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.convertScaleAbs(frame, alpha=2, beta=-150)

        # apply clahe
        new_frame = apply_Canny(frame)

        # Write the frame to the output video
        out.write(new_frame)

    # Release everything
    cap.release()
    out.release()
    cv2.destroyAllWindows()

    with open('highpass_vids.txt', 'a') as f:
        f.write(f'{output_video_path}\n')


alter_video('July/videos/video_capture_2024-07-01_09-08-21.mp4')
