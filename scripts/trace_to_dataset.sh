#!/bin/bash

## transform trace to dataset
targets=( 
         "../traces/dpc3_traces/600.perlbench_s-210B.champsimtrace.xz" 
          # "../traces/dpc3_traces/628.pop2_s-17B.champsimtrace.xz" 
        #   "/etc/hosts" 
        )

dataset_dir="../dataset"

if [ ! -d ${dataset_dir} ]; then
    echo "Create ${dataset_dir} directory..."
    mkdir ${dataset_dir}
fi

cd ../traces
# 
echo "Compile trace transformer..."
make clean
make -j2

for i in "${targets[@]}"
do
    if [ -f "${i}" ]; then
       ../traces/trpr.o -t $i -o ${dataset_dir}
    else
        echo "Error: ${i} doesn't exist..."
    fi
done