import numpy as np
import skrf as rf
import afrp

#very simpified auto port detection for networks
#
#Port Mapping output list is set up like so:
#   The index of a cell is a port
#   The value at an index is a port
#   Those two values make a through
#   EX:
#       idx:  0  1  2  3
#       val: [1, 0, 3, 2]
#       Here you see the index value pair is a through and both sides
#       are containd in the array. This is so one can look up any port
#       and see where it is connected.
def getPortMapping(net: rf.network):

    num_ports=net.s.shape[1]
    
    Port_Mapping=[-1] * net.s.shape[1]
    thru_ratio=0.5
    S = abs(net.s[0,:,:])
    #loop through the magnitude of all the positions
    #in the s matrix at the first frequency point
    for i in range(num_ports):
        maxS = 0
        tmpRow = []
        for j in range(num_ports):
            tmpRow.append(S[i,j])
            if S[i,j] > maxS:
                maxS = S[i,j]
                

        if maxS == 0:
            print("ERROR: No through found for port: "+i)
            return
        #devide all point in a row by the max mag
        row = tmpRow/maxS
        #for all positions in the row after above calculation, look of all poisitions
        #greater than or equal to 0.5. This says most of the energy is going to those ports
        for idx,mag in enumerate(row):
            if mag >= thru_ratio:
                if i != idx:
                    if Port_Mapping[i] == -1:
                        Port_Mapping[i]=idx
                    else: 
                        #if more than 1 place in the row has a value > 0.5 
                        #then a open, spliter, or joiner exists
                        print("Warning: Splitter/Joiner/Open detected!!")
                        Port_Mapping[i]=[Port_Mapping[i],idx]
        if Port_Mapping[i] == -1:
            print("ERROR: No through found for port: "+i)
            return
    return Port_Mapping
    
#for testing 
#net = rf.Network(r"C:\Users\jonb\Documents\20190802_T1380302_Comparison_Old_to New\RAW\NewM_NewF.s32p")
#print(getPortMapping(net))