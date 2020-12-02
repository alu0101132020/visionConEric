#!/usr/bin/env python3


import webbrowser
import matplotlib.pyplot as plt
import sys
from statistics  import stdev
from PIL import Image


# Function that asserts that the image is grayscale.
def is_grey_scale(img):
    imgConverted = img.convert('RGB')
    w,h = imgConverted.size
    for i in range(w):
        for j in range(h):
            r,g,b = imgConverted.getpixel((i,j))
            if r != g != b: return False
    return True

def count_pixels_values_relative(img):
    relative_histogram = [0] * 256
    w,h = img.size
    for i in range(w):
        for j in range(h):
            relative_histogram[img.getpixel((i,j))] += 1
    return relative_histogram

def count_pixels_values_acumulative(relative_histogram):
    acumulative_histogram = [0] * 256
    total = 0
    for i in range(256):
        acumulative_histogram[i] = relative_histogram[i] + total
        total = acumulative_histogram[i]
        
    return acumulative_histogram

def y_axis_setter():
    y_axis = [0] * 256

    for i in range(len(y_axis)):
        y_axis[i] = i
    
    return y_axis

def obtain_extension(imageFileName) :
    return imageFileName.split('.')[1]

def image_size(image):
    w,h = image.size
    return w * h

def find_min_max(relative_histogram):
    i = 0
    while (i < len(relative_histogram) and relative_histogram[i] == 0): 
        i += 1
    
    j = 255
    while (j >= 0 and relative_histogram[j] == 0): 
        j -= 1
    return [i, j]

def summ_of_values(relative_histogram) :
    summ = 0
    for i in range(len(relative_histogram)):
        summ += relative_histogram[i] * i
    return summ


def get_bright(relative_histogram, img):
    total_pixels = image_size(img)
    total_values = summ_of_values(relative_histogram)
    return total_values / total_pixels

def get_contrast(relative_histogram) :
    return stdev(relative_histogram)
    

# We get the argument from pronm (name if the image)
imageFileName = sys.argv[1]

image = Image.open(imageFileName)

if (not is_grey_scale(image)) :
    gs_image = image.convert(mode='L')
    array = imageFileName.split('.')
    imageFileName = array[0] + '_grayscale.jpg' 
    gs_image.save(imageFileName)

relative_histogram = count_pixels_values_relative(image)

acumulative_histogram = count_pixels_values_acumulative(relative_histogram)

y_axis = y_axis_setter()

plt.plot(y_axis, relative_histogram)
plt.title('Amount of pixels with each value')
plt.xlabel('Values')
plt.ylabel('Amount')
# plt.show()

plt.plot(y_axis, acumulative_histogram)
plt.title('Amount of pixels acumulated for each value')
plt.xlabel('Values')
plt.ylabel('Amount acumulated')
# plt.show()

print(obtain_extension(imageFileName))
print(image_size(image))
print(find_min_max(relative_histogram))
print(get_bright(relative_histogram, image))
print(get_contrast(relative_histogram))
# webbrowser.open(imageFileName)





