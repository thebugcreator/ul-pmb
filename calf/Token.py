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

class CharSeq :
    def __init__(self, string, is_token = False) :
        self.string = string 
        self.is_token = is_token
    def __str__(self) -> str:
        return self.string
    def __repr__(self) -> str:
        return self.__str__()

class PhraseToken (CharSeq) :
    def __init__(self, string, items = None, is_token=False):
        super().__init__(string, is_token)
        if items == None :
            self.items == (string,)
        else :
            self.items = items
        
    def __repr__(self) :
        return str(self.items)
    def __str__(self) -> str:
        return self.__repr__()

class SolidToken (CharSeq) :
    def __init__(self, string):
        super().__init__(string, True)
        