# functions_def.py

from Token import *
from constants import considered_letters, patterns



def tokenise(sentence: str, iob_option=False, by_contract=True, cut_mod=True):
    """ 
    this function tokenises the sentence passed to it, in a cutter-based manner. the result is a 'Tree' object, which has an attribute 'items'.
    each element of the 'items' list could be a subsentence(string) , a token , or a subtree recursively. but usually it ends up 
    with no string item and all of them have converted to tokens. we add a eva_items with the same size for the purpose of evaluation.
    """
    if type(sentence) is not str :
        print('wrong input type!')
        return -1
    weAddSpace = False
    if (sentence[-2] in considered_letters+"0123456789") and by_contract:
        # If there's not a space before the terminal symbol, add one
        # if sentence[-1] in (".", "!", "?",):
            well_formed_sentence = sentence[0:-1] + " " + sentence[-1]
            sentence = well_formed_sentence
            weAddSpace = True

    tree = Tree(sentence)
    # tree.items.append(sentence)
    # tree = sentence

    il_y_a_Rule(tree) # 
    # applying the rules in patterns
    for pat, toks in patterns.items():
        tree = apply_rule(tree, rule, pat, toks)
        # if i == 1 :break
    spaceRule(tree)
    namedEntity(tree)
    apaRule(tree)
    hyphRule(tree)

    IOB_tags = tree.get_IOBs()
    last = IOB_tags[-1]
    IOB_tags[-1] = last[:-1] # removng the extra 'o' from the end of the punctuation token
    if weAddSpace:
        last = IOB_tags[-2]
        IOB_tags[-2] = last[:-1] #  removng the extra 'o' from the end of the last token
    return tree.get_tokens(), IOB_tags, tree.get_tokens_eva() 
###########
def namedEntity(tree):
    flag = False
    ind = -1
    ne = []
    toDel = []
    Conj = ['In', 'And', 'But', 'Otherwise', 'Or', 'By', 'However', 'Le', 'La', 'Les', 'Un', 'Une', 'Des', 'Ce', 'Ou']
    for i, item in enumerate(tree.items):
        if flag:
            if type(item) is Tree : 
                flag = False
                ne = []
                toDel.extend( list( range(ind+1, i)  )  )
                namedEntity(item)
                continue
            elif type(item) is SpaceToken and ( not item.representation.istitle() ):
                flag = False
                ne = []
                toDel.extend( list( range(ind+1, i)  )  )
                continue
            elif  type(item) is SpaceToken and (  item.representation.istitle() ):
                ne.extend(item.items)
                tree.items[ind] = Token(*ne) 
                # tree.items[ind].items.extend(item.items)
                # print(tree.items[ind].items)
                tree.items[i] = ''
                # IOB tag
                tree.IOBs [ind] = tree.items[ind].IOB + "O"
                tree.IOBs [i] = ""

                # apply the same to the eva_items
                tree.eva_items[ind][0] = (Token(*ne), ne[0])
                tree.eva_items[ind].append((BlankToken(), item.items[0] ))

                # tree.eva_items[i][0] = (BlankToken(), item.items[0] )
                tree.eva_items[i][0] = (BlankToken(), '' )
                
        else:
            if type(item) is Tree : 
                namedEntity(item)
                continue
            elif i==0 and ( type(item) is SpaceToken ) and item.representation.istitle() and (item.representation in Conj) :
                # print('lets continue')
                continue
            elif ( type(item) is SpaceToken ) and not item.representation.istitle():
                # print('not title', item)
                pass
            elif ( type(item) is SpaceToken ) and item.representation.istitle():
                flag = True
                ne = []
                ne.extend(item.items)
                # tree.items[i] = 
                ind = i

    for i in range( len(tree.items)-1, 0, -1):
        if tree.items[i] == '':
            del tree.items[i]
            del tree.eva_items[i]
            # print('deleted item', i)
            del tree.IOBs[i]

def apply_rule(tree, rule, p, t):
    """
    this function is just for calling another function, like 'Rule' function. it might seem to be redundant, but preferably I kept it.
    """
    ### this line was for testing during development. ( if type(tree) is str : tree = rule (tree, p, t)  )
    for i in range(len(tree.items)):
        if type(tree.items[i]) is Token:
            pass
        elif type(tree.items[i]) is str:
            res = rule(tree.items[i], p, t)
            if type(res) is Tree:  
                tree.items[i] = res
                tree.eva_items[i] = res
                tree.IOBs [i] = res
        elif type(tree.items[i]) is Tree:
            apply_rule(tree.items[i], rule, p, t)
    return tree # In fact we don't need to return anything because the tree is changed on itself. this line is also kind of redundant.


def rule (string, pattern, tokens):
    """
    The input is supposed to be an string including some specific phrases like "Aujourd'hui" .
    """
    if string.find(pattern) <0 : return string
    items = string.split(pattern)
    subtree = Tree()
    for item in items[:-1] :
        if len(item) > 0 : 
            subtree.items.append(item)
            subtree.eva_items.append(item)
            subtree.IOBs.append("S")
        for t in tokens :
            subtree.items.append(Token(t))
            subtree.IOBs.append("B" + "I" * (len(t)-1) +"O")
            if len(t.split(' ')) > 1 :
                ar= [] # an array of pairs of  (token , 'token representation')
                for i, it in enumerate( t.split(' ') ) :
                    if i == 0 :
                        ar.append((Token(t),it))
                        continue
                    else:
                        ar.append( (BlankToken(), it))
                subtree.eva_items.append(ar)
            else:
                subtree.eva_items.append([(Token(t),t)])
    if len(items[-1]) > 0 : 
        subtree.items.append(items[-1])
        subtree.eva_items.append(items[-1])
        subtree.IOBs.append("S")
    return subtree

def il_y_a_Rule(tree):
    """
    This rule is for detecting 'il y a' in the sentence and base on the context, decide to tokenise it as one or three tokens. 
    """
    for  i, item in enumerate(tree.items) :
        if type(item) is str :
            if item.find("il y a ") < 0 and item.find("Il y a ") < 0 : 
                return # in case that there is not an instance of il_y_a
            else :
                ind = max(item.find("il y a "), item.find("Il y a "))
                l = len("il y a ")
                # if item.find("il y a ") >= 0 : ind = item.find("il y a ") 
                if item[ ind+len("il y a ") ] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] :
                    subtree = Tree()
                    subtree.items.append( item[:ind] )
                    subtree.eva_items.append( item[:ind] )
                    subtree.IOBs.append (len(item[:ind])*"S" )

                    subtree.items.append( Token("il", "y", "a") )
                    subtree.eva_items.append( [(Token("il", "y", "a"), "il"), (BlankToken(), 'y'), (BlankToken(), 'a')] )
                    subtree.IOBs.append( "B" + (len("il y a")-1)*"I" + "O")


                    subtree.items.append( item[ ind+l: ] )
                    subtree.eva_items.append( item[ ind+l: ] )
                    subtree.IOBs.append("S")

                    tree.items[i] = subtree
                    tree.eva_items[i] = subtree
                    tree.IOBs[i] = subtree


def hyphRule(tree):
    """ hyphen rule. like dit-moi should be seperated."""
    for i, item in enumerate(tree.items):
        if type(item) is SpaceToken:
            # tokens = item.items
            for part in item.items :  #  we suppose that this SpaceToken has just one item,
                if "-" in part[1:-1] :
                    temp = part.split("-")
                    if temp[-1] not in ['moi', 'toi', 'LUI', 'lui', 'ELLE', 'elle', 'soi', 'nous', 'vous', 'EUX', 'eux', 'ELLES', 'elles'] : continue
                    subtree = Tree()
                    subtree.items.append( Token(temp[0]) )
                    subtree.items.append( Token("-"+temp[1]) )
                    #
                    subtree.eva_items.append( [(Token(temp[0]), temp[0])] )
                    subtree.eva_items.append( [(Token("-"+temp[1]), "-"+temp[1] )] )
                    #
                    subtree.IOBs.append("B" + "I"*(len(temp[0])-1))
                    subtree.IOBs.append("B"+ "I"*(len(temp[1])) +"O")

                    tree.items[i] = subtree 
                    tree.eva_items[i] = subtree 
                    tree.IOBs[i] = subtree
                break # we suppose that this Token has just one item, because it is tokenised after "spaceToken" function
        elif type(item) is Tree :
            hyphRule(item)


def apaRule(tree, *args):
    """ 
    apostrophe rule, this rule is for seperating concatenations like "J'habite" into two tokens.
    """
    for i, item in enumerate(tree.items) :
        if type(item) is SpaceToken :
            # token_parts = item.items
            for part in  item.items : #  we suppose that this SpaceToken has just one item,
                if "'" in part[1:-1] :
                    temp = part.split("'")
                    subtree = Tree()
                    subtree.items.append( Token(temp[0]+"'")  )
                    subtree.items.append( Token(temp[1])  )
                    # do the same to eva_items
                    subtree.eva_items.append( [(Token(temp[0]+"'"), temp[0]+"'")])
                    subtree.eva_items.append( [(Token(temp[1]), temp[1])])
                    #
                    subtree.IOBs.append("B" + "I"*(len(temp[0])))
                    subtree.IOBs.append("B"+ "I"*(len(temp[1])-1) +"O")

                    tree.items[i] = subtree
                    tree.eva_items[i] = subtree
                    tree.IOBs[i] = subtree
                break # because we suppose that this Token has just one item, because it is tokenised after "spaceToken" function
        elif type(item) is Tree :
            apaRule(item)






def spaceRule(tree):
    """ tokenising by space"""
    for i in range(len(tree.items)) :
        if type(tree.items[i]) is Token :
            pass
        elif type(tree.items[i]) is str :
            # s = tree.items[i]
            s_term = tree.items[i].split(' ')
            res = Tree()
            for term in s_term :
                if len(term) > 0  : 
                    res.items.append( SpaceToken(term) )
                    res.eva_items.append( [(SpaceToken(term) , term )] )
                    res.IOBs.append( "B" + "I" * (len(term) - 1) + "O")
            # res = rule (tree.items[i], p, t)
            if type(res) is Tree :  
                tree.items[i] = res
                tree.eva_items[i] = res
                tree.IOBs[i] = res
        elif type(tree.items[i]) is Tree :
            spaceRule(tree.items[i])

def leven(a, b):
    """ 
    levenshtein distance between two strings.
    """
    if len(b) == 0: return len(a)
    elif len(a) == 0 : return len(b)
    elif a[0]==b[0] : return leven(a[1:], b[1:])
    else : return 1 + min( leven(a[1:], b) , leven(a, b[1:]), leven(a[1:], b[1:]) )
#

def ilyaRule(tree):
    for i, item in enumerate(tree.items):
        if type(item) is str:
            if item.find("il y a ") < 0 and item.find("Il y a ") < 0: return
            ind = 0
            l = len("il y a ")
            if item.find("il y a ") >= 0: ind = item.find("il y a ")
            if item[ind + l] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                subtree = Tree()
                subtree.items.append(item[:ind])
                subtree.items.append(Token("il", "y", "a"))
                subtree.items.append(item[ind + l:])
                tree.items[i] = subtree

    pass


def isCapital(item):
    if type(item) is SpaceToken:
        if item.representation.istitle():
            return True
    elif type(item) is Tree:
        # nE(item)
        return False


def nE(tree):
    b, e = -1, -1

    for i, item in enumerate(tree.items):
        if isCapital(item) and b < 0:
            b = i
        if b >= 0 and not isCapital(item) and e < 0:
            e = i
    if len(tree.items[b:e]) > 1:
        t = Token(*tree.items[b:e])
        tree.items[b] = t

    for i, item in enumerate(tree.items):
        if type(item) is Tree: nE(item)


# def hyphRule(tree):
#     for i, item in enumerate(tree.items):
#         if type(item) is SpaceToken:
#             tokens = item.items
#             for token in tokens:
#                 if "-" in token[1:-1]:
#                     temp = token.split("-")
#                     if temp[-1] in ["moi", 'moi', 'toi', 'LUI', 'ELLE', 'soi', 'nous', 'vous', 'EUX', 'ELLES']: continue
#                     subtree = Tree()
#                     subtree.items.append(Token(temp[0]))
#                     subtree.items.append(Token("-" + temp[1]))
#                     tree.items[i] = subtree
#         elif type(item) is Tree:
#             hyphRule(item)


# def apaRule(tree, *args):
#     """ apostrophe rule"""
#     for i, item in enumerate(tree.items):
#         if type(item) is SpaceToken:
#             tokens = item.items
#             for token in tokens:
#                 if "'" in token[1:-1]:
#                     temp = token.split("'")
#                     subtree = Tree()
#                     subtree.items.append(Token(temp[0] + "'"))
#                     subtree.items.append(Token(temp[1]))
#                     tree.items[i] = subtree
#         elif type(item) is Tree:
#             apaRule(item)


# def rule(string, pattern, tokens):
#     if string.find(pattern) < 0: return string
#     items = string.split(pattern)
#     subtree = Tree()
#     for item in items[:-1]:
#         if len(item) > 0: subtree.items.append(item)
#         for t in tokens:
#             subtree.items.append(Token(t))
#     if len(items[-1]) > 0: subtree.items.append(items[-1])
#     return subtree


# def spaceRule(tree):
#     """ tokenising by space"""
#     for i in range(len(tree.items)):
#         if type(tree.items[i]) is Token:
#             pass
#         elif type(tree.items[i]) is str:
#             s = tree.items[i]
#             s_term = s.split(' ')
#             res = Tree()
#             for term in s_term:
#                 if len(term) > 0: res.items.append(SpaceToken(term))
#             # res = rule (tree.items[i], p, t)
#             if type(res) is Tree:  tree.items[i] = res
#         elif type(tree.items[i]) is Tree:
#             spaceRule(tree.items[i])


# def rule(seglist, term):
#     return rule1(seglist, term)
if __name__ == "__main__":
    sen = input("input the sentence: ")
    tree = tokenise(sen, True)
    # print(tree)
    print(tree)
    print()
    # print(*tree.graph() , sep='\n')
