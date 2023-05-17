import cv2
import numpy as np
import pytesseract

def clean_text(input_str):
    # Split the input string by newlines
    lines = input_str.split('\n')
    
    # Remove any empty lines
    lines = [line.strip() for line in lines if line.strip()]
    
    # Convert each line to a float and return as a list
    return [float(line) for line in lines]

def interpolate_color_scale(colors, shear_stress_values, color):
    # Convert the color scale to a NumPy array
    color_scale = np.array(colors)

    # if the color is darker than the darkest color in the color scale, return the corresponding shear stress value
    if np.all(color <= color_scale[-1]):
        return shear_stress_values[-1]
    # if the color is lighter than the lightest color in the color scale, return the corresponding shear stress value
    elif np.all(color >= color_scale[0]):
        return shear_stress_values[0]

    shear_stress_values = clean_text(shear_stress_values)

    # Find the two colors closest to the given color
    distances = np.linalg.norm(color_scale - color, axis=1)
    nearest_indices = np.argsort(distances)[:2]
    nearest_colors = color_scale[nearest_indices]

    # Find the corresponding shear stress values for the nearest colors
    value_lower = shear_stress_values[nearest_indices[0]]
    value_upper = shear_stress_values[nearest_indices[1]]

    # Interpolate the shear stress value for the given color
    diff = nearest_colors[1] - nearest_colors[0]
    if np.all(diff == 0):
        # If the two nearest colors are the same, return the corresponding shear stress value
        interpolated_value = value_upper
    else:
        # Otherwise, interpolate using the formula for linear interpolation
        t = np.linalg.norm((color - nearest_colors[0]) / diff)
        interpolated_value = (1 - t) * value_upper + t * value_lower

    return interpolated_value


# Open the input video file
input_video = cv2.VideoCapture('input.mp4')

# Get the frame rate and size of the input video
fps = int(input_video.get(cv2.CAP_PROP_FPS))
width = int(input_video.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(input_video.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Define the region of interest (ROI) where the red spot is located
roi_x = 180
roi_y = 0
roi_width = 320
roi_height = height

# Define ROI of color scale
roi_x2 = 700
roi_y2 = 0
roi_width2 = 200
roi_height2 = height

ret, frame = input_video.read()
roi_scale = frame[roi_y2:roi_y2+roi_height2, roi_x2:roi_x2+roi_width2]

# convert the ROI to the HSV color space
hsv_roi = cv2.cvtColor(roi_scale, cv2.COLOR_BGR2HSV)

# threshold the ROI to isolate the red shades present in the color scale
mask = cv2.inRange(hsv_roi, (0, 100, 100), (30, 255, 255))

# use cv2.findContours to find the contours of the red shades
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# draw the contours on a black image to create a mask of the red shades
mask_contours = np.zeros_like(mask)
cv2.drawContours(mask_contours, contours, -1, 255, cv2.FILLED)

# apply the mask to the ROI to obtain a binary image of the red shades
red_shades = cv2.bitwise_and(roi_scale, roi_scale, mask=mask_contours)

# get the bounding box of the red shades in the original frame
x_red, y_red, w_red, h_red = cv2.boundingRect(mask_contours)

# save the binary image as a reference for detecting the red spot in subsequent frames of the video
cv2.imwrite('red_shades.jpg', red_shades)

data = np.reshape(red_shades, (-1,3))
data = np.float32(data)

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
flags = cv2.KMEANS_RANDOM_CENTERS
compactness,labels,centers = cv2.kmeans(data,4,None,criteria,10,flags)

# if the sum of all channels is less than 10 then it is black
colors = []
for center in centers:
    if np.sum(center) > 10:
        colors.append(center)

# sort the colors from darkest to lightest
colors = sorted(colors, key=lambda x: np.sum(x))

# Create a video writer object to save the cropped video
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
output_video = cv2.VideoWriter('output_video.mp4', fourcc, fps/16, (width, height))

# percentage threshold
min_red_percentage = 5000

# Loop through the frames of the input video and crop each frame to the ROI
while input_video.isOpened():
    # Read the next frame from the input video
    ret, frame = input_video.read()
    if not ret:
        break

    # Crop the frame to the ROI
    cropped_frame = frame[roi_y:roi_y+roi_height, roi_x:roi_x+roi_width]

    # convert the ROI to the HSV color space
    hsv_roi = cv2.cvtColor(cropped_frame, cv2.COLOR_BGR2HSV)

    # threshold the ROI to isolate the red shades present in the color scale
    mask_contours = cv2.inRange(hsv_roi, (0, 100, 100), (30, 255, 255))

    contours, hierarchy = cv2.findContours(mask_contours, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    big_contours = []

    for i in range(len(contours)):
        cnt = contours[i]+ np.array([roi_x, roi_y])
        area = cv2.contourArea(cnt)
        if area > min_red_percentage and hierarchy[0][i][3] == -1:
            big_contours.append(cnt)

    frame_show = frame.copy()

    # draw the big contours on the original frame by accounting for the ROI offset
    cv2.drawContours(frame_show, big_contours, -1, (0, 0, 255), 2)

    # check if there are any big contours
    if len(big_contours) > 0:

        # show the scale frame in the original frame in a bounding box
        cv2.rectangle(frame, (roi_x2 + x_red, y_red - 10), (roi_x2 + x_red + w_red + 70, y_red + h_red+10), (0, 255, 0), 2)

        # crop the scale frame to the bounding box of the red shades
        cropped_scale = frame[y_red-10:y_red+h_red+10, x_red+roi_x2:x_red+w_red+roi_x2+70]

        # show the thresholded image
        # cv2.imshow('Thresholded', cropped_scale)
        
        # Perform OCR
        shear_values = pytesseract.image_to_string(cropped_scale)

        average_shear = 0
        tot = 0

        # for each pixel in the contour, print the pixel color
        for cnt in big_contours:
            for pixel in cnt:
                color = frame[pixel[0][1], pixel[0][0]]
                shear_value = interpolate_color_scale(colors, shear_values, color)
                average_shear += shear_value
                tot += 1
        average_shear /= tot
        cv2.putText(frame_show, 'Average Shear: ' + str(average_shear), (x_red, y_red), cv2.FONT_HERSHEY_TRIPLEX, 1, (255, 255, 0), 2, cv2.FONT_HERSHEY_TRIPLEX)
        cv2.imshow('Cropped Frame', frame_show)
        # record the frame
        output_video.write(frame_show)

    # Display the cropped frame
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

# Release the video capture and video writer objects
input_video.release()
output_video.release()

# Close all windows
cv2.destroyAllWindows()
