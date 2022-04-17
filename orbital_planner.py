# Ronnie Frank Pires Stone 
# Satellite Earth Imaging Project 
# CLASP Department - University of Michigan Ann Arbor
# 5) Sample Orbit Propagator 

# Importing libraries:

import math 
import numpy as np 

def orbital_planner(nSats, rOrbit, nTimes, time):

   dtor = np.pi/180.0
   
   rOrbit = float(rOrbit)
   mu = 3.99e14
   vOrbit = np.sqrt(mu/(rOrbit*1000.0))
   period = 2*np.pi*(rOrbit*1000.0)/vOrbit
   PercentOfOrbit = time/period
   StartTheta = np.pi / 2.0 * 1.01 # math.pi
   EndTheta = StartTheta + 2.0*np.pi * PercentOfOrbit

   # nSats = number of satellites 
   # rOrbit = orbital radius
   # nTimes = number of pictures

   t = np.linspace(StartTheta,EndTheta,nTimes)

   # Note: 0 -> PI (Northern Hemisphere)
   # Note: 0 -> -PI (Southern Hemisphere) 

   l = len(t)

   mx = np.zeros([nSats,l])
   my = np.zeros([nSats,l])

   x = np.zeros(l)
   y = np.zeros(l)
        
   j = 0

   while j < nSats:

      i = 0

      while i < l:

         x[i] =  rOrbit*math.cos(t[i])
         y[i] =  rOrbit*math.sin(t[i])

         i += 1 

      mx[j] = x
      my[j] = y

      t = t + (2*math.pi)/nSats

      j += 1

   return mx, my
