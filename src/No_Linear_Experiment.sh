#!/bin/bash

starttime=`date +'%Y-%m-%d-%H-%M-%S'`
Log_FILE=$3"/Log_File_"$starttime
`mkdir -p $Log_FILE`
`touch $Log_FILE"/non_linear.log"`
python3 LoopRanker.py $1 $2 | tee ${Log_FILE}"/non_linear.log"
