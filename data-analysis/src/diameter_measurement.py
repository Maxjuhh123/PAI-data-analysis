"""
Module for diameter measurement functionality.
"""
from typing import List


class DiameterMeasurement:
    PIXEL_SIZE = 5  # Each pixel is 5nm

    """
    Represent a diameter measurement.
    """

    def __init__(self, vessel_id: int, diameter: float):
        self.vessel_id = vessel_id
        self.diameter = diameter  # Diameter in pixels

    def __repr__(self):
        """
        Convert the measurement to a string.

        :return: String representation of the measurement
        """
        return f'DiameterMeasurement(id={self.vessel_id}, diameter={self.diameter})'


def read_diameter_measurement_row(row: List[str]) -> DiameterMeasurement:
    """
    Read a row describing a diameter measurement (in pixels) from a csv file.

    :param row: The row
    :return: The diameter measurement
    """
    vessel_id = int(row[0])
    diameter = float(row[1])
    return DiameterMeasurement(vessel_id, diameter)


def filter_diameter_measurements(measurements: List[DiameterMeasurement], max_diameter: float, pixel_measurements: bool) -> List[float]:
    """
    Filter diameter measurements and transform to nm if specified.

    :param measurements: The measurements
    :param max_diameter: The maximum allowed diameter (in nm)
    :param pixel_measurements: Whether you want your results to be measured in pixels (True) or nm (False)
    :return: The list of filtered measurements in pixels or nm
    """
    factor = 1 if pixel_measurements else DiameterMeasurement.PIXEL_SIZE
    max_allowed = max_diameter / DiameterMeasurement.PIXEL_SIZE if pixel_measurements else max_diameter

    return [factor * measurement.diameter for measurement in measurements if measurement.diameter <= max_allowed]