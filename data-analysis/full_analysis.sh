#!/bin/bash
pip install -r requirements.txt

# Change these two values to represent the input path to the csv file and output folder path respectively
INPUT_FOLDER='../resources/data'
OUTPUT_FOLDER='../resources/output'

for file_path in "$INPUT_FOLDER"/*; do
        echo "Generating histogram for $INPUT_PATH"
        python src/main.py --output_type histogram --file_path "$file_path" --output_folder $OUTPUT_FOLDER
        echo "Generating violin plot for $INPUT_PATH"
        python src/main.py --output_type violinplot --file_path "$file_path" --output_folder $OUTPUT_FOLDER
    done

# Keep terminal open after completion
$SHELL