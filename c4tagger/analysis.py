import argparse
from collections import Counter

import pandas as pd
import spacy
from matplotlib import pyplot as plt
import seaborn as sns

import utils

data_directory = "data"
languages = ["de", "en", "it", "nl"]
default_tsv_filename = "train.tsv"


# %%
def build_directory(*args) -> str:
    """
    Function used to build directory string
    :param args: list of folder and file in tree
    """
    result = ""
    for i in range(len(args) - 1):
        result += args[i] + "/"
    result += args[-1]
    return result


# %%
def extract_data(filename):
    """
    This function is to read the conll file (not readable by conllu)
    :param filename: full name of the conll file
    :return: an array of documents
    """
    sentences = []
    # Open the conll file
    with open(filename, encoding="utf8") as file:
        # Array to store sentence data
        sentence = []
        # Read the file line by line
        for line in file.readlines():
            # The blank line is to separate the documents
            if line != "\n":
                if line[0] == "#":
                    continue
                # Order: tok tok sym sem cat
                token = line.split("\t")
                # Merge the token into the sentence
                sentence.append(token)
            else:
                # Document break found, save the document data
                sentences.append(sentence)
                # Refresh the var for new document
                sentence = []
    return sentences


# %%
def get_pos_sem_tag(filename, pipeline):
    """
    This function is to get the POS tags using Spacy and the SEM tag provided in the coNLL file.
    Write the result in a csv file
    :param filename: name of the coNLL file
    :param pipeline: spacy pipeline. Make sure you install it using `python -m spacy download <pipeline name>`
    :return: number of records
    """
    pipeline = spacy.load(pipeline)
    data = extract_data(filename)
    # Tokens for each doc
    tokens = []
    # POS tags for each doc
    poss = []
    # SEM tags for each dog
    sems = []
    # Loop over the data retrieved from the CONLL file
    for item in data:
        # Tokens for getting POS tags using spacy
        token = " ".join([e[0] for e in item])
        # Process the tokens
        minidoc = pipeline(token)
        # Get spacy POS tags
        pos_tags = [token.pos_ for token in minidoc]
        # Get provided SEM tags
        sem_tags = [e[3] for e in item]
        # Convert tag list to string and put in the list
        poss.append(" ".join(pos_tags))
        sems.append(" ".join(sem_tags))
        # Save the corresponding token
        tokens.append(token)
    # Export CSV
    minidf = pd.DataFrame()
    minidf["pos"] = poss
    minidf["sem"] = sems
    minidf["tok"] = tokens
    minidf.to_csv(filename + ".tsv", sep="\t", encoding="utf8", index=False)
    return len(poss)


# %%
def pre_process_spacy_pos_NE(pos_tags):
    """
    This function is to pre process the Spacy POS tags.
    To merge the consecutive PROPN tags into one
    :param pos_tags: list of POS tags
    :return: processed list of POS tags
    """
    results = []
    # Loop over the POS tags
    for i in range(len(pos_tags)):
        # Not further processing the unintended tags
        if pos_tags[i] != "PROPN" and pos_tags[i] != "X":
            results.append(pos_tags[i])
        # Aim at the PROPN tag
        if pos_tags[i] == "PROPN":
            try:
                # Check if the preceding tag is intended
                if pos_tags[i - 1] != "PROPN" and pos_tags[i - 1] != "X":
                    results.append(pos_tags[i])
                # Ignore the next PROPN or X tags if this one is already PROPN
                if pos_tags[i + 1] == "PROPN" and pos_tags[i] == "X":
                    continue
            except IndexError:
                # Handling the Index Error
                continue
    return results


# %%
def get_pos_sem_alignment(lang, show_non_aligned=False, extract_errors=False):
    """
    Get POS-SEM tag alignment
    :param lang: tsv filename
    :param show_non_aligned: Choose to show the non-aligned documents
    :param extract_errors: Choose to extract the non-aligned documents to tsv
    :return:
    """
    file_directory = build_directory(data_directory, lang, default_tsv_filename)
    print("Inspecting", file_directory)
    minidf = pd.read_csv(file_directory, sep="\t")
    pos_tags = dict()
    err_sentences = list()
    err_raw_pos = list()
    err_pos = list()
    err_sem = list()
    # Loop over the data frame
    for index, value in minidf.iterrows():
        # Extract record info of POS tags and SEM tags (and tokens as well)
        raw_pos = value["pos"].split(" ")
        pos = pre_process_spacy_pos_NE(raw_pos)
        sem = value["sem"].split(" ")
        tok = value["tok"]
        # Ignore the non-aligned pairs
        if len(pos) != len(sem):
            # Store the non-aligned sentences
            if extract_errors:
                err_sentences.append(tok)
                err_raw_pos.append(" ".join(raw_pos))
                err_pos.append(" ".join(pos))
                err_sem.append(" ".join(sem))
            # Choose to print them out
            if show_non_aligned:
                print(tok, pos, sem)
            continue
        for i in range(len(pos)):
            # Get the POS-SEM pair
            ptag = pos[i]
            stag = sem[i]
            try:
                # Put the SEM tag into the sub-collection of a POS tag
                pos_tags[ptag].add(stag)
            except KeyError:
                # If the POS tag doesn't exist, add one
                pos_tags[ptag] = set()
                pos_tags[ptag].add(stag)
    # Export the error data
    if extract_errors:
        err_df = pd.DataFrame()
        err_df["document"] = err_sentences
        err_df["raw_pos"] = err_raw_pos
        err_df["processed_pos"] = err_pos
        err_df["sem"] = err_sem
        err_df.to_csv("inspections/error.tsv", sep="\t", encoding="UTF-8")
        print("Extracted.")
    return pos_tags


# %%

def get_pos_sem_pairs(tsv_filename, sampling=False, samples=100):
    """
    Get POS-SEM tag pairs
    """
    minidf = pd.read_csv(tsv_filename, sep="\t")
    if sampling:
        minidf = minidf.sample(n=samples)
    pos_sem_pairs = list()
    # Loop over the data frame
    for index, value in minidf.iterrows():
        # Extract record info of POS tags and SEM tags (and tokens as well)
        pos = value["pos"].split(" ")
        pos = pre_process_spacy_pos_NE(pos)
        sem = value["sem"].split(" ")
        # Ignore the non-aligned pairs
        if len(pos) != len(sem):
            continue
        for i in range(len(pos)):
            # Get the POS-SEM pair
            ptag = pos[i]
            stag = sem[i]
            pair = (ptag, stag)
            pos_sem_pairs.append(pair)
    return pos_sem_pairs


# %%
def get_unique_tags(tsv_filename):
    """
    Get POS-SEM tags
    """
    minidf = pd.read_csv(tsv_filename, sep="\t")
    pos_tags = set()
    sem_tags = set()
    # Loop over the data frame
    for index, value in minidf.iterrows():
        # Extract record info of POS tags and SEM tags (and tokens as well)
        pos = value["pos"].split(" ")
        pos = pre_process_spacy_pos_NE(pos)
        sem = value["sem"].split(" ")
        # Ignore the non-aligned pairs
        if len(pos) != len(sem):
            continue
        for i in range(len(pos)):
            # Get the POS-SEM pair
            ptag = pos[i]
            stag = sem[i]
            pos_tags.add(ptag)
            sem_tags.add(stag)
    return pos_tags, sem_tags


# %%
def get_cooccurrences(lang, visualise=False, savefig=False) -> pd.DataFrame:
    """
    This function is to create the co-occurrence dataframe for inference
    :param lang: language to infer from
    :param visualise: Choose to or not to show a heatmap of the results
    :param savefig: Choose to or not to export an image of the heatmap
    """
    file_directory = build_directory(data_directory, lang, default_tsv_filename)
    # Get POS-SEM tag pars
    pos_sem_pairs = get_pos_sem_pairs(file_directory)
    # Get the unique tags of each to count
    pos_tags, sem_tags = get_unique_tags(file_directory)
    # Sort the list of tags for data visualisation coherence
    pos_tags = sorted(pos_tags)
    sem_tags = sorted(sem_tags)
    # Count the co-occurrences
    pair_occurrences = Counter(pos_sem_pairs)
    # Create a dataframe out of the data collected
    result_df = pd.DataFrame(columns=pos_tags, index=sem_tags).fillna(0)
    for (ptag, stag), frequency in pair_occurrences.items():
        result_df[ptag][stag] = int(frequency)

    if visualise:
        # Set the visual stuff on air
        plt.subplots(figsize=(10, 20))
        sns.heatmap(result_df, cmap="YlGnBu", annot=True, fmt="d")
        if savefig:
            plt.savefig("heatmaps/" + lang + ".jpg")
        plt.show()
    return result_df


# %%
def get_stacked_cooc(_lang, sample_size=100, visualise=False, savefig=False) -> pd.DataFrame:
    """
    Get the co-occurrences of sem-pos tags in different languages
    """
    pos_tags = set()  # For saving unique POS tags
    sem_tags = set()  # For saving unique SEM tags
    mul_pairs = list()  # For saving co-occurrences
    langs = _lang.split(",")  # Chosen languages should be separated by comma

    for lang in langs:
        file_directory = build_directory(data_directory, lang, default_tsv_filename)
        # Get POS-SEM tag pars
        pos_sem_pairs = get_pos_sem_pairs(file_directory, sampling=True, samples=sample_size)
        # Get the unique tags of each to count
        pos, sem = get_unique_tags(file_directory)
        pos_tags.update(pos)
        sem_tags.update(sem)
        mul_pairs += pos_sem_pairs

    # Count the co-occurrences
    pair_occurrences = Counter(mul_pairs)
    # Create a dataframe out of the data collected
    result_df = pd.DataFrame(columns=pos_tags, index=sem_tags).fillna(0)
    for (ptag, stag), frequency in pair_occurrences.items():
        result_df[ptag][stag] = int(frequency)

    if visualise:
        # Set the visual stuff on air
        plt.subplots(figsize=(10, 20))
        sns.heatmap(result_df, cmap="YlGnBu", annot=True, fmt="d")
        if savefig:
            plt.savefig("heatmaps/" + "_".join(langs) + ".jpg")
        plt.show()
    return result_df


# %%
def get_tagging_rules(_lang, sample_size=100):
    """
    Get the tagging rule based on the highest co-occurrence of semantic tag along with the POS tag
    """
    sc_df = get_stacked_cooc(_lang, sample_size=sample_size)
    pos_sem = dict()

    for col in sc_df.columns:
        if col == "VERB":
            pos_sem[col] = "EVE"  # EVENT tag, to be disambiguated
        else:
            pos_sem[col] = sc_df[col].idxmax()
    return pos_sem


# %%
def get_data_from_tsv(_lang) -> pd.DataFrame:
    """
    For retrieving data (sentence, sem tag, pos tag) from the tsv files
    """
    file_directory = build_directory(data_directory, _lang, default_tsv_filename)
    return pd.read_csv(file_directory, sep="\t", encoding="UTF-8")


# %%

# Command Line facilitation
if __name__ == "__main__":
    args = utils.get_analysis_cli_ars()
    if args.command == "extract":
        file = args.file
        pipeline = args.pipeline
        print(get_pos_sem_tag(file, pipeline))
    elif args.command == "inspect":
        lang = args.lang
        extract_errors = args.extract_err
        results = get_pos_sem_alignment(lang, extract_errors=extract_errors)
        [print(key, results[key]) for key in results.keys()]
    elif args.command == "get_cooc":
        lang = args.lang
        stacked = args.stacked
        sample_size = args.sample_size
        visualise = args.visualise
        savefig = args.savefig
        if stacked:
            get_stacked_cooc(lang, sample_size=sample_size, visualise=visualise, savefig=savefig)
        else:
            get_cooccurrences(lang, visualise=visualise, savefig=savefig)
    else:
        raise RuntimeError(">> Invalid command!")
