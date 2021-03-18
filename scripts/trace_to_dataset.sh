#!/bin/bash

## transform trace to dataset
targets=( "../traces/dpc3_traces/600.perlbench_s-210B.champsimtrace.xz" 
        #   "../traces/dpc3_traces/600.perlbench_s-210B.champsimtrace.xz" 
        #   "/etc/hosts" 
        )

dataset_dir="../dataset"

cd ../traces
make

for i in "${targets[@]}"
do
   ../traces/trpr -t $i -o dataset_dir
done