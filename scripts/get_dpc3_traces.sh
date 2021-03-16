#!/bin/bash
## download traces based on spec2017_simpoint.txt
mkdir -p $PWD/../dpc3_traces
while read LINE
do
    wget -P $PWD/../dpc3_traces -c http://hpca23.cse.tamu.edu/champsim-traces/speccpu/$LINE
done < spec2017_simpoint.txt
