import argparse


def get_cli_args() -> argparse.Namespace:
    """
    Get command line arguments.
    I stole this from the dummy package of our course.
    """
    parser = argparse.ArgumentParser(description="Interpreter")
    subparsers = parser.add_subparsers(help='sub-command', dest='command')

    # Add Command Line arguments for the interpreter
    parser_knn = subparsers.add_parser("interpret", help="Data exploration")

    # Add Command Line arguments to update deprecated data just in case
    parser_knn = subparsers.add_parser("update", help="Update data")

    return parser.parse_args()
