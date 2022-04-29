# Token.py :
class Token:
    def __init__(self, *args):
        self.items = [*args]
        self.representation = "_".join(self.items)
        self.IOB = "B" + ( len(self.representation)-1 ) * "I"

    def __str__(self):
        return self.representation

    def __repr__(self):
        return self.representation

    def __getitem__(self, item):
        return self.items[item]

    def __len__(self):
        return len(self.representation)

class SpaceToken(Token):
    pass

class BlankToken(Token) :
    def __init__(self):
        super().__init__()


class Tree:
    def __init__(self, string=None) -> None:
        self.items = []
        self.eva_items = []
        self.IOBs = []
        if type(string) is str and len(string) > 0: 
            self.items.append(string)
            self.eva_items.append(string)
            # self.IOBs.append(len(string) * "S")
            self.IOBs.append("String")

    def __str__(self) -> str:
        res = ""
        for item in self.items:
            res = res + str(item) + ' '
        return res
        # return '_'.join(self.items)

    def show(self):
        res = ""
        for i in self.items:
            if type(i) is str:
                res = res + i
            elif type(i) is Tree:
                res = res + i.show()
            else:
                res = res + '[' + i.__str__() + ']'
        return res

    def get_tokens(self):
        res= []
        for item in self.items :
            if type(item) is Tree :
                res.extend(item.get_tokens() )
            else:#if type(item) is 
                res.append(item.__str__())
        return res
    def get_tokens_eva(self):
        res = []
        for item in self.eva_items :
            if type(item) is Tree :
                res.extend(item.get_tokens_eva())
            else:
                res.extend(item)
        return res

    def get_IOBs(self):
        res =[]
        for item in self.IOBs :
            if type(item) is Tree :
                res.extend(item.get_IOBs())
            else:
                res.append(item)
        return res



    def graph(self, inden=4):
        if len(self.items) == 0:
            return []
        elif len(self.items) == 1:
            if type(self.items[0]) is str:
                return [self.items[0]]
            elif type(self.items[0]) is Tree:
                return self.items[0].graph(inden)
            else:  # elif type(self.items[0]) is Token :
                return [self.items[0].__str__()]
        else:
            res = []
            pre1 = '.' + '-' * inden + ' '
            pre2 = '|' + '-' * inden + ' '
            pre3 = '|' + ' ' * inden + ' '
            pre4 = ' ' + ' ' * inden + ' '
            pre = pre1
            for i, item in enumerate(self.items):
                if i == 1: pre = pre2
                if type(item) is str:
                    res.append(pre + item)
                    # if i != len(self.items)-1: res.append( '|')
                elif type(item) is Tree:
                    temp = item.graph(inden)
                    res.append(pre + temp[0])
                    if i == len(self.items) - 1: pre3 = pre4
                    for t in temp[1:]:
                        res.append(pre3 + t)
                else:  # elif type(item) is Token
                    res.append(pre + item.__str__())
                    # if i != len(self.items)-1: res.append( '|')
            return res


# class CharSeq :
#     def __init__(self, string, is_token = False) :
#         self.string = string 
#         self.is_token = is_token
#     def __str__(self) -> str:
#         return self.string

# class PhraseToken (CharSeq) :
#     def __init__(self, string, items = None, is_token=False):
#         super().__init__(string, is_token)
#         if items == None :
#             self.items == (string,)
#         else :
#             self.items = items
#     def __repr__(self) :
#         return str(self.items)
#     def __str__(self) -> str:
#         return self.__repr__()
