"""
Module relating to vascular branch measurements
"""
from typing import List
from measurement import Measurement


class BranchMeasurement(Measurement):
    """
    Class to represent branch measurements.
    """

    def __init__(self, measurement_id: int, branch_count: int, junction_count: int, end_point_voxel_count: int,
                 junction_voxel_count: int, slab_voxel_count: int, avg_branch_length: float, triple_point_count: int,
                 quadruple_point_count: int, max_branch_length: float):
        self.measurement_id = measurement_id
        self.branch_count = branch_count
        self.junction_count = junction_count
        self.end_point_voxel_count = end_point_voxel_count
        self.junction_voxel_count = junction_voxel_count
        self.slab_voxel_count = slab_voxel_count
        self.avg_branch_length = avg_branch_length
        self.triple_point_count = triple_point_count
        self.quadruple_point_count = quadruple_point_count
        self.max_branch_length = max_branch_length


def read_branch_measurements_from_row(row: List[str]) -> BranchMeasurement:
    """
    Read a branch measurement from a row.

    :param row: Row of measurements as strings
    :return: The measurements as an object
    """
    return BranchMeasurement(
        int(row[0]),
        int(row[1]),
        int(row[2]),
        int(row[3]),
        int(row[4]),
        int(row[5]),
        float(row[6]),
        int(row[7]),
        int(row[8]),
        float(row[9])
    )
