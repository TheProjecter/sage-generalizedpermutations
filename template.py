r"""
General template for different types of generalized permutations and Rauzy diagrams

Here is the main file concerning the storage of general permutations. It's useful
for each of the type reduced or labeled. Because it's almost the same thing. Almost
every method here start with the special word 'twin'.


TODO:
    Construct the inheritance as combinatorial types inclusion
    (to allow stratas manipulations)
    Have an independent flip tableau (to have the same _twin_rauzy_move

    Wrap the twin : not access 'directly' to it (it will be defined in C later).

    Strata and Stratas types (derived from Partition)

    Everybody must have a parent (very useful for alphabet..., we look for an
    alphabet in each parent).

    parent here means RauzyDiagram, Strata, ReducedPermutation, ....

    define what self.__list__ must do
"""
#*****************************************************************************
#       Copyright (C) 2008 Vincent Delecroix <delecroix@iml.univ-mrs.fr>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
#*****************************************************************************

from string import replace

from sage import SageObject
#from sage.structure.sage_object import SageObject


defaut_alphabet = Alphabet("123456789")
# this defaut alphabet must be an infinite alphabet which permit a universal
# numerotation.
# For bilabels we need something like A x {0,1} and consider special numerotation
# with this.
# think about alphabetize.


def is_GeneralizedPermutation(obj):
    r"""
    Returns True if obj is a Generalized Permutation

    EXAMPLES:
        sage : is_GeneralizedPermutation(('a b c','c b a'))
        False
        sage : is_GeneralizedPermutation(GeneralizedPermutation('a b c','c b a'))
        True
    """
    return isinstance(obj, GeneralizedPermutation)


class GeneralizedPermutation(SageObject) :
    r"""
    General template for all types of GeneralizedPermutation.
    """
    def __repr__(self) :
        l = list(self)
        return ' '.join(map(str,l[0])) + "\n" + ' '.join(map(str,l[1]))


    def __len__(self) :
        return (len(self._twin[0]) + len(self._twin[1])) / 2


    def length_top(self) :
        r"""
        Returns the number of intervals in the top segment.

        OUTPUT:
            an integer

        EXAMPLES:
            sage : p = GeneralizedPermutation('a b c d', 'c a d b')
            sage : p.lenght_top()
            4

            sage : p = GeneralizedPermutation('a b c b c d d', 'e e a')
            p.length_top()
            7
        """
        return len(self._twin[0])


    def length_bottom(self) :
        r"""
        Return the number of intervals in the bottom segment.

        OUTPUT:
            an integer

        EXAMPLES:
            sage : p = GeneralizedPermutation('a b c d', 'c a d b')
            sage : p.length_bottom()
            4

            sage : p = GeneralizedPermutation('a b c b c d d','e e a')
            sage : p.length_bottom()
            3
        """
        return len(self._twin[1])


    def length(self, interval=None) :
        r"""
        Returns a 2-uple of lengths.

        p.length() is identical to (p.length_top(), p.length_bottom())
        If an interval is specified, it returns the length of the specified
        interval.

        INPUT:
            interval -- 0 or 1

        OUTPUT:
            a 2-uple of integers

        EXAMPLES :
            sage : p = GeneralizedPermutation('a b c d', 'c a d b')
            sage : p.length()
            (4,4)

            sage : p = GeneralizedPermutation('a b c b c d d','e e a')
            sage : p.length()
            (7,3)

        """
        if interval == None :
            return len(self._twin[0]),len(self._twin[1])
        else :
            return len(self._twin[interval])
            


    def __getitem__(self,i) :
        r"""
        Get the label of a specified interval

        INPUT:
            i -- integer 0 or 1
              or 2-uple of integer and slice  0,1 and a slice between 0 and
              length_top() (if 0) and between 0 and length_bottom() (if 1)
              or 2-uple of integers : 0,1 and the other between 0 and length_top()
              (if 0) and between 1 and length_bottom() (if 1)

        EXAMPLES:
            sage : p = GeneralizedPermutation('a b c d', 'd c b a')
            sage : p[0]
            ['a', 'b', 'c', 'd']
            sage : p[1]
            ['d', 'c', 'b', 'a']
            sage : p[0][2:]
            ['c', 'd']
            sage : p[0][-1]
            ['d']
            sage : p[1][-1]
            ['a']
        """
        s = self.__list__()
        if type(i) == int :
            return s[i]
        if type(i) == tuple :
            if (len(i) != 2) or (type(i[0]) != int) : raise IndexError
            return s[i[0]][i[1]]


    def rauzy_move(self, winner) :
        loser_to = self._get_loser_to(winner)
        # beware here, loser_to can contain 2 or 3 items
        # (depending on the presence of flip)

        self._twin_rauzy_move(winner, loser_to)
        
        if hasattr(self, '_move_data') :
            self._move_data((winner, self.length_top() - 1),
                           (1-winner, self.length_bottom() - 1),
                           loser_to[:2])


def is_AbelianPermutation(obj):
    r"""
    Returns true if obj is an Abelian Permutation.

    An abelian permutation is obtained as codage of interval exchange transformations.

    EXAMPLES:
        sage : p = GeneralizedPermutation('a b c', 'c b a')
        sage : is_AbelianPermutation(p)
        True

        sage : p = GeneralizedPermutation('a b b', 'c c a')
        sage : is_AbelianPermutation(p)
        False
    """
    return isinstance(obj, AbelianPermutation)


class AbelianPermutation(GeneralizedPermutation) :
    r"""
    General template for AbelianPermutation

    ...DO NOT USE...

    AUTHORS:
        - Vincent Delecroix (2008-12-20)
    """
    def _init_twin(self, a=None):
        if a is None : a = [[],[]]

        self._twin = [a[0][:],a[1][:]]
        for i in range(len(self._twin[0])) :
            c = self._twin[0][i]
            j = self._twin[1].index(c)
            self._twin[0][i] = j
            self._twin[1][j] = i


    def _init_alphabet(self,a) :
        r"""
        Create an alphabet from a interval list and assign it to 
        self._alphabet.
        """
        
        self._alphabet = Alphabet(a[0])


    def _get_loser_to(self, winner) :
        r"""
        This function return the position of the future loser position.

        The function is redefined in the flipped class.
        """
        return (1-winner, self._twin[winner][-1]+1)
        

    def _twin_rauzy_move(self, winner_interval, loser_to) :
        r"""
        Do a Rauzy move (only on the twin_list) for this choice of winner.
        """
        loser_interval = 1 - winner_interval

        loser_twin_interval = winner_interval
        loser_twin_position = self._twin[loser_interval][-1]

        loser_interval_to, loser_position_to = loser_to

        # move the loser
        del self._twin[loser_interval][-1]
        self._twin[loser_interval_to].insert(loser_position_to, loser_twin_position)
        self._twin[loser_twin_interval][loser_twin_position] = loser_position_to

        # increment the twins in the winner interval
        for j in range(loser_position_to + 1, self.length(loser_interval_to)) :
            self._twin[winner_interval][self._twin[loser_interval_to][j]] += 1


    def is_reducible(self, return_decomposition=False) :
        r"""
        Test of reducibility

        An abelian permutation p = (p0,p1) is reducible if
        the set(p0[:i]) = set(p1[:i]) for an i < len(p0)

        OUTPUT:
            a boolean
            
        EXAMPLE:
            sage : p = GeneralizedPermutation('a b c', 'c b a')
            sage : p.is_reducible()
            False

            sage : p = GeneralizedPermutation('a b c', 'b a c')
            sage : p.is_reducible()
            True
        """
        s0, s1 = 0, 0
        for i in range(len(self)-1) :
            s0 += i
            s1 += self._twin[0][i]
            if s0 == s1 :
                if return_decomposition :
                    return True, (self[0][:i+1], self[0][i+1:], self[1][:i+1], self[1][i+1:])
                return True
        if return_decomposition :
            return False, None
        return False


    def is_rauzy_movable(self, winner=0) :
        r"""
        Test of Rauzy movability (with an eventual specified choice of winner)

        An abelian permutation is rauzy_movable with 0 and 1 type
        simultaneously. But, for compatibility with quadratic permutations, a
        winner could be specified.

        A Rauzy move can be performed on an abelian permutation if and only the
        two extremities intervals don't have the same label.

        remark : rauzy_movability implies reducibility
        
        INPUT:
            eventually a winner : 0 or 1

        OUTPUT:
            a boolean

        EXAMPLES:
            sage : p = GeneralizedPermutation('a b c', 'c b a')
            sage : p.is_rauzy_movable()
            True
            sage : p.is_rauzy_movable(0)
            True
            sage : p.is_rauzy_movable(1)
            True

            sage : p = GeneralizedPermutation('a b c', 'b a c')
            sage : p.is_rauzy_movable()
            False
            sage : p.is_rauzy_movable(0)
            False
            sage : p.is_rauzy_movable(1)
            False

        AUTHORS:
            - Vincent Delecroix (2008-12-20)
        """
        return self._twin[winner][-1] != len(self._twin[winner]) - 1


    def strata(self) :
        r"""
        Return the strata corresponding to any suspension of the corresponding
        IET.

        The permutation must be irreducible. (? could consider product of strata ?)

        OUTPUT:
            an AbelianStrata object

        EXAMPLES:
            sage : p = GeneralizedPermutation('a b c', 'c b a')
            sage : p.strata()

        REFERENCES
            Zorich

        AUTHORS:
            - Vincent Delecroix (2008-12-20)
        """
        return 'H'

    def gender(self) :
        r"""
        Return the gender corresponding to any suspension of the corresponding
        IET.

        OUTPUT:
            an integer

        EXAMLES:
            sage : p = GeneralizedPermutation('a b c', 'c b a')
            sage : p.gender()
            1

        REFERENCES:
            Veech

        AUTHORS:
            - Vincent Delecroix (2008-12-20)
        """
        
    
   
class QuadraticPermutation(GeneralizedPermutation) :
    r"""
    General template for QuadraticPermutation

    ...DO NOT USE...
    """


    def _init_twin(self,a):
        # creation of the twin
        self._twin = [[],[]]
        l = [[(0,j) for j in range(len(a[0]))],[(1,j) for j in range(len(a[1]))]]
        for i in range(2) :
            for j in range(len(l[i])) :
                if l[i][j] == (i,j) :
                    if a[i][j] in a[i][j+1:] :
                        # two up or two down
                        j2 = (a[i][j+1:]).index(a[i][j]) + j + 1
                        l[i][j] = (i,j2)
                        l[i][j2] = (i,j)
                    else :
                        # one up, one down (here i=0)
                        j2 = a[1].index(a[i][j])
                        l[0][j] = (1,j2)
                        l[1][j2] = (0,j)

        self._twin[0] = l[0]
        self._twin[1] = l[1]


    def _init_alphabet(self, intervals) :
        r"""
        Intialization procedure of the alphabet of self from intervals list
        
        assignement to self._alphabet.
        """
        tmp_alphabet = []
        for letter in intervals[0] + intervals[1] :
            if letter not in tmp_alphabet :
                tmp_alphabet.append(letter)

        self._alphabet = Alphabet(tmp_alphabet)



    def is_reducible(self, return_decomposition=False) :
        r"""
        Test of reducibility

        A quadratic (or generalized) permutation is reducible if there exist a
        decomposition
            A1 u B1 | ... | B1 u A2
            A1 u B2 | ... | B2 u A2
        where no corners is empty, or exactly one corner is empty
        and it is on the left, or two and they are both on the
        right or on the left.

        INPUT:
            you can eventually set return_decomposition to True

        OUTPUT:
            an integer
            or
            an integer and a tuple
            if return_decomposition is set as True it return a 2-uple
        (test,decomposition) where test is the preceding test and
        decomposition is a 4-uple (A11,A12,A21,A22) where :
        A11 = A1 u BA
        A12 = B1 u A2
        A21 = A1 u B2
        A22 = B2 u A2

        REFERENCES:
            Boissy-Lanneau

        AUTHORS:
            - Vincent Delecroix (2008-12-20)
        """
        l0 = self.length_top()
        l1 = self.length_bottom()
        s = list(self)

        # testing no corner empty eventually one or two on the left
        A11, A12, A21, A22 = [], [], [], []
        for i1 in range(0, l0) :
            if (i1 > 0) and (s[0][i1-1] in A11) :
                A11 = []
                break
            A11 = s[0][:i1]

            for i2 in range(l0 - 1, i1 - 1, -1) :
                if s[0][i2] in A12 :
                    A12 = []
                    break
                A12 = s[0][i2:]

              
                for i3 in range(0, l1) :
                    if (i3 > 0) and (s[1][i3-1] in A21) :
                        A21 = []
                        break
                    A21 = s[1][:i3]

                    
                    for i4 in range(l1 - 1, i3 - 1, -1) :
                        if s[1][i4] in A22 :
                            A22 = []
                            break
                        A22 = s[1][i4:]
    

                        if sorted(A11 + A22) == sorted(A12 + A21) :
                            if return_decomposition :
                                return True, (A11,A12,A21,A22)
                            return True

                    else : A22 = []
                else : A21 = []
            else : A12 = []
        else : A11 = []        


        # testing two corners empty on the right (i2 = i4 = 0)
        A11, A21 = s[0][:1], s[1][:1]

        for i1 in range(1, l0) :
            if s[0][i1-1] in A11 :
                A11 = s[0][:1]
                break
            A11 = s[0][:i1]

            
            for i3 in range(1, l1) :
                if s[1][i3-1] in A21 :
                    A21 = s[1][:1]
                    break
                A21 = s[1][:i3]

                if sorted(A11)  == sorted(A21) :
                    if return_decomposition :
                        return True,(A11,A12,A21,A22)
                    return True
            else : A11 = s[0][:1]
        else : A21 = s[1][:1]
                
        if return_decomposition :
            return False, ()
        return False


    def is_rauzy_movable(self,winner) :
        r"""
        Test of Rauzy movability (with an eventual specified choice of winner)

        A quadratic (or generalized) permutation is rauzy_movable with 0 and 1
        type depending on the possible length of the last interval. It's
        depend of the length equation.

        INPUT:
            a winner : 0 or 1

        OUTPUT:
            a boolean

        EXAMPLES:
            sage : p = GeneralizedPermutation('a b b', 'c c a')
            sage : p.is_reducible()
            False
            sage : p = GeneralizedPermutation('a b c', 'b a c')
            sage : p.is_reducible()
            True

        AUTHORS:
            - Vincent Delecroix (2008-12-20)
        """
        loser = 1 - winner
        
        # the same letter at the right-end (False)
        if (self._twin[0][-1][0] == 1) and (self._twin[0][-1][1] == self.length_bottom() - 1) :
            return False
        
        # the winner (or loser) letter is repeated on the other interval (True)
        if self._twin[winner][-1][0] == loser : return True
        if self._twin[loser][-1][0] == winner : return True

        # the loser letters is the only letter repeated in the loser interval (False)
        if [i for i,_ in self._twin[loser]].count(loser) == 2 :
            return False

        return True


    def _get_loser_to(self, winner) :
        r"""
        This function return the position of the future loser position.

        The function is redefined in the flipped class.
        """
        loser = 1 - winner
        
        if self._twin[winner][-1][0] == loser :
            return (loser, self._twin[winner][-1][1] + 1)
        else :
            return (winner, self._twin[winner][-1][1])

        

    def _twin_rauzy_move(self, winner_interval, loser_to) :
        loser_interval = 1 - winner_interval

        loser_interval_to, loser_position_to = loser_to
        loser_twin_interval, loser_twin_position = self._twin[loser_interval][-1]

        # increment the twins in the winner interval
        interval = [(self._twin[loser_interval_to][j], j) for j in range(loser_position_to, len(self._twin[loser_interval_to]))]
        for (i,j),k in interval : self._twin[i][j] = (loser_interval_to, k+1)
        
        # prepare the loser new position in its twin
        self._twin[loser_twin_interval][loser_twin_position] = loser_to

        # move the loser
        loser_twin = self._twin[loser_interval][-1]
        self._twin[loser_interval_to].insert(loser_position_to, loser_twin)
        del self._twin[loser_interval][-1]



###################
##### FLIPPED #####
###################
def _labelize_flip(t) :
    if t[1] == 1 :
        return ' ' + str(t[0])
    else :
        return '-' + str(t[0])


class FlippedGeneralizedPermutation(GeneralizedPermutation) :
    r"""
    General template for all flipped types

    flip is integrated in the twin with 1 or -1
    """
    pass


    def __repr__(self) :
        l = list(self)
        return ' '.join(map(_labelize_flip,l[0])) + "\n" + ' '.join(map(_labelize_flip, l[1]))


    def __getitem__(self,i) :
        r"""
        Get labels and flips of specified interval
        """
        s = self.__list__()
        if type(i) == int :
            if i == 0 : return s[0]
            elif i == 1 : return s[1]
            else : raise IndexError
        if type(i) == tuple :
            if (len(i) != 2) or (type(i[0]) != int ) : raise IndexError
            return s[i[0]][i[1]]


    def rauzy_move(self, winner) :
        loser_to = self._get_loser_to(winner)

        self._flip_rauzy_move(winner, loser_to)
        self._twin_rauzy_move(winner, loser_to)
        
        if hasattr(self, '_move_data') :
            self._move_data((winner, self.length_top() - 1),
                           (1-winner, self.length_bottom() - 1),
                           loser_to)


    def _init_flips(self, a, flips):
        self._flips = [a[0][:],a[1][:]]
        for k in range(2) :
            for i,c in enumerate(self._flips[k]) :
                if c in flips :
                    flip = -1
                else :
                    flip = 1
                self._flips[k][i] = flip




class FlippedAbelianPermutation(AbelianPermutation, FlippedGeneralizedPermutation) :
    r"""
    General template for all flipped abelian permutation
    
    ...DO NOT USE...

    TODO :
      the _twin and the _flips lists must be implemented with Pyrex
      (or Cython) as a tableau.
    """


    def _get_loser_to(self, winner) :
        r"""
        This function return the position of the future loser position.
        """
        if self._flips[winner][-1] == 1 :
            # non flipped winner
            return (1-winner, self._twin[winner][-1]+1)
        else :
            # flipped winner
            return (1-winner, self._twin[winner][-1])
        

    def _flip_rauzy_move(self, winner, loser_to) :
        loser = 1 - winner

        loser_twin_interval, loser_twin_position = winner, self._twin[loser][-1]
        loser_interval_to, loser_position_to = loser_to

        flip = self._flips[winner][-1] * self._flips[loser][-1]

        self._flips[loser_twin_interval][loser_twin_position] = flip

        del self._flips[loser][-1]
        self._flips[loser_interval_to].insert(loser_position_to, flip)
        



class FlippedQuadraticPermutation(QuadraticPermutation, FlippedGeneralizedPermutation) :
    """Everything concerning the twin list is here"""


    def _get_loser_to(self, winner) :
        r"""
        This function return the position of the future loser position.

        The function is redefined in the flipped class.
        """
        loser = 1 - winner
        
        if self._twin[winner][-1][0] == loser :
            if self._flips[winner][-1] == 1 :
                return (loser, self._twin[winner][-1][1] + 1)
            else :
                return (loser, self._twin[winner][-1][1])
        else :
            if self._flips[winner][-1] == 1 :
                return (winner, self._twin[winner][-1][1])
            else :
                return (winner, self._twin[winner][-1][1] + 1)


    def _flip_rauzy_move(self, winner, loser_to) :
        loser = 1 - winner

        loser_twin_interval, loser_twin_position = self._twin[loser][-1]
        loser_interval_to, loser_position_to = loser_to

        flip = self._flips[winner][-1] * self._flips[loser][-1]

        self._flips[loser_twin_interval][loser_twin_position] = flip

        del self._flips[loser][-1]
        self._flips[loser_interval_to].insert(loser_position_to, flip)


##############################
##      RAUZY DIAGRAMS      ##
##############################
class RauzyDiagram(SageObject) :
    r"""
    General template for Rauzy Diagram
    """
    def __init__(self, p) :
        self._permutations = [p.copy()]
        self._neighbours = [[None,None]]

        self.complete()

        self._n = len(p)
        self.first_vertex(self._permutations[0])
        self._permutations = map(self.permutation_to_vertex, self._permutations)


    def __repr__(self) :
        r"""
        Representation of general Rauzy Diagram

        Just use the functions vertex_to_one_line_str and edge_to_str that
        must be defined for each child.

        AUTHORS:
            -Vincent Delecroix (2008-12-20)
        """
        s = ""
        for i in range(len(self._permutations)-1) :
            s += "%3d : " %(i) + self.vertex_to_one_line_str(i) + "  " + self.edges_to_str(i) + "\n"
        i = len(self._permutations)-1
        s += "%3d : " %(i) + self.vertex_to_one_line_str(i) + "  " + self.edges_to_str(i)
        return s


    def __getitem__(self,i) :
        r"""
        Translate the vertex to storage to permutation

        Just use the function vertex_to_permutation that must be defined
        in each child.

        INPUT:
            i -- integer

        AUTHORS:
            - Vincent Delecroix (2008-12-20)
        """
        if type(i) != int :
            raise TypeError("must be an integer")
        return self.vertex_to_permutation(i)


    def __len__(self) :
        r"""
        Number of vertices.

        OUTPUT:
            an integer
        """
        return len(self._permutations)


    def complete(self) :
        r"""
        Completion of the Rauzy diagram.

        A Rauzy diagram is the reunion of all permutations that could be
        obtained with successive rauzy moves. This function just use the
        functions __getitem__ and is_rauzy_movable and rauzy_move which must
        be defined for child and their corresponding permutation types.

        AUTHORS:
            - Vincent Delecroix (2008-12-20)
        """
        i = 0
        N = len(self._permutations)

        while i < N :
            p = self._permutations[i]

            for t in (0,1) :
                if p.is_rauzy_movable(t) :
                    q = p.copy()
                    q.rauzy_move(t)
                    j = self.add_vertex(q)
                    self._neighbours[i][t] = j
                else :
                    self._neighbours[i][t] = -1
                
            i += 1
            N = len(self._permutations)


    def add_vertex(self, p) :
        r"""
        Add a vertex if it's not yet in and return the corresponding index

        (perhaps a try...except is less performant than a count)

        INPUT:
            A permutations

        AUTHORS:
            - Vincent Delecroix (2008-20-12)
        """
        try :
            return self._permutations.index(p)

        except ValueError :
            self._permutations.append(p)
            self._neighbours.append([None,None])
            return len(self._permutations) - 1


    def vertex_to_permutation(self, i) :
        r"""
        The defaut implementation.

        All the permutation is stored.
        """
        return self._permutations[i][0]


    def permutation_to_vertex(self, p) :
        r"""
        The defaut implementation (store all)
        """
        return p


    def vertex_to_str(self, i) :
        r"""
        Generic algorithm.

        This implementation use the str method of permutation.
        """
        return str(self._permutations[i])


    def vertex_to_one_line_str(self, i) :
        r"""
        The defaut implementation

        This implemenetation use the str method of the permutation. And
        replace all new lines strings by a space
        """
        return replace(str(self._permutations[i]), "\n", ", ")


    def edges_to_str(self, i) :
        r"""
        The defaut implementation.
        """
        return str(self._neighbours[i])


    def first_vertex(self,p):
        pass


    def dot(self,
            edge0_label = "", edge0_style = "dotted",
            edge1_label = "", edge1_style = "bold",
            opt=['overlap="scale"']) :
        r"""
        Return a dot graph string

        a dot file is simply a formated text file containg a graph. Some
        software uses this format to compute graph pictures. This function
        treats the translation from Rauzy diagram to dot file.
        
        INPUT:
            there is a lot of options that should be parametrized, but most of
            the time, nothing is a good solution. x means here 0 or 1.
            * edgex_label : A label that will be print over each edge
            * edgex_style : one between "bold" , "dotted" and "dashed" (defaut
            is dotted)

            TODO :
            * winner_letter_on_edge : a boolean (defaut is False)
            * loser_letter_on_edge : a boolean (defaut is False)

        OUTPUT:
            a string

        EXAMPLES:
            sage : d = RauzyDiagram('a b c', 'c b a')
            sage : print d.dot()
            digraph G {
            	overlap="scale";
            	/* nodes */
            	node [];
            	0 [label = "a b c\nc b a"];
            	1 [label = "a b c\nc a b"];
            	2 [label = "a c b\nc b a"];
            
            	/* edges of type 0 */
            	edge [style = dotted];
            	0->1;
            	1->0;
            	2->2;
            
            	/* edges of type 1 */
            	edge [style = bold];
            	0->2;
            	1->1;
            	2->0;
            }
            

        AUTHORS:
            - Vincent Delecroix
        """
        s = ""
        
        s += "digraph G {\n"

        for c in opt:
            s += "\t"+c+";"

        # initialization of node and edges properties
        node_properties = "";
        edge0_properties = "style = %s" %(edge0_style)
        if edge0_label != "" :
            edge0_properties += ", label = '%s'" %(edge0_label)

        edge1_properties = "style = %s" %(edge1_style)
        if edge1_label != "" :
            edge1_properties += ", label = '%s'" %(edge1_label)


        # creation of nodes
        s += "\n\t/* nodes */\n"
        s += "\tnode [%s];\n" %(node_properties)

        for k in range(len(self._permutations)) :
            s += """\t%d [label = "%s"];\n""" %(k, self.vertex_to_str(k))

        # creation of edges
        # edges 0
        s += "\n\t/* edges of type 0 */\n"
        s += "\tedge [%s];\n" %(edge0_properties)
        for i,n in enumerate(self._neighbours) :
            if n[0] != -1 :
                s += """\t%d->%d;\n""" %(i,n[0])

        #edges 1
        s += "\n\t/* edges of type 1 */\n"
        s += "\tedge [%s];\n" %(edge1_properties)
        for i,n in enumerate(self._neighbours) :
            if n[1] != -1 :
                s += """\t%d->%d;\n""" %(i,n[1])

        # end
        s += "}\n"

        return s



class FlippedRauzyDiagram(RauzyDiagram) :
    r"""
    Generic class for flipped Rauzy Diagram.

    The main difference is that is possible to exclude reducible
    permutations of our graph.
    """

    def complete(self, reducible=False) :
        r"""
        Completion of the Rauzy diagram.


        INPUT:
            reducible -- (defaut: False) allow or not reducible permutations.
        A Rauzy diagram is the reunion of all permutations that could be
        obtained with successive rauzy moves. This function just use the
        functions __getitem__ and is_rauzy_movable and rauzy_move which must
        be defined for child and their corresponding permutation types.

        AUTHORS:
            - Vincent Delecroix (2008-12-20)
        """
        i = 0
        N = len(self._permutations)

        while i < N :
            p = self._permutations[i]

            for t in (0,1) :
                if p.is_rauzy_movable(t) :
                    q = p.copy()
                    q.rauzy_move(t)
                    if (reducible == True) or not q.is_reducible() :
                        j = self.add_vertex(q)
                        self._neighbours[i][t] = j
                    else :
                        self._neighbours[i][t] = -2
                else :
                    self._neighbours[i][t] = -1
                
            i += 1
            N = len(self._permutations)

