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

    ilyaRule(tree)
    for pat, toks in patterns.items() :
        tree = apply_rule(tree, rule, pat, toks)
        # if i == 1 :break
    spaceRule(tree)
    # nE(tree)
    apaRule(tree)
    hyphRule(tree)

    return tree

def apply_rule(tree, rule, p, t) :
    # if type(tree) is str : tree = rule (tree, p, t)
    for i in range(len(tree.items)) :
        if type(tree.items[i]) is Token :
            pass
        elif type(tree.items[i]) is str :
            res = rule( tree.items[i], p, t)
            if type(res) is Tree :  tree.items[i] = res
        elif type(tree.items[i]) is Tree :
            apply_rule(tree.items[i], rule, p, t)
    return tree



def ilyaRule(tree):
    for  i, item in enumerate(tree.items) :
        if type(item) is str :
            if item.find("il y a ") < 0 and item.find("Il y a ") < 0 : return
            ind = 0
            l = len("il y a ")
            if item.find("il y a ") >= 0 : ind = item.find("il y a ") 
            if item[ ind+l ] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] :
                subtree = Tree()
                subtree.items.append( item[:ind] )
                subtree.items.append( Token("il", "y", "a") )
                subtree.items.append( item[ ind+l: ] )
                tree.items[i] = subtree



    pass

def isCapital(item):
    if type(item) is SpaceToken:
        if item.representation.istitle():
            return True
    elif type(item) is Tree :
        # nE(item)
        return False


def nE(tree):
    b , e= -1, -1

    for  i, item in enumerate(tree.items) :
        if isCapital(item) and b<0 :
            b = i
        if b>=0 and  not isCapital(item) and e<0 :
            e = i
    if len(tree.items[b:e]) > 1 : 
        t = Token( *tree.items[b:e] )
        tree.items[b] = t
        
    for  i, item in enumerate(tree.items) :
        if type(item) is Tree : nE(item)


def hyphRule(tree):
    for i, item in enumerate(tree.items):
        if type(item) is SpaceToken:
            tokens = item.items
            for token in tokens :
                if "-" in token[1:-1] :
                    temp = token.split("-")
                    if temp[-1] in ["moi", 'moi', 'toi', 'LUI', 'ELLE', 'soi', 'nous', 'vous', 'EUX', 'ELLES'] : continue
                    subtree = Tree()
                    subtree.items.append( Token(temp[0]) )
                    subtree.items.append( Token("-"+temp[1]) )
                    tree.items[i] = subtree 
        elif type(item) is Tree :
            hyphRule(item)


def apaRule(tree, *args):
    """ apostrophe rule"""
    for i, item in enumerate(tree.items) :
        if type(item) is SpaceToken :
            tokens = item.items
            for token in tokens :
                if "'" in token[1:-1] :
                    temp = token.split("'")
                    subtree = Tree()
                    subtree.items.append( Token(temp[0]+"'")  )
                    subtree.items.append( Token(temp[1])  )
                    tree.items[i] = subtree
        elif type(item) is Tree :
            apaRule(item)





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

def spaceRule(tree):
    """ tokenising by space"""
    for i in range(len(tree.items)) :
        if type(tree.items[i]) is Token :
            pass
        elif type(tree.items[i]) is str :
            s = tree.items[i]
            s_term = s.split(' ')
            res = Tree()
            for term in s_term :
                if len(term) > 0  : res.items.append( SpaceToken(term) )
            # res = rule (tree.items[i], p, t)
            if type(res) is Tree :  tree.items[i] = res
        elif type(tree.items[i]) is Tree :
            spaceRule(tree.items[i])


# def rule(seglist, term):
#     return rule1(seglist, term)
if __name__ == "__main__" :
    sen = input("input the sentence: ")
    tree = tokenise(sen, False)
    # print(tree)
    print(tree.show() )
    print()
    # print(*tree.graph() , sep='\n')

    