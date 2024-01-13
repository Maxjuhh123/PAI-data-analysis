# PAI-data-analysis
This repository contains code to be used for analyzing photoacoustic images. The codebase is divided into three directories which will be explained below.

## Resources
The `resources` directory contains two subdirectories: `data` and `output`. The data directory should contain `.csv` files describing diameter measurements.
The first row of these files should contain headers, other rows should contain the other data, the id of the measurement is contained in the first column, 
while the diameter measurement is located in the second column. 

Results of the analysis will be saved in the `output` directory. If this directory does not exist in your codebase, you should create it to prevent errors.

## Data Gathering
The `data-gathering` directory contains [ImageJ](https://imagej.net/ij/) macros to analyze photoacoustic images. It contains two files:
1. [analysis.ijm](data-gathering/src/analysis.ijm): Gather general vascular data from a collection of photoacoustic images and save it as a `.csv` file.
2. [diameter-analysisv2.ijm](data-gathering/src/diameter-analysisv2.ijm): Gather blood vessel diameter measurements for a single photoacoustic images, the resulting table should be saved to a `.csv` file.

The results of the [diameter-analysisv2.ijm](data-gathering/src/diameter-analysisv2.ijm) macro should be saved as a `.csv` in the `resources/output` directory previously mentioned.

## Data Analysis
This module contains python code and bash scripts to easily generate data visualizations from the photoacoustic image data gathered.
The visualization that can currently be generated are:
- Histograms
- Violin Plots

You can run the analysis in two ways:

### Using Bash Scripts
The easiest way is by using the two bash scripts [histogram.sh](data-analysis/histogram.sh) and [violin.sh](data-analysis/violin.sh) which generate histograms and violin plots respectively.
In order to execute any of the two files you must:
1. Be able to execute `.sh` files on your computer.
2. Have python and pip installed on your computer.
3. In both files set the following variable:
   - `INPUT_PATH`: path to the .csv file containing the data e.g. `'../resources/data/532_OR_55_index0.csv'`
4. Execute the `.sh` files (double click should work).

### Using a Terminal
You can also execute the python scripts in a terminal by using these steps:
1. Make sure python is installed in your terminal (try executing the following command):
    ```commandline
    python --version
    ```
2. Execute the following commands, each input will be described below:
    ```commandline
    cd data-analysis 
    ```
    ```commandline
    pip install -r requirements.txt
    ```
    ```commandline
    python src/main.py --file_path file-path --output_type output-type --output_folder output-path
    ```
   - file-path: Replace this value with the path to your data file e.g. `../resources/data/532_OR_55_index0.csv`
   - output-type: Replace this value with the type of graph you wish to produce (histogram or violinplot)
   - output-path: Replace this value with the path to your output folder (default is ../resources/data)
