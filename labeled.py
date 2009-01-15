r"""
Definition of labeled type permutation

    A labeled (generalized) permutation is better suited to study dynamics of
    a translation surface than reduced object. To study strata prefer reduced
    object (Rauzy diagrams are significantly smaller ex. for the permutation
    ('a b d b e','e d c a c') the labeled Rauzy diagram contains 8760
    permutations, and the reduced only 73).

AUTHORS:
    -- Vincent Delecroix (2008-12-20) : initial version


    For creation of a labeled permutation simply use the class factory,
    GeneralizedPermutation :
    sage : p = GeneralizedPermutation('a b c', 'c b a')

    or eventually
    sage : p = GeneralizedPermutation('a b c', 'c b a', reduced = False)

    The same thing works for Rauzy diagrams :
    sage : d1 = RauzyDiagram('a b c', 'c b a')
    sage : d2 = RauzyDiagram('a b c', 'c b a', reduced = False)

    You can compose matrix or substitution along a path in the Rauzy diagram :
    sage : d = RauzyDiagram('a b c', 'c b a')
    sage : s = d.path_to_substitution(0,0,1,0,1)
    sage : m = d.path_to_matrix(0,0,1,0,1)

"""

from defaut import WordMorphism
import template


class NeighbourError(Exception) :
    def __init__(self, value) :
        self.value = value

    def __str__(self) :
        return self.value
    

class LabeledPermutation(object) :
    r"""
    General template for labeled objects

    ...NOT FOR USAGE...
    """

    def __init__(self, a) :
        self._intervals = [a[0][:], a[1][:]]

        self._twin = [[],[]]
        self._init_twin(a)


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



class AbelianPermutation(template.AbelianPermutation, LabeledPermutation) :
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
        p = AbelianPermutation(([],[]))
        p._twin[0].extend(self._twin[0])
        p._twin[1].extend(self._twin[1])
        p._intervals[0].extend(self._intervals[0])
        p._intervals[1].extend(self._intervals[1])
        return p


    def rauzy_move(self, winner) :
        r"""
        Perform a Rauzy move on the labeled Abelian permutation with a given
        choice of winner.

        INPUT:
            a winner interval : it's must be 0 (for top) or 1 (for bottom)

        EXAMPLES:
            sage : p = GeneralizedPermutation('a b c','c b a')
            sage : p.rauzy_move(0)
            sage : print p
            a b c
            b c a

        AUTHORS:
            - Vincent Delecroix (2008-20-12)
        """
        loser = 1 - winner

        i_win = self._twin[winner][-1]
        loser_letter = self._intervals[loser].pop()
        self._intervals[loser].insert(i_win+1, loser_letter)

        self._twin_rauzy_move(winner)


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

        winner_letter = self._intervals[winner][-1]
        loser_letter = self._intervals[loser][-1]
        d = dict(zip(self._intervals[0],self._intervals[0]))
        
        if winner == 0 : d[loser_letter] = loser_letter + winner_letter
        else : d[loser_letter] = winner_letter + loser_letter

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
        return AbelianRauzyDiagram(self)


#####################################################################
##############    QUADRATIC LABELED PERMUTATIONS    #################
#####################################################################

class QuadraticPermutation(template.QuadraticPermutation, LabeledPermutation) :
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
        p = QuadraticPermutation(([],[]))
        p._twin[0].extend(self._twin[0])
        p._twin[1].extend(self._twin[1])
        p._intervals[0].extend(self._intervals[0])
        p._intervals[1].extend(self._intervals[1])
        return p
       

    def rauzy_move(self,winner) :
        r"""
        Perform a Rauzy move of the quadratic permutation move with a given
        choice of winner.

        INPUT:
            a winner interval : it's must be 0 (for top) or 1 (for bottom)

        EXAMPLES:
            sage : p = GeneralizedPermutation('a b b','c c a')
            sage : p.rauzy_move(0)
            sage : print p
            a b c
            b c a

        AUTHORS:
            - Vincent Delecroix (2008-20-12)
        """
        loser = 1 - winner

        i_win = self._twin[winner][-1]

        if i_win[0] == loser : incr = 1
        else : incr = 0
        
        loser_letter = self._intervals[loser].pop()
        self._intervals[i_win[0]].insert(i_win[1] + incr, loser_letter)

        self._twin_rauzy_move(winner)

    def rauzy_diagram(self) :
        r"""
        Create the Rauzy diagram associated with this permutation

        OUTPUT:
            a RauzyDiagram

        EXAMPLES:
            sage : p = GeneralizedPermutation('a b b', 'c c a')
            sage : d = p.rauzy_diagram()

        For more information, try help RauzyDiagram or help labeled.QuadraticPermutation
        """
        return QuadraticRauzyDiagram(self)



##################################
#####     RAUZY DIAGRAMS     #####
##################################

class LabeledRauzyDiagram(object) :
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
            an indice of a vertex

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
            an indice of a vertex

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
            an indice of an edge

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
            function must be of the form (indice,type) -> element
            Moreover function(None) must be an identity element for
            initialization.

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


    def edge_to_substitution(self, i, winner) :
        if (i == None) : return WordMorphism({})

        loser = 1 - winner
        loser_letter = self._permutations[i][loser][-1]
        up_letter = self._permutations[i][0][-1]
        down_letter = self._permutations[i][1][-1]

        return WordMorphism({loser_letter : down_letter + up_letter})



    def edge_to_matrix(self, i, t) :
        if i == None : return identity_matrix(len(self._alphabet))
        winner = self.numerize(self._permutations[i][t][-1])
        loser = self.numerize(self._permutations[i][1-t][-1])
        m = identity_matrix(len(self._alphabet))
        m[winner, loser] = 1
        return m


    def edge_to_winner(self, i, t) :
        if i == None : return []
        return [self._permutations[i][t][-1]]


    def edge_to_loser(self, i, t) :
        if i == None : return []
        return [self._permutations[i][1-t][-1]]

    
    def path_to_winner(self, *args) :
        return self.path_composition(args, self.edge_to_winner, composition = list.__add__)


    def path_to_loser(self, *args) :
        return self.path_composition(args, self.edge_to_loser, composition = list.__add__)


    def path_to_substitution(self, *args) :
        r"""
        the path must be of the form :
        (i,type,type,type,...,type)
        or
        (i,(type,n1),(type,n2),...,(type,nk))
        or a mix
        (i,type,(type,n1),type,type,(type,n2),...)

        if an element is with (type,n) form the object must
        support a poweration with ** symbol"""
        
        return self.path_composition(args, self.edge_to_substitution)

    def path_to_matrix(self, *args) :
        return self.path_composition(args, self.edge_to_matrix)

        
class AbelianRauzyDiagram(template.RauzyDiagram, LabeledRauzyDiagram) :
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
            a labeled.AbelianPermutation

        AUTHOR:
            - Vincent Delecroix (2008-12-20)
        """
        self._alphabet = p[0][:]
        self.numerize = lambda l : self._alphabet.index(l)
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
        return AbelianPermutation([a0,a1])




class QuadraticRauzyDiagram(template.RauzyDiagram, LabeledRauzyDiagram) :
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
            a labeled.QuadraticPermutation

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
            a labeled.QuadraticPermutation

        AUTHOR:
            - Vincent Delecroix (2008-12-20)
        """
        a0 = self._permutations[i][0].split()
        a1 = self._permutations[i][1].split()
        return QuadraticPermutation([a0,a1])
