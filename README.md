# CS7290 Memory Dependency Prediction Project

Some resources: https://github.com/ChampSim/ChampSim

### Dependency
Python 3.7, PyTorch >= 1.7, torchvision >= 0.8

## Data Preparation 

### Trace download
If you want to download the original traces of SPEC2017, run `get_dpc3_traces.sh` to get the trace data.
```sh
cd scripts
./get_dpc3_traces.sh
```
### Dataset download or generate

* If you want to download pre-generated dataset, ~~run `get_dataset.sh`. Adjust what dataset to download by manipulating `dataset_download_list.txt`~~  
Just access and download from [here](https://gtvault.sharepoint.com/sites/CS7290LoadStorePredictionProject/Shared%20Documents/dataset/)

* If you want regenerate or customized generate dataset, run `trace_to_dataset.sh` to transform trace to training/validation data. But the **Trace download** step has to be done first.
```sh
cd scripts
./trace_to_dataset.sh
```
