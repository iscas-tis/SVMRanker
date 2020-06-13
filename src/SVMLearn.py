
import sys
import os
import datetime
import random
from LearnRanker import *
from LearnMultiRanker import *

def generateTemplate(templateFullPath, indexOfTemplate, numOfVar):
	if indexOfTemplate == 0:
		generateLinearTemplateFile(templateFullPath, indexOfTemplate, 1,numOfVar)
	elif indexOfTemplate == 1:
		generateNonLinearTemplateFile(templateFullPath, indexOfTemplate,1,numOfVar)
	elif indexOfTemplate == 2:
		generateLinearTemplateFile(templateFullPath, indexOfTemplate, 3,numOfVar)
	elif indexOfTemplate == 3:
		generateNonLinearTemplateFile(templateFullPath, indexOfTemplate,3,numOfVar)
	elif indexOfTemplate == 4:
		generateLinearTemplateFile(templateFullPath, indexOfTemplate, 5,numOfVar)
	elif indexOfTemplate == 5:
		generateNonLinearTemplateFile(templateFullPath, indexOfTemplate,5,numOfVar)
	elif indexOfTemplate == 6:
		generateLinearTemplateFile(templateFullPath, indexOfTemplate, 7,numOfVar)
	elif indexOfTemplate == 7:
		generateNonLinearTemplateFile(templateFullPath, indexOfTemplate,7,numOfVar)


def generateNonLinearTemplateFile(templateFullPath, indexOfTemplate, numOfG, numOfVar):
	# if os.path.exists(os.path.join(templateFullPath,'template'+str(indexOfTemplate))):
	# 	return
	f_info = open(os.path.join(templateFullPath,'Info'+str(indexOfTemplate)),'w')
	result = ''
	for i in range(numOfG):
		rows = random.randint(max(1, numOfVar-2), numOfVar+2)
		for j in range(rows):
			for k in range(numOfVar+1):
				if k==numOfVar:
					result +="1"
				else:
					randomvalue = random.randint(-4,4)
					if randomvalue == 4:
						randomvalue = 0.5
					elif randomvalue == -4:
						randomvalue = -0.5
					result +=str(randomvalue)+","
			result += " \n"
		result+="\n"
		f_info.write(str(rows)+'\n')
	f_info.close()
	f_template = open(os.path.join(templateFullPath,'template'+str(indexOfTemplate)),'w')
	f_template.write(result)
	f_template.close()


def generateLinearTemplateFile(templateFullPath, indexOfTemplate, numOfG, numOfVar):
	# if os.path.exists(os.path.join(templateFullPath,'template'+str(indexOfTemplate))):
	# 	return
	f = open(os.path.join(templateFullPath,'template'+str(indexOfTemplate)),'w')
	result = ''
	for i in range(numOfG):
		for j in range(numOfVar+1):
			for k in range(numOfVar+1):
				if k==numOfVar:
					result +="1"
				elif (j==k ):
					result +="1,"
				else:
					result +="0,"
			result += " \n"
		result+="\n"
	f.write(result)
	f.close()
	f = open(os.path.join(templateFullPath,'Info'+str(indexOfTemplate)),'w')
	for i in range(numOfG):
		f.write(str(numOfVar+1)+'\n')
	f.close()

def array_2_nospace_str(array):
	result = ""
	for x in array:
		result+=str(x)+','
	return result[:-1]


def SVMLearnNested(sourceFilePath, sourceFileName, 
				   templatePath, templateFileName, 
				   Info, logFolder, 
				   parse_oldtime, parse_newtime,
				   sample_strategy):
	rank_oldtime=datetime.datetime.now()
	rf_list = []
	if int(Info[0]) == 0:
		numOfTemplate = 1#8
		templateFullPath = os.path.join(os.path.split(os.path.realpath(__file__))[0],templatePath,templateFileName)
		print("template full path", templateFullPath, templateFileName)
		if not os.path.exists(templateFullPath):
			os.makedirs(templateFullPath)
		x,y = (),()
		i = 0
		for i in range(numOfTemplate):
			tempalate_start = datetime.datetime.now()
			print('------Using Template %d -----------'% i)
			generateTemplate(templateFullPath, i, int(Info[1]))
			result, x, y, rf= LearnRanker(os.path.join(os.path.split(os.path.realpath(__file__))[0],templatePath,templateFileName), i, sample_strategy, (), ())
			template_end = datetime.datetime.now()
			print(result)
			print('Time For Template %d Is--->%f ms\n' % (i, float((tempalate_start-template_end).total_seconds())*1000))
			rf_list.append(rf)
			if result != 'UNKNOWN':
				break
			i = (i+1)%numOfTemplate
	rank_newtime=datetime.datetime.now()
	f = open(os.path.join(logFolder,'AnalysisTimeForALL.log'),'a')
	f.write('Time For %s Is ---> %f ms\n' %(os.path.join(sourceFilePath,sourceFileName),float((parse_newtime-parse_oldtime).total_seconds())*1000  + float((rank_newtime-rank_oldtime).total_seconds())*1000 ))
	print('Time For %s Is ---> %f ms\n' %(os.path.join(sourceFilePath,sourceFileName),float((parse_newtime-parse_oldtime).total_seconds())*1000  + float((rank_newtime-rank_oldtime).total_seconds())*1000 ))
	print('Program is terminating' if result=='FINITE' else (result if result =='UNKNOWN' else 'Program is non-terminating'))
	return result, rf_list


def SVMLearnMulti(sourceFilePath, sourceFileName, 
				  logFolder, 
				  parse_oldtime, parse_newtime, 
				  sample_strategy, cutting_strategy, template_strategy):
	from OneLoop import L
	rank_oldtime=datetime.datetime.now()
	result, rf_list = LearnMultiRanker(L, 5, sample_strategy, cutting_strategy, template_strategy, 1, (), (), True)
	if result == "FINITE":
	    printSummary(len(rf_list), result, rf_list)
	else:
	    print("--------------------LEARNING MULTIPHASE SUMMARY-------------------")
	    print("LEARNING RESULT: ", result)
	rank_newtime=datetime.datetime.now()
	f = open(os.path.join(logFolder,'AnalysisTimeForALL.log'),'a')
	f.write('Time For %s Is ---> %f ms\n' %(os.path.join(sourceFilePath,sourceFileName),float((parse_newtime-parse_oldtime).total_seconds())*1000  + float((rank_newtime-rank_oldtime).total_seconds())*1000 ))
	print('Time For %s Is ---> %f ms\n' %(os.path.join(sourceFilePath,sourceFileName),float((parse_newtime-parse_oldtime).total_seconds())*1000  + float((rank_newtime-rank_oldtime).total_seconds())*1000 ))
	print('Program is terminating' if result=='FINITE' else (result if result =='UNKNOWN' else 'Program is non-terminating'))
	
	return result, rf_list


# def parsing_boogie(jarFile,fileName,outputPythonFile,outputInfoFile):
# 	jpype.startJVM(jpype.getDefaultJVMPath(), "-Djava.class.path=%s" %jarFile) 
# 	javaClass = jpype.JClass('main.MainForOne') 
# 	para = jpype.JArray(jpype.JString)([fileName,'0',outputPythonFile,outputInfoFile])
# 	javaClass.main(para)
# 	jpype.shutdownJVM()






'''
sourceFile = sys.argv[1]

logFile = sys.argv[2]

(sourceFilePath, sourceFileName) = os.path.split(sourceFile)


templatePath = 'template'
templateFileName = '.'.join([sourceFileName.strip(),'template'])
version = '.'.join(sys.version.strip().split(' ')[0].split('.')[0:2])
pythonCommand = "python"+version

path = os.path.split(os.path.realpath(__file__))[0]

javaOutputInfo = 'info.tmp'

parse_oldtime=datetime.datetime.now()
generatePythonLoopCommand = [
	'java', 
	'-jar', 
	os.path.join(path,'../Boogie2python/boogie2python.jar'), 
	os.path.join(path,sourceFilePath,sourceFileName), 
	'0', 
	os.path.join(path,'OneLoop.py'), 
	os.path.join(path,javaOutputInfo)
	]
os.system(' '.join(generatePythonLoopCommand))
# parsing_boogie(
# 	os.path.abspath(os.path.join(path,'../Boogie2python/boogie2python.jar')),
# 	os.path.join(path,sourceFilePath,sourceFileName), 
# 	os.path.join(path,'OneLoop.py'), 
# 	os.path.join(path,javaOutputInfo)
# 	)
Info = getLoopInfo()
parse_newtime = datetime.datetime.now()
from  LearnRanker import *
rank_oldtime=datetime.datetime.now()
#os.system('rm -f '+os.path.join(path,javaOutputInfo))
if int(Info[0]) == 0:
	numOfTemplate = 1#8
	templateFullPath = os.path.join(path,templatePath,templateFileName)
	if not os.path.exists(templateFullPath):
		os.makedirs(templateFullPath)
	x,y = (),()
	i = 0
	#while(True):
	for i in range(numOfTemplate):
		tempalate_start = datetime.datetime.now()
		print('------Using Template %d -----------'% i)
		generateTemplate(i, int(Info[1]))
		# learnRankFunctionCommand = [
		# 	'timeout 5m',
		# 	pythonCommand, 
		# 	os.path.join(path,'LearnRanker.py'), 
		# 	os.path.join(path,templatePath,templateFileName),
		# 	#array_2_nospace_str([int(Info[1])+1]*3), 
		# 	logFile,
		# 	sourceFileName
		# 	]
		#os.system(' '.join(learnRankFunctionCommand))
		result, x, y = LearnRanker(os.path.join(path,templatePath,templateFileName), i, (), ())
		template_end = datetime.datetime.now()
		print(result)
		print('Time For Template %d Is--->%f ms\n' % (i, float((tempalate_start-template_end).total_seconds())*1000))
		if result != 'UNKNOWN':
			break
		i = (i+1)%numOfTemplate
rank_newtime=datetime.datetime.now()
f = open(os.path.join(logFile,'AnalysisTimeForALL.log'),'a')
f.write('Time For %s Is ---> %f ms\n' %(os.path.join(sourceFilePath,sourceFileName),float((parse_newtime-parse_oldtime).total_seconds())*1000  + float((rank_newtime-rank_oldtime).total_seconds())*1000 ))
print('Time For %s Is ---> %f ms\n' %(os.path.join(sourceFilePath,sourceFileName),float((parse_newtime-parse_oldtime).total_seconds())*1000  + float((rank_newtime-rank_oldtime).total_seconds())*1000 ))
print('Program is terminating' if result=='FINITE' else (result if result =='UNKNOWN' else 'Program is non-terminating'))
'''