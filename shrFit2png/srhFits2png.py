# -*- coding: utf-8 -*-
"""
Created on Mon May 30 02:54:01 2016

@author: Sergey
"""
import numpy as NP
import matplotlib.pyplot as PL
from skimage.transform import warp, AffineTransform
from astropy import constants
from sunpy import coordinates
import os
import time

from srhFitsFile_1 import SrhFitsFile
from BadaryRAO import BadaryRAO

freqs5 = [2, 5, 8, 11, 14]
#freqs32 = int(NP.linspace(0, 31, 32))
scan = 30
path='/home/ivan/xsrhedik/fits/'
path_out = '/home/ivan/xsrhedik/png'
files = os.listdir(path)
for file in files:
    if file.endswith('.fit') and file.endswith('mf', 0, 2):
        print(file)

        sF = SrhFitsFile(os.path.join(path, file), 512);
        RAO = BadaryRAO(sF.dateObs.split('T')[0])
        
        if len(sF.freqList) == 15:
            freqs = freqs5
        else:
            freqs = NP.linspace(0, len(sF.freqList)-1, len(sF.freqList)).astype(int)
            
        for freq in freqs:
            for scan in range(0,1):
                sF.setCalibIndex(scan);
                sF.setFrequencyChannel(freq);
                hAngle = sF.omegaEarth * (sF.freqTime[freq, scan] - RAO.culmination)
                delta = RAO.declination
                phi = RAO.observatory.lat
                
                cosP = NP.sin(hAngle) * NP.cos(delta)
                cosQ = NP.cos(hAngle) * NP.cos(delta) * NP.sin(phi) - NP.sin(delta) * NP.cos(phi)
                gP =  NP.arctan(NP.tan(hAngle)*NP.sin(delta));
                gQ =  NP.arctan(-(NP.sin(delta) / NP.tan(hAngle) + NP.cos(delta) / (NP.sin(hAngle)*NP.tan(phi))));
                
                if hAngle > 0:
                    gQ = NP.pi + gQ;
                g = gP - gQ;
                  
                FOV_p = 2.*(constants.c / (sF.freqList[freq]*1e6)) / (RAO.base*NP.sqrt(1. - cosP**2.));
                FOV_q = 2.*(constants.c / (sF.freqList[freq]*1e6)) / (RAO.base*NP.sqrt(1. - cosQ**2.));
                
                FOV = NP.deg2rad(2*4.91104*511./3600.)
                wP  = int(512*FOV/FOV_p.to_value());
                wQ  = int(512*FOV/FOV_q.to_value());
                
                sF.vis2uv(scan,phaseCorrect=True);
                sF.uv2lmImage();
                data = sF.lcp
                
                pqMatrix = NP.zeros((3,3))
                pqMatrix[0, 0] =  NP.cos(gP) - NP.cos(g)*NP.cos(gQ)
                pqMatrix[0, 1] = -NP.cos(g)*NP.cos(gP) + NP.cos(gQ)
                pqMatrix[1, 0] =  NP.sin(gP) - NP.cos(g)*NP.sin(gQ)
                pqMatrix[1, 1] = -NP.cos(g)*NP.sin(gP) + NP.sin(gQ)
                pqMatrix /= NP.sin(g)**2.
                pqMatrix[2, 2] = 1.
                
                scale = AffineTransform(scale=(256/wP,256/wQ))
                rotate = AffineTransform(rotation = NP.deg2rad(coordinates.get_sun_P(sF.dateObs).to_value()))
                shift = AffineTransform(translation=(-256,-256))
                matrix = AffineTransform(matrix=pqMatrix)
                back_shift = AffineTransform(translation=(256,256))
                
                dataResult0 = warp(data.real,(shift + (scale + back_shift)).inverse)
                dataResult1 = warp(dataResult0,(shift + (matrix + back_shift)).inverse)
                
                fig, ax = PL.subplots()
                ax.set_aspect(1)
                ax.set_yticks([])
                ax.set_xticks([])
                res = ax.imshow(dataResult1, cmap = 'hot')
                name = sF.dateObs.split('T')[0] + '_' + time.strftime("%H:%M:%S", time.gmtime(7937.907296))
                name += '_' + str('%d' % sF.freqList[freq]) + '_' + str(scan) + '.png'
                PL.savefig(os.path.join(path_out, name))
                PL.close()
