# PAI-data-analysis
This repository contains code to be used for analyzing photoacoustic images. The codebase is divided into three directories which will be explained below.

## Resources
The `resources` directory contains two subdirectories: `data` and `output`. The data directory should contain `.csv` files describing diameter measurements.
The first row of these files should contain headers, other rows should contain the other data, the id of the measurement is contained in the first column, 
while the diameter measurement is located in the second column. 

Results of the analysis will be saved in the `output` directory. 
If any of the resource directories does not exist, you should create it. The directory structure should look like this:

```
PAI-data-analysis/
   resources/
      data/
         ..your csv files..
      output/
         ..your output files..
```

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
- Scatter Plots

You can run the analysis in two ways:

### Using Bash Scripts
The easiest way is by using bash scripts [histogram.sh](data-analysis/histogram.sh), [violin.sh](data-analysis/violin.sh), and [scatter.sh](data-analysis/scatter.sh), which generate histograms, violin plots, and scatter plots respectively.
In order to execute any of the two files you must:
1. Be able to execute `.sh` files on your computer.
2. Have python and pip installed on your computer.
3. In all three files set the following variables:
   - `INPUT_PATH`: path to the .csv file containing the data e.g. `'../resources/data/532_OR_55_index0.csv'`
   - `PIXEL_MEASUREMENTS`: set to `true` if you want your results in pixels and `false` if you want them in microns.
4. Execute the `.sh` files (double click should work).

If you wish to perform an analysis for all `.csv` files in a folder, you can execute the [full_analysis.sh](data-analysis/full_analysis.sh) file.
In this file you have a few variables: `INPUT_FOLDER`, `OUTPUT_FOLDER`, and `PIXEL_MEASUREMENTS` which define paths to the input and output folders and whether we want pixel measurements (true) or microns (false) measurements respectively. The default values
for these variables should work if you follow the directory structure described above, otherwise you can adjust these variables to suit your needs.

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
    python src/main.py --file_path file-path --output_type output-type --output_folder output-path --pixel_measurements pixel-measurements
    ```
   - file-path: Replace this value with the path to your data file e.g. `../resources/data/532_OR_55_index0.csv`
   - output-type: Replace this value with the type of graph you wish to produce (histogram or violinplot)
   - output-path: Replace this value with the path to your output folder (default is ../resources/data)
   - pixel-measurements: Replace this value with `true` or `false` depending on if you want your measurements in pixels (True) or microns (False)
### Changing Constants
There are a few constants located in the python scripts which you can customize:
- `HISTOGRAM_BIN_COUNT`: The amount of bins to use in histograms
- `MAX_DIAMETER`: The maximum diameter (in microns) to consider in the analysis
- `PIXEL_SIZE`: Size of a pixel (in microns)
