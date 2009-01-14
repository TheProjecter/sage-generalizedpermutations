r"""
Definition of reduced object


    a reduced (generalized) permutation is better suitted to study strata of
    Abelian (or quadratic) holomorphic forms on Riemann surfaces. The Rauzy
    diagram is an invariant of such a component. Corentin  Boissy proved the
    identification between Rauzy diagrams and connected components of strata.
    But the geometry of the diagram is not yet totally understood.

AUTHORS: 
    -- Vincent Delecroix (2008-12-20): initial version
"""

import template
SageObject = object

class ReducedPermutation(SageObject) :
    r"""
    Template for reduced objects
    """

    def __init__(self, a) :
        self._twin = [[],[]]

        self._init_alphabet(a)
        self._alphabetize = lambda i : self._alphabet[i]

        self._init_twin(a)

        self.rauzy_move = self._twin_rauzy_move


    def get_alphabet(self) :
        return self._alphabet
        

    def set_alphabet(self,l) :
        if (type(l) != tuple) and (type(l) != list) and (type(l) != str) : raise TypeError("Must be tuple, list or string")
        elif len(l) != len(self) : raise TypeError("Bad length")
        else :
            self._alphabet = tuple(l)


    doc_alphabet = "Eventual alphabet for the representation of the reduced permutation"

    alphabet = property(fget = get_alphabet, fset = set_alphabet, doc=doc_alphabet)



######################################
#####     ABELIAN PERMUTATION    #####
######################################
class AbelianPermutation(ReducedPermutation, template.AbelianPermutation):
    r"""
    reduced Abelian permutation

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
        p = AbelianPermutation(([],[]))
        p._twin[0].extend(self._twin[0])
        p._twin[1].extend(self._twin[1])
        p._alphabet = self._alphabet
        return p

    
    def _init_alphabet(self,a) :
        self._alphabet = tuple(a[0][:])


    def __list__(self) :
        r"""
        mutation of the permutation to a list of two lists
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
        q = AbelianPermutation(("",""))
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
        return AbelianRauzyDiagram(self)


#####################################################################
##############    QUADRATIC REDUCED PERMUTATIONS    #################
#####################################################################

class QuadraticPermutation(ReducedPermutation, template.QuadraticPermutation):
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

        p = QuadraticPermutation(([],[]))
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
        i_a = 0
        l = ([False]*len(self._twin[0]),[False]*len(self._twin[1]))
        # False means empty here
        for i in range(2) :
            for j in range(len(l[i])) :
               if  l[i][j] == False :
                    l[i][j] = self._alphabetize(i_a)
                    l[self._twin[i][j][0]][self._twin[i][j][1]] = self._alphabetize(i_a)
                    i_a += 1
        return l
        

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
        return (self._twin[0] == other._twin[0]) and (self._twin[1] == other._twin[1])


    def __ne__(self, other) :
        r"""
        Test of difference
        """
        return (self._twin[0] != other._twin[0]) or (self._twin[1] != other._twin[1])


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

        return QuadraticRauzyDiagram(self)


############################
####     FLIPPED       #####
############################

class FlippedReducedPermutation(SageObject) :
    r"""
    Template for reduced permutation with flip

    ...Will soon be...
    """
    pass


class FlippedAbelianPermutation(FlippedReducedPermutation, template.FlippedAbelianPermutation) :
    r"""
    Flipped reduced abelian permutation

    ...Will soon be...
    """
    pass


class FlippedQuadraticPermutation(FlippedReducedPermutation, template.FlippedQuadraticPermutation) :
    r"""
    Flipped reduced quadratic (or generalized) permutation

    ...Will soon be...
    """
    pass



###################################################
#############    RAUZY DIAGRAMS    ################
###################################################


class AbelianRauzyDiagram(template.RauzyDiagram) :
    r"""
    Reduced Rauzy diagram of abelian permutations.

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
        r"""
        Translation of the reduced Abelian permutation to a vertex

        Vertex storage depends of the type of the permutation. Moreover this
        storage function should be change in future version.

        INPUT:
            a reduced.AbelianPermutation

        OUTPUT:
            a "vertex-typed" object (actually string)

        AUTHORS:
            - Vincent Delecroix (2008-12-20)
        """
        return ' '.join(list(p)[1])
        

    def vertex_to_permutation(self, i) :
        r"""
        Translation of a vertex indice to a permutation.

        This function invert the permutation_to_vertex one.

        INPUT:
            an indice of a vertex

        OUTPUT:
            a reduced.AbelianPermutation

        AUTHOR:
            - Vincent Delecroix (2008-12-20)
        """
        a0 = self._a0.split()
        a1 = self._permutations[i].split()
        return AbelianPermutation([a0,a1])


    def vertex_to_str(self, i) :
        r"""
        String for the representation of a vertex.

        INPUT:
            an indice of a vertex

        OUTPUT:
            a string

        AUTHOR:
            - Vincent Delecroix (2008-12-20)

        """
        return self._a0 + "\\n" + self._permutations[i]


    def vertex_to_one_line_str(self, i) :
        r"""
        One line string for the representation of a vertex.

        INPUT:
            an indice of a vertex

        OUTPUT:
            a string

        AUTHOR:
            - Vincent Delecroix (2008-12-20)
        """
        return self._permutations[i]


    def edges_to_str(self, i) :
        r"""
        One line string for the representation of a couple of edges (the
        0-neighbour and the 1-neighbour).

        INPUT:
            an indice of an edge

        OUTPUT:
            a string

        AUTHOR:
            - Vincent Delecroix (2008-12-20)
        """
        return str(self._neighbours[i])
        

    def first_vertex(self, p) :
        r"""
        A special intialization before the insertion of the first vertex.

        INPUT:
            a reduced.AbelianPermutation

        AUTHOR:
            - Vincent Delecroix (2008-12-20)
        """
        self._a0 = ' '.join(list(p)[0])


#####################################################
###########    QUADRATIC RAUZY DIAGRAM    ###########
#####################################################
class QuadraticRauzyDiagram(template.RauzyDiagram) :
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
        r"""
        Translation of a reduced quadratic permutation to a vertex

        Vertex storage depends of the type of the permutation. Moreover this
        storage function should be change in future version.

        INPUT:
            a reduced.QuadraticPermutation

        OUTPUT:
            a "vertex-typed" object (actually 2-uple of strings)

        AUTHORS:
            - Vincent Delecroix (2008-12-20)
        """
        l = list(p)
        return (' '.join(l[0]), ' '.join(l[1]))
        

    def vertex_to_permutation(self, i) :
        r"""
        Translation of a vertex indice to a permutation.

        This function invert the permutation_to_vertex one.

        INPUT:
            an indice of a vertex

        OUTPUT:
            a reduced.QuadraticPermutation

        AUTHORS:
            - Vincent Delecroix (2008-12-20)
        """
        a0 = self._permutations[i][0].split()
        a1 = self._permutations[i][1].split()
        return QuadraticPermutation([a0,a1])


    def vertex_to_str(self, i) :
        r"""
        String for the representation of a vertex.

        INPUT:
            an indice of a vertex

        OUTPUT:
            a string

        AUTHORS:
            - Vincent Delecroix (2008-12-20)

        """
        return self._permutations[i][0] + "\\n" + self._permutations[i][1]


    def vertex_to_one_line_str(self, i) :
        r"""
        One line string for the representation of a vertex.

        INPUT:
            an indice of a vertex

        OUTPUT:
            a string

        AUTHORS:
            - Vincent Delecroix (2008-12-20)
        """
        return str(self._permutations[i])


    def edges_to_str(self, i) :
        r"""
        One line string for the representation of a couple of edges (the
        0-neighbour and the 1-neighbour).

        INPUT:
            an indice of an edge

        OUTPUT:
            a string

        AUTHORS:
            - Vincent Delecroix (2008-12-20)
        """
        return str(self._neighbours[i])
