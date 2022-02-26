#Token.py : 
class Token:
    def __init__(self, *args):
        self.items = [*args]
        self.representation = "_".join(self.items)

    def __str__(self):
        return self.representation 

    def __repr__(self):
        return self.representation 

    def __getitem__(self, item):
        return self.items[item]

    def __len__(self):
        return len(self.representation)

class Tree:
    def __init__(self, string = None) -> None:
        self.items = []
        if type(string) is str and len(string) > 0 : self.items.append(string)

    def __str__(self) -> str:
        res = ""
        for item in self.items :
            res = res + str(item)
        return res

    def show(self):
        res = ""
        for i in self.items :
            if type(i) is str :
                res = res + i
            elif type(i) is Token:
                res = res + '[' + i.__str__() + ']'
            elif type(i) is Tree :
                res = res + i.show()

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

