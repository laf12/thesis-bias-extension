import cv2

def rgb_to_hsv(rgb_tuple, type):
    r, g, b = rgb_tuple
    r /= 255
    g /= 255
    b /= 255
    max_val = max(r, g, b)
    min_val = min(r, g, b)
    diff = max_val - min_val

    # Calculate the hue value
    if diff == 0:
        hue = 0
    elif max_val == r:
        hue = 60 * (((g - b) / diff) % 6)/2
    elif max_val == g:
        hue = 60 * (((b - r) / diff) + 2)/2
    else:
        hue = 60 * (((r - g) / diff) + 4)/2

    # Calculate the saturation value
    if type == 'lower':
        saturation = 100
        value = 100
    else:
        saturation = 255
        value = 255

    return (hue, saturation, value)

def apply_mask(frame, mask_name, data_loaded):

    """Apply the mask to the frame to obtain the red spot"""
    # convert the ROI to the HSV color space
    hsv_roi = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # hsv_roi = frame

    # if the name of the mask is 'red', use the mask of the red shades
    if mask_name == 'red':

        # threshold the ROI to isolate the red shades present in the color scale in bgr format
        mask_contours = cv2.inRange(hsv_roi, rgb_to_hsv(tuple(data_loaded['mask']['red']['lower']), 'lower'), rgb_to_hsv(tuple(data_loaded['mask']['red']['upper']), 'higher'))
        

    # if the name of the mask is 'green', use the mask of the green shades
    elif mask_name == 'green':
                
        # threshold the ROI to isolate the green shades present in the color scale
        mask_contours = cv2.inRange(hsv_roi, rgb_to_hsv(tuple(data_loaded['mask']['green']['lower']), 'lower'), rgb_to_hsv(tuple(data_loaded['mask']['green']['upper']), 'higher'))
        

    # if the name of the mask is 'blue', use the mask of the blue shades
    elif mask_name == 'blue':
            
        # threshold the ROI to isolate the blue shades present in the color scale
        mask_contours = cv2.inRange(hsv_roi, rgb_to_hsv(tuple(data_loaded['mask']['blue']['lower']), 'lower'), rgb_to_hsv(tuple(data_loaded['mask']['blue']['upper']), 'higher'))


    contours, hierarchy = cv2.findContours(mask_contours, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    big_contours = []

    for i in range(len(contours)):
        cnt = contours[i] #+ np.array([roi_x, roi_y])
        area = cv2.contourArea(cnt)
        if area > data_loaded['min_areas'][mask_name] and hierarchy[0][i][3] == -1:
            big_contours.append(cnt)

    frame_show = frame.copy()

    # draw the big contours on the original frame by accounting for the ROI offset
    if mask_name == 'red':
        cv2.drawContours(frame_show, big_contours, -1, (0, 0, 255), 2)
    elif mask_name == 'blue':
        cv2.drawContours(frame_show, big_contours, -1, (255, 0, 0), 2)
    elif mask_name == 'green':
        cv2.drawContours(frame_show, big_contours, -1, (0, 255, 0), 2)

    return big_contours, frame_show

