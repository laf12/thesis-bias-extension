import cv2
import numpy as np
import pytesseract

def detect_pins(image, data_loaded):
    # ROI
    x = data_loaded['pins_roi']['x']
    y = data_loaded['pins_roi']['y']
    w = data_loaded['pins_roi']['w']
    h = data_loaded['pins_roi']['h']

    # Crop the image
    image = image[y:y+h, x:x+w]

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply adaptive thresholding
    _, thresholded = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    # Find contours of bright spots
    contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw contours on the original image
    result = image.copy()
    cv2.drawContours(result, contours, -1, (0, 255, 0), 2)


    cv2.imshow('Detected Circles', result)

    return result

def detect_clamp(image, data_loaded):
    
   # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Canny edge detection
    edges = cv2.Canny(gray, 20, 150)

    # Apply Hough Line Transform
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=70, minLineLength=150, maxLineGap=500)

    # Filter lines based on angle and length
    min_line_length = 150  # Adjust this threshold as needed
    max_line_angle = 20  # Adjust this threshold as needed
    detected_lines = []
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]

            # Calculate line length and angle
            line_length = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
            line_angle = np.arctan2(y2 - y1, x2 - x1) * 180 / np.pi

            # Filter lines based on length and angle threshold
            if line_length > min_line_length and abs(line_angle) < max_line_angle:
                detected_lines.append(line)

    # Draw detected lines on the original image
    result = image.copy()

    # get the vertical distance between each two lines
    distances = []
    min_distance = 1000
    if len(detected_lines) > 1:
        for i in range(len(detected_lines)-1):
            x1, y1, x2, y2 = detected_lines[i][0]
            x3, y3, x4, y4 = detected_lines[i+1][0]
            distance = np.abs((y1+y2)/2 - (y3+y4)/2)
            if distance > 200:
                distances.append(distance)
                if distance < min_distance:
                    min_distance = distance
                    cv2.line(result, (x1, y1), (x2, y2), (0, 0, 255), 2)
                    # draw the vertical line
                    cv2.line(result, (x3, y3), (x4, y4), (0, 0, 255), 2)

    # cv2.imshow('Detected Lines', result)
    print(min_distance/ppcm)

    return min_distance/ppcm


ppcm = 25.0



