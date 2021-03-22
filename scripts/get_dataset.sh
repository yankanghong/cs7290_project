#!/bin/bash
## download dataset custom
DATASET_DIR="$PWD/../dataset"
mkdir -p ${DATASET_DIR}
while read LINE
do
    if [[ ${LINE:0:1} != '#' ]]  
    then
        echo $LINE
        wget -P ${DATASET_DIR} -c https://gtvault.sharepoint.com/sites/CS7290LoadStorePredictionProject/Shared%20Documents/dataset/$LINE.dat
        wget -P ${DATASET_DIR} -c https://gtvault.sharepoint.com/sites/CS7290LoadStorePredictionProject/Shared%20Documents/dataset/$LINE.lab
    fi
done < dataset_download_list.txt