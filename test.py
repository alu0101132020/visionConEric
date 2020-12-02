#!/usr/bin/env python3

# import cv2 
  
# # Save image in set directory 
# # Read RGB image 
# img = cv2.imread('g4g.png')  
  
# # Output img with window name as 'image' 
# cv2.imshow('image', img)  
  
# # Maintain output window utill 
# # user presses a key 
# cv2.waitKey(0)         
  
# # Destroying present windows on screen 
# cv2.destroyAllWindows()


	
# example of saving a grayscale version of a loaded image
from PIL import Image
# load the image
image = Image.open('color.jpg')
# convert the image to grayscale
gs_image = image.convert(mode='L')

gs_image.save('opera_house_grayscale.jpg')
# load the image again and show it
image2 = Image.open('opera_house_grayscale.jpg')
# show the image
image2.show()