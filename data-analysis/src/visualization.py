"""
Module for data analysis (visualization).
"""
from typing import List
from diameter_measurement import DiameterMeasurement, filter_diameter_measurements
from file_utils import save_figure
import matplotlib.pyplot as plt


HISTOGRAM_BIN_COUNT = 30
MAX_DIAMETER = 40  # in nm


def generate_analysis_visualization(measurements: List[DiameterMeasurement],
                                    output_type: str,
                                    output_folder_path: str,
                                    file_name: str,
                                    pixel_measurements: bool) -> None:
    """
    Analyze measurements and generate visualization.

    :param measurements: The list of measurements
    :param output_type: Type of output graph
    :param output_folder_path: Path to folder where output will be saved
    :param file_name: Name of original image file
    :param pixel_measurements: Whether you want your results to be measured in pixels (True) or nm (False)
    :return:
    """

    if output_type == 'histogram':
        generate_histogram(measurements, output_folder_path, file_name, pixel_measurements)
    elif output_type == 'violinplot':
        generate_violinplot(measurements, output_folder_path, file_name, pixel_measurements)
    elif output_type == 'scatterplot':
        generate_scatterplot(measurements, output_folder_path, file_name, pixel_measurements)
    else:
        print(f'Unsupported output type: {output_type}')


def generate_histogram(measurements: List[DiameterMeasurement], output_folder_path: str, file_name: str, pixel_measurements: bool) -> None:
    """
    Generate a histogram of the measurements and save to a file.

    :param measurements: The measurements
    :param output_folder_path: Path to the output folder
    :param file_name: Name of original image file
    :param pixel_measurements: Whether you want your results to be measured in pixels (True) or nm (False)
    """
    diameters = filter_diameter_measurements(measurements, MAX_DIAMETER, pixel_measurements)
    plt.hist(diameters, density=True, bins=HISTOGRAM_BIN_COUNT)

    plt.title('Histogram of Vessel Diameters')
    plt.ylabel('Probability')
    plt.xlabel(f'Vessel diameter {"(pixels)" if pixel_measurements else "(nm)"}')

    save_path = output_folder_path + f'/{file_name}-hist.png'
    save_figure(save_path)


def generate_violinplot(measurements: List[DiameterMeasurement], output_folder_path: str, file_name: str, pixel_measurements: bool) -> None:
    """
    Generate a violin plot of the measurements and save to a file.

    :param measurements: The measurements
    :param output_folder_path: Path to the output folder
    :param file_name: Name of original image file
    :param pixel_measurements: Whether you want your results to be measured in pixels (True) or nm (False)
    """
    diameters = filter_diameter_measurements(measurements, MAX_DIAMETER, pixel_measurements)
    plt.violinplot(diameters, showextrema=True, showmedians=True)

    plt.title('Violin Plot of Vessel Diameters')
    plt.ylabel(f'Vessel diameter {"(pixels)" if pixel_measurements else "(nm)"}')
    plt.xlabel('')

    save_path = output_folder_path + f'/{file_name}-violin.png'
    save_figure(save_path)


def generate_scatterplot(measurements: List[DiameterMeasurement], output_folder_path: str, file_name: str, pixel_measurements: bool) -> None:
    """
    Generate a scatter plot of the measurements and save to a file.

    :param measurements: The measurements
    :param output_folder_path: Path to the output folder
    :param file_name: Name of original image file
    :param pixel_measurements: Whether you want your results to be measured in pixels (True) or nm (False)
    """
    diameters = filter_diameter_measurements(measurements, MAX_DIAMETER, pixel_measurements)
    y = [0 for _ in range(len(diameters))]
    plt.scatter(diameters, y, marker='o')
    plt.xlabel(f'Diameter {"(pixels)" if pixel_measurements else "(nm)"}')
    plt.title('Scatter Plot of Vessel Diameters')

    save_path = output_folder_path + f'/{file_name}-scatter.png'
    save_figure(save_path)
