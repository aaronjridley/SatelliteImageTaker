# Ronnie Frank Pires Stone 
# Satellite Earth Imaging Project 
# CLASP Department - University of Michigan Ann Arbor
# 1) Equatorial Image Grid

# Importing libraries:

import math 
import numpy as np

# Satellite coordinates:

def image_grid(x,y,z,n,m,alpha,r):

 # Defining basic parameters: 

 d = math.sqrt(x**2 + y**2 + z**2) # Distance between satellite and planet center

 tht = 2*(np.arcsin(r/d))  # Calculating theta minimum (the minimum angle to see the whole Earth from that distance)

 # Defining what the satellite sees: 

 if tht >= alpha: # If theta minimum is larger than the field of view

  phi = math.pi - np.arcsin((d/r)*math.sin(alpha/2.0)) 
  beta = math.pi - phi - alpha/2.0
  i = r*math.sin(beta)

 else: # If theta minimum is smaller than the field of view 

  i = d*math.tan(alpha/2.0)


 # Defining the pixelated vectors as a function of distance:

 pixel_size_x = (2*i)/m # Pixel size in the horizontal direction 
 pixel_size_y = (2*i)/n # Pixel size in the vertical direction 

 X = np.linspace(-i + pixel_size_x/2, i - pixel_size_x/2, num = m) # Vector of midpoints of each horizontal pixel 
 Y = np.linspace(-i + pixel_size_y/2, i - pixel_size_y/2, num = n) # Vector of midpoints of each vertical pixel 



 # Defining the latitude vector: 
 
 Y_lat = [0]*n # Creates a vector with an "n" number of zero entries

 counter = 0 # Iterator 
 divider = 1 # Helps to spread dark spaces evenly across the globe image 

 while counter < len(Y): # While there are pixels to be considered 

  if r < abs(Y[counter]): # If the pixel is outside of the Earth 

   divider = divider*-1  # Change the side  
   Y_lat[counter] = 999*divider   # Throw it very far away from everything else 

  else: # If the pixel is inside of the Earth 

   rat = Y[counter]/r # Define a ratio between the vertical distance and the radius 
   Y_lat[counter] = 90 - (180*np.arccos(rat))/(math.pi) # Use the definition of latitude to find its corresponding value 

  counter += 1 # Iterator goes up 



 # The idea is to solve this case from an equatorial perspective and then transform it through a rotation to its actual coordinates 
 # Here we assume that the point at which our satellite is looking at is defined as 0 lat and 0 lon

 # Temporary Equatorial View Latitude Matrix: 

 NM_lat = np.zeros((n, m)) # Initializes the latitude matrix to be returned for this function 

 ct1 = 0 # Iterator no.1 

 while ct1 < n: # Iterates through the vertical pixels 

  ct2 = 0 # Iterator no.2 

  while ct2 < m: # Iterates through the horizontal pixels 

   NM_lat[ct1][ct2] = Y_lat[len(Y) - ct1 - 1]  # Iterating backwards because negative values should go last in the matrix 

   ct2 += 1 # Iterator no.2 goes up 

  ct1 += 1 # Iterator no.1 goes up 



 # Temporary Equatorial View Longitude Matrix:

 NM_lon = np.zeros((n,m)) # Initializes the longitude matrix to be returned for this function 

 X_lon = [0]*m # Initializes placeholder for current row being iterated in the matrix 

 ct1 = 0 # Iterator no.1 

 divider = 1 # See above 

 while ct1 < n: # Iterates through vertical pixels 

   ct2 = 0 # Iterator no.2 

   # We find radius of the new circle:

   gamma = math.pi/2 - abs((Y_lat[ct1]*math.pi)/180)
   rprime = r*math.sin(gamma)
  
   while ct2 < m: # Iterates through horizontal pixels 

     if rprime < abs(X[ct2]) or rprime <= 0: # If the pixel is outside of the circle 

       divider = -divider         # See above
       X_lon[ct2] = 999*divider  # See above 

     else: # Otherwise use the definition of lon to calculate the values of that lat row

       theta = 180*(np.arcsin(X[ct2]/rprime))/math.pi
       X_lon[ct2] = theta

     ct2 += 1 # Iterator no.2 goes up 

   NM_lon[ct1] = X_lon # Saves the current longitude row into its proper location in the matrix 

   ct1 += 1 # Iterator no.1 goes up 




 # As you might have noticed the longitude matrix was completed in one loop whereas the latitude matrix is now being completed in two steps 
 # This is why it is now important to filter out which latitudes are geometrically impossible due to the Earth's curvature 

 # Updated Equatorial View Latitude Matrix:

 ct1 = 0 # Iterator no.1 

 while ct1 < n: # Iterates through the vertical pixels  

  ct2 = 0 # Iterator no.2 

  while ct2 < m: # Iterates through the horizontal pixels 

   # Throwing away the bad apples: 

   if NM_lon[ct1][ct2] == -999: 

     NM_lat[ct1][ct2] = -999

   elif NM_lon[ct1][ct2] == 999:

     NM_lat[ct1][ct2] = 999 

   ct2 += 1 # Iterator no.2 goes up 

  ct1 += 1 # Iterator no.1 goes up 

 return(NM_lon,NM_lat)