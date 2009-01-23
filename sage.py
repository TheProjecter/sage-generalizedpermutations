SageObject = object

class Alphabet(tuple) :
    rank = tuple.__getitem__

    def unrank(self, letter) :
        l = list(self)
        return l.index(letter)

class Matrix :
    pass

def identity_matrix(*args):
    raise NotImplementedError

def WordMorphism(dict) :
    def __call__(self,w) :
        raise NotImplementedError

    def __mul__(self, other) :
        raise NotImplementedError
