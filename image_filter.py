# Ronnie Frank Pires Stone 
# Satellite Earth Imaging Project 
# CLASP Department - University of Michigan Ann Arbor
# 3) Image Filtering

# Importing libraries:

from PIL import Image
import numpy as np 
from numpy import array
from scipy.misc import toimage

# Function from the internet.
# Will be useful later.

def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return int(idx)

def image_filter(x,y):

 # Image of interest:

 im = Image.open('Reference.png')
 
 # Tranforms png image to numpy array:

 im_matrix = array(im)

 # Gets the dimensions of the array:

 x_pixels = im.size[0]
 y_pixels = im.size[1]

 # Calculates pixel size in terms of latitude and longitude:

 x_pixel_size = (2*180)/float(x_pixels)
 y_pixel_size = (2*90)/float(y_pixels)

 # Creates pixelated latitude and longitude vectors:

 lon_vector = np.linspace(-180 + x_pixel_size/2, 180 - x_pixel_size/2, x_pixels)
 lat_vector = np.linspace(-90 + y_pixel_size/2, 90 - y_pixel_size/2, y_pixels)

 # Initializing latitude grid:

 NM_lat = np.zeros((y_pixels,x_pixels)) 

 ct1 = 0

 while ct1 < y_pixels:

  ct2 = 0

  while ct2 < x_pixels: 

    NM_lat[ct1][ct2] = lat_vector[len(lat_vector) - ct1 - 1]

    ct2 += 1

  ct1 += 1

 # Initializing longitude grid:

 NM_lon = np.zeros((y_pixels,x_pixels))

 ct1 = 0

 while ct1 < y_pixels:

  ct2 = 0

  while ct2 < x_pixels:

    NM_lon[ct1][ct2] = lon_vector[ct2]

    ct2 += 1

  ct1 += 1

 # Matching the two images and creating two index matrices: 

 idx_matrix_x = np.zeros((x.shape[0],x.shape[1]))
 idx_matrix_y = np.zeros((y.shape[0],y.shape[1]))
 
 ct1 = 0

 while ct1 < x.shape[0]:

  ct2 = 0

  while ct2 < x.shape[1]:

    idx_x = find_nearest(NM_lon[0],x[ct1][ct2])
    idx_y = find_nearest(NM_lat[:,idx_x],y[ct1][ct2])
   
    idx_matrix_x[ct1][ct2] = idx_x
    idx_matrix_y[ct1][ct2] = idx_y

    ct2 += 1

  ct1 += 1

 # Filtering the image:
 
 filtered_image = np.zeros((x.shape[0],x.shape[1],4))

 ct1 = 0

 while ct1 < x.shape[0]:

   ct2 = 0 

   while ct2 < x.shape[1]:
   
     ct3 = 0

     while ct3 < 4:

       filtered_image[ct1][ct2][ct3] = im_matrix[int(idx_matrix_y[ct1][ct2])][int(idx_matrix_x[ct1][ct2])][ct3]

       ct3 += 1

     ct2 += 1

   ct1 += 1

 picture = toimage(filtered_image)

 return(picture)