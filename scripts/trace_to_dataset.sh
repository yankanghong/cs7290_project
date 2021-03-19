#!/bin/bash

## transform trace to dataset
targets=( 
        #  "../traces/dpc3_traces/600.perlbench_s-210B.champsimtrace.xz" 
          "../traces/dpc3_traces/628.pop2_s-17B.champsimtrace.xz" 
        #   "/etc/hosts" 
        )

dataset_dir="../dataset"

cd ../traces
make clean
make -j2

for i in "${targets[@]}"
do
   ../traces/trpr.o -t $i -o ${dataset_dir}
done