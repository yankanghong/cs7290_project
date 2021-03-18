#!/bin/bash
## download traces based on spec2017_simpoint.txt
mkdir -p $PWD/../traces/dpc3_traces
while read LINE
do
    if [[ ${LINE:0:1} != '#' ]]  
    then
        wget -P $PWD/../traces/dpc3_traces -c http://hpca23.cse.tamu.edu/champsim-traces/speccpu/$LINE
    fi
done < spec2017_simpoint.txt
