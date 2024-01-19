"""
Module for analyzing branches.
"""
import csv
import os
from typing import List

from matplotlib import pyplot as plt
from file_utils import save_figure
from branch_measurement import BranchMeasurement, read_branch_measurements_from_row


def read_branch_measurements(file_path: str) -> List[BranchMeasurement]:
    """
    Read branch measurements of a single image from a csv file.

    :param file_path: Path to csv file
    :return: The list of branch measurements
    """
    csv_file = open(file_path)
    reader = csv.reader(csv_file)

    # Skip header row
    next(reader, None)

    return [read_branch_measurements_from_row(row) for row in reader]


def scatterplot_junctions_and_branches(branch_measurements: List[BranchMeasurement], file_name: str) -> None:
    """
    Generate scatterplot of junction count and branch count.

    :param branch_measurements: List of branch measurements
    :param file_name: Name of original csv file
    """
    junction_counts = [x.junction_count for x in branch_measurements]
    branch_counts = [x.branch_count for x in branch_measurements]

    plt.scatter(junction_counts, branch_counts, marker='o')
    plt.xlabel('Junctions')
    plt.ylabel('Branches')

    save_path = '../../resources/output/branch-analysis/' + file_name + ".png"
    save_figure(save_path)


def generate_branch_measurement_graphs(branch_measurements: List[BranchMeasurement], file_name: str) -> None:
    """
    Given branch measurements of an image, generate graphs.

    :param branch_measurements: List of branch measurements
    :param file_name: Name of original csv file
    """
    scatterplot_junctions_and_branches(branch_measurements, file_name)


if __name__ == '__main__':
    measurement_paths = os.listdir('../../resources/data/branch-data')
    # Skip branch info files
    measurement_paths = [path for path in measurement_paths if 'branch-info' not in path]

    # Generate graphs for each image data file
    for path in measurement_paths:
        csv_path = '../../resources/data/branch-data/' + path
        measurements = read_branch_measurements(csv_path)
        generate_branch_measurement_graphs(measurements, path)
