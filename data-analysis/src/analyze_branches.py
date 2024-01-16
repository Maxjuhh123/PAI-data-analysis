"""
Module for analyzing branches.
"""

from argparse import Namespace, ArgumentParser
from file_utils import read_branch_measurements, extract_file_name
from visualization import generate_analysis_visualization


def get_args() -> Namespace:
    """
    Get arguments from command line.

    :return: Namespace containing arguments
    """
    parser = ArgumentParser()
    parser.add_argument('--file_path', type=str, default='../resources/output.csv')
    parser.add_argument('--output_path', type=str, default='../resources/output')
    return parser.parse_args()


def generate_branch_graphs(file_path: str, output_folder: str) -> None:
    """
    For a single csv file, generate the graphs and save them to the output folder.

    :param file_path: Path to the file
    :param output_folder: Path to output folder
    """
    measurements = read_branch_measurements(args.file_path)
    file_name = extract_file_name(file_path)
    graph_types = ['density/branch_count']
    for output_type in graph_types:
        generate_analysis_visualization(measurements, output_type, output_folder, file_name, False)


if __name__ == '__main__':
    args = get_args()
    generate_branch_graphs(args.file_path, args.output_path)
