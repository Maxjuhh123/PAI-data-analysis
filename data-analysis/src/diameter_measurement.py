"""
Module for diameter measurement functionality.
"""
from typing import List


PIXEL_SIZE = 5  # Each pixel is 5nm


class DiameterMeasurement:
    """
    Represent a diameter measurement.
    """

    def __init__(self, vessel_id: int, diameter: float):
        self.vessel_id = vessel_id
        self.diameter = diameter  # Diameter in nm

    def __repr__(self):
        """
        Convert the measurement to a string.

        :return: String representation of the measurement
        """
        return f'DiameterMeasurement(id={self.vessel_id}, diameter={self.diameter})'


def read_diameter_measurement_row(row: List[str]) -> DiameterMeasurement:
    """
    Read a row describing a diameter measurement from a csv file.

    :param row: The row
    :return: The diameter measurement
    """
    vessel_id = int(row[0])
    diameter = float(row[1]) * PIXEL_SIZE
    return DiameterMeasurement(vessel_id, diameter)
