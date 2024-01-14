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


def generate_graph_for_csv(file_path: str, output_type: str, output_folder: str) -> None:
    """
    For a single csv file and graph type, generate the graph and save it to the output folder.

    :param file_path: Path to the file
    :param output_type: Type of output graph
    :param output_folder: Path to output folder
    """
    diameter_measurements = read_diameter_measurements(file_path)
    file_name = extract_file_name(file_path)
    generate_analysis_visualization(diameter_measurements, output_type, output_folder, file_name)


if __name__ == '__main__':
    """
    Entry point of the application.
    """
    args = get_args()

    generate_graph_for_csv(args.file_path, args.output_type, args.output_folder)