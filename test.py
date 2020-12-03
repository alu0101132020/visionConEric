#!/usr/bin/env python3

import webbrowser
import matplotlib.pyplot as plt
import sys
from statistics  import stdev
from PIL import Image
import sklearn
import math

# Function that asserts that the image is grayscale.
def is_grey_scale(img):
    imgConverted = img.convert('RGB')
    w,h = imgConverted.size
    for i in range(w):
        for j in range(h):
            r,g,b = imgConverted.getpixel((i,j))
            if r != g != b: return False
    return True

# Function that counts for each possible value how many pixels are there, and returns the array that contains all that information.
def count_pixels_values_relative(img):
    relative_histogram = [0] * 256
    w,h = img.size
    for i in range(w):
        for j in range(h):
            relative_histogram[img.getpixel((i,j))] += 1
    return relative_histogram

# Function that counts for each possible value and all the previous one how many pixels are there, and returns the array that contains all that information.
def count_pixels_values_acumulative(relative_histogram):
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

# Function that returns a file name, extracts the extension and returns it.
def obtain_extension(imageFileName) :
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
def summ_of_values(relative_histogram) :
    summ = 0
    for i in range(len(relative_histogram)):
        summ += relative_histogram[i] * i
    return summ

# Function that returns the brightness of the image, defined as the division of the sum of all the pixels values by the ammount of pixeles.
def get_bright(relative_histogram, img):
    total_pixels = image_size(img)
    total_values = summ_of_values(relative_histogram)
    return total_values / total_pixels

def get_contrast(relative_histogram, img) :
    total_pixels = image_size(img)
    mean = get_bright(relative_histogram, img)
    summ = 0
    for i in range(len(relative_histogram)):
        summ += relative_histogram[i] * ((i - mean)**2)
    summ = math.sqrt(summ / total_pixels)
    return summ

def normalize_histogram(array, img) :
    arrayNormalized = array.copy()
    size = image_size(img)
    for i in range(len(array)) :
        arrayNormalized[i] = arrayNormalized[i] / size
    return arrayNormalized

def conversion_array(A, B) :
    array = y_axis_setter()
    for i in range(len(array)) :
        value = array[i] * A + B
        if value > 255:
            array[i] = 255
        elif value < 0:
            array[i] = 0
        else:
            array[i] = int(value)

    return array

def conversion(img, A, B) :
    new_img = img.load()
    w,h = img.size
    array = conversion_array(A, B)
    for i in range(w) :
        for j in range(h) :
            new_img[i, j] = array[img.getpixel((i,j))]

    return img
    
def show_histograms(img, relative_histogram, accumulative_histogram) :
    y_axis = y_axis_setter()
    relative_histogram_normalized = normalize_histogram(relative_histogram, img)
    accumulative_histogram_normalized = normalize_histogram(accumulative_histogram, img)

    plt.plot(y_axis, relative_histogram_normalized)
    plt.title('Amount of pixels with each value')
    plt.xlabel('Values')
    plt.ylabel('Amount')
    plt.show()

    plt.plot(y_axis, accumulative_histogram_normalized)
    plt.title('Amount of pixels acumulated for each value')
    plt.xlabel('Values')
    plt.ylabel('Amount acumulated')
    plt.show()

def define_sections(number_of_sections) :
    sections = [0]
    start_of_section = 0
    for i in range (number_of_sections - 1) :
        string = 'Section ' + str(i + 1) + ' starts in ' + str(start_of_section) + '. Where do you want it to end? -> '
        end_of_section = int(input(string))
        if (start_of_section < 255 and start_of_section < end_of_section) :
            sections.append(end_of_section)
            start_of_section = end_of_section
        else:
            break
    return sections

def fill_sections_array(index_start_of_section, sections, array) :
    index_end_of_section = index_start_of_section + 1
    start_value = int(input('Introduce which value from 0 to 255 you want the section [' + str(sections[index_start_of_section]) + ', ' + str(sections[index_end_of_section]) + '] to start: '))
    end_value = int(input('Introduce which value from 0 to 255 you want the section [' + str(sections[index_start_of_section]) + ', ' + str(sections[index_end_of_section]) + '] to end: '))
    y_difference = end_value - start_value
    x_difference = sections[index_end_of_section] - sections[index_start_of_section]
    A = y_difference / x_difference
    B = start_value - A * sections[index_start_of_section]
    j = sections[index_start_of_section]
    while j < sections[index_end_of_section] : 
        value = array[j] * A + B
        if value > 255:
            array[j] = 255
        elif value < 0:
            array[j] = 0
        else:
            array[j] = int(value)
        j += 1

def transformation_by_sections(img, relative_histogram) :
    number_of_sections = int(input('Insert the number of sections in which you want to divide the histogram: '))
    sections = define_sections(number_of_sections)
    if not (len (sections) != number_of_sections) :
        sections.append(255)
        array = y_axis_setter()

        for i in range (number_of_sections) :
            fill_sections_array(i, sections, array)
        
        new_img = img.load()
        w,h = img.size
        for i in range(w) :
            for j in range(h) :
                new_img[i, j] = array[img.getpixel((i,j))]
        return img
    else:
        error_string = 'There was an error inserting a section.'
        error_string += "Start of section can't be bigger than an end of section an end of Section can't be bigger than 255"
        print(error_string)



# We get the argument from pronm (name if the image)
imageFileName = sys.argv[1]

image = Image.open(imageFileName)

if (not is_grey_scale(image)) :
    image = image.convert(mode='L')
    array = imageFileName.split('.')
    imageFileName = array[0] + '_grayscale.jpg' 
    image.save(imageFileName)

relative_histogram = count_pixels_values_relative(image)

accumulative_histogram = count_pixels_values_acumulative(relative_histogram)

# show_histograms(image, relative_histogram, accumulative_histogram)

current_brightness = get_bright(relative_histogram, image)
current_contrast = get_contrast(relative_histogram, image)
# print(obtain_extension(imageFileName))
# print(image_size(image))
print(find_min_max(relative_histogram))
print(round(current_brightness, 2))
print(round(current_contrast, 2))

# new_brightness = float(input('Insert brightness that you would like to change to: '))
# new_contrast = float(input('Insert constrast that you would like to change to: '))

# A = current_contrast / new_contrast
# B = new_brightness - current_brightness * A

# new_img = conversion(image, A, B)

new_img = transformation_by_sections(image, relative_histogram)

array = imageFileName.split('.')
imageFileConverted = array[0] + '_converted.jpg' 
new_img.save(imageFileConverted)
# webbrowser.open(imageFileName)
