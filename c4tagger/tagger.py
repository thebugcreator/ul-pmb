# Placeholder for imports


# Tagger
def manual_tagging(_postags: list, tagging_rules: dict,) -> list:
    """
    This function is used to manually tag a single document according to its POS tags
    :param _postags: The POS tags of the document separated by spaces
    :param tagging_rules: The dictionary to look up the SEM tags using POS tags
    Return: A list of SEM tags separated by spaces
    """
    # Turn the POS tag string into a list
    out_stag = []
    for ptag in _postags:
        try:
            out_stag.append(tagging_rules[ptag])
        except KeyError:
            out_stag.append("ZZZ")
    return out_stag
