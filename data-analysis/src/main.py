"""
Main module, get analysis results from data input.
"""
from argparse import Namespace, ArgumentParser
from file_utils import read_diameter_measurements, extract_file_name
from visualization import generate_analysis_visualization


def get_args() -> Namespace:
    """
    Get arguments from CLI contained in a namespace.

    args:
    1. file_path: path to csv file containing data.
    2. output_type: type of output of the analysis
    3. output_folder: path to folder where the analysis output should be daved

    :return: Namespace containing CLI arguments
    """
    parser = ArgumentParser()
    parser.add_argument('--file_path', type=str, default='../resources/data/532_OR_55_index0.csv')
    parser.add_argument('--output_type', type=str, default='histogram')
    parser.add_argument('--output_folder', type=str, default='../resources/output')
    return parser.parse_args()


if __name__ == '__main__':
    """
    Entry point of the application.
    """
    args = get_args()
    file_path = args.file_path
    diameter_measurements = read_diameter_measurements(file_path)

    output_type = args.output_type
    output_folder_path = args.output_folder
    file_name = extract_file_name(file_path)
    generate_analysis_visualization(diameter_measurements, output_type, output_folder_path, file_name)
