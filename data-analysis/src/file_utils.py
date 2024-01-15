"""
Module for file utility.
"""
import csv
import os
from typing import IO, List

from matplotlib import pyplot as plt

from diameter_measurement import DiameterMeasurement, read_diameter_measurement_row


def load_csv(file_path: str) -> IO:
    """
    Load a csv file given a file_path, throws an error if the file was not found or is not a csv file.

    :param file_path: Path to the file
    :return:
    """
    if not file_path.endswith('.csv'):
        raise IOError('Expected csv file as data input')
    return open(file_path)


def extract_file_name(file_path: str) -> str:
    """
    Extract the filename (without filetype) from the path.

    :param file_path: Path to the file
    :return: File name
    """
    return os.path.basename(file_path).replace('.csv', '')


def read_diameter_measurements(file_path: str) -> List[DiameterMeasurement]:
    """
    Read diameter measurements from csv file given the path to the file.

    :param file_path: Path to the csv file.
    :return: List containing the diameter measurements
    """
    csv_file = load_csv(file_path)
    reader = csv.reader(csv_file)

    # Skip header row
    next(reader, None)

    return [read_diameter_measurement_row(row) for row in reader]


def save_figure(path: str) -> None:
    """
    Save a figure to a file.

    :param path: Path to save the figure to.
    """
    plt.savefig(path)
    print(f'saved figure to {path}')
