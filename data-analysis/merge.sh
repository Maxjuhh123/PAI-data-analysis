#!/bin/bash

# Set the output file name
output_file="merged_data.csv"

# Remove the output file if it already exists
rm -f "$output_file"

# Loop through all CSV files in the folder
for file in *.csv; do
    # Skip the output file itself
    if [ "$file" != "$output_file" ]; then
        # Append all lines from the current CSV file to the output file, skipping the header
        tail -n +2 "$file" >> "$output_file"
    fi
done

echo "Merged data saved to $output_file"
