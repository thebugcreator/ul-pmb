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

