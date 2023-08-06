import skrf as rf
import afrp
import numpy as np
from scipy.interpolate import interp1d
import matplotlib 
from typing import Optional
from Extrapolate_DC import Extrapolate_DC

#input is a NxN sparameter/network
#optional input:
#   Number of ponits to use (defalt, NrPointsToUse = 10)
#   Scale (defalt, Scale = [])
#   Method (defalt, Method = None) must be a string "ABS", "REAL", or "DB"

#returns a NxN matrix of Extrapolated values
def Extrapolate_Whole_DC(spar: rf.Network, NrPointsToUse: int = 10,Scale: list = [],Method: str = None,out: Optional[rf.Network] = None):
    
    newSpar = spar
    value = np.zeros(shape = (newSpar.s.shape[1],newSpar.s.shape[2]))
    for i in range(newSpar.s.shape[1]):
        for j in range(newSpar.s.shape[2]):
            #value[(i*newSpar.s.shape[2])+j] = Extrapolate_DC(spar.s[:,i,j],NrPointsToUse = NrPointsToUse,Scale = Scale,Method = Method,out = spar)
            value[i,j] = Extrapolate_DC(newSpar.s[:,i,j],NrPointsToUse = NrPointsToUse,Scale = Scale,Method = Method,out = spar)

    return value

    