'''
Created on 21st March.
@author:  
    Xuechao Sun (sunxc@ios.ac.cn)
'''

import numpy as np
from OneLoop import L
import time
import sys
import os
from util import *

def LearnRanker(templateFilePath, indexOfTemplate, x, y ):
    #templateFilePath = sys.argv[1]
    # listOfUxDimension = [int(x) for x in sys.argv[2].split(',')]
    #logPath = sys.argv[2]
    #exampleName = sys.argv[2]
    #############Log
    # if not os.path.exists(logPath):
    #     os.makedirs(logPath)
    # logFile = os.path.join(logPath,exampleName+".log")
    # f = open(logFile,'w')
    # f.write("")
    # f.close()
    # f = open(logFile,'a')

    #############template
    infoFile = open(os.path.join(templateFilePath,'Info'+str(indexOfTemplate)),'r')
    info = []
    for line in infoFile.readlines():
        line = line.strip()
        if line== '':
            continue
        info.append(line)
    listOfUxDimension= [int(x) for x in info]
    
    listOfUx = parse_template(templateFilePath,L[2],listOfUxDimension, indexOfTemplate)
    rf = NestedTemplate( #NestedRankingFunction(
        # list of U(x)
        listOfUx
        # list of C
        , [0.001] *len(listOfUx)
        # Delta
        , 0)
    # number of variables   

    ret = 'UNKNOWN'
   # oldtime=datetime.datetime.now()
    try:
        ret,new_x,new_y = train_ranking_function(L, rf, x, y)
    except Exception as e:
        # print("ERROR:\n" + str(e)+"\n")
        print( "\n" + str(e)+"\n")
        new_x,new_y  = x,y
    #newtime=datetime.datetime.now()
    #f = open(os.path.join(logPath,'AnalysisTimeForTraining.log'),'a')
    #f.write('Time For %s Is ---> %f ms\n' %(templateFilePath,float((newtime-oldtime).total_seconds())*1000 ))

    #f.close()
    if ret== 'FINATE':
        print(rf)
        # print('#num_pos = ', rf.get_num_of_pos(), ' #num_neg = ', rf.get_num_of_neg())
    return ret,new_x,new_y

#if __name__ == '__main__':
  #  main()
