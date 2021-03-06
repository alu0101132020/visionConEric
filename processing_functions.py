#!/usr/bin/env python3

import webbrowser
import matplotlib.pyplot as plt
import sys
from statistics  import stdev
from PIL import Image
import sklearn
import math
from math import *

# Function that asserts that the image is grayscale.
def is_grey_scale(img):
    imgConverted = img.convert('RGB')
    w,h = imgConverted.size
    for i in range(w):
        for j in range(h):
            r,g,b = imgConverted.getpixel((i,j))
            if r != g != b: return False
    return True

def grayscale_check_and_convertion(imageFileName):
    img = Image.open(imageFileName)
    if (not is_grey_scale(img)):
        img = img.convert(mode='L')
    return img

# Function that counts for each possible value how many pixels are there, and returns the array that contains all that information.
def count_pixels_values_relative(img):
    relative_histogram = [0] * 256
    w,h = img.size
    for i in range(w):
        for j in range(h):
            relative_histogram[img.getpixel((i,j))] += 1
    return relative_histogram

# Function that counts for each possible value and all the previous one how many pixels are there, and returns the array that contains all that information.
def count_pixels_values_acumulative(img):
    relative_histogram = count_pixels_values_relative(img)
    acumulative_histogram = [0] * 256
    total = 0
    for i in range(256):
        acumulative_histogram[i] = relative_histogram[i] + total
        total = acumulative_histogram[i]
        
    return acumulative_histogram

# Function that returns a list of 256 elements that contains the cardinal of the current element.
def y_axis_setter():
    y_axis = [0] * 256

    for i in range(len(y_axis)):
        y_axis[i] = i
    
    return y_axis

def y_axis_setter_from_list(my_list):
    y_axis = [0] * len(my_list)

    for i in range(len(y_axis)):
        y_axis[i] = i
    
    return y_axis


# Function that returns a file name, extracts the extension and returns it.
def obtain_extension(imageFileName):
    return imageFileName.split('.')[1]

# Function that returns the image size, defined as the multiplication of the width and height.
def image_size(img):
    w,h = img.size
    return w * h

# Function that returns the first and the last value of the image that are used in the grayscale.
def find_min_max(relative_histogram):
    i = 0
    while (i < len(relative_histogram) and relative_histogram[i] == 0): 
        i += 1
    
    j = 255
    while (j >= 0 and relative_histogram[j] == 0): 
        j -= 1
    return [i, j]

# Function that returns the summ of all the grayscale values.
def summ_of_values(relative_histogram):
    summ = 0
    for i in range(len(relative_histogram)):
        summ += relative_histogram[i] * i
    return summ

# Function that returns the brightness of the image, defined as the division of the sum of all the pixels values by the ammount of pixeles.
def get_bright(img):
    relative_histogram = count_pixels_values_relative(img)
    total_pixels = image_size(img)
    total_values = summ_of_values(relative_histogram)
    return total_values / total_pixels

def get_contrast(img):
    relative_histogram = count_pixels_values_relative(img)
    total_pixels = image_size(img)
    mean = get_bright(img)
    summ = 0
    for i in range(len(relative_histogram)):
        summ += relative_histogram[i] * ((i - mean)**2)
    summ = sqrt(summ / total_pixels)
    return summ

def get_entropy(img):
    acc = 0.0

    accumulative_histogram = count_pixels_values_relative(img)
    accumulative_histogram_normalized = normalize_histogram(accumulative_histogram, img)

    for i in accumulative_histogram_normalized:
        if i != 0:
            log_result = log2(i)
            acc += i * log_result   
    
    entropy = acc * -1
    return entropy

def normalize_histogram(array, img):
    arrayNormalized = array.copy()
    size = image_size(img)
    for i in range(len(array)):
        arrayNormalized[i] = arrayNormalized[i] / size
    return arrayNormalized

def conversion_array(A, B):
    array = y_axis_setter()
    for i in range(len(array)):
        value = array[i] * A + B
        if value > 255:
            array[i] = 255
        elif value < 0:
            array[i] = 0
        else:
            array[i] = int(value)

    return array

def conversion(img, new_brightness, new_contrast):
    current_brightness = get_bright(img)
    current_contrast = get_contrast(img)

    A = new_contrast / current_contrast
    B = new_brightness - current_brightness * A

    new_img = img.load()
    w,h = img.size
    array = conversion_array(A, B)
    for i in range(w):
        for j in range(h):
            new_img[i, j] = array[img.getpixel((i,j))]

    return img

def show_absolute_histogram(img):
        relative_histogram = count_pixels_values_relative(img)
        y_axis = y_axis_setter()
        relative_histogram_normalized = normalize_histogram(relative_histogram, img)
        plt.plot(y_axis, relative_histogram_normalized)
        plt.title('Amount of pixels with each value')
        plt.xlabel('Values')
        plt.ylabel('Amount')
        plt.show()

def show_accumulative_histogram(img):
    accumulative_histogram = count_pixels_values_acumulative(img)
    y_axis = y_axis_setter()
    accumulative_histogram_normalized = normalize_histogram(accumulative_histogram, img)
    plt.plot(y_axis, accumulative_histogram_normalized)
    plt.title('Amount of pixels acumulated for each value')
    plt.xlabel('Values')
    plt.ylabel('Amount acumulated')
    plt.show()

def show_histograms(img):
    show_absolute_histogram(img)
    show_accumulative_histogram(img)

def show_histogram_from_list(my_list):
    y_axis = y_axis_setter_from_list(my_list)
    plt.plot(y_axis, my_list)
    plt.title('Amount of pixels acumulated for each value')
    plt.xlabel('Values')
    plt.ylabel('Amount acumulated')
    plt.show()

def transformation_by_sections(img, array):
        new_img = img.load()
        w,h = img.size
        for i in range(w):
            for j in range(h):
                new_img[i, j] = array[img.getpixel((i,j))]
        return img
    

def equalize_histogram(img, codification_bits=8):
    relative_histogram = count_pixels_values_relative(img)
    accumulative_histogram = count_pixels_values_acumulative(img)
    
    chart = [0] * 256
    size = image_size(img)

    for i in range(len(chart)):
        chart[i] = max(0, round((2**codification_bits / size) * accumulative_histogram[i]) - 1)

    new_img = img.load()
    w,h = img.size
    for i in range(w):
        for j in range(h):
            new_img[i, j] = chart[img.getpixel((i,j))]
    return img

def specify_histogram(img1, img2):
    relative_histogram1 = count_pixels_values_relative(img1)
    accumulative_histogram1 = count_pixels_values_acumulative(img1)
    relative_histogram2 = count_pixels_values_relative(img2)
    accumulative_histogram2 = count_pixels_values_acumulative(img2)
    accumulative_histogram_normalized1 = normalize_histogram(accumulative_histogram1, img1)
    accumulative_histogram_normalized2 = normalize_histogram(accumulative_histogram2, img2)
    # print("hola1")
    # show_accumulative_histogram(img1)
    # print("hola2")
    # show_accumulative_histogram(img2)
    chart = [0] * 256
    for i in range(len(chart)):
        chart[i] = find_grayscale_value(accumulative_histogram_normalized1[i], accumulative_histogram_normalized2)

    new_img = img1.load()
    w,h = img1.size
    for i in range(w):
        for j in range(h):
            new_img[i, j] = chart[img1.getpixel((i,j))]
    return img1

def find_grayscale_value(normalized_ammount_of_pixels, accumulative_histogram_normalized):
    for i in range(len(accumulative_histogram_normalized)):
        if (accumulative_histogram_normalized[i] >= normalized_ammount_of_pixels):
            if normalized_ammount_of_pixels - accumulative_histogram_normalized[i - 1] < accumulative_histogram_normalized[i] - normalized_ammount_of_pixels:
                if (i != 0): 
                    return i - 1
                else:
                    return 0
            else:
                return i

def gamma_correction(img, gamma_value):
    chart = [0] * 256
    for i in range(len(chart)):
        chart[i] = round(255 * (i / 255)**gamma_value)

    new_img = img.load()
    w,h = img.size
    for i in range(w):
        for j in range(h):
            new_img[i, j] = chart[img.getpixel((i,j))]
    return img

def get_ROI(img, first_point, second_point):
    min_x = sys.maxsize
    min_y = sys.maxsize
    max_x = -sys.maxsize - 1
    max_y = -sys.maxsize - 1
    for point in [first_point, second_point]:
        if point[0] < min_x:
            min_x = point[0]
        if point[1] < min_y:
            min_y = point [1]
        if point[0] > max_x:
            max_x = point[0]
        if point[1] > max_y:
            max_y = point [1]
    w, h = img.size
    new_img = Image.new('L', (max_x - min_x, max_y - min_y))
    if (min_x >= 0 and max_x < w) and (min_y >= 0 and max_y < h):
        i = min_x
        while i < max_x:
            j = min_y
            while j < max_y:
                new_img.putpixel((i - min_x, j - min_y), img.getpixel((i, j)))
                j += 1
            i += 1
        return new_img
    else:
        print("Los valores no son válidos.")

curr_pos = 0
list_of_plots = []
ax = None
fig = None

def key_event(e):
    global curr_pos
    global ax
    global fig

    if e.key == "right":
        curr_pos = curr_pos + 1
    elif e.key == "left":
        curr_pos = curr_pos - 1
    else:
        return
    curr_pos = curr_pos % len(list_of_plots)
    ax.cla()
    plt.title(list_of_plots[curr_pos][2])
    ax.plot(list_of_plots[curr_pos][0], list_of_plots[curr_pos][1])
    fig.canvas.draw()

def show_list_of_histograms(list_of_histograms):
    global list_of_plots
    global ax
    global fig
    list_of_plots = list_of_histograms
    fig = plt.figure()
    fig.canvas.mpl_connect('key_press_event', key_event)
    ax = fig.add_subplot(111)
    plt.title(list_of_plots[0][2])
    ax.plot(list_of_plots[0][0], list_of_plots[0][1])
    plt.show()

def digitalization(img, sampling_value, cuantification_bits):
    if (cuantification_bits < 8):
        chart = y_axis_setter()
        for i in range(len(chart)):
            chart[i] *= (255 / ((1 << cuantification_bits) - 1))
        w, h = img.size
        i = 0
        summ = 0
        while i < w:
            j = 0
            while j < h:
                k = 0
                while k < sampling_value:   
                    l = 0
                    while l < sampling_value:
                        if (i + k < w and j + l < h):
                            summ += img.getpixel((i + k, j + l))
                        l+= 1
                    k += 1
                k = 0
                summ /= (sampling_value * sampling_value)
                while k < sampling_value:
                    l = 0
                    while l < sampling_value:
                        if (i + k < w and j + l < h):
                            img.putpixel((i + k, j + l), int(chart[floor(summ)]))
                        l+= 1
                    k += 1
                summ = 0
                j += sampling_value
            i += sampling_value

    return img


# --------------------- SEGUNDA PARTE -------------------------------------------- SEGUNDA PARTE -------------------------------------------- SEGUNDA PARTE -------------------------------------------- SEGUNDA PARTE -------------------------------------------- SEGUNDA PARTE -----------------------

def horizontal_mirror(img):
    w, h = img.size

    for i in range(int(w/2)):
        for j in range(h):
            aux_pixel = img.getpixel((i, j))
            img.putpixel((i, j), img.getpixel((w-i-1, j)))
            img.putpixel((w-i-1, j), aux_pixel)

    return img

def vertical_mirror(img):
    w, h = img.size

    for i in range(w):
        for j in range(int(h/2)):
            aux_pixel = img.getpixel((i, j))
            img.putpixel((i, j), img.getpixel((i, h-j-1)))
            img.putpixel((i, h-j-1), aux_pixel)

    return img

def traspose(img):
    w, h = img.size
    trasposed_img = Image.new('L', (h, w))
    img = img.convert(mode='L')

    for i in range(h):
        for j in range(w):
            trasposed_img.putpixel((i, j), img.getpixel((j, i)))

    return trasposed_img

def escalate_dimensions(img, x, y, operation):
    escalated_img = Image.new('L', (x, y))

    if operation == 0:
        interpole_VMP(img, escalated_img)
    elif operation == 1:
        interpole_bilineal(img, escalated_img)

    return escalated_img


def escalate_percentage(img, x, y, operation):
    w, h = img.size
    escalated_img = Image.new('L', (floor(x/100 * w), floor(y/100 * h)))

    if operation == 0:
        interpole_VMP(img, escalated_img)
    elif operation == 1:
        interpole_bilineal(img, escalated_img)

    return escalated_img

def interpole_VMP(img, final_img):
    w, h = img.size
    w2, h2 = final_img.size
    print(w2, h2, w, h)

    for i in range(w2):
        for j in range(h2):
            final_img.putpixel((i, j), img.getpixel((floor(w * i/w2), floor(h * j/h2))))

    return final_img

def interpole_bilineal(img, final_img):
    w, h = img.size
    w2, h2 = final_img.size
    # print(w2, h2, w, h)

    for i in range(w2):
        for j in range(h2):
            # print(i, j)
            w_floor = floor(w * i/w2)
            h_floor = floor(h * j/h2)

            if (ceil(h * j/h2) >= h):
                h_ceil = floor(h * j/h2)
            else:
                h_ceil = ceil(h * j/h2)

            if(ceil(w * i/w2) >= w):
                w_ceil = floor(w * i/w2)
            else:
                w_ceil = ceil(w * i/w2)

            A = img.getpixel((w_floor, h_ceil))
            B = img.getpixel((w_ceil, h_ceil))
            C = img.getpixel((w_floor, h_floor))
            D = img.getpixel((w_ceil, h_floor))
            p = (w * i/w2) - w_floor
            q = (h * j/h2) - h_floor

            value = round(C + (D - C) * p + (A - C) * q + (B + C - A - D) * p * q)
            final_img.putpixel((i, j), value)

    return final_img

def rotate_img(img):
    w, h = img.size
    rotated_img = Image.new('L', (h, w))
    img = img.convert(mode='L')

    for i in range(h):
        for j in range(w):
            rotated_img.putpixel((w - j - 1, i), img.getpixel((i, j)))

    return rotated_img

# mostrar contraste y brillo,
