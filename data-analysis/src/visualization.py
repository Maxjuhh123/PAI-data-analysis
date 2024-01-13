"""
Module for data analysis (visualization).
"""
from typing import List
from diameter_measurement import DiameterMeasurement
import matplotlib.pyplot as plt

HISTOGRAM_BIN_COUNT = 50


def generate_analysis_visualization(measurements: List[DiameterMeasurement],
                                    output_type: str,
                                    output_folder_path: str,
                                    file_name: str) -> None:
    """
    Analyze measurements and generate visualization.

    :param measurements: The list of measurements
    :param output_type: Type of output graph
    :param output_folder_path: Path to folder where output will be saved
    :param file_name: Name of original image file
    :return:
    """

    if output_type == 'histogram':
        generate_histogram(measurements, output_folder_path, file_name)
    elif output_type == 'violinplot':
        generate_violinplot(measurements, output_folder_path, file_name)
    else:
        print(f'Unsupported output type: {output_type}')


def generate_histogram(measurements: List[DiameterMeasurement], output_folder_path: str, file_name: str) -> None:
    """
    Generate a histogram of the measurements and save to a file.

    :param measurements: The measurements
    :param output_folder_path: Path to the output folder
    :param file_name: Name of original image file
    """
    diameters = [measurement.diameter for measurement in measurements]
    plt.hist(diameters, density=True, bins=HISTOGRAM_BIN_COUNT)

    plt.title('Histogram of Vessel Diameters')
    plt.ylabel('Probability')
    plt.xlabel('Vessel diameter (nm)')

    save_path = output_folder_path + f'/{file_name}-hist.png'
    plt.savefig(save_path)
    print(f'saved figure to {save_path}')


def generate_violinplot(measurements: List[DiameterMeasurement], output_folder_path: str, file_name: str) -> None:
    """
    Generate a violin plot of the measurements and save to a file.

    :param measurements: The measurements
    :param output_folder_path: Path to the output folder
    :param file_name: Name of original image file
    """
    diameters = [measurement.diameter for measurement in measurements]
    plt.violinplot(diameters, showextrema=True, showmedians=True)

    plt.title('Violin Plot of Vessel Diameters')
    plt.ylabel('Vessel diameter (nm)')
    plt.xlabel('')

    save_path = output_folder_path + f'/{file_name}-violin.png'
    plt.savefig(save_path)
    print(f'saved figure to {save_path}')
