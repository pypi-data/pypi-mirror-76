import matlab.engine

def VP(dutDir,calDir,calMap,portMap,freq):
  
  eng = matlab.engine.start_matlab()
  eng.VPWrapper(dutDir,calDir,calMap,portMap,freq);
  
#Example    
#VP(r'C:\Users\jonb\Documents\20190802_T1380302_Comparison_Old_to New\RAW\NewM_NewF.s32p',r'C:\Users\jonb\Documents\20190802_T1380302_Comparison_Old_to New\CAL',{'C','C','D','D','B','B','A','A','D','D','C','C','A','A','B','B','G','G','H','H','F','F','E','E','H','H','G','G','E','E','F','F'},{1,3,5,6,9,10,13,14,17,18,21,22,25,26,29,30,2,4,8,7,12,11,16,15,20,19,24,23,28,27,32,31},0);
    