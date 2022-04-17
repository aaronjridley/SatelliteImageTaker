# Ronnie Frank Pires Stone 
# Satellite Earth Imaging Project 
# CLASP Department - University of Michigan Ann Arbor
# 6) 1st Method Implementation 

# Importing libraries and helper functions:

import math 
import numpy as np

def area_lonlat(NM_flux, NM_lat, NM_lon, Max):

   l = len(NM_flux)
   Sum = 0 
   c1 = 1
   while c1 < l-1:
   
      c2 = 1 
      
      while c2 < l-1: 
      
         if NM_lat[c1][c2] < 0 or NM_lat[c1 - 1][c2] == 1998 or NM_lat[c1][c2 + 1] == 1998 or NM_lat[c1 + 1][c2] == 1998 or NM_lat[c1][c2 - 1] == 1998:
      
            Dlat = 0
            Dlon = 0  
      
         else: 
                
            North_lat = abs(NM_lat[c1][c2] - NM_lat[c1 - 1][c2])
            East_lat = abs(NM_lat[c1][c2] - NM_lat[c1][c2 + 1])
            South_lat = abs(NM_lat[c1][c2] - NM_lat[c1 + 1][c2])
            West_lat = abs(NM_lat[c1][c2] - NM_lat[c1][c2 - 1])
            
            Dlat = (North_lat + East_lat + South_lat + West_lat)/4
            
            North_lon = abs(NM_lon[c1][c2] - NM_lon[c1 - 1][c2])
            East_lon = abs(NM_lon[c1][c2] - NM_lon[c1][c2 + 1])
            South_lon = abs(NM_lon[c1][c2] - NM_lon[c1 + 1][c2])
            West_lon = abs(NM_lon[c1][c2] - NM_lon[c1][c2 - 1])
            
            Dlon = (North_lon + East_lon + South_lon + West_lon)/4
      
         if NM_flux[c1][c2] < Max/10:
      
            Aurora = 0 
      
         else:
      
            Aurora = 1 
      
         Sum = Sum + Dlat*Dlon*Aurora*np.cos(NM_lat[c1][c2]*3.1415/180.0)
      
         c2 += 1
      
      c1 += 1 
   
   return Sum
