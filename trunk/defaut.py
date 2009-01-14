r"""
elementary definition of two simple types :
Matrix (as list of list)
WordMorphism (as dictionnary)
"""

def reversed_enumerate(l) :
    for i in range(len(l)-1,-1,-1) : yield i,l[i]


class WordMorphism(dict) :
    """implementation of elementary word morphism
    image of a word (it's callable from a string or a list)
    composition as multiplication

    sage : m = WordMorphism({'a':'ab','b':'bca','c':'ca'})
    sage : m('abc')
    abbcaca
    """

    def __repr__(self) :
        l = []
        for i in self :
            l.append(i + "->" + self[i])
        return ', '.join(l)
    
    def __call__(self,w) :
        l = list(w)
        for i,letter in reversed_enumerate(l) :
            if self.has_key(letter) : l[i:i+1] = self[letter]
        return ''.join(l)
    
    def __mul__(self,other) :
        d = WordMorphism({})
        for letter in other :
            d[letter] = self(other(letter))

        for letter in self :
            if letter not in other : d[letter] = self[letter]

        return d
