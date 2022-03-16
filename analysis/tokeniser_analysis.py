import pandas as pd
import spacy
from nltk.metrics.scores import precision, recall, f_measure
from nltk.metrics import ConfusionMatrix
from nltk.tokenize import word_tokenize, WordPunctTokenizer
import numpy as np

# Loading tsv into data frame
df = pd.read_csv("../pmb_french_163.tsv", sep="\t")

# Get gold tokenisation
gold_tokenisation = df["French tokenisation"]
gold_tokens = []
for gt in gold_tokenisation:
    gold_tokens.append(gt.split(" "))

# Get the string literals for tokenisation
gold_literals = df["French translation"]
gold_ids = df["ID"]


def get_nltk_tokenisation(string_literals: list) -> pd.DataFrame:
    """
    This method is to tokenise sentences using NLTK methods
    :return: A dataframe containing string literal, word-tokenised tokenisation, and wordpunct-tokenised tokenisation
        of the string literal/sentence
    """
    # Get nltk tokenisation
    # to evaluate the two different tokenisers provided by default by nltk
    nltk_wt_tokenisation = [" ".join(word_tokenize(item, language="french")) for item in string_literals]
    nltk_wp_tokenisation = [" ".join(WordPunctTokenizer().tokenize(item)) for item in string_literals]

    # Export NLTK tokenisation to tsv to compare
    df_nltk = pd.DataFrame()
    df_nltk["ID"] = gold_ids
    df_nltk["literal"] = string_literals
    df_nltk["wt"] = nltk_wt_tokenisation
    df_nltk["wp"] = nltk_wp_tokenisation
    df_nltk["are_similar"] = [int(row["wt"] == row["wp"]) for index, row in df_nltk.iterrows()]  #
    return df_nltk


def get_spacy_tokenisation(string_literals: list) -> pd.DataFrame:
    # Get spacy tokenisation
    pipeline_sm = spacy.load("fr_core_news_sm")
    pipeline_md = spacy.load("fr_core_news_md")
    tokenisation_sm = []
    tokenisation_md = []
    are_similar = []
    # Get every sentence from gold literals into the pipeline
    for item in string_literals:
        doc_sm = pipeline_sm(item)
        doc_md = pipeline_md(item)
        token_sm = " ".join([token.text for token in doc_sm])
        token_md = " ".join([token.text for token in doc_md])
        are_similar.append(int(token_md == token_sm))
        tokenisation_sm.append(token_sm)
        tokenisation_md.append(token_md)
    df_spacy = pd.DataFrame()
    df_spacy["ID"] = gold_ids
    df_spacy["literal"] = string_literals
    df_spacy["sm"] = tokenisation_sm
    df_spacy["md"] = tokenisation_md
    df_spacy["are_similar"] = are_similar
    return df_spacy


def get_calf_tokenisation(string_literals: list) -> pd.DataFrame:
    pass


def generate_iob_from_tokens(tokens):
    """
    To get the IOB tags of a list of tokens
    :param tokens: A list of tokens
    :return: IOB tags
    """
    iobs = []
    for i, token in enumerate(tokens):
        if token:
            iob = ["I"] * len(token)
            iob[0] = "B"
        else:
            iob = []
        iobs.append("".join(iob))
    return "".join(iobs)


def calculate_pair_scores(refset, goldset):
    """
    To calculate the P, R, and F1 score of a reference tagset against the gold one.
    :param refset: the reference tagset
    :param goldset: the gold tagset
    :return: P, R, F1 score respectively
    """
    return precision(refset, goldset), recall(refset, goldset), f_measure(refset, goldset, 1)


def analyse_spacy_tokenisation():
    spacydf = pd.read_csv("spacy_tokenisation.tsv", sep="\t", encoding="utf-8")
    spacy_tokens = spacydf[["ID", "md"]]
    spacy_tokens["gold"] = gold_tokenisation
    evaluations = []
    for i, val in spacy_tokens.iterrows():
        ref = val["md"].split(" ")
        gold = val["gold"].split(" ")
        iobref = generate_iob_from_tokens(ref)
        iobgold = generate_iob_from_tokens(gold)
        try:
            cm = ConfusionMatrix(iobref,iobgold)
            evaluations.append(cm.evaluate())
        except ValueError:
            print("Unable to analyse: ",val["ID"])
    return evaluations

# Export the results to tsv files
# get_spacy_tokenisation(gold_literals).to_csv("spacy_tokenisation.tsv", index=False, encoding="utf8", sep="\t")
# get_nltk_tokenisation(gold_literals).to_csv("nltk_tokenisation.tsv", index=False, encoding="utf8", sep="\t")
