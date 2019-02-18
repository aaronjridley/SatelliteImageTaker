# Ronnie Frank Pires Stone 
# Satellite Earth Imaging Project 
# CLASP Department - University of Michigan Ann Arbor
# 7) 2nd Method Implementation 

# Importing libraries and helper functions:

import math 
import numpy as np

def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return int(idx)

def missing_lonlat(NM_lat, NM_lon, Reference, NM_flux, Reference_Mean):

	l = len(NM_lat)

	counter = 0

	c1 = 0 

	while c1 < l:

		c2 = 0 

		while c2 < l: 

			if Reference[0][c1][c2] == 1998 or NM_flux[c1][c2] < Reference_Mean or NM_lat[c1][c2] < -10: # The 1998 is just a number that I use to show that the pixel is out of bounds 

				Reference[0][c1][c2] = 0 
				Reference[1][c1][c2] = 0

			else:

				current_lat = Reference[0][c1][c2]
				current_lon = Reference[1][c1][c2]

				lat_idx = find_nearest(NM_lat, current_lat)
				lon_idx = find_nearest(NM_lon, current_lon)

				lat1 = lat_idx/l
				lat2 = lat_idx%l 

				lon1 = lon_idx/l
				lon2 = lon_idx%l 

				if abs(NM_lat[lat1][lat2] - current_lat) < 180/float(l): 

					if abs(NM_lon[lon1][lon2] - current_lon) < 360/float(l):

						Reference[0][c1][c2] = 1
						Reference[1][c1][c2] = 1 
						counter += 1

			c2 += 1

		c1 += 1

	return counter 




		 
