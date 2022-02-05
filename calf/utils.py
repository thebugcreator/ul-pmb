import argparse

regular_letters = "abcdefghijklmnopqrstuvwxyz"
french_letters = "éàèùâêîôûçëïüœ"
considered_letters = regular_letters + french_letters


def get_cli_args() -> argparse.Namespace:
    """
    Get command line arguments.
    I stole this from the dummy package of our course.
    """
    parser = argparse.ArgumentParser(description="Calf")
    subparsers = parser.add_subparsers(help='sub-command', dest='command')

    # Add Command Line arguments for the tokeniser
    parser_knn = subparsers.add_parser("tokenise", help="Tokenise a sentence")
    parser_knn.add_argument("--sentence", type=str, default="Ne soyez pas paresseux !", help="The sentence to tokenise")
    parser_knn.add_argument("--iob", type=bool, default=False, help="Binary option to display the IOB tags")

    # Add Command Line arguments for the extractor
    parser_knn = subparsers.add_parser("extract", help="Tokenise and extract sentences in a tsv file")
    parser_knn.add_argument("indir", type=str, help="Input file directory")
    parser_knn.add_argument("--outdir", type=str, default="6261677565747465.tsv", help="Output file directory")
    parser_knn.add_argument("--iob", type=bool, default=False, help="Binary option to extract the IOB tags")


    return parser.parse_args()
