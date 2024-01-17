"""
Utility file for generating gaussian fits of diameter data
"""
import os
from typing import List

import numpy as np
from matplotlib import pyplot as plt
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
    min = 0
    max = 100

    bins = [i for i in range(min, max)]
    colors = ['red', 'blue', 'green', 'purple', 'pink', 'magenta', 'cyan', 'black', 'gray', 'yellow', 'orange']
    lines = []
    for i in range(len(imgs)):
        img_name = imgs[i]
        diameters = load_diameters_for_image(img_name)
        # Fit gaussian to diameters
        # Gaussian Fit
        (mu, sigma) = norm.fit(diameters)
        y = norm.pdf(bins, mu, sigma)

        mu = np.round(mu, 2)
        sigma = np.round(sigma, 2)

        line = plt.plot(bins, y, color=colors[i], linewidth=2, label=f'{img_name}: μ={mu} σ={sigma}')

    plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.25), ncol=2)  # Adjust the ncol as needed
    plt.xlabel('Diameter (nm)')
    plt.ylabel('Density')

    plt.tight_layout()

    # Increase the height of the figure
    fig = plt.gcf()
    fig.set_size_inches(fig.get_size_inches()[0] + 1, fig.get_size_inches()[1] + 4)
    plt.title('Gaussian Fits of Diameters', y=1.25)
    plt.savefig('../../resources/output/fits.png')
