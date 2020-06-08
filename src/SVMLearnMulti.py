
import sys
import os
import datetime
import random

sourceFile = sys.argv[1]
(sourceFilePath, sourceFileName) = os.path.split(sourceFile)
logFile = sys.argv[2]


version = '.'.join(sys.version.strip().split(' ')[0].split('.')[0:2])
pythonCommand = "python"+version

path = os.path.split(os.path.realpath(__file__))[0]

javaOutputInfo = 'info.tmp'


parse_oldtime=datetime.datetime.now()

generatePythonLoopCommand = [
	'java', 
	'-jar', 
	os.path.join(path,'../Boogie2python/boogie2pythonMulti.jar'), 
	os.path.join(path,sourceFilePath,sourceFileName), 
	'0', 
	os.path.join(path,'OneLoop.py'), 
	os.path.join(path,javaOutputInfo)
]

os.system(' '.join(generatePythonLoopCommand))


parse_newtime = datetime.datetime.now()
from LearnMultiRanker import *
from OneLoop import L
rank_oldtime=datetime.datetime.now()

result, rf_list = LearnMultiRanker(L, 4, "MINI", 1, (), ())
if result == "FINITE":
    printSummary(len(rf_list), result, rf_list)
else:
    print("--------------------LEARNING MULTIPHASE SUMMARY-------------------")
    print("LEARNING RESULT: ", result)
rank_newtime=datetime.datetime.now()
f = open(os.path.join(logFile,'AnalysisTimeForALL.log'),'a')
f.write('Time For %s Is ---> %f ms\n' %(os.path.join(sourceFilePath,sourceFileName),float((parse_newtime-parse_oldtime).total_seconds())*1000  + float((rank_newtime-rank_oldtime).total_seconds())*1000 ))
print('Time For %s Is ---> %f ms\n' %(os.path.join(sourceFilePath,sourceFileName),float((parse_newtime-parse_oldtime).total_seconds())*1000  + float((rank_newtime-rank_oldtime).total_seconds())*1000 ))
print('Program is terminating' if result=='FINITE' else (result if result =='UNKNOWN' else 'Program is non-terminating'))
