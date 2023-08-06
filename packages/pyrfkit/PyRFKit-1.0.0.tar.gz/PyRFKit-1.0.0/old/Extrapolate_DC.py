import skrf as rf
import numpy as np
from scipy.interpolate import interp1d
from typing import Optional


def extrapolate_dc(s ,NrPointsToUse: int = 10,Scale: list = [],Method: str = None,out: Optional[rf.Network] = None) -> float:
    '''
    OPT_Vars = {
        "PlotResults": 0,
        "NrPointsToUse": 10,
        "Scale": [],
        "Method": []
    }
    #loop through all variable input
    for k, v in varargin.items():
        #checks if varargin input is in the dictionary that stores the optional input.
        #this check is case insensitive for easier input
        if k.lower() in set(x.lower() for x in OPT_Vars):
            OPT_Vars[k] = v #replaces defalt value with variable input value
    '''
    #s = spar.s
    #s = np.transpose(s, [1, 2, 0])
    #shape = s.shape
    s = np.squeeze(s)
    s = np.transpose(s[:])
    #s = np.asarray(s)
    #s = s.flatten()

    NrFreqPonts = len(s)
    NrPointsInInterpolation = min(NrFreqPonts,NrPointsToUse)

    if not Scale:
        InterpolationScale = list(range(-NrPointsInInterpolation,0))+ list(range(1,1+NrPointsInInterpolation))
        if len(InterpolationScale) == 1:
            InterpolationScale = InterpolationScale[0]
        FinalScale = list(range(-NrPointsInInterpolation,NrPointsInInterpolation+1))
        if len(FinalScale) == 1:
            FinalScale = FinalScale[0]
        Scale = [range(1,NrFreqPonts+1)]

    else:
        Scale = np.asarray(Scale).flatten()
        InterpolationScale = list(-Scale[range(NrPointsInInterpolation-1,-1,-1)])+ list(Scale[range(0,NrPointsInInterpolation+1)])
        if len(InterpolationScale) == 1:
            InterpolationScale = InterpolationScale[0]
        FinalScale = list(-Scale[range(NrPointsInInterpolation-1,-1,-1)])+list(Scale[range(0,NrPointsInInterpolation)])
        if len(FinalScale) == 1:
            FinalScale = FinalScale[0]
        FinalScale.insert(int(len(FinalScale)/2),0)

    #getting sligtly different values for this. probaby a rounding error when calculating s
    absyvoorinterpolatie = list(np.flip(abs(s[range(0,NrPointsInInterpolation)])))+ list(abs(s[range(0,NrPointsInInterpolation)]))
    absxvoorinterpolatie = InterpolationScale
    absinterpolatie_result = interp1d(absxvoorinterpolatie,absyvoorinterpolatie,fill_value = 'extrapolate' ,kind = 'cubic') #ask adam G about this in matlab
    absDC_value = absinterpolatie_result(0)
    # absDC_value = absinterpolatie_result.y[NrPointsInInterpolation]
    if absDC_value > 1:
        absDC_value = 1
    if absDC_value <= 0:
        absDC_value = 0

    absDC_value = np.sign(np.real(s[0]))*absDC_value

    realyvoorinterpolatie = list(np.flip(np.real(s[range(0,NrPointsInInterpolation)])))+ list(np.real(s[range(0,NrPointsInInterpolation)]))
    realxvoorinterpolatie = InterpolationScale
    realinterpolatie_result = interp1d(realxvoorinterpolatie,realyvoorinterpolatie,fill_value = 'extrapolate',kind = 'cubic')
    realDC_value = realinterpolatie_result(0)
    #realDC_value = realinterpolatie_result.y[NrPointsInInterpolation +1]

    dbyvroorinterpolatie = list(np.flip(afrp.db.dB(s[range(0,NrPointsInInterpolation)])))+list(afrp.db.dB(s[range(0,NrPointsInInterpolation)]))
    dbsxvoorinterpolatie = InterpolationScale
    dbinterpolatie_result = interp1d(dbsxvoorinterpolatie,dbyvroorinterpolatie,fill_value = 'extrapolate',kind = 'cubic')
    dbDC_value_dB = dbinterpolatie_result(0)
    #dbDC_value_dB = dbinterpolatie_result.y[NrPointsInInterpolation+1]
    if dbDC_value_dB>0:
        dbDC_value_dB = 0
    dbDC_value = np.sign(np.real(s[0]))*(10**(dbDC_value_dB/20.0))

    if realDC_value<-1:
        realDC_value = -1
    if realDC_value>1:
        realDC_value = 1

    if not Method:
        if float(absDC_value)>0.5:
            Method = "ABS"
        else:
            Method = "REAL"

    if Method == "ABS":
        DC_value = absDC_value
    elif Method == "DB":
        DC_value = dbDC_value
    else:
        DC_value = realDC_value



    '''
    if PlotResults is True or 1:
        newData = np.insert(s[range(0,NrFreqPonts)],0 ,DC_value)

        newData1 = s[0:NrPointsInInterpolation]
        mx = max(2*NrPointsInInterpolation,30)
        fig, ((ax1,ax2),(ax3,ax4))= matplotlib.pyplot.subplots(nrows =2,ncols=2)
        scale = list(Scale[0])


        ax1.plot([0]+scale,np.real(newData),color = 'red')
        ax1.plot(scale[0:NrPointsInInterpolation],np.real(newData1),color = 'green')
        ax1.plot(0,np.real(newData[0]),'bx')
        ax1.set_xlabel("Sample point")
        ax1.set_title('REAL')
        ax1.set_xlim(0,mx)


        ax2.plot([0]+scale,np.imag(newData),color = 'red')
        ax2.plot(scale[0:NrPointsInInterpolation],np.imag(newData1),color = 'green')
        ax2.plot(0,np.imag(newData[0]),'bx')
        ax2.set_title('IMAG')
        ax2.set_xlim(0,mx)
        ax2.set_xlabel('Sample point')


        ax3.plot([0]+scale,afrp.db.dB(newData),color = 'red')
        ax3.plot(scale[0:NrPointsInInterpolation],afrp.db.dB(newData1),color = 'green')
        ax3.plot(0,afrp.db.dB(newData[0]),'bx')
        ax3.set_title('dB')
        ax3.set_xlim(0,mx)
        ax3.set_xlabel('Sampel point')


        ax4.plot([0]+scale,np.angle(newData),color = 'red')
        ax4.plot(scale[0:NrPointsInInterpolation],np.angle(newData1),color = 'green')
        ax4.plot(0,np.angle(newData[0]),'bx')
        ax4.set_title('Phase')
        ax4.set_xlabel('Sample point')
        ax4.set_xlim(0,mx)
        matplotlib.pyplot.show()

    '''

    #sdata_dc = np.insert(s,0,DC_value)
    return DC_value#,sdata_dc

#newSpar = rf.Network(r"C:\Users\jonb\Documents\20190802_T1380302_Comparison_Old_to New\RAW\NewM_NewF.s32p")
#Extrapolate_DC(newSpar.s[:,0,0])



#import csv
#paths = [r'C:\Users\jonb\Documents\20190802_T1380302_Comparison_Old_to New\RAW\NewM_NewF.s32p',r'C:\Users\jonb\Documents\20190802_T1380302_Comparison_Old_to New\RAW\NewM_NewF_Reordered.s32p'
#    ,r'C:\Users\jonb\Documents\20200124_MAGICMIRROR_NVACX\RAW\WITHOUT_MM.s32p',r'C:\Users\jonb\Documents\20190918_T1426301_5mm_Webfacing_Report\RAW\Measurement_Rev0.s32p'
#    ,r'C:\Users\jonb\Documents\20200115_T1543401_NVAM_5\RAW\NVAM_5.s20p',r'C:\Users\jonb\Documents\20190802_T1380302_Comparison_Old_to New\RAW\a.s4p']
#val = [0,0]
#valScale = [0,0]
#valMethABS = [0,0]
#valMethDB = [0,0]
#valMethREAL = [0,0]
#valNmToUse = [0,0]
#for p in paths:
#    spar = rf.Network(p)
#    s = spar.s
#    sz = s.shape[1]
#    for x in range(0,sz):
#        for y in range(0,sz):
#            sdatatmp = s[:,x,y]
#            val.append(Extrapolate_DC(sdatatmp))
#           # valScale.append(Extrapolate_DC(sdatatmp, Scale = [range(2,12)]))
#            valMethABS.append(Extrapolate_DC(sdatatmp,Method = "ABS"))
#            valMethDB.append(Extrapolate_DC(sdatatmp,Method = "DB"))
#            valMethREAL.append(Extrapolate_DC(sdatatmp,Method = "REAL"))
#            valNmToUse.append(Extrapolate_DC(sdatatmp,NrPointsToUse=20))

#finalM = val+valNmToUse+valMethABS+valMethDB+valMethREAL
#with open(r'tests\results.csv') as csvfile:
#    reader = csv.reader(csvfile)
#    i = 0
#    for row in reader:
#        for col in row:
#            if float(col) == 0 and float(finalM[1]) == 0:
#                eps = 1
#            elif float(col) == 0:
#                col = 0.00000000001
#                eps = col/float(finalM[i])
#            else:
#                eps = float(col)/float(finalM[i])
#            if eps is not None:
#                if eps < 0.9999 or eps > 1.001:
#                    print(col+"error in value")
#                else:
#                    print(col)
#                i = i + 1


