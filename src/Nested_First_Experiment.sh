#!/bin/bash

# format: %s.%N 
function getTiming() {     
	start=$1     
	end=$2         
	start_s=$(echo $start | cut -d '.' -f 1)     
	start_ns=$(echo $start | cut -d '.' -f 2)     
	end_s=$(echo $end | cut -d '.' -f 1)     
	end_ns=$(echo $end | cut -d '.' -f 2)     
	time=$(( ( 10#$end_s - 10#$start_s ) * 1000 + ( 10#$end_ns / 1000000 - 10#$start_ns / 1000000 ) ))     
	echo "$time ms" 
	echo "Time for "$3": "$time" ms" >> $4	
} 

function dealFile(){
	
	startTime=`date +'%s.%N'`

	timeout 5m python3 SVMLearn.py $1 $2 | tee $2"/"$3".log"

	endTime=`date +'%s.%N'`
	getTiming $startTime $endTime $1 $2"/summarize.log"	
}

function ergodic(){
  for file in `ls $1`  
  do
    if [ -d $1"/"$file ]
    then
      ergodic $1"/"$file
    else
      local path=$1"/"$file 
      local name=$file      
      local size=`du --max-depth=1 $path|awk '{print $1}'` 
      echo $name  $size $path 
      dealFile $path $2 $file
    fi
  done
}
IFS=$'\n' #must contains this command.

echo $1$2
INIT_PATH=$1
echo $INIT_PATH
starttime=`date +'%Y-%m-%d-%H-%M-%S'`
Log_FILE=$2"/Log_File_"$starttime
`mkdir -p $Log_FILE`
`touch $Log_FILE"/summarize.log"`
echo "" >> ${Log_FILE}"/AnalysisTimeForTraining.log"
echo "" >> ${Log_FILE}"/AnalysisTimeForALL.log"
ergodic $1 ${Log_FILE}

#python3.5 LearnRanker.py Log
