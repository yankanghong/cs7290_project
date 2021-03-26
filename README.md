# CS7290 Memory Dependency Prediction Project

Some resources: https://github.com/ChampSim/ChampSim

### Dependency
Python 3.7, PyTorch >= 1.7, torchvision >= 0.8

## Data Preparation 

### Trace 
If you want to download the original traces of SPEC2017, run `get_dpc3_traces.sh` to get the trace data. Manipulate the `spec2017_simpoint` to get desired traces
```sh
cd scripts
./get_dpc3_traces.sh
```
### Dataset 

#### Generate dataset
To generate or customized generate dataset, Use `trace_to_dataset.sh` to transform trace to training/validation data. 
```sh
cd scripts
./trace_to_dataset.sh [-w window_size] [-n max_instr]
```
`trace_to_dataset.sh` accepts optional arguments to customize the generation of dataset:
| Args | Meaning  | Default Value |
| :------------: |:---------------:| :---------------:| 
| -w      | define the instruction window size (aka. the column length of generated 2D matrix data/label) | 64 |
| -n     | maximum number of instructions before exit     |  1000000  |

Notice: remember to perform **Trace download** first.
#### Download pre-generated dataset

* *OUTDATED* ~~If you want to download pre-generated dataset, run `get_dataset.sh`. Adjust what dataset to download by manipulating `dataset_download_list.txt`  
Just access and download from [here](https://gtvault.sharepoint.com/sites/CS7290LoadStorePredictionProject/Shared%20Documents/dataset/)~~


