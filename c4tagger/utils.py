import argparse
import spacy

DEFAULT_FR_PIPELINES = spacy.load("fr_core_news_md")
DEFAULT_EN_PIPELINES = spacy.load("en_core_web_md")
DEFAULT_IT_PIPELINES = spacy.load("it_core_news_md")


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
    parser_knn.add_argument("--l1", type=str, default="fr", help="The first language")
    parser_knn.add_argument("--l2", type=str, default="it", help="The second language")

    return parser.parse_args()


def get_pipeline(language):
    if language == "fr":
        return DEFAULT_FR_PIPELINES
    elif language == "it":
        return DEFAULT_IT_PIPELINES
    elif language == "en":
        return DEFAULT_EN_PIPELINES
    else:
        raise ValueError("{0} is not a supported language".format(language))
    pass
