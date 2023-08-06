import matplotlib.pyplot as plt
import numpy as np
import skrf as rf
import afrp 



def plotTest(spar: rf.Network, ports: list =[], ax: plt.axes = None):

    if ax is None:
        #initalize ax as new axes
        fig, ax= plt.subplots()
    
    
    ax.plot(np.real(afrp.db.dB(spar.s[:,0,1])),color = 'red')
    #spar.plot_s_db()
    plt.show()
       
    #plot \/

spar = rf.Network(r'C:\Users\jonb\Documents\20190802_T1380302_Comparison_Old_to New\RAW\NewM_NewF.s32p')
plotTest(spar)