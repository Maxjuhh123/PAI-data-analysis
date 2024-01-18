"""
Utility file for generating gaussian fits of diameter data
"""
import os
from typing import List

import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
from scipy.stats import norm

from file_utils import read_diameter_measurements
from diameter_measurement import DiameterMeasurement


def load_diameters_for_image(image_name: str) -> List[float]:
    """
    Given an image name, load all diameters as floats.

    :param image_name: Name of image
    :return: The list of diameter measurements
    """
    csv_name = image_name.replace('png', 'csv').replace('jpg', 'csv').replace('jpeg', 'csv')
    csv_path = '../../resources/data/' + csv_name
    return [measurement.diameter * DiameterMeasurement.PIXEL_SIZE for measurement in read_diameter_measurements(csv_path)]


if __name__ == '__main__':
    imgs = os.listdir('../../resources/images')

    colors = ['red', 'blue', 'green', 'purple', 'pink', 'magenta', 'cyan', 'black', 'gray', 'yellow', 'orange']
    lines = []
    for i in range(len(imgs)):
        img_name = imgs[i]
        diameters = load_diameters_for_image(img_name)

        bin_width = int(min(diameters))
        hist, bin_edges = np.histogram(diameters, bins=np.arange(min(diameters), max(diameters) + bin_width, bin_width),
                                       density=True)

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

        # Plot the histogram and the fitted distribution
        plt.plot(x_range, fitted_distribution, color=colors[i], linewidth=2, label=f'{img_name}: μ={np.round(mu_fit, 2)} σ={np.round(sigma_fit, 2)}')

    plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.25), ncol=2)  # Adjust the ncol as needed
    plt.xlabel('Diameter (nm)')
    plt.ylabel('Density')

    plt.tight_layout()

    # Increase the height of the figure
    fig = plt.gcf()
    fig.set_size_inches(fig.get_size_inches()[0] + 1, fig.get_size_inches()[1] + 4)
    plt.title('Gaussian Fits of Diameters', y=1.25)
    plt.savefig('../../resources/output/fits.png')
