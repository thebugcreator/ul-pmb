from collections import Counter
import analysis


def manual_tagging(text:str, _postags:str, pos_sem_alm:dict):
    tokens = text.split(" ")
    postags = _postags.split(" ")
    semtags = list()
    for i in range(len(tokens)):
        semtags.append(pos_sem_alm[postags[i]])

    return " ".join(semtags)

def