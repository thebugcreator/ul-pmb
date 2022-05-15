import argparse

import pandas as pd
import spacy


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


# get_pos_sem_tag("train_gold_it", "it_core_news_md")
# get_pos_sem_tag("train_gold_en", "en_core_web_md")


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


# print(pre_process_spacy_pos_NE(['PROPN', 'PROPN', 'X', 'PROPN', 'PROPN', 'VERB', 'ADP', 'NUM', 'PUNCT']))
# Result: ['PROPN', 'VERB', 'ADP', 'NUM', 'PUNCT']


# %%
def get_pos_sem_alignment(tsv_filename, show_non_aligned=False, extract_errors=False):
    """
    Get POS-SEM tag alignment
    :param tsv_filename: csv filename
    :param show_non_aligned: Choose to show the non-aligned documents
    :param extract_errors: Choose to extract the non-aligned documents to tsv
    :return:
    """
    minidf = pd.read_csv(tsv_filename, sep="\t")
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
        err_df = pd.DataFrame(list(zip(err_raw_pos, err_pos, err_sem)),
                              index=err_sentences,
                              columns=["raw_pos", "processed_pos", "sem"])
        err_df.to_csv("inspections/error.tsv", sep="\t", encoding="UTF-8")
        print("Extracted.")
    return pos_tags


# pos_tags = get_pos_sem_alignment("train_gold_it.tsv")
# print(pos_tags)

# %%
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Data extractor")
    subparsers = parser.add_subparsers(help='sub-command', dest='command')

    # Add Command Line arguments for the extractor
    parser_c4 = subparsers.add_parser("extract", help="Data extraction")
    parser_c4.add_argument("--file", type=str, default="en", help="CoNLL file path")
    parser_c4.add_argument("--pipeline", type=str, default="en_core_web_sm", help="Spacy pipeline name")
    # Add Command Line arguments to interpret the alignment
    parser_c4 = subparsers.add_parser("inspect", help="Data inspection")
    parser_c4.add_argument("--file", type=str, default="fr", help="TSV file path")
    parser_c4.add_argument("--extract_errors", type=bool, default=False,
                           help="Choose to or not to extract the non aligned documents")
    args = parser.parse_args()
    if args.command == "extract":
        file = args.file
        pipeline = args.pipeline
        print(get_pos_sem_tag(file, pipeline))
    elif args.command == "inspect":
        file = args.file
        extract_errors = args.extract_errors
        results = get_pos_sem_alignment(file, extract_errors=extract_errors)
        [print(key, results[key]) for key in results.keys()]
    else:
        raise RuntimeError(">> Invalid command!")
