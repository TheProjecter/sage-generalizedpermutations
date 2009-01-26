r"""
Definition of labeled type permutation

    A labeled (generalized) permutation is better suited to study dynamics of
    a translation surface than reduced object. To study strata prefer reduced
    object (Rauzy diagrams are significantly smaller ex. for the permutation
    ('a b d b e','e d c a c') the labeled Rauzy diagram contains 8760
    permutations, and the reduced only 73).

    AUTHORS:
        -- Vincent Delecroix (2008-12-20) : initial version


    EXAMPLES:
        For creation of a labeled permutation simply use the class factory,
        GeneralizedPermutation:
        sage : p = GeneralizedPermutation('a b c', 'c b a')

        or eventually:
        sage : p = GeneralizedPermutation('a b c', 'c b a', reduced = False)

        The same thing works for Rauzy diagrams:
        sage : d1 = RauzyDiagram('a b c', 'c b a')
        sage : d2 = RauzyDiagram('a b c', 'c b a', reduced = False)
        
        You can compose matrix or substitution along a path in the Rauzy
        diagram:
        sage : d = RauzyDiagram('a b c', 'c b a')
        sage : s = d.path_to_substitution(0,0,1,0,1)
        sage : m = d.path_to_matrix(0,0,1,0,1)

    TODO:
       insert an alphabet in the definition and consider just alphabet for
       representation (and use a defaut alphabet otherwise).
       (add a parameter construct_alphabet_from_intervals in the constructor
       We must permit 
          uncomplete labelization (two intervals could have the same name)
          bilabeled permutations (all labels distincts. Useful for codage of 
       linear involutions).
       Morevoer the presence of an alphabet will be useful for the
       WordMorphism definition.

       Think about the roles of __list__ and __repr__...

       We must be able to interact on the numerotation of intervals in twice
       manner :
          change the alphabet
          change the labelization
       But there will be a problem for bilabellization

       For labeled Abelian Rauzy Diagram the storage is clear : the upper interval is 
       not important
"""


from string import replace

from sage import SageObject
#from sage.structure.sage_object import SageObject
from sage import Alphabet
#from sage.combinat.words.alphabet import Alphabet
from sage import WordMorphism
#from sage.combinat.words.morphism import WordMorphism
from sage import Matrix, identity_matrix
#from sage.matrix.constructor import Matrix, identity_matrix



from template import AbelianPermutation, QuadraticPermutation
from template import FlippedAbelianPermutation, FlippedQuadraticPermutation
from template import RauzyDiagram, FlippedRauzyDiagram



class LabeledPermutation(SageObject):
    r"""
    General template for labeled objects

    ...DO NOT USE...
    """

    def __init__(self, a) :
        self._intervals = [a[0][:], a[1][:]]

        self._twin = [[],[]]

        self._init_twin(a)
        self._init_alphabet(a)


    def __list__(self) :
        r"""
        the permutations as a list of two lists

        EXAMPLES:
            sage : p = GeneralizedPermutation('a b c', 'c b a')
            sage : list(p)
            [['a', 'b', 'c'], ['c', 'b', 'a']]
            
            sage : p = GeneralizedPermutation('a b b', 'c c a')
            sage : list(p)
            [['a', 'b', 'c'], ['c', 'c', 'a']]

        AUTHORS:
            - Vincent Delecroix (2008-12-20)
        """
        return [self._intervals[0][:], self._intervals[1][:]]


    def __eq__(self,other) :
        r"""
        Test of equality

        Two labeled permutations are equal if they have the same intervals
        numerotation.

        EXAMPLES:
            sage : p = GeneralizedPermutation('a b c', 'c b a')
            sage : q = GeneralizedPermutation('p q r', 'r q p')
            sage : p == q
            False

        AUTHORS:
            - Vincent Delecroix (2008-12-20)
        """
        return (self._intervals == other._intervals)

   
    def __ne__(self,other) :
        r"""
        Test of difference

        AUTHORS:
            - Vincent Delecroix (2008-12-20)
        """
        return (self._intervals != other._intervals)


    def _move_data(self, winner, loser, loser_to) :
        r"""
        Modification of data.

        Called from GeneralizedPermutation::rauzy_move.
        
        INPUT:
            winner -- 2-uple (winner_interval, winner_position)
            loser -- 2-uple (loser_interval, loser_position)
            loser_to -- 2-up (loser_interval_to, loser_position_to)
        """
        loser_letter = self._intervals[loser[0]].pop()
        self._intervals[loser_to[0]].insert(loser_to[1], loser_letter)


class LabeledAbelianPermutation(LabeledPermutation, AbelianPermutation) :
    r"""
    labeled Abelian permutation

    EXAMPLES:
        Reducibility testing :
        sage : p = GeneralizedPermutation('a b c', 'c b a')
        sage : p.is_reducible()
        False

        sage : q = GeneralizedPermutation('a b c d', 'b a d c')
        sage : q.is_reducible()
        True


        Rauzy movability and Rauzy move :
        sage : p = GeneralizedPermutation('a b c', 'c b a')
        sage : p.is_rauzy_movable(0)
        True
        sage : p.rauzy_move(1)
        sage : p
        a b c
        c a b
        sage : p.is_rauzy_movable(0)
        True
        sage : p.rauzy_move(0)
        sage : p
        a b c
        c b a


        Rauzy diagrams
        sage : p = GeneralizedPermutation('a b c', 'c b a')
        sage : p.rauzy_diagram()
         0 : ('a b c', 'c b a')  [1, 2]
         1 : ('a b c', 'c a b')  [0, 1]
         2 : ('a c b', 'c b a')  [2, 0]

    AUTHORS:
        - Vincent Delecroix (2008-12-20)
    """

    def copy(self) :
        r"""
        Do a copy of the Abelian permutation.

        EXAMPLES:
            sage : p = GeneralizedPermutation('a b c', 'c b a')
            sage : q = p.copy()
            sage : p == q
            True
            sage : p.rauzy_move(0)
            sage : p == q
            False

        AUTHORS:
            - Vincent Delecroix (2008-12-20)
        """
        p = LabeledAbelianPermutation(([],[]))
        p._twin[0].extend(self._twin[0])
        p._twin[1].extend(self._twin[1])
        p._intervals[0].extend(self._intervals[0])
        p._intervals[1].extend(self._intervals[1])
        return p


    def rauzy_move_substitution(self, winner) :
        r"""
        Consider the operation done on the codage (a WordMorphism)
        corresponding to a RauzyMove
        
        INPUT:
            a winner interval : it's must be 0 (for top) or 1 (for bottom)

        OUTPUT:
            a WordMorphism

        EXAMPLES:
            sage : p = GeneralizedPermutation('a b c', 'c b a')
            sage : s0 = p.rauzy_move_substitution(0)
            sage : p.rauzy_move(0)
            sage : s1 = p.rauzy_move_substitution(1)
            sage : p.rauzy_move(1)
            sage : s = s0 * s1
        """
        loser = 1 - winner

        loser_letter = self._intervals[loser][-1]

        up_letter = self._intervals[0][-1]
        down_letter = self._intervals[1][-1]

        d = dict([(letter,letter) for letter in self._intervals[0]])
        d[loser_letter] = down_letter + up_letter

        return WordMorphism(d)

        
    def rauzy_diagram(self) :
        r"""
        Create the Rauzy diagram associated with this permutation

        OUTPUT :
            a RauzyDiagram

        EXAMPLES :
            sage : p = GeneralizedPermutation('a b c', 'c b a')
            sage : d = p.rauzy_diagram()
            sage : d
            0 : ('a b c',' c b a')  [1, 2]
            1 : ('a b c', 'c a b')  [0, 1]
            2 : ('a c b', 'c b a')  [2, 0]

        For more information, try help RauzyDiagram
        """
        return LabeledAbelianRauzyDiagram(self)


#####################################################################
##############    QUADRATIC LABELED PERMUTATIONS    #################
#####################################################################

class LabeledQuadraticPermutation(LabeledPermutation, QuadraticPermutation) :
    r"""
    labeled quadratic (or generalized) permutation

    EXAMPLES:
        Reducibility testing :
        sage : p = GeneralizedPermutation('a b b', 'c c a')
        sage : p.is_reducible()
        False

        sage : p = GeneralizedPermutation('a b c a', 'b d d c')
        sage : p.is_reducible()
        True
        sage : test, decomposition = p.is_reducible(return_decomposition = True)
        sage : test
        True
        sage : decomposition
        (['a'],['c','a'],[],['c'])

    
        Rauzy movavability and Rauzy move :
        sage : p = GeneralizedPermutation('a b b', 'c c a')
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
        sage : p.rauzy_diagram()
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

    AUTHORS:
        - Vincent Delecroix (2008-12-20)
    """

    def copy(self) :
        r"""
        Do a copy of the Quadratic permutation.

        EXAMPLES:
            sage : p = GeneralizedPermutation('a b b', 'c c a')
            sage : q = p.copy()
            sage : p == q
            True
            sage : p.rauzy_move(0)
            sage : p == q
            False

        AUTHORS:
            - Vincent Delecroix (2008-20-12)
        """
        p = LabeledQuadraticPermutation(([],[]))
        p._twin[0].extend(self._twin[0])
        p._twin[1].extend(self._twin[1])
        p._intervals[0].extend(self._intervals[0])
        p._intervals[1].extend(self._intervals[1])
        return p
       


    def rauzy_diagram(self) :
        r"""
        Create the Rauzy diagram associated with this permutation

        OUTPUT:
            a RauzyDiagram

        EXAMPLES:
            sage : p = GeneralizedPermutation('a b b', 'c c a')
            sage : d = p.rauzy_diagram()

        For more information, try help RauzyDiagram or help LabeledQuadraticPermutation
        """
        return LabeledQuadraticRauzyDiagram(self)


#######################
####    FLIPPED    ####
#######################
class FlippedLabeledPermutation(LabeledPermutation) :
    r"""
    General template for labeled objects

    ...NOT FOR USAGE...
    """

    def __init__(self, a, flips=[]) :
        self._intervals = [a[0][:], a[1][:]]

        self._twin = [[],[]]
        self._init_twin(a)
        self._init_flips(a,flips)


    def __list__(self) :
        r"""
        the permutations as a list of two lists
        """
        a0 = zip(self._intervals[0], self._flips[0])
        a1 = zip(self._intervals[1], self._flips[1])
        return [a0,a1]


    def __eq__(self,other) :
        r"""
        Test of equality

        """
        return (self._intervals == other._intervals) and (self._flips == other._flips)

   
    def __ne__(self,other) :
        r"""
        Test of difference

        AUTHORS:
            - Vincent Delecroix (2008-12-20)
        """
        return (self._intervals != other._intervals) or (self._flips != other._flips)



class FlippedLabeledAbelianPermutation(FlippedLabeledPermutation, FlippedAbelianPermutation) :
    r"""
    labeled Abelian permutation

    EXAMPLES:
        Reducibility testing :
        sage : p = GeneralizedPermutation('a b c', 'c b a')
        sage : p.is_reducible()
        False

        sage : q = GeneralizedPermutation('a b c d', 'b a d c')
        sage : q.is_reducible()
        True


        Rauzy movability and Rauzy move :
        sage : p = GeneralizedPermutation('a b c', 'c b a')
        sage : p.is_rauzy_movable(0)
        True
        sage : p.rauzy_move(1)
        sage : p
        a b c
        c a b
        sage : p.is_rauzy_movable(0)
        True
        sage : p.rauzy_move(0)
        sage : p
        a b c
        c b a


        Rauzy diagrams
        sage : p = GeneralizedPermutation('a b c', 'c b a')
        sage : p.rauzy_diagram()
         0 : ('a b c', 'c b a')  [1, 2]
         1 : ('a b c', 'c a b')  [0, 1]
         2 : ('a c b', 'c b a')  [2, 0]

    AUTHORS:
        - Vincent Delecroix (2008-12-20)
    """

    def copy(self) :
        r"""
        Do a copy of the Abelian permutation.

        EXAMPLES:
            sage : p = GeneralizedPermutation('a b c', 'c b a')
            sage : q = p.copy()
            sage : p == q
            True
            sage : p.rauzy_move(0)
            sage : p == q
            False

        AUTHORS:
            - Vincent Delecroix (2008-12-20)
        """
        p = FlippedLabeledAbelianPermutation(([],[]))
        p._twin[0].extend(self._twin[0])
        p._twin[1].extend(self._twin[1])
        p._flips[0].extend(self._flips[0])
        p._flips[1].extend(self._flips[1])
        p._intervals[0].extend(self._intervals[0])
        p._intervals[1].extend(self._intervals[1])
        return p


    def rauzy_move_substitution(self, winner) :
        r"""
        Consider the operation done on the codage (a WordMorphism)
        corresponding to a RauzyMove
        
        INPUT:
            a winner interval : it's must be 0 (for top) or 1 (for bottom)

        OUTPUT:
            a WordMorphism

        EXAMPLES:
            sage : p = GeneralizedPermutation('a b c', 'c b a')
            sage : s0 = p.rauzy_move_substitution(0)
            sage : p.rauzy_move(0)
            sage : s1 = p.rauzy_move_substitution(1)
            sage : p.rauzy_move(1)
            sage : s = s0 * s1
        """
        loser = 1 - winner

        loser_letter = self._intervals[loser][-1]

        up_letter = self._intervals[0][-1]
        down_letter = self._intervals[1][-1]

        d = dict([(letter,letter) for letter in self._intervals[0]])
        d[loser_letter] = down_letter + up_letter

        return WordMorphism(d)

        
    def rauzy_diagram(self) :
        r"""
        Create the Rauzy diagram associated with this permutation

        OUTPUT :
            a RauzyDiagram

        EXAMPLES :
            sage : p = GeneralizedPermutation('a b c', 'c b a')
            sage : d = p.rauzy_diagram()
            sage : d
            0 : ('a b c',' c b a')  [1, 2]
            1 : ('a b c', 'c a b')  [0, 1]
            2 : ('a c b', 'c b a')  [2, 0]

        For more information, try help RauzyDiagram
        """
        return FlippedLabeledAbelianRauzyDiagram(self)


class FlippedLabeledQuadraticPermutation(FlippedLabeledPermutation, FlippedQuadraticPermutation) :

    def copy(self) :
        r"""
        Do a copy of the Abelian permutation.

        EXAMPLES:
            sage : p = GeneralizedPermutation('a b c', 'c b a')
            sage : q = p.copy()
            sage : p == q
            True
            sage : p.rauzy_move(0)
            sage : p == q
            False

        AUTHORS:
            - Vincent Delecroix (2008-12-20)
        """
        p = FlippedLabeledQuadraticPermutation(([],[]))
        p._twin[0].extend(self._twin[0])
        p._twin[1].extend(self._twin[1])
        p._flips[0].extend(self._flips[0])
        p._flips[1].extend(self._flips[1])
        p._intervals[0].extend(self._intervals[0])
        p._intervals[1].extend(self._intervals[1])
        return p

        
    def rauzy_diagram(self) :
        r"""
        Create the Rauzy diagram associated with this permutation

        OUTPUT :
            a RauzyDiagram

        EXAMPLES :
            sage : p = GeneralizedPermutation('a b c', 'c b a')
            sage : d = p.rauzy_diagram()
            sage : d
            0 : ('a b c',' c b a')  [1, 2]
            1 : ('a b c', 'c a b')  [0, 1]
            2 : ('a c b', 'c b a')  [2, 0]

        For more information, try help RauzyDiagram
        """
        return FlippedRauzyDiagram(self)


##################################
#####     RAUZY DIAGRAMS     #####
##################################
class NeighbourError(Exception):
    def __init__(self, value) :
        self.value = value

    def __str__(self) :
        return self.value
    

class LabeledRauzyDiagram(SageObject) :
    r"""
    Template for Rauzy diagrams of labeled permutations
    """

    
    def permutation_to_vertex(self, p) :
        r"""
        Translation of the a labeled permutation to a vertex

        Vertex storage depends of the type of the permutation. Moreover this
        storage function should be change in future version.
        
        INPUT:
        a labeled Permutation
        
        OUTPUT:
        a "vertex-typed" object (actually a 2-uple of strings)
        
         AUTHORS:
         - Vincent Delecroix (2008-12-20)
         """     
        l = list(p)
        return (' '.join(l[0]),' '.join(l[1]))
    

    def vertex_to_str(self, i) :
        r"""
        String for the representation of a vertex.

        INPUT:
        i -- indice of a vertex
        
        OUTPUT:
        a string
        
        AUTHOR:
             - Vincent Delecroix (2008-12-20)
             """
        return self._permutations[i][0] + "\\n" + self._permutations[i][1]
    
    
    def vertex_to_one_line_str(self, i) :
        r"""
        One line string for the representation of a vertex.
        
        INPUT:
            i -- an indice of a vertex
        
        OUTPUT:
            a string
        
        AUTHOR:
            - Vincent Delecroix (2008-12-20)
         """
        return str(self._permutations[i])


    def edges_to_str(self, i) :
        r"""
        One line string for the representation of a couple of edges (the
        0-neighbour and the 1-neighbour).
        
        INPUT:
            i -- an indice of an edge

        OUTPUT:
            a string

        AUTHOR:
             - Vincent Delecroix (2008-12-20)
        """
        return str(self._neighbours[i])


    def path_composition(self, path, function, composition = None) :
        r"""
        Compose an edges function on a path

        INPUT:
            path -- a Path (actually a tuple)
            function -- function must be of the form (indice,type) -> element
            Moreover function(None,None) must be an identity element for
            initialization.
            composition -- the composition function for the function. * if None (defaut None)

        EXAMPLES:
        
        AUTHOR:
            - Vincent Delecroix (2008-12-20)
        """
        if path == () : return function(None,None)

        result = function(None,None)
        i = path[0]
        for step in path[1:] :
            if type(step) == int :
                if composition == None :
                    result = result * function(i,step)
                else :
                    result = composition(result, function(i,step))

                if self._neighbours[i][step] == -1 :
                    raise NeighbourError("No neighbour with this edge type")
                i = self._neighbours[i][step]  

            elif (type(step) == tuple) and (len(step) == 2) :
                for j in range(step[1]) :
                    if composition == None :
                        result = result * function(i, step)
                    else :
                        result = composition(result, function(i, step[0]))
                    if self._neighbours[i][step] == -1 :
                        raise NeighbourError
                    i = self._neighbours[i][step[0]]
            else : raise TypeError("No neighbour with this edge type")

        return result


    def edge_to_substitution(self, i = None, winner = None) :
        r"""
        Return the substitution corresponding to the edge

        INPUT:
            i -- integer
            winner -- 0,1, the type of the edge

        OUTPUT:
            A WordMorphism

        EXAMPLES:
            sage : d = RauzyDiagram('a b c', 'c b a')
            sage : d.edge_to_substitution(0,1)
        """
        d = dict([(letter,letter) for letter in self._alphabet])
        if (i == None) and (winner == None) : return WordMorphism(d)

        loser_letter = self._permutations[i][1-winner][-1]

        up_letter = self._permutations[i][0][-1]
        down_letter = self._permutations[i][1][-1]

        d[loser_letter] = down_letter + up_letter

        return WordMorphism(d)



    def edge_to_matrix(self, i = None, winner = None):
        r"""
        Return the corresponding matrix

        INPUT:
            i -- integer (number of a permutation)
            winner -- 0 or 1, the type of the edge

        OUTPUT:
            A matrix

        EXAMPLES:
            sage: d = RauzyDiagram('a b c','c b a')
            RauzyDiagram on three letters
            sage : d.edge_to_matrix(0,1,0)
        """
        if (i == None) and (winner == None) : return identity_matrix(len(self._alphabet))

        winner_index = self.numerize(self._permutations[i][winner][-1])
        loser_index = self.numerize(self._permutations[i][1-winner][-1])

        m = identity_matrix(len(self._alphabet))
        m[winner_index, loser_index] = 1
        return m


    def edge_to_winner(self, i = None, winner = None):
        r"""
        Return the winner's name

        INPUT:
            i -- integer
            winner -- 0 or 1, the type of the edge

        OUTPUT:
            A list of one letter
        """
        if i == None : return []
        return [self._permutations[i][winner][-1]]


    def edge_to_loser(self, i = None, winner = None) :
        r"""
        Return the loser's name

        INPUT:
            i -- integer
            winner -- 0 or 1, the type of the edge

        OUTPUT:
            A list of one letter
        """
        if i == None : return []
        return [self._permutations[i][1-winner][-1]]

    
    def path_to_winner(self, *args) :
        return self.path_composition(args, self.edge_to_winner, composition = list.__add__)


    def path_to_loser(self, *args) :
        return self.path_composition(args, self.edge_to_loser, composition = list.__add__)


    def path_to_substitution(self, *args) :
        return self.path_composition(args, self.edge_to_substitution)


    def path_to_matrix(self, *args) :
        return self.path_composition(args, self.edge_to_matrix)

        
class LabeledAbelianRauzyDiagram(LabeledRauzyDiagram, RauzyDiagram) :
    r"""
    Labeled Rauzy diagram of abelian permutations.

    EXAMPLES:
        sage : d = RauzyDiagram('a b c', 'c b a')
        sage : d
         0 : ('a b c', 'c b a')  [1, 2]
         1 : ('a b c', 'c a b')  [0, 1]
         2 : ('a c b', 'c b a')  [2, 0]
        
    AUTHORS:
        - Vincent Delecroix (2008-12-20)
    """


    def first_vertex(self, p) :
        r"""
        A special intialization before the insertion of the first vertex.

        INPUT:
            p -- a LabeledAbelianPermutation

        OUTPUT:
            None

        AUTHOR:
            - Vincent Delecroix (2008-12-20)
        """
        self._alphabet = Alphabet(p[0])   # an OrderedAlphabet_Finite
        self.numerize = lambda l : self._alphabet.rank(l)
        self.alphabetize = lambda i : self._alphabet[i]

    def vertex_to_permutation(self, i) :
        r"""
        Translation of a vertex indice to a permutation.

        This function invert the permutation_to_vertex function.

        INPUT:
            an indice of a vertex

        OUTPUT:
            a labeled Permutation

        AUTHOR:
            - Vincent Delecroix (2008-12-20)
        """
        a0 = self._permutations[i][0].split()
        a1 = self._permutations[i][1].split()
        return LabeledAbelianPermutation([a0,a1])




class LabeledQuadraticRauzyDiagram(LabeledRauzyDiagram, RauzyDiagram) :
    r"""
    Labeled Rauzy diagram of quadratic permutations.

    EXAMPLES:
        sage : d = RauzyDiagram('a b b', 'c b a')
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
        
    AUTHORS:
        - Vincent Delecroix (2008-12-20)
    """


    def first_vertex(self, p) :
        r"""
        A special intialization before the insertion of the first vertex.

        INPUT:
            a LabeledQuadraticPermutation

        AUTHOR:
            - Vincent Delecroix (2008-12-20)
        """
        tmp_alphabet = []
        for letter in p[0]+p[1] :
            if letter not in tmp_alphabet : tmp_alphabet.append(letter)

        self._alphabet = tmp_alphabet
        self.numerize = lambda l : self._alphabet.index(i)
        self.alphabetize = lambda i : self._alphabet[i]


    def vertex_to_permutation(self, i) :
        r"""
        Translation of a vertex indice to a permutation.

        This function invert the permutation_to_vertex function.

        INPUT:
            an indice of a vertex

        OUTPUT:
            a LabeledQuadraticPermutation

        AUTHOR:
            - Vincent Delecroix (2008-12-20)
        """
        a0 = self._permutations[i][0].split()
        a1 = self._permutations[i][1].split()
        return LabeledQuadraticPermutation([a0,a1])



########
## FLIP

class FlippedLabeledRauzyDiagram(FlippedRauzyDiagram, LabeledRauzyDiagram) :
    def first_vertex(self,p):
        pass

class FlippedLabeledAbelianRauzyDiagram(FlippedLabeledRauzyDiagram) :
    pass

class FlippedLabeledQuadraticRauzyDiagram(FlippedLabeledRauzyDiagram) :
    pass
