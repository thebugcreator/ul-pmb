import argparse
import spacy


def get_interpreter_cli_args() -> argparse.Namespace:
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


def get_analysis_cli_ars() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Data extractor")
    subparsers = parser.add_subparsers(help='sub-command', dest='command')

    # Add Command Line arguments for the extractor
    parser_c4 = subparsers.add_parser("extract", help="Data extraction")
    parser_c4.add_argument("--file", type=str, default="en", help="CoNLL file path")
    parser_c4.add_argument("--pipeline", type=str, default="en_core_web_sm", help="Spacy pipeline name")
    # Add Command Line arguments to interpret the alignment
    parser_c4 = subparsers.add_parser("inspect", help="Data inspection")
    parser_c4.add_argument("--lang", type=str, default="it", help="TSV file path")
    parser_c4.add_argument("--extract_err", type=bool, default=False,
                           help="Choose to or not to extract the non aligned documents")
    # Add the coocurences extractor
    parser_c4 = subparsers.add_parser("get_cooc", help="POS-SEM cooccurrences")
    parser_c4.add_argument("--lang", type=str, default="it", help="Language")
    parser_c4.add_argument("--stacked", type=bool, default=False, help="Stacking language samples")
    parser_c4.add_argument("--sample_size", type=int, default=500, help="Number of stacked samples")
    parser_c4.add_argument("--visualise", type=bool, default=True, help="Visualisation choice")
    parser_c4.add_argument("--savefig", type=bool, default=True, help="Figure export choice")
    return parser.parse_args()


def get_pipeline(language):
    if language == "fr":
        return spacy.load("fr_core_news_md")
    elif language == "it":
        return spacy.load("it_core_news_md")
    elif language == "en":
        return spacy.load("en_core_web_md")
    elif language == "de":
        return spacy.load("de_core_news_sm")
    elif language == "nl":
        return spacy.load("nl_core_news_sm")
    else:
        raise ValueError("{0} is not a supported language".format(language))
    pass
