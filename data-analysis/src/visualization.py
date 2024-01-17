"""
Module for data analysis (visualization).
"""
from typing import List

import numpy as np

from measurement import Measurement
from diameter_measurement import DiameterMeasurement, filter_diameter_measurements
from branch_measurement import BranchMeasurement
from file_utils import save_figure
import matplotlib.pyplot as plt
from scipy.stats import norm

HISTOGRAM_BIN_WIDTH = np.sqrt(2) + 0.0000001
MAX_DIAMETER = 100  # in microns


def generate_analysis_visualization(measurements: List[Measurement], output_type: str, output_folder_path: str,
                                    file_name: str, pixel_measurements: bool) -> None:
    """
    Analyze measurements and generate visualization.

    :param measurements: The list of measurements
    :param output_type: Type of output graph
    :param output_folder_path: Path to folder where output will be saved
    :param file_name: Name of original image file
    :param pixel_measurements: Whether you want your results to be measured in pixels (True) or microns (False)
    :return:
    """

    if output_type == 'histogram':
        generate_histogram(measurements, output_folder_path, file_name, pixel_measurements)
    elif output_type == 'violinplot':
        generate_violinplot(measurements, output_folder_path, file_name, pixel_measurements)
    elif output_type == 'scatterplot':
        generate_scatterplot(measurements, output_folder_path, file_name, pixel_measurements)
    elif output_type == 'density/branch_count':
        generate_density_branch_count_plot(measurements, output_folder_path, file_name)
    else:
        print(f'Unsupported output type: {output_type}')


def generate_density_branch_count_plot(measurements: List[BranchMeasurement],
                                       output_folder_path: str, file_name) -> None:
    """
    Plot vessel density against average branch count.

    :param measurements: The measurements
    :param output_folder_path: The output file path
    :param file_name: The file name
    """
    densities = [measurement.area_percentage for measurement in measurements]
    branch_lengths = [measurement.num_branches for measurement in measurements]
    plt.scatter(densities, branch_lengths, marker='o')
    plt.xlabel('Vessel density (%)')
    plt.ylabel('Branch count')
    plt.title('Vessel Density and Branch Count')

    save_path = output_folder_path + f'/{file_name}-scatter.png'
    save_figure(save_path)


def generate_histogram(measurements: List[DiameterMeasurement], output_folder_path: str,
                       file_name: str, pixel_measurements: bool) -> None:
    """
    Generate a histogram of the measurements and save to a file.

    :param measurements: The measurements
    :param output_folder_path: Path to the output folder
    :param file_name: Name of original image file
    :param pixel_measurements: Whether you want your results to be measured in pixels (True) or microns (False)
    """
    diameters = filter_diameter_measurements(measurements, MAX_DIAMETER, pixel_measurements)

    # Histogram
    bins_start = 0
    bins_end = int(np.ceil(max(diameters)))
    bins_step = int(np.ceil(min(diameters)))
    bins = [i for i in range(bins_start, bins_end, bins_step)]
    plt.hist(diameters, density=True, bins=bins)
    plt.title('Histogram of Vessel Diameters')
    plt.ylabel('Probability')
    plt.xlabel(f'Vessel diameter {"(pixels)" if pixel_measurements else "(microns)"}')

    # Gaussian Fit
    (mu, sigma) = norm.fit(diameters)
    y = norm.pdf(bins, mu, sigma)
    plt.plot(bins, y, 'r--', linewidth=2, label=f'Gaussian Fit: μ={mu} σ={sigma}')
    plt.legend()

    save_path = output_folder_path + f'/{file_name}-hist.png'
    save_figure(save_path)


def generate_violinplot(measurements: List[DiameterMeasurement], output_folder_path: str,
                        file_name: str, pixel_measurements: bool) -> None:
    """
    Generate a violin plot of the measurements and save to a file.

    :param measurements: The measurements
    :param output_folder_path: Path to the output folder
    :param file_name: Name of original image file
    :param pixel_measurements: Whether you want your results to be measured in pixels (True) or microns (False)
    """
    diameters = filter_diameter_measurements(measurements, MAX_DIAMETER, pixel_measurements)
    plt.violinplot(diameters, showextrema=True, showmedians=True)

    plt.title('Violin Plot of Vessel Diameters')
    plt.ylabel(f'Vessel diameter {"(pixels)" if pixel_measurements else "(microns)"}')
    plt.xlabel('')

    save_path = output_folder_path + f'/{file_name}-violin.png'
    save_figure(save_path)


def generate_scatterplot(measurements: List[DiameterMeasurement], output_folder_path: str,
                         file_name: str, pixel_measurements: bool) -> None:
    """
    Generate a scatter plot of the measurements and save to a file.

    :param measurements: The measurements
    :param output_folder_path: Path to the output folder
    :param file_name: Name of original image file
    :param pixel_measurements: Whether you want your results to be measured in pixels (True) or microns (False)
    """
    diameters = filter_diameter_measurements(measurements, MAX_DIAMETER, pixel_measurements)
    y = [0 for _ in range(len(diameters))]
    plt.scatter(diameters, y, marker='o')
    plt.xlabel(f'Diameter {"(pixels)" if pixel_measurements else "(microns)"}')
    plt.title('Scatter Plot of Vessel Diameters')

    save_path = output_folder_path + f'/{file_name}-scatter.png'
    save_figure(save_path)
