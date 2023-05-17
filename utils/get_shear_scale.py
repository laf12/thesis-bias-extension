import cv2
import numpy as np
import pytesseract
import yaml

def process_ocr_text(ocr_text):
    elements = []
    current_element = ""

    for char in ocr_text:
        if char == '\n':
            if current_element:
                elements.append(current_element)
            current_element = ""
        else:
            current_element += char

    if current_element:
        elements.append(current_element)

    return elements

# Function to read the YAML file
def read_yaml(file):
    with open(file, 'r') as stream:
        data_loaded = yaml.safe_load(stream)
    return data_loaded

def read_shear_scale(frame, data_loaded):

    # Get the region of interest (ROI) of the color scale
    roi_x = data_loaded['scale_roi']['x']
    roi_y = data_loaded['scale_roi']['y']
    roi_width = data_loaded['scale_roi']['w']
    roi_height = data_loaded['scale_roi']['h']

    # Crop the frame to the ROI
    frame_copy = frame[roi_y:roi_y + roi_height, roi_x:roi_x + roi_width].copy()

    gray_image = cv2.cvtColor(frame_copy, cv2.COLOR_BGR2GRAY)

    # invert the image
    gray_image = cv2.bitwise_not(gray_image)

    # find black regions in the image
    ret, thresh = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    # find contours in the image
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # show the contours on the frame with an area greater than 1000
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 100:
            # replace all pixels withing the contour with white 
            cv2.fillPoly(frame_copy, pts=[cnt], color=(255, 255, 255))


    # divide the cropped frame into 16 equal parts
    # h = (roi_height-20) // 16

    # draw the lines on the cropped frame
    # for i in range(1, 18):
    #     # perform ocr on each part of the cropped frame
    #     area = frame_copy[(i-1)*h:i*h, 0:roi_width].copy()
    #     # zoom the image
    #     area = cv2.resize(area, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    #     shear_value = pytesseract.image_to_string(area, config='--psm 6 digits -c tessedit_char_whitelist=0123456789.-')
    #     big_text.append(shear_value)


    frame_copy = cv2.resize(frame_copy, None, fx=5, fy=5, interpolation=cv2.INTER_CUBIC)
    shear_values = pytesseract.image_to_string(frame_copy, config='--psm 6 digits -c tessedit_char_whitelist=0123456789.-')
    shear_values = process_ocr_text(shear_values)

    for i in range(len(shear_values)):
        try:
            # Try converting the value to a float
            value = float(shear_values[i])
        except ValueError:
            # If conversion fails, replace the value with the average of the previous and next valid numbers
            prev_value = float(shear_values[i-1]) if i > 0 else 0.0
            next_value = float(shear_values[i+1]) if i < len(shear_values) - 1 else 0.0
            value = (prev_value + next_value) / 2.0
            
        shear_values[i] = value
    
    # print(shear_values)

    return shear_values