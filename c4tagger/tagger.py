import analysis


def manual_tagging(_postags: str, pos_sem_alm: dict) -> str:
    """
    This function is used to manually tag a single document according to its POS tags
    :param _postags: The POS tags of the document separated by spaces
    :param pos_sem_alm: The dictionary to look up the SEM tags using POS tags

    Return: A list of SEM tags separated by spaces
    """
    # Turn the POS tag string into a list
    postags = _postags.split(" ")
    semtags = list()
    for i in range(len(postags)):
        # Get the according SEM tag
        semtags.append(pos_sem_alm[postags[i]])

    return " ".join(semtags)


def get_probable_tag(_source_file) -> dict:
    """
    This function is to infer the most probable SEM tag from the POS tag
    :param _source_file: TSV file to infer
    """
    cooc_df = analysis.get_cooccurrences(_source_file)

    pos_sem_ref = dict()
    for column in cooc_df.columns:
        if column != "VERB":
            pos_sem_ref[column] = cooc_df[column].idxmax()
        else:
            # Set the tag to be a general EVENT (E99) tag subjecting to further disambiguation
            pos_sem_ref[column] = "E99"
    return pos_sem_ref

