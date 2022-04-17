# Ronnie Frank Pires Stone 
# Satellite Earth Imaging Project 
# CLASP Department - University of Michigan Ann Arbor
# 4) IDL Reader 

# Importing libraries:

import numpy as np 
import pylab as pl  
#from scipy.misc import toimage
from numpy import array
from PIL import Image
import matplotlib.pyplot as plt	# Python's plotting library 


def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return int(idx)

def image_heatmap(current_file, x, y, image):

    im_matrix = array(image)

    iIndex_ = 6
    # iIndex_ = 0
    
    with open (current_file) as IDL:
        IDL_lines = IDL.readlines()
        IDL.close()

        iTimeLine = IDL_lines.index('TIME\n')
        iNorthLine = IDL_lines.index('BEGIN NORTHERN HEMISPHERE\n') + 1
        iSouthLine = IDL_lines.index('BEGIN SOUTHERN HEMISPHERE\n') + 1
        
        iNumLine = IDL_lines.index('NUMERICAL VALUES\n')

        nLats = int(IDL_lines[iNumLine+2][1:5])
        nMlts = int(IDL_lines[iNumLine+3][1:5])

        hours = IDL_lines[29][3:5]
        minutes = IDL_lines[30][3:5]
        UT = float(hours) + float(minutes)/60.0
        
        data = np.zeros((16471*2,3))
        
        eFlux = np.zeros((nLats * 2 - 1, nMlts))
        lons = np.zeros(nMlts)
        lats = np.zeros(nLats * 2 - 1)

        # Nothern Hemisphere:
        counter = 0

        for iMlt in range(nMlts):
            for iLat in range(nLats):
                parts = IDL_lines[iNorthLine + counter].split()
                eFlux[iLat][iMlt] = float(parts[iIndex_])
                lons[iMlt] = (UT*15.0 - float(parts[1]) - 90 + 360.0) % 360
                lats[iLat] = 90.0 - float(parts[0])

                parts = IDL_lines[iSouthLine + counter].split()
                eFlux[iLat + nLats - 1][iMlt] = float(parts[iIndex_])
                lons[iMlt] = (UT*15.0 - float(parts[1]) - 90 + 360.0) % 360
                lats[iLat + nLats - 1] = 90.0 - float(parts[0])
                counter += 1
                
        #fig = plt.figure(figsize = (10,10))
        #ax = fig.add_subplot(111)
        #cax = ax.pcolor(eFlux)
        #fig.savefig('test2.png')
        #plt.close()

        #counter = 0
        #while (counter < 16471):
        #    parts = IDL_lines[iNorthLine + counter].split()
        #    data[counter][0] = 90.0 - float(parts[0])
        #    data[counter][1] = UT*15.0 - float(parts[1]) - 90
        #    if (data[counter][1] > 180):
        #        data[counter][1] = data[counter][1] - 360 
        #    elif (data[counter][1] < -180):
        #        data[counter][1] = data[counter][1] + 360 
        #    # Hall Conductivity: [28:39]
        #    # Pedersen Conductivity:[41:52]
        #    # Current Density: [54:65]
        #    # E-Flux: [80:91] 
        #    data[counter][2] = float(parts[6])
        #    counter += 1
        #
        ## Southern Hemisphere
        #
        #counter = 0
        #
        #while (counter < 16471):
        #    data[16471 + counter][0] = 90 - float(IDL_lines[16516 + counter][2:13])
        #    # data[16471 + counter][1] = float(IDL_lines[16516 + counter][15:26]) - 180 
        #    data[16471 + counter][1] = UT*15 - float(IDL_lines[43 + counter][15:26]) - 90
        #    if data[16471 + counter][1] > 180:
        #        data[16741 + counter][1] = data[16471 + counter][1] - 360 
        #    elif data[16471 + counter][1] < -180:
        #        data[16471 + counter][1] = data[16471 + counter][1] + 360 
        #    data[16471 + counter][2] = float(IDL_lines[16516 + counter][80:91])
        #    counter += 1

    # Matching the two images and creating two index matrices: 

    idx_matrix = np.zeros((x.shape[0],x.shape[1]))
    #position_matrix = np.zeros((x.shape[0],x.shape[1]))

    scale_temp = np.zeros(181)
    lon_data = np.zeros(181)
    lat_data = np.zeros(181)

    nX = x.shape[0]
    nY = x.shape[1]

    dlat = lats[1] - lats[2]
    dmlt = lons[1] - lons[2]
    iOff = int(np.round(lons[0] / dmlt))

    # x is longitude
    # y is latitude
    for iX in range(nX):
        for iY in range(nY):
            lon = (x[iX][iY] + 360.0) % 360.0
            lat = y[iX][iY]
            iLatIndex = int(np.round((90 - lat) / dlat))
            iLonIndex = (nMlts - int(np.round(lon / dmlt)) + iOff) % nMlts
            idx_matrix[iX][iY] = eFlux[iLatIndex][iLonIndex]
            
    #ct1 = 0
    #
    #while (ct1 < x.shape[0]):
    #
    #    ct2 = 0
    #
    #    while (ct2 < x.shape[1]):
    #
    #        if (x[ct1][ct2] == 1998):
    #
    #            idx_matrix[ct1][ct2] = 0 
    #
    #        else:
    #
    #            idx_y = find_nearest(data[:,0],y[ct1][ct2])
    #
    #            c = 0
    #
    #            while c < 181:
    #
    #                lon_data[c] = (data[idx_y + 91*c][1])
    #
    #                scale_temp[c] = idx_y + 91*c
    #
    #                c += 1 
    #
    #            idx_x = find_nearest(lon_data, x[ct1][ct2])
    #
    #            idx_abs = find_nearest(scale_temp, idx_x)
    #
    #            idx_matrix[ct1][ct2] = data[idx_y + idx_x*91][1]
    #
    #        ct2 += 1
    #
    #    ct1 += 1

    # Scaling:

    idx_matrix_rel = np.zeros((x.shape[0],x.shape[1]))
    abs_maximum = np.max(idx_matrix)
    abs_minimum = np.min(idx_matrix)
    rel_maximum = 255
    rel_minimum = 0 

    idx_matrix_rel = ((idx_matrix - abs_minimum) / (abs_maximum - abs_minimum)) * (rel_maximum - rel_minimum) + rel_minimum
    
    #ct1 = 0 
    #
    #while (ct1 < x.shape[0]):
    #
    #    ct2 = 0 
    #    
    #    while (ct2 < x.shape[1]):
    #
    #        idx_matrix_rel[ct1][ct2] = ((idx_matrix[ct1][ct2] - abs_minimum)/(abs_maximum - abs_minimum))*(rel_maximum - rel_minimum) + rel_minimum
    #
    #        ct2 += 1 
    #
    #    ct1 += 1 

    # Filtering the image:

    nColors = 3
    filtered_image = np.zeros((x.shape[0],x.shape[1],nColors))
 
    ct1 = 0

    while ct1 < x.shape[0]:

        ct2 = 0 

        while ct2 < x.shape[1]:
   
            ct3 = 0

            while ct3 < nColors:

                if ct3 == 0:

                    filtered_image[ct1][ct2][ct3] = idx_matrix_rel[ct1][ct2]

                elif ct3 == 1 or ct3 == 2: 

                    filtered_image[ct1][ct2][ct3] = 0

                else:

                    filtered_image[ct1][ct2][ct3] = 255

                ct3 += 1

            ct2 += 1

        ct1 += 1

    picture = Image.fromarray(filtered_image.astype(np.uint8))
    
    return (picture, idx_matrix)
