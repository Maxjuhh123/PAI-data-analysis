"""
Module relating to vascular branch measurements
"""
from typing import List
from measurement import Measurement


class BranchMeasurement(Measurement):
    """
    Class to represent branch measurements.
    """

    def __init__(self, measurement_id: int, label: str, area_percentage: float, vasculature_length: float, num_branches: int,
                 avg_branch_length: float, max_branch_length: float, mean_vessel_distance: float,
                 min_vessel_distance: float):
        self.measurement_id = measurement_id
        self.label = label
        self.area_percentage = area_percentage
        self.vasculature_length = vasculature_length
        self.num_branches = num_branches
        self.avg_branch_length = avg_branch_length
        self.max_branch_length = max_branch_length
        self.mean_vessel_distance = mean_vessel_distance
        self.min_vessel_distance = min_vessel_distance


def read_branch_measurements_from_row(row: List[str]) -> BranchMeasurement:
    """
    Read a branch measurement from a row.

    :param row: Row of measurements as strings
    :return: The measurements as an object
    """
    return BranchMeasurement(
        int(row[0]),
        row[1],
        float(row[2]),
        float(row[3]),
        int(row[4]),
        float(row[5]),
        float(row[6]),
        float(row[7]),
        float(row[8])
    )
