#!/usr/bin/env python

import re
import numpy as np
from datetime import datetime

#-----------------------------------------------------------------------------
# 
#-----------------------------------------------------------------------------

def read_iono_one_file(file_to_read):

    print(file_to_read)

    fpin = open(file_to_read,'r')

    IsDone = 0;

    Header = {}
    Header["nVars"] = 0
    Header["nTheta"] = 0
    Header["iTheta"] = -1
    Header["nPhi"] = 0
    Header["iPsi"] = -1
    Header["Vars"] = []
    Header["time"] = 0
    Header["filename"] = file_to_read

    IonoNorthData = {}
    IonoSouthData = {}

    while (IsDone == 0):

        line = fpin.readline()

        if (not line):
            IsDone = 1
        else:

            m = re.search(r"NUMERICAL VALUES",line)
            if m:
                line = fpin.readline()
                m = re.search(r"(\d+) ",line)
                if m:
                    Header["nVars"] = int(m.group(0))
                line = fpin.readline()
                m = re.search(r"(\d+) ",line)
                if m:
                    Header["nTheta"] = int(m.group(0))
                line = fpin.readline()
                m = re.search(r"(\d+) ",line)
                if m:
                    Header["nPhi"] = int(m.group(0))
                print(Header["nVars"],Header["nTheta"],Header["nPhi"])
    
            m = re.search(r"TIME",line)
            if m:
                t = []
                for i in range(7):
                    line = fpin.readline()
                    m = re.search(r"(\d+) ",line)
                    if m:
                        t.append(int(m.group(0)))
                Header["time"] = datetime(t[0],t[1],t[2],t[3],t[4],t[5],t[6])
                print(Header["time"])
    
            m = re.search(r"VARIABLE LIST",line)
            if m:
                for i in range(Header["nVars"]):
                    line = fpin.readline()
                    m = re.search(r"(\d+) (.+)",line)
                    if m:
                        Header["Vars"].append(m.group(2))
                iVar = 0;
                for var in Header["Vars"]:
                    m = re.search(r"Theta",var)
                    if m:
                        Header["iTheta_"] = iVar
                    m = re.search(r"Psi",var)
                    if m:
                        Header["iPsi_"] = iVar
                    iVar += 1
                    
    
            m = re.search(r"BEGIN NORTHERN HEMISPHERE",line)
            if m:
                Data = {}
                for iVar in range(Header["nVars"]):
                    Data[iVar] = []
                for iPhi in range(Header["nPhi"]):
                    for iTheta in range(Header["nTheta"]):
                        line = fpin.readline()
                        d = line.split()
                        for iVar in range(Header["nVars"]):
                            Data[iVar].append(float(d[iVar]))
                for iVar in range(Header["nVars"]):
                    iono = np.array(Data[iVar])
                    IonoNorthData[iVar] = iono.reshape((Header["nPhi"],Header["nTheta"]))
                            
            m = re.search(r"BEGIN SOUTHERN HEMISPHERE",line)
            if m:
                Data = {}
                for iVar in range(Header["nVars"]):
                    Data[iVar] = []
                for iPhi in range(Header["nPhi"]):
                    for iTheta in range(Header["nTheta"]):
                        line = fpin.readline()
                        d = line.split()
                        for iVar in range(Header["nVars"]):
                            Data[iVar].append(float(d[iVar]))
                for iVar in range(Header["nVars"]):
                    iono = np.array(Data[iVar])
                    iono = iono.reshape((Header["nPhi"],Header["nTheta"]))
                    iono = np.fliplr(iono)
                    IonoSouthData[iVar] = iono
                IonoSouthData[Header["iTheta_"]] = 180.0 - IonoSouthData[Header["iTheta_"]]
            
    fpin.close()

    return Header, IonoNorthData, IonoSouthData


