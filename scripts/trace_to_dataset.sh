#!/bin/bash

# Path to folders
DATA_DIR="$PWD/../data"
TRACE_DIR="${DATA_DIR}/traces"
DATASET_DIR="${DATA_DIR}/dataset"
GEN_DIR="$PWD/../src/data_generator"

# Parse args from command line
IW_SIZE=64
MAX_INSTR=1000000

POSITIONAL=()
while [[ $# -gt 0 ]]
do
key="$1"

case $key in
    -w|--window)
    IW_SIZE="$2"
    shift # past argument
    shift # past value
    ;;
    -n|--number)
    MAX_INSTR="$2"
    shift # past argument
    shift # past value
    ;;    
    *)    # unknown option
    echo "Unkown option encounter: ${key} "
    exit 1
    ;;
esac
done
set -- "${POSITIONAL[@]}" # restore positional parameters

echo "TRACE DIR      = ${TRACE_DIR}"
echo "DATASET_DIR    = ${DATASET_DIR}"
echo "INSTR WINDOW   = ${IW_SIZE}"
echo "MAX INSTR NUMBER   = ${MAX_INSTR}"
if [[ -n $1 ]]; then
    echo "Last line of file specified as non-opt/last argument:"
    tail -1 "$1"
fi


## transform trace to dataset
targets=( 
         "${TRACE_DIR}/dpc3_traces/600.perlbench_s-210B.champsimtrace.xz" 
          # "${TRACE_DIR}/dpc3_traces/628.pop2_s-17B.champsimtrace.xz" 
        )


## Start transform
if [ ! -d ${DATASET_DIR}/train ]; then
    echo "Create ${DATASET_DIR} directory..."
    mkdir -p ${DATASET_DIR}/train
    mkdir -p ${DATASET_DIR}/validate
fi

# Compile trace transformer
cd ${GEN_DIR}
echo
echo "Compile trace transformer..."
make clean
make -j4
echo

for i in "${targets[@]}"
do
    if [ -f "${i}" ]; then
        # -t: target(input), -o: output dir, -w: instruction window size
       ./trpr.o -t ${i} -o ${DATASET_DIR} -w ${IW_SIZE} -n ${MAX_INSTR}
    else
        echo "Error: ${i} doesn't exist..."
    fi
done