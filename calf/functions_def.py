#functions_def.py

from Token import *
from constants import considered_letters, patterns

def tokenise(sentence: str, iob_option = False, by_contract = True, cut_mod = True):
    if  ( sentence[-2]  in considered_letters ) and  by_contract :
        # If there's not a space before the terminal symbol, add one
        if sentence[-1] in ( ".", "!", "?", ):
            well_formed_sentence = sentence[0:-1] + " " + sentence[-1]
            sentence = well_formed_sentence
    
    tree = Tree()
    tree.items.append(sentence)
    # tree = sentence
    
    for pat, toks in patterns.items() :
        tree = apply_rule(tree, rule, pat, toks)
        # if i == 1 :break
    lastRule(tree)
    return tree

def apply_rule(tree, rule, p, t) :
    # if type(tree) is str : tree = rule (tree, p, t)
    for i in range(len(tree.items)) :
        if type(tree.items[i]) is Token :
            pass
        elif type(tree.items[i]) is str :
            res = rule (tree.items[i], p, t)
            if type(res) is Tree :  tree.items[i] = res
        elif type(tree.items[i]) is Tree :
            apply_rule(tree.items[i], rule, p, t)
    return tree



def rule (string, pattern, tokens):
    if string.find(pattern) <0 : return string
    items = string.split(pattern)
    subtree = Tree()
    for item in items[:-1] :
        if len(item) > 0 : subtree.items.append(item)
        for t in tokens :
            subtree.items.append(Token(t))
    if len(items[-1]) > 0 : subtree.items.append(items[-1])
    return subtree

def lastRule(tree):
    """ tokenising by space"""
    for i in range(len(tree.items)) :
        if type(tree.items[i]) is Token :
            pass
        elif type(tree.items[i]) is str :
            s = tree.items[i]
            s_term = s.split(' ')
            res = Tree()
            for term in s_term :
                if len(term) > 0  : res.items.append( Token(term) )
            # res = rule (tree.items[i], p, t)
            if type(res) is Tree :  tree.items[i] = res
        elif type(tree.items[i]) is Tree :
            lastRule(tree.items[i])


# def rule(seglist, term):
#     return rule1(seglist, term)
if __name__ == "__main__" :
    sen = input("input the sentence: ")
    tree = tokenise(sen, False)
    # print(tree)
    print(tree.show() )

    