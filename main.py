#!/usr/bin/env python

# Ronnie Frank Pires Stone 
# Satellite Earth Imaging Project 
# CLASP Department - University of Michigan Ann Arbor
# 1) Main

# Importing libraries and helper functions:

# Importing libraries and helper functions:

import math # Python's math library 
import numpy as np # Python's numpy library 
import glob # Python's unix pathname expansion library 
import os # Python's operating system functionality library 
import matplotlib.pyplot as plt	# Python's plotting library 
from PIL import Image  # Python's image processing library 
#from scipy.misc import toimage # Python's scientific library 

# Custom Functions for the Application:

# Function to create numerical equatorial lat and lon grid
from image_grid import image_grid 
# Function to rotate numerical equatorial grid to the desired coordinate
from image_rotation import image_rotation
# Function to convert numerical lat and lon grid into an image
from image_filter import image_filter
# Function to convert image into a auroral value heatmap 
from image_heatmap import image_heatmap
# Function to propagate simple circular orbits 
from orbital_planner import orbital_planner

# Function to implement an weighted area method 
from area_lonlat import area_lonlat
# Function to implement a direct grid comparison method 
from missing_lonlat import missing_lonlat

from iono_routines import *


def make_vector(x, y, z):
    v = [x, y, z]
    m = np.sqrt(x*x + y*y + z*z)
    v = v / m
    return v

def get_angle(v1, v2):
    dot = np.sum(v1 * v2)
    angle = np.arccos(dot)
    return angle

# ------------------------------------------------------------------
# 1) Data fetching 
# ----------------------------------------------------------------
# File sorting: 

# This function returns the sorting parameter for the IDL files 
def sortKeyFunc(s): 
    return int(os.path.basename(s)[9:13])

# Path to files directory
# Determines that IDL files are numerically sorted
idl_files = sorted(glob.glob("Data/it*.idl"), key=os.path.getmtime)
# Sort parameter becomes [9:13] position in file header
idl_files.sort(key=sortKeyFunc)

# Retrieves the number of IDL files 
nFiles = len(idl_files)

Header0, IonoNorthData, IonoSouthData = read_iono_one_file(idl_files[0])
Header1, IonoNorthData, IonoSouthData = read_iono_one_file(idl_files[-1])

dt = Header1['time']-Header0['time']
dt = float(dt.seconds)
print(dt)

# Input data:

#n = int(raw_input('Horizontal Number of Pixels? '))
#m = int(raw_input('Vertical Number of Pixels? '))
#nTimes = int(raw_input('Number of frames? '))
#nSats = int(raw_input('Number of Satellites? '))

n = 128*2
m = 128*2
nTimes = 3
nSats = 2

dtor = np.pi / 180.0

rEarth = 6372.0 # Approximated and given in kilometers (Earth Radius)
rOrbit = rEarth + 20000.0

alpha = 18.0 * dtor # Approximated and given in radians (Field of View)

# Satellite(s) coordinates in time (3D Cartesian System centered at the Earth)

OrbitX, OrbitZ = orbital_planner(nSats, rOrbit, nTimes, dt)
 
print(OrbitX)
print(OrbitZ)

# ------------------------------------------------------------------
# 2) Reference image for method implementation processing 
# -----------------------------------------------------------------------

# Reference frame definition: (Directly above the North Pole)

# Setting x = 0 and y = 0 is not advisable 
x = 1
y = 1

# This range captures the entire Earth
z = rOrbit

# Produce reference image: 

# Equatorial grid 
(NM_lon, NM_lat) = image_grid(x,y,z,n,m,alpha,rEarth, 0.0)
# Rotates to north pole 
(NM_lon_rotated, NM_lat_rotated) = image_rotation(NM_lon, NM_lat, x, y, z, rEarth)
# Produces the image 
(NM_image) = image_filter(NM_lon_rotated, NM_lat_rotated)
# Produces the heatmap 
(NM_aurora, NM_flux) = image_heatmap(idl_files[0], NM_lon_rotated, NM_lat_rotated, NM_image)


# Method 1 (Comment out if Method 2 is being implemented, also look inside the loop for further instructions)

Reference_Mean = np.mean(NM_flux)
Reference_Max = np.amax(NM_flux)
Reference = area_lonlat(NM_flux, NM_lat_rotated, NM_lon_rotated, Reference_Max)

# Method 2 (Comment out if Method 1 is being implemented, also look inside the loop for further instructions)

# Reference_Mean = np.mean(NM_flux)
# Reference_Flux = NM_flux
# Reference = (NM_lat_rotated, NM_lon_rotated)
# Reference_counter = missing_lonlat(NM_lat_rotated, NM_lon_rotated, Reference, Reference_Flux, Reference_Mean)

# ------------------------------------------------------------------
# 3) Main loop:	
# ------------------------------------------------------------------
	
# Define matrices to store results: 

# Stores the results for the current satellite 
Partial_Results = np.zeros(nTimes)

# Stores all satellite results in one matrix 
Results = np.zeros([nSats,nTimes])

iSat = 0 


while iSat < nSats: # While there are satellites in orbit 

    iTime = 0

    while iTime < nTimes:	# While there are pictures to be taken 

        iFile = int(np.round(nFiles * float(iTime / nTimes)))
        
        # Satellite's x-displacement per picture taken 
        x = OrbitX[iSat][iTime] + 1  
        # Satellite's y-displacement per picture taken
        y = 1
        # Satellite's z-displacement per picture taken
        z = OrbitZ[iSat][iTime] + 1

        vPole = make_vector(-x, -y, np.sign(z) * rEarth - z)
        vCenter = make_vector(-x, -y, -z)
        angle = get_angle(vPole, vCenter)
        shift = 0.0 # np.sign(z) * angle / alpha / np.cos(angle)

        print('angle to pole : ', angle, shift)
            
        # Get image: 
        (NM_lon, NM_lat) = image_grid(x, y, z, n, m, alpha, rEarth, shift)
        (NM_lon_rotated, NM_lat_rotated) = image_rotation(NM_lon, NM_lat, x, y, z, rEarth)
        (NM_image) = image_filter(NM_lon_rotated, NM_lat_rotated)
        (NM_aurora, NM_flux) = image_heatmap(idl_files[iFile], NM_lon_rotated, NM_lat_rotated, NM_image)
        
        # Method 1: (Comment out if Method 2 is being implemented, also look outside of the loop for further instructions)
        
        NM_result = float(area_lonlat(NM_flux, NM_lat_rotated, NM_lon_rotated, Reference_Mean))/float(Reference)
        
        # Method 2: (Comment out if Method 1 is being implemented, also look outside of the loop for further instructions)
        
        # NM_mean = np.mean(NM_flux)
        # NM_result = float((missing_lonlat(NM_lat_rotated, NM_lon_rotated, Reference, NM_flux, NM_mean)))/float(Reference_counter)
        
        # Stores results for the current satellite in the current frame: 
        
        Partial_Results[iTime] = NM_result
        
        # Saving the constructed image: 
        
        sSat = 'Sat{:04d}'.format(iSat+1)
        sImage = '{:04d}'.format(iTime+1)
        ResultsFile = sSat+"_Result"+sImage+".png"
        HeatmapFile = sSat+"_Heatmap"+sImage+".png"
        
        # Saves the image in the current directory
        NM_image.save(ResultsFile) 
        NM_aurora.save(HeatmapFile) 
        	
        # Making sure the user sees that the program is running without any errors: 
        
        print('')
        print('Current Satellite: ' + str(iSat + 1) + ' of ' + str(nSats))
        print('Current Frame: ' + str(iTime + 1) + ' of ' + str(nTimes))
        print(NM_result)
        	
        iTime += 1 # Iterator goes up 
 	
    Results[iSat] = Partial_Results

    iSat += 1 # Iterator goes up 

# 4) Data processing and plotting:	
# -----------------------------------------------------------------------------------------------------------------------------------------------

i = 0

Summation = np.zeros(nTimes)
Maxima = np.zeros(nSats)

while i < nTimes:

    Maxima = Results[:,i]
    Summation[i] = np.amax(Maxima)

    i += 1

j = 0 

fig, axarr = plt.subplots(2, sharex=True)
xaxis = np.arange(nTimes)

while j < len(Results):

    axarr[1].plot(xaxis, Results[j])
    axarr[0].plot(xaxis, Summation)
    axarr[0].set_ylim([0, 1])
    axarr[1].set_ylim([0, 1])

    j += 1

plt.xlabel('Period')
plt.ylabel('Aurora Percentage')
plt.title('Satellite Number vs. Aurora Visibility')
plt.show()


