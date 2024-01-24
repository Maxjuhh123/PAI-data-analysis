"""
Generate gaussian fitting of diameter data and an estimated shift of that fitting
"""
import os
from typing import List

import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
from scipy.stats import norm

from file_utils import read_diameter_measurements
from diameter_measurement import DiameterMeasurement

SHOULD_NORMALIZE = False


def load_diameters_for_image(image_name: str) -> List[float]:
    """
    Given an image name, load all diameters as floats.

    :param image_name: Name of image
    :return: The list of diameter measurements
    """
    csv_name = image_name.replace('png', 'csv').replace('jpg', 'csv').replace('jpeg', 'csv')
    csv_path = '../../resources/data/diameter-data/' + csv_name
    return [measurement.diameter * DiameterMeasurement.PIXEL_SIZE for measurement in
            read_diameter_measurements(csv_path)]


def plot_distribution(diameters: List[float], color: str, label: str) -> None:
    """
    Estimate and plot gaussian fit of diameters.

    :param diameters: List of diameters
    :param color: The color of the line in the plot
    :param label: The label of the line in the plot
    """
    bin_width = int(min(diameters))
    hist, bin_edges = np.histogram(diameters, bins=np.arange(min(diameters), max(diameters) + bin_width, bin_width),
                                   density=True)
    # Plot regular distribution
    # Calculate bin centers
    bin_centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])

    # Define the normal distribution function
    def normal_distribution(x, mu, sigma):
        return norm.pdf(x, mu, sigma)

    # Fit the normal distribution using curve_fit
    # Initial guess for parameters (you may need to adjust this based on your data)
    initial_params = [np.mean(diameters), np.std(diameters)]

    # Use curve_fit to find the best-fit parameters
    params, covariance = curve_fit(normal_distribution, bin_centers, hist, p0=initial_params)

    # Extract the fitted parameters
    mu_fit, sigma_fit = params

    # Generate the fitted normal distribution
    x_range = [i for i in range(0, 100)]
    fitted_distribution = normal_distribution(x_range, mu_fit, sigma_fit)

    if SHOULD_NORMALIZE:
        # Normalize
        fitted_distribution = [x / norm.pdf(mu_fit, mu_fit, sigma_fit) for x in fitted_distribution]

    # Plot the fitted distribution
    plt.plot(x_range, fitted_distribution, color=color, linewidth=2,
             label=label)


if __name__ == '__main__':
    imgs = os.listdir('../../resources/images')

    img_name = '532_OR_47_index0.jpeg'
    diameters = load_diameters_for_image(img_name)
    plot_distribution(diameters, 'blue', 'Diameter distribution in healthy tissue')

    shifted_diameters = [diameter * 1.82 if 6 <= diameter <= 30 else diameter for diameter in diameters]
    plot_distribution(shifted_diameters, 'magenta', 'Expected diameter distribution in inflamed tissue')

    legend_font = {'size': 14}
    plt.rc('font', **legend_font)
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.25), ncol=1)  # Adjust the ncol as needed
    label_font = {'size': 16}
    plt.xlabel('Diameter (μm)', fontdict=label_font)
    plt.ylabel('Density', fontdict=label_font)

    plt.tight_layout()

    # Increase the height of the figure
    fig = plt.gcf()
    fig.set_size_inches(fig.get_size_inches()[0] + 3, fig.get_size_inches()[1] + 2)
    plt.title(f'Expected {"Normalized " if SHOULD_NORMALIZE else ""}Diameter Distribution Shift',
              y=1.25, fontdict={'weight': 'bold', 'size': 20})
    plt.savefig(f'../../resources/output/{img_name}-shifted-fits{"-normalized" if SHOULD_NORMALIZE else ""}.png')
