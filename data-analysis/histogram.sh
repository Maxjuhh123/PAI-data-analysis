#!/bin/bash
pip install -r requirements.txt

# Change these two values to represent the input path to the csv file and output folder path respectively
INPUT_PATH='../resources/data/532_OR_55_index0.csv'
OUTPUT_PATH='../resources/output'

echo "Generating histogram for $INPUT_PATH"
python src/main.py --output_type histogram --file_path $INPUT_PATH --output_folder $OUTPUT_PATH

# Keep terminal open after completion
$SHELL