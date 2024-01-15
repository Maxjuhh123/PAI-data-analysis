#!/bin/bash
pip install -r requirements.txt

# Change the INPUT_PATH variable to point to your csv file
INPUT_PATH='../resources/data/532_OR_55_index0.csv'
OUTPUT_PATH='../resources/output'
PIXEL_MEASUREMENTS='true'

echo "Generating scatter plot for $INPUT_PATH"
python src/main.py --output_type scatterplot --file_path $INPUT_PATH --output_folder $OUTPUT_PATH --pixel_measurements $PIXEL_MEASUREMENTS

# Keep terminal open after completion
$SHELL