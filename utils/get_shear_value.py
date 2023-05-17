import cv2
import numpy as np
import ast

def calculate_distance(color1, color2):
    b1, g1, r1 = color1
    b2, g2, r2 = color2
    distance = np.linalg.norm([b1 - b2, g1 - g2, r1 - r2])
    return distance

def find_closest_color_indices(color, color_list):
    closest_color1_index = 0
    closest_color2_index = 1
    min_distance1 = calculate_distance(color, color_list[closest_color1_index])
    min_distance2 = calculate_distance(color, color_list[closest_color2_index])

    for i in range(2, len(color_list)):
        distance = calculate_distance(color, color_list[i])
        if distance < min_distance1:
            closest_color2_index = closest_color1_index
            min_distance2 = min_distance1
            closest_color1_index = i
            min_distance1 = distance
        elif distance < min_distance2:
            closest_color2_index = i
            min_distance2 = distance

    return closest_color1_index, closest_color2_index

def interpolate_color_scale(colors, shear_stress_values, color):
    # Convert the color scale to a NumPy array
    color_scale = np.array(colors)

    # normalize the color
    color = color / 255

    # if the color is darker than the darkest color in the color scale, return the corresponding shear stress value
    if np.all(color <= color_scale[-1]):
        return shear_stress_values[-1]
    # if the color is lighter than the lightest color in the color scale, return the corresponding shear stress value
    elif np.all(color >= color_scale[0]):
        return shear_stress_values[0]

    # Find the two colors closest to the given color
    distances = np.linalg.norm(color_scale - color, axis=1)
    nearest_indices = np.argsort(distances)[:2]
    nearest_colors = color_scale[nearest_indices]
    nearest_indices = find_closest_color_indices(color, color_scale)
    nearest_colors = [color_scale[nearest_indices[0]], color_scale[nearest_indices[1]]]

    # Find the corresponding shear stress values for the nearest colors
    value_lower = shear_stress_values[nearest_indices[0]]
    value_upper = shear_stress_values[nearest_indices[1]]

    # Interpolate the shear stress value for the given color
    diff = nearest_colors[1] - nearest_colors[0]
    if np.all(diff == 0):
        # If the two nearest colors are the same, return the corresponding shear stress value
        interpolated_value = value_upper
    else:
        # replace the 0s in diff with 1s to avoid division by 0
        diff[diff == 0] = 1/255
        # Otherwise, interpolate using the formula for linear interpolation
        t = np.sqrt(np.sum((color - nearest_colors[0]) ** 2) / np.sum(diff ** 2))
        interpolated_value = (1 - t) * value_upper + t * value_lower

    return interpolated_value

# def get_scale_colors(shear_scale_colors):
#     # Convert the color scale to a NumPy array
#     img = cv2.imread(shear_scale_colors)
#     # enlarge the image
#     img = cv2.resize(img, (0,0), fx=10, fy=10)
#     data = np.reshape(img, (-1,3))
#     data = np.float32(data)

#     criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
#     flags = cv2.KMEANS_RANDOM_CENTERS
#     compactness,labels,centers = cv2.kmeans(data,18,None,criteria,10,flags)

#     # if the sum of all channels is larger than 200*3 then it is white
#     colors = []
#     for center in centers:
#         if np.sum(center) < 240*3 and np.sum(center) > 100:
#             colors.append(center)

#     # sort the colors from darkest to lightest
#     # colors = sorted(colors, key=lambda x: np.sum(x))
#     colors = sort_colors_by_rainbow(colors)
#     print(colors)

#     return colors

def get_scale_colors(data_loaded):
    # Convert the color scale to a NumPy array
    colors = data_loaded["color_order"]
    colors = np.array(colors)
    colors = [ast.literal_eval(color) for color in colors]
    # to BGR
    colors = [(rgb[2]/255, rgb[1]/255, rgb[0]/255) for rgb in colors]
    return colors

def get_contour_area(contour):
    total = 0
    for cnt in contour:
        total += cv2.contourArea(cnt)
    return total

def get_average_shear(contour, colors, shear_stress_values, frame):
    # for each contour, calculate the average shear by averaging the shear values of all pixels in the contour
    total_shear = 0
    total_pixels = 0
    for cnt in contour:
        for pixel in cnt:
            # get the color of the pixel
            color = frame[pixel[0][1]][pixel[0][0]]

            # interpolate the shear stress value for the given color
            shear = interpolate_color_scale(colors, shear_stress_values, color)

            # add the shear stress value to the total shear
            total_shear += shear
            total_pixels += 1

    # return the average shear if the contour is not empty 
    if len(contour) > 0:
        # return total_shear / get_contour_area(contour)
        return total_shear / total_pixels
    else:
        return 0
    



