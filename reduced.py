r"""
Definition of reduced object


    A reduced (generalized) permutation is better suited to study strata of
    Abelian (or quadratic) holomorphic forms on Riemann surfaces. The Rauzy
    diagram is an invariant of such a component. Corentin  Boissy proved the
    identification of Rauzy diagrams with connected components of stratas.
    But the geometry of the diagram is not yet totally understood.

AUTHORS: 
    -- Vincent Delecroix (2008-12-20): initial version
"""
from sage import SageObject
#from sage.structure.sage_object import SageObject
Alphabet = tuple
#from sage.combinat.words.alphabet import Alphabet

from template import AbelianPermutation, QuadraticPermutation
from template import FlippedAbelianPermutation, FlippedQuadraticPermutation
from template import RauzyDiagram


class ReducedPermutation(SageObject) :
    r"""
    Template for reduced objects

    ...DO NOT USE...
    """

    def __init__(self, intervals=[[],[]], alphabet = None) :
        r"""
        Constructor of ReducedPermutation.

        INPUT:
            intervals -- a list of two list of labels or a ReducedPermutation
            alphabet --  (defaut: None) any object that can be used to
            initialize an Alphabet  or None. In this latter case, the
            letter of intervals are used to generate an alphabet.
        """
        self._twin = [[],[]]


        self._init_twin(intervals)

        if alphabet == None :
            self._init_alphabet(intervals)
        elif isinstance(alphabet, Alphabet) :
            if len(alphabet) < len(self) : raise TypeError("The alphabet is too short")
            self._alphabet = alphabet
        else :
            self._alphabet = Alphabet(alphabet)
            if len(alphabet) < len(self) : raise TypeError("The alphabet is too short")
        
        self._alphabetize = lambda i : self._alphabet[i]



    def get_alphabet(self) :
        r"""
        Return the alphabet.
        """
        return self._alphabet
        

    def set_alphabet(self,l) :
        r"""
        Set a new alphabet.
        """
        a = Alphabet(l)
        if len(a) != len(self) : raise TypeError("Must be of the same length the permutation is")
        self._alphabet = a


    doc_alphabet = "Alphabet for the representation of the reduced permutation"

    alphabet = property(fget = get_alphabet, fset = set_alphabet, doc=doc_alphabet)


######################################
#####     ABELIAN PERMUTATION    #####
######################################
class ReducedAbelianPermutation(ReducedPermutation, AbelianPermutation):
    r"""
    Reduced Abelian permutation

    Abelian Permutation without numerotation of intervals. For initialization,
    you should use GeneralizedPermutation which is the class factory for all
    permutation types.

    EXAMPLES :
        Equality testing (no equality of letters but just of ordering) :
        sage : p = GeneralizedPermutation('a b c', 'c b a', reduced = True)
        sage : q = GeneralizedPermutation('p q r', 'r q p', reduced = True)
        sage : p == q
        True

    
        Reducibility testing :
        sage : p = GeneralizedPermutation('a b c', 'c b a', reduced = True)
        sage : p.is_reducible()
        False

        sage : q = GeneralizedPermutation('a b c d', 'b a d c', reduced = True)
        sage : q.is_reducible()
        True


        Rauzy movability and Rauzy move :
        sage : p = GeneralizedPermutation('a b c', 'c b a', reduced = True)
        sage : p.is_rauzy_movable(1)
        True
        sage : p.rauzy_move(1)
        sage : p
        a b c
        b c a
        sage : p.is_rauzy_movable(1)
        True
        sage : p.rauzy_move(1)
        sage : p
        a b c
        c b a


        Rauzy diagrams :
        sage : p = gp.GeneralizedPermutation('a b c d', 'd a b c')
        sage : p_red = gp.GeneralizedPermutation('a b c d', 'd a b c', reduced = True)
        sage : d = p.rauzy_diagram()
        sage : d_red = p_red.rauzy_diagram()
        sage : len(d), len(d_red)
        12, 6
        sage : d
         0 : ('a b c d', 'd a b c')  [1, 0]
         1 : ('a b c d', 'd c a b')  [2, 3]
         2 : ('a b c d', 'd b c a')  [0, 4]
         3 : ('a b d c', 'd c a b')  [5, 1]
         4 : ('a d b c', 'd b c a')  [4, 6]
         5 : ('a b d c', 'd c b a')  [3, 7]
         6 : ('a c d b', 'd b c a')  [8, 2]
         7 : ('a c b d', 'd c b a')  [9, 10]
         8 : ('a c d b', 'd b a c')  [6, 11]
         9 : ('a c b d', 'd a c b')  [11, 9]
        10 : ('a d c b', 'd c b a')  [10, 5]
        11 : ('a c b d', 'd b a c')  [7, 8]
        sage : d_red
         0 : d a b c  [1, 0]
         1 : d c a b  [2, 3]
         2 : d b c a  [0, 4]
         3 : c d a b  [5, 1]
         4 : b c d a  [4, 5]
         5 : c d b a  [3, 2]
    """

    def copy(self) :
        r"""
        Do a copy of the Abelian permutation.

        EXAMPLES :
            sage : p = GeneralizedPermutation('a b c', 'c b a', reduced = True)
            sage : q = p.copy()
            sage : p == q
            True
            sage : p.rauzy_move(0)
            sage : p == q
            False
        """
        p = ReducedAbelianPermutation(([],[]))
        p._twin[0].extend(self._twin[0])
        p._twin[1].extend(self._twin[1])
        p._alphabet = self._alphabet
        return p

    
    def _init_alphabet(self,a) :
        self._alphabet = Alphabet(a[0])


    def __list__(self) :
        r"""
        Mutation of the permutation to a list of two lists.
        """
        a0 = map(self._alphabetize, range(0,len(self)))
        a1 = map(self._alphabetize, self._twin[1])
        return [a0,a1]
        

    def __eq__(self,other) :
        r"""
        Test of equality

        Two reduced permutations are equal if they have the same order of
        apparition of intervals. Non necessarily the same alphabet.
        (perhaps it's better to change ?)

        EXAMPLES:
            sage : p = GeneralizedPermutation('a b c', 'c b a', reduced = True)
            sage : q = GeneralizedPermutation('b a c', 'c a b', reduced = True)
            sage : p == q
            True

        AUTHORS:
            - Vincent Delecroix (2008-12-20)
        """
        return self._twin[0] == other._twin[0]


    def __ne__(self,other) :
        r"""
        Test of difference
        """
        return self._twin[0] != other._twin[0]
    

    def copy(self) :
        r"""
        Do a copy of the Abelian permutation.

        EXAMPLES :
            sage : p = GeneralizedPermutation('a b c', 'c b a', reduced = True)
            sage : q = p.copy()
            sage : p == q
            True
            sage : p.rauzy_move(0)
            sage : p == q
            False
        """
        q = ReducedAbelianPermutation(("",""))
        q._twin = [self._twin[0][:], self._twin[1][:]]
        q._alphabet = self._alphabet
        q._alphabetize = lambda i : self._alphabet[i]

        return q
        
        
    def rauzy_diagram(self) :
        r"""
        Create the Rauzy diagram associated with this permutation

        OUTPUT:
            a Rauzy diagram (tyhe type is reduced.AbelianRauzyDiagram)

        EXAMPLES:
            sage : p = GeneralizedPermutation('a b c d', 'd a b c')
            sage : d = p.rauzy_diagram()
            sage : d
             0 : d a b c  [1, 0]
             1 : d c a b  [2, 3]
             2 : d b c a  [0, 4]
             3 : c d a b  [5, 1]
             4 : b c d a  [4, 5]
             5 : c d b a  [3, 2]

        For more information, try help RauzyDiagram

        AUTHORS :
            - Vincent Delecroix (2008-12-20)
        """
        return ReducedAbelianRauzyDiagram(self)


#####################################################################
##############    QUADRATIC REDUCED PERMUTATIONS    #################
#####################################################################
def alphabetized_qtwin(twin, alphabet) :
    i_a = 0
    l = ([False]*len(twin[0]),[False]*len(twin[1]))
    # False means empty here
    for i in range(2) :
        for j in range(len(l[i])) :
            if  l[i][j] == False :
                l[i][j] = alphabet[i_a]
                l[twin[i][j][0]][twin[i][j][1]] = alphabet[i_a]
                i_a += 1
    return l


def numerized_qflips(twin, flips) :
    r"""
    Return a list of flips as numbers.
    """
    ntwin = alphabetized_qtwin(twin, [1,2,3,4,5,6,7,8,9])  # TO MODIFY !!!
    l = []
    for interval in (0,1) :
        for j,flip in enumerate (self._flips[i]):
            if (self._flips == -1) and (ntwin[i][j] not in l) :
                l.append(ntwin[i][j])
    return l
        

class ReducedQuadraticPermutation(ReducedPermutation, QuadraticPermutation):
    r"""
    reduced quadratic (or generalized) permutation

    EXAMPLES :
        Reducibility testing :
        sage : p = GeneralizedPermutation('a b b', 'c c a', reduced = True)
        sage : p.is_reducible()
        False

        sage : p = GeneralizedPermutation('a b c a', 'b d d c', reduced = True)
        sage : p.is_reducible()
        True
        sage : test, decomposition = p.is_reducible(return_decomposition = True)
        sage : test
        True
        sage : decomposition
        (['a'],['c','a'],[],['c'])

    
        Rauzy movavability and Rauzy move :
        sage : p = GeneralizedPermutation('a b b', 'c c a', reduced = True)
        sage : p.is_rauzy_movable(0)
        True
        sage : p.rauzy_move(0)
        sage : p
        a a b b
        c c
        sage : p.is_rauzy_movable(0)
        False
        sage : p.rauzy_move(1)
        sage : p
        a a b
        b c c


        Rauzy diagrams
        sage : p = GeneralizedPermutation('a b b', 'c c a')
        sage : p_red = GeneralizedPermutation('a b b', 'c c a', reduced = True)
        sage : d = p.rauzy_diagram()
        sage : d_red = p_red.rauzy_diagram()
        sage : len(d), len(d_red)
        12, 4
        sage : d
         0 : ('a b b', 'c c a')  [1, 0]
         1 : ('a a b b', 'c c')  [-1, 2]
         2 : ('a a b', 'b c c')  [2, 3]
         3 : ('a a', 'b b c c')  [4, -1]
         4 : ('c a a', 'b b c')  [5, 4]
         5 : ('c c a a', 'b b')  [-1, 6]
         6 : ('c c a', 'a b b')  [6, 7]
         7 : ('c c', 'a a b b')  [8, -1]
         8 : ('b c c', 'a a b')  [9, 8]
         9 : ('b b c c', 'a a')  [-1, 10]
        10 : ('b b c', 'c a a')  [10, 11]
        11 : ('b b', 'c c a a')  [0, -1]
        sage : d_red
         0 : ('a b b', 'c c a')  [1, 0]
         1 : ('a a b b', 'c c')  [-1, 2]
         2 : ('a a b', 'b c c')  [2, 3]
         3 : ('a a', 'b b c c')  [0, -1]
    """

    def copy(self) :
        r"""
        Do a copy of the Quadratic permutation.

        EXAMPLES :
            sage : p = GeneralizedPermutation('a b b', 'c c a', reduced = True)
            sage : q = p.copy()
            sage : p == q
            True
            sage : p.rauzy_move(0)
            sage : p == q
            False

        AUTHORS :
            - Vincent Delecroix (2008-20-12)
        """
        p = ReducedQuadraticPermutation(([],[]))
        p._twin[0].extend(self._twin[0])
        p._twin[1].extend(self._twin[1])
        p._alphabet = self._alphabet
        return p

    def _init_alphabet(self,a) :
        r"""
        Intialization procedure of the alphabet of self
        """
        tmp_alphabet = []
        for letter in a[0]+a[1] :
            if letter not in tmp_alphabet :
                tmp_alphabet.append(letter)

        self._alphabet = tuple(tmp_alphabet)


    def __list__(self) :
        r"""
        the permutations as a list of two lists

        EXAMPLES:
        sage : p = GeneralizedPermutation('a b b', 'c c a', reduced = True)
        sage : list(p)
        [['a', 'b', 'c'], ['c', 'c', 'a']]

        AUTHORS:
            - Vincent Delecroix (2008-12-20)
        """
        return alphabetized_qtwin(self._twin, self.alphabet)
        

    def __eq__(self, other) :
        r"""
        Test of equality

        Two reduced permutations are equal if they have the same order of
        apparition of intervals. Non necessarily the same alphabet.
        (perhaps it's better to change ?)

        EXAMPLES:
            sage : p = GeneralizedPermutation('a b b', 'c c a', reduced = True)
            sage : q = GeneralizedPermutation('b a a', 'c c b', reduced = True)
            sage : r = GeneralizedPermutation('t s s', 'w w t', reduced = True)
            sage : p == q
            True
            sage : p == r
            True

        AUTHORS:
            - Vincent Delecroix (2008-12-20)
        """
        return (self._twin == other._twin)


    def __ne__(self, other) :
        r"""
        Test of difference
        """
        return (self._twin != other._twin)


    def rauzy_diagram(self) :
        r"""
        Create the Rauzy diagram associated with this permutation

        OUTPUT:
            a Rauzy diagram (tyhe type is reduced.AbelianRauzyDiagram)

        EXAMPLES:
            sage : p = GeneralizedPermutation('a b c d', 'd a b c')
            sage : d = p.rauzy_diagram()
            sage : d
             0 : d a b c  [1, 0]
             1 : d c a b  [2, 3]
             2 : d b c a  [0, 4]
             3 : c d a b  [5, 1]
             4 : b c d a  [4, 5]
             5 : c d b a  [3, 2]

        For more information, try help RauzyDiagram

        AUTHORS :
            - Vincent Delecroix (2008-12-20)
        """

        return ReducedQuadraticRauzyDiagram(self)




####################################################
#############    FLIPPED ABELIAN    ################
####################################################
class FlippedReducedPermutation(ReducedPermutation) :
    r"""
    Flipped Reduced Permutation.

    ... DO NOT USE...
    """
    def __init__(self, intervals=[[],[]], flips=[[],[]], alphabet=None) :
        self._twin = [[],[]]

        if alphabet == None : self._init_alphabet(intervals)
        else : self._alphabet = alphabet
        
        self._alphabetize = lambda i : self._alphabet[i]

        self._init_twin(intervals)
        self._init_flips(intervals, flips)



class FlippedReducedAbelianPermutation(FlippedAbelianPermutation, FlippedReducedPermutation) :
    r"""
    Flipped Reduced Abelian Permutation.

    EXAMPLES:
        sage : p = GeneralizedPermutation('a b c','c b a', flips=['a'])
        sage : p.rauzy_move(1)
        sage : p
        -c -a  b
        -c  b -a
    """
    def _init_alphabet(self,a) :
        r"""
        Intialization procedure of the alphabet of self
        """
        tmp_alphabet = []
        for letter in a[0]+a[1] :
            if letter not in tmp_alphabet :
                tmp_alphabet.append(letter)

        self._alphabet = tuple(tmp_alphabet)


    def __list__(self) :
        r"""
        Mutation of the permutation in a list of two lists
        """
        a0 = zip(map(self._alphabetize, range(0,len(self))), self._flips[0])
        a1 = zip(map(self._alphabetize, self._twin[1]), self._flips[1])
        return [a0,a1]

    
    def __eq__(self, other) :
        r"""
        Tests equality.
        """
        return (self._twin[0] == other._twin[0]) and (self._flips[0] == other._flips[0])


    def __ne__(self, other) :
        r"""
        Tests difference.
        """
        return (self._twin[0] != other._twin[0]) or (self._flips[0] != other._flips[0])


    def copy(self) :
        p = FlippedReducedAbelianPermutation()
        p._twin = [self._twin[0][:], self._twin[1][:]]
        p._flips = [self._flips[0][:], self._flips[1][:]]
        p._alphabet = self._alphabet
        return p

    def rauzy_diagram(self):
        return FlippedReducedAbelianRauzyDiagram(self)


class FlippedReducedQuadraticPermutation(FlippedQuadraticPermutation, FlippedReducedPermutation) :
    r"""
    Flipped Reduced Quadratic Permutation.
    """
    def __list__(self) :
        r"""
        Mutation of the permutation in a list of two lists.
        """
        i_a = 0
        l = ([False]*len(self._twin[0]),[False]*len(self._twin[1]))
        # False means empty here
        for i in range(2) :
            for j in range(len(l[i])) :
               if  l[i][j] == False :
                    l[i][j] = (self._alphabetize(i_a), self._flips[i][j])
                    l[self._twin[i][j][0]][self._twin[i][j][1]] = (self._alphabetize(i_a), self._flips[i][j])
                    i_a += 1
        return l


    def copy(self) :
        p = FlippedReducedQuadraticPermutation()
        p._twin = [self._twin[0][:], self._twin[1][:]]
        p._flips = [self._flips[0][:], self._flips[1][:]]
        p._alphabet = self._alphabet
        return p


    def _init_alphabet(self,a) :
        r"""
        Intialization procedure of the alphabet of self
        """
        tmp_alphabet = []
        for letter in a[0]+a[1] :
            if letter not in tmp_alphabet :
                tmp_alphabet.append(letter)

        self._alphabet = tuple(tmp_alphabet)


    def __eq__(self, other) :
        r"""
        Tests equality.
        """
        return (self._twin == other._twin) and (self._flips == other._flips)


    def __ne__(self, other) :
        r"""
        Test inequality.
        """
        return (self._twin != other._twin) or (self._flips != other._flips)

    def rauzy_diagram(self) :
        return FlippedReducedQuadraticRauzyDiagram(self)

###################################################
#############    RAUZY DIAGRAMS    ################
###################################################
class ReducedRauzyDiagram(RauzyDiagram) :
    r"""
    """
    def get_alphabet(self) :
        return self.__alphabet

    def set_alphabet(self, value) :
        alpha = Alphabet(value)
        if len(alpha) < self._n : 
            raise TypeError("Not enough value in your alphabet")
        self.__alphabet = value

    def alphabetize(self, i) :
        if not isinstance(i, int) :
            raise TypeError("%s not an integer" %(str(i)))
        return self.__alphabet[i]

    doc_alphabet = "alphabet for representations of permutations in this diagram"
            
    alphabet = property(fset = set_alphabet, fget = get_alphabet, doc=doc_alphabet)


class ReducedAbelianRauzyDiagram(ReducedRauzyDiagram) :
    r"""
    Reduced Rauzy diagram of Abelian permutations.

    EXAMPLES:
        sage : d = RauzyDiagram('a b c', 'c b a', reduced = True)
        sage : d
         0 : c b a  [1, 2]
         1 : c a b  [0, 1]
         2 : b c a  [2, 0]
        
    AUTHORS:
        - Vincent Delecroix (2008-12-20)
    """
    
    def permutation_to_vertex(self, p) :
        return tuple(p._twin[0])
        

    def vertex_to_permutation(self, i) :
        a1 = self._permutations[i]
        a0 = range(len(a1))
        alphabet = self.alphabet
        return ReducedAbelianPermutation([a0,a1], alphabet=alphabet)


    def vertex_to_str(self, i) :
        return ' '.join(self.alphabet) + "\\n" + ' '.join(map(self.alphabetize,self._permutations[i]))


    def vertex_to_one_line_str(self, i) :
        return ' '.join(map(self.alphabetize,self._permutations[i]))


    def edges_to_str(self, i) :
        return str(self._neighbours[i])
        

    def first_vertex(self, p) :
        self.alphabet = p.alphabet



class ReducedQuadraticRauzyDiagram(ReducedRauzyDiagram) :
    r"""
    Reduced Rauzy diagram of quadratic (or generalized) permutations.

    EXAMPLES:
        sage : d = RauzyDiagram('a b b', 'c c a', reduced = True)
        sage : d
         0 : ('a b b', 'c c a')  [1, 0]
         1 : ('a a b b', 'c c')  [-1, 2]
         2 : ('a a b', 'b c c')  [2, 3]
         3 : ('a a', 'b b c c')  [0, -1]
        
    AUTHORS:
        - Vincent Delecroix (2008-12-20)
    """

    
    def permutation_to_vertex(self, p) :
        return (p._twin[0], p._twin[1])
        

    def vertex_to_permutation(self, i) :
        raise NotImplementedError




    def vertex_to_str(self, i) :
        atwin = alphabetized_qtwin(self._permutations[i], self.alphabet)
        return ' '.join(atwin[0])  + "\n" + ' '.join(atwin[1])


    def vertex_to_one_line_str(self, i) :
        atwin = alphabetized_qtwin(self._permutations[i], self.alphabet)
        return ' '.join(atwin[0]) + ", " + ' '.join(atwin[1])


    def edges_to_str(self, i) :
        return str(self._neighbours[i])

    def first_vertex(self, p) :
        self.alphabet = p.alphabet



class FlippedReducedAbelianRauzyDiagram(ReducedRauzyDiagram):
    r"""
    Reduced Rauzy diagram of flipped Abelian permutations.

    EXAMPLES:
        sage : d = RauzyDiagram('a b c', 'c b a', reduced = True, flips=['a'])

    """
    
    def permutation_to_vertex(self, p) :
        flips = [k for k,_ in filter(lambda (i,j) : j == -1, enumerate(p._flips))]
        return (p._twin[0], flips)


    def vertex_to_permutation(self, i) :
        raise NotImplementedError


    def vertex_to_str(self, i) :
        str0 = ""
        str1 = ""
        flips = map(self.alphabetize, self._permutations[i][1])
  
        for letter in self.alphabet :
            if letter in flips :
                str0 += "-"+letter+" "
            else :
                str0 += " "+letter+" "

        for j in self._permutations[i][0] :
            letter = self.alphabetize(j)
            if letter in flips :
                str1 += "-"+letter+" "
            else :
                str1 += " "+letter+" "
            
        return str0 + "\\n" + str1


    def vertex_to_one_line_str(self, i) :
        str1 = ""
        flips = map(self.alphabetize, self._permutations[i][1])

        for j in self._permutations[i][0] :
            letter = self.alphabetize(j)
            if letter in flips :
                str1 += "-"+letter+" "
            else :
                str1 += " "+letter+" "
            
        return str1


    def edges_to_str(self, i) :
        return str(self._neighbours[i])
        

    def first_vertex(self, p) :
        self.alphabet = p.alphabet



class FlippedReducedQuadraticRauzyDiagram(ReducedRauzyDiagram) :
    r"""
    Reduced Rauzy diagram of flipped Abelian permutations.

    EXAMPLES:
        sage : d = RauzyDiagram('a b c', 'c b a', reduced = True, flips=['a'])

    """
    def permutation_to_vertex(self, p) :
        return (p._twin, p._flips)


    def vertex_to_permutation(self, i) :
        raise NotImplementedError


    def vertex_to_str(self, i) :
        atwin = alphabetized_qtwin(self._permutations[i], self.alphabet)
        return ' '.join(atwin[0]) + "\\n" + ' '.join(atwin[1])


    def vertex_to_one_line_str(self, i) :
        atwin = alphabetized_qtwin(self._permutations[i], self.alphabet)
        return ' '.join(atwin[0]) + ", " + ' '.join(atwin[1])


    def edges_to_str(self, i) :
        return str(self._neighbours[i])
        

    def first_vertex(self, p) :
        self.alphabet = p.alphabet
