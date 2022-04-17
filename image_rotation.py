# Ronnie Frank Pires Stone 
# Satellite Earth Imaging Project 
# CLASP Department - University of Michigan Ann Arbor
# 2) Geometric Rotation

# Importing libraries:

import math 
import numpy as np 
from sympy import Symbol, nonlinsolve

def image_rotation(x,y,X,Y,Z,r):

  X = int(X)
  Y = int(Y)
  Z = int(Z)

  # Calculate the x,y,z coordinates of the intersection point in the globe:

  x_sphere = Symbol('x_sphere') # Creates a x-position variable on the sphere surface
  y_sphere = Symbol('y_sphere') # Creates a y-position variable on the sphere surface
  z_sphere = Symbol('z_sphere') # Creates a z-position variable on the sphere surface
  lamb = Symbol('lamb')         # Creates a vector line parameter called lambda 



  # Apply vector algebra to find the intersection point of the center line of the satellite's FOV and the Earth:

  f1 = X*lamb - x_sphere                                # Equation 1
  f2 = Y*lamb - y_sphere                                # Equation 2 
  f3 = Z*lamb - z_sphere                                # Equation 3 
  f4 = (lamb*X)**2 + (lamb*Y)**2 + (lamb*Z)**2 - int(r**2)   # Equation 4 

  (neg,pos) = nonlinsolve((f1,f2,f3,f4), (x_sphere,y_sphere,z_sphere,lamb)) # Returns the two intersection points as a tuple couple 



  # Make sure we are getting the nearest point:

  if neg[3] > 0: # If lambda is positive we have the correct point 

    x_sphere = float(neg[0])  # Assigns the x-value to the variable 
    y_sphere = float(neg[1])  # Assigns the y-value to the variable 
    z_sphere = float(neg[2])  # Assigns the z-value to the variable 

  else: # Otherwise we are backtracking 

  	x_sphere = float(pos[0])  # Assigns the x-value to the variable 
  	y_sphere = float(pos[1])  # Assigns the y-value to the variable 
  	z_sphere = float(pos[2])  # Assigns the z-value to the variable 

  

  # Now we need to rotate about the y-axis to adjust the latitudes and about z-axis to adjust the longitudes
  # To do that we calculate the difference in longitude between (0,0) and the intersection point.
  # For that purpose we apply a little bit of trigonometry: 



  # I do not actually remember how I made the rest of this work so I will comment on this later:
  # --------------------------------------------------------------------------------------------

  # Latitude of intersection point:

  lat = np.arcsin(z_sphere/r)

  # Radius of new circle:

  rprime = r*math.sin(math.pi/2 - lat)

  # Distance between 0,0 and intersection point:

  s = math.sqrt((x_sphere - rprime)**2 + y_sphere**2)

  # Longitude of intersection point:

  lon = np.arccos(1 - ((s**2)/(2*rprime**2)))

  # Corrects longitude sign:

  if y_sphere < 0:

  	lon = -lon 

  # 3) LATITUDE ROTATION METHOD 

  # Refer to Rodriguez's Rotation Formula on a sphere.
  # Angle of rotation is the lat difference between center of equator image and center of intersection point. 

  # Latitude rotation loop:
  
  x_lat = np.zeros((x.shape[0],x.shape[1]))
  y_lat = np.zeros((y.shape[0],y.shape[1]))
  x_lat = x_lat + 999
  y_lat = y_lat + 999

  ct1 = 0 

  while ct1 < y.shape[0]:

   ct2 = 0 

   while ct2 < y.shape[1]:

    if abs(y[ct1][ct2]) != 999:

     x_spherical = r*math.cos(math.pi*(y[ct1][ct2])/180)*math.cos(math.pi*(x[ct1][ct2])/180)
     y_spherical = r*math.cos(math.pi*(y[ct1][ct2])/180)*math.sin(math.pi*(x[ct1][ct2])/180)
     z_spherical = r*math.sin(math.pi*(y[ct1][ct2]/180))

     beta = -lat

     k = np.array([0,1,0])
     a = np.array([x_spherical,y_spherical,z_spherical])

     b = math.cos(beta)*a + math.sin(beta)*(np.cross(k,a)) + np.dot(k,a)*(1 - math.cos(beta))*k

     # I now have the cartesian coordinates of my rotation matrix. Easy: 

     phi = math.atan2(b[1],b[0])

     # theta = 180*((np.arctan(math.sqrt(b[0]**2 + b[1]**2)/(b[2]))))/math.pi

     theta = np.arccos(b[2]/r)
      
     result = 90 - (180*theta)/math.pi

     x_rotated = r*math.sin(theta)*math.cos(phi)
     y_rotated = r*math.sin(theta)*math.sin(phi)
     z_rotated = r*math.cos(theta)

     y_lat[ct1][ct2] = result
     x_lat[ct1][ct2] = (180*phi)/math.pi

    ct2 += 1

   ct1 += 1 

  # 3) LONGITUDE ROTATION METHOD 

  # Unlike the complicated method used above, this is a simple addition process.
  # Angle of rotation is the lon difference between center of equator image and center of intersection point. 
  
  # Longitude rotation loop:
  
  x_lon = np.zeros((x.shape[0],x.shape[1]))
  y_lon = np.zeros((y.shape[0],y.shape[1]))
  x_lon = x_lat + 999
  y_lon = y_lat + 999

  ct1 = 0 

  while ct1 < x.shape[0]:

   ct2 = 0 

   while ct2 < x.shape[1]:

    if abs(x_lat[ct1][ct2]) != 999:

     x_spherical = r*math.cos(math.pi*(y_lat[ct1][ct2])/180)*math.cos(math.pi*(x_lat[ct1][ct2])/180)
     y_spherical = r*math.cos(math.pi*(y_lat[ct1][ct2])/180)*math.sin(math.pi*(x_lat[ct1][ct2])/180)
     z_spherical = r*math.sin(math.pi*(y_lat[ct1][ct2]/180))

     beta = lon

     k = np.array([0,0,1])

     a = np.array([x_spherical,y_spherical,z_spherical])

     b = math.cos(beta)*a + math.sin(beta)*(np.cross(k,a)) + np.dot(k,a)*(1 - math.cos(beta))*k

     phi = math.atan2(b[1],b[0])

     theta = np.arccos(b[2]/r)
      
     if theta <= 90:

       result = 90 - (180*theta)/math.pi

     elif theta > 90:

       result = - (180*theta)/math.pi - 90
     
     x_rotated = r*math.sin(theta)*math.cos(phi)
     y_rotated = r*math.sin(theta)*math.sin(phi)
     z_rotated = r*math.cos(theta)

     y_lon[ct1][ct2] = result
     x_lon[ct1][ct2] = (180*phi)/math.pi
      
    ct2 += 1

   ct1 += 1 
  
  return(x_lon,y_lon)
  

