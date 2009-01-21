r"""
General template for different types of generalized permutations and Rauzy diagrams


Here is the main file concerning the storage of general permutations. It's useful
for each of the type reduced or labeled. Because it's almost the same thing. Almost
every method here start with the special word 'twin'.


TODO:
    Construct the inheritance as combinatorial types inclusion
    (to allow stratas manipulations)
"""
#*****************************************************************************
#       Copyright (C) 2008 Vincent Delecroix <delecroix@iml.univ-mrs.fr>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
#*****************************************************************************


#from sage.structure.sage_object import SageObject
SageObject = object


class InvolutionWithoutFixedPoint(SageObject) :
    r"""
    Generic type to study geometry and dynamic of interval exchange map type.
    This type derive from the CombinatorialClass, but all interval exchange
    maps directly derive from this one.


    ALGORITHM:
        A Generalized Permutation contains the following private thing :
            __involution : a list

    EXAMPLES:
        InvolutionWithoutFixedPoint

    TODO:
        Develop the general method
        Define what must be redefined for each child
        Provide a good way to initialization
        Think about a Pyrex implementation because the only problem is the void
        pointer to data (is it possible to derive from the CombinatorialClass
        and be a pyrex file ?)
    """
#########################
####    LOW LEVEL    ####
#########################
    def __init__(self, involution = [], k=0):
        self.__involution = [[i,None] for i in involution]
 
    def __repr__(self) :
        return str(self.__involution[:self.__k]) + "\n" + str(self.__involution[self.__k:])
 
    def __len__(self) :
        return self.length()

    def __iter__(self) :
        raise NotImplementedError

    def __reversed__(self) :
        raise NotImplementedError

    def __list__(self) :
        raise NotImplementedError

    def next(self) :
        raise NotImplementedError

    def previous(self) :
        raise NotImplementedError

    def last(self):
        raise NotImplementedError

    def first(self):
        raise NotImplementedError

    def move(self, from_pos, to_pos) :
        r"""
        Perform a geometric move on the involution (data moves with no change).
        """
        if from_pos < to_pos :
            mover_twin_pos = self.__involution[from_pos][0]

            for i in [j[0] for j in self.__involution[from_pos+1 : to_pos+1]] : self.__involution[i][0] -= 1
            self.__involution[mover_twin_pos][0] = to_pos

            self.__involution.insert(to_pos+1, self.__involution[from_pos])
            del self.__involution[from_pos]


        elif to_pos < from_pos :
            mover_twin_pos = self.__involution[from_pos][0]
            
            for i in [j[0] for j in self.__involution[to_pos : from_pos]] : self.__involution[i][0] += 1
            self.__involution[mover_twin_pos][0] = to_pos

            self.__involution.insert(to_pos, self.__involution[from_pos])
            del self.__involution[from_pos+1]


    
    def is_abelian(self):
        r"""
        Returns True if the underlying generalized permutation is a real permutation.
        """
        if self.length_top() != self.length_bottom() :
            return False

        for i in range(self.length_bottom()) :
            if self.__involution[i][0] < self.__k : return False

        for i in range(self.length_bottom(), len(self)) :
            if self.__involution[i][0] > self.__k : return False

        return True
        

    def is_quadratic(self) :
        r"""
        Returns True if the underlying generalized permutation is not a permutation.
        """
        return not self.is_abelian()


    def is_valid(self) :
        r"""
        Returns True if the datas correspond to a possible linear involution.
        """
        m1 = len(filter(lambda i : i < self.__k, self.__involution[:self.__k]))
        m2 = len(filter(lambda i : i > self.__k, self.__involution[self.__k:]))
        
        if ((m1 == 0) and (m2 > 0)) or ((m1 > 0) and (m2 == 0)) :
            return False

        return True
            

        

    

############################
####    MIDDLE LEVEL    ####
############################
class GeneralizedPermutation(object) :
    def lengths(self) :
        r"""
        Returns a 2-uple of lengths.

        p.length() is identical to (p.length_top(), p.length_bottom())

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
        return (self.length_top(), self.length_bottom())


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
        return self.__k


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
        return len(self.__involution) - self.__k


    def length(self) :
        r"""
        Returns the length of the involution.
        """
        return len(self.__involution) / 2

    


#     def __getitem__(self,i) :
#         r"""
#         Get the label of a specified interval

#         INPUT:
#             i -- integer 0 or 1
#               or 2-uple of integer and slice  0,1 and a slice between 0 and
#               length_top() (if 0) and between 0 and length_bottom() (if 1)
#               or 2-uple of integers : 0,1 and the other between 0 and length_top()
#               (if 0) and between 1 and length_bottom() (if 1)

#         EXAMPLES:
#             sage : p = GeneralizedPermutation('a b c d', 'd c b a')
#             sage : p[0]
#             ['a', 'b', 'c', 'd']
#             sage : p[1]
#             ['d', 'c', 'b', 'a']
#             sage : p[0][2:]
#             ['c', 'd']
#             sage : p[0][-1]
#             ['d']
#             sage : p[1][-1]
#             ['a']
#         """
#         s = self.__list__()
#         if type(i) == int :
#             return s[i]
#         if type(i) == tuple :
#             if (len(i) != 2) or (type(i[0]) != int) : raise IndexError
#             return s[i[0]][i[1]]




# def is_AbelianPermutation(obj):
#     r"""
#     Returns true if obj is an Abelian Permutation.

#     An abelian permutation is obtained as codage of interval exchange transformations.

#     EXAMPLES:
#         sage : p = GeneralizedPermutation('a b c', 'c b a')
#         sage : is_AbelianPermutation(p)
#         True

#         sage : p = GeneralizedPermutation('a b b', 'c c a')
#         sage : is_AbelianPermutation(p)
#         False
#     """
#     return False


# class AbelianPermutation(GeneralizedPermutation) :
#     r"""
#     General template for AbelianPermutation
#     """
#     def _init__involution(self,a):
#         self.__involution = [a[0][:],a[1][:]]
#         for i in range(len(self.__involution[0])) :
#             c = self.__involution[0][i]
#             j = self.__involution[1].index(c)
#             self.__involution[0][i] = j
#             self.__involution[1][j] = i


#     def __involution_rauzy_move(self, winner) :
#         r"""
#         Perform a Rauzy move for the twin list

#         INPUT:
#             winner -- must be 0 or 1

#         AUTHORS:
#             - Vincent Delecroix (2008-12-20)
#         """

#         loser = 1 - winner

#         i_win = self.__involution[winner][-1]
#         i_los = self.__involution[loser][-1]
        
#         # move the loser
#         del self.__involution[loser][-1]
#         self.__involution[loser].insert(i_win+1, i_los)
#         self.__involution[winner][i_los] = i_win+1

#         # increment the twins in the winner interval
#         for j in range(i_win + 2, len(self.__involution[loser])) :
#             self.__involution[winner][self.__involution[loser][j]] += 1


#     def is_reducible(self, return_decomposition=False) :
#         r"""
#         Test of reducibility

#         An abelian permutation p = (p0,p1) is reducible if
#         the set(p0[:i]) = set(p1[:i]) for an i < len(p0)

#         OUTPUT:
#             a boolean
            
#         EXAMPLE:
#             sage : p = GeneralizedPermutation('a b c', 'c b a')
#             sage : p.is_reducible()
#             False

#             sage : p = GeneralizedPermutation('a b c', 'b a c')
#             sage : p.is_reducible()
#             True
#         """
#         s0, s1 = 0, 0
#         for i in range(len(self)-1) :
#             s0 += i
#             s1 += self.__involution[0][i]
#             if s0 == s1 :
#                 if return_decomposition :
#                     return True, (self[0][:i+1], self[0][i+1:], self[1][:i+1], self[1][i+1:])
#                 return True
#         if return_decomposition :
#             return False, None
#         return False


#     def is_rauzy_movable(self, winner=0) :
#         r"""
#         Test of Rauzy movability (with an eventual specified choice of winner)

#         An abelian permutation is rauzy_movable with 0 and 1 type
#         simultaneously. But, for compatibility with quadratic permutations, a
#         winner could be specified.

#         A Rauzy move can be performed on an abelian permutation if and only the
#         two extremities intervals don't have the same label.

#         remark : rauzy_movability implies reducibility
        
#         INPUT:
#             eventually a winner : 0 or 1

#         OUTPUT:
#             a boolean

#         EXAMPLES:
#             sage : p = GeneralizedPermutation('a b c', 'c b a')
#             sage : p.is_rauzy_movable()
#             True
#             sage : p.is_rauzy_movable(0)
#             True
#             sage : p.is_rauzy_movable(1)
#             True

#             sage : p = GeneralizedPermutation('a b c', 'b a c')
#             sage : p.is_rauzy_movable()
#             False
#             sage : p.is_rauzy_movable(0)
#             False
#             sage : p.is_rauzy_movable(1)
#             False

#         AUTHORS:
#             - Vincent Delecroix (2008-12-20)
#         """
#         return self.__involution[winner][-1] != len(self.__involution[winner]) - 1


#     def strata(self) :
#         r"""
#         Return the strata corresponding to any suspension of the corresponding
#         IET.

#         The permutation must be irreducible. (? could consider product of strata ?)

#         OUTPUT:
#             an AbelianStrata object

#         EXAMPLES:
#             sage : p = GeneralizedPermutation('a b c', 'c b a')
#             sage : p.strata()

#         REFERENCES
#             Zorich

#         AUTHORS:
#             - Vincent Delecroix (2008-12-20)
#         """
#         return 'H'


#     def gender(self) :
#         r"""
#         Return the gender corresponding to any suspension of the corresponding
#         IET.

#         OUTPUT:
#             an integer

#         EXAMLES:
#             sage : p = GeneralizedPermutation('a b c', 'c b a')
#             sage : p.gender()
#             1

#         REFERENCES:
#             Veech

#         """
        
# def is_QuadraticPermutation(obj):
#     r"""
#     Test of quadraticity.

#     EXAMPLES:
#         sage : p = GeneralizedPermutation('a b b','c c a')
#         sage : is_QuadraticPermutation(p)
#         True

#         sage : p = GeneralizedPermutation('a b c', 'c b a')
#         sage : is_QuadraticPermutation(p)
#         False
#     """
#     return isinstance(obj, QuadraticPermutation)

    
   
# class QuadraticPermutation(GeneralizedPermutation) :
#     r"""
#     General template for QuadraticPermutation
#     """


#     def _init__involution(self,a):
#         # creation of the twin
#         self.__involution = [[],[]]
#         l = [[(0,j) for j in range(len(a[0]))],[(1,j) for j in range(len(a[1]))]]
#         for i in range(2) :
#             for j in range(len(l[i])) :
#                 if l[i][j] == (i,j) :
#                     if a[i][j] in a[i][j+1:] :
#                         # two up or two down
#                         j2 = (a[i][j+1:]).index(a[i][j]) + j + 1
#                         l[i][j] = (i,j2)
#                         l[i][j2] = (i,j)
#                     else :
#                         # one up, one down (here i=0)
#                         j2 = a[1].index(a[i][j])
#                         l[0][j] = (1,j2)
#                         l[1][j2] = (0,j)

#         self.__involution[0] = l[0]
#         self.__involution[1] = l[1]


#     def is_reducible(self, return_decomposition=False) :
#         r"""
#         Test of reducibility

#         A quadratic (or generalized) permutation is reducible if there exist a
#         decomposition
#             A1 u B1 | ... | B1 u A2
#             A1 u B2 | ... | B2 u A2
#         where no corners is empty, or exactly one corner is empty
#         and it is on the left, or two and they are both on the
#         right or on the left.

#         INPUT:
#             you can eventually set return_decomposition to True

#         OUTPUT:
#             an integer
#             or
#             an integer and a tuple
#             if return_decomposition is set as True it return a 2-uple
#         (test,decomposition) where test is the preceding test and
#         decomposition is a 4-uple (A11,A12,A21,A22) where :
#         A11 = A1 u BA
#         A12 = B1 u A2
#         A21 = A1 u B2
#         A22 = B2 u A2

#         REFERENCES:
#             Boissy-Lanneau

#         AUTHORS:
#             - Vincent Delecroix (2008-12-20)
#         """
#         l0 = self.length_top()
#         l1 = self.length_bottom()
#         s = list(self)

#         # testing no corner empty eventually one or two on the left
#         A11, A12, A21, A22 = [], [], [], []
#         for i1 in range(0, l0) :
#             if (i1 > 0) and (s[0][i1-1] in A11) :
#                 A11 = []
#                 break
#             A11 = s[0][:i1]

#             for i2 in range(l0 - 1, i1 - 1, -1) :
#                 if s[0][i2] in A12 :
#                     A12 = []
#                     break
#                 A12 = s[0][i2:]

              
#                 for i3 in range(0, l1) :
#                     if (i3 > 0) and (s[1][i3-1] in A21) :
#                         A21 = []
#                         break
#                     A21 = s[1][:i3]

                    
#                     for i4 in range(l1 - 1, i3 - 1, -1) :
#                         if s[1][i4] in A22 :
#                             A22 = []
#                             break
#                         A22 = s[1][i4:]
    

#                         if sorted(A11 + A22) == sorted(A12 + A21) :
#                             if return_decomposition :
#                                 return True, (A11,A12,A21,A22)
#                             return True

#                     else : A22 = []
#                 else : A21 = []
#             else : A12 = []
#         else : A11 = []        


#         # testing two corners empty on the right (i2 = i4 = 0)
#         A11, A21 = s[0][:1], s[1][:1]

#         for i1 in range(1, l0) :
#             if s[0][i1-1] in A11 :
#                 A11 = s[0][:1]
#                 break
#             A11 = s[0][:i1]

            
#             for i3 in range(1, l1) :
#                 if s[1][i3-1] in A21 :
#                     A21 = s[1][:1]
#                     break
#                 A21 = s[1][:i3]

#                 if sorted(A11)  == sorted(A21) :
#                     if return_decomposition :
#                         return True,(A11,A12,A21,A22)
#                     return True
#             else : A11 = s[0][:1]
#         else : A21 = s[1][:1]
                
#         if return_decomposition :
#             return False, ()
#         return False


#     def is_rauzy_movable(self,winner) :
#         r"""
#         Test of Rauzy movability (with an eventual specified choice of winner)

#         A quadratic (or generalized) permutation is rauzy_movable with 0 and 1
#         type depending on the possible length of the last interval. It's
#         depend of the length equation.

#         INPUT:
#             a winner : 0 or 1

#         OUTPUT:
#             a boolean

#         EXAMPLES:
#             sage : p = GeneralizedPermutation('a b b', 'c c a')
#             sage : p.is_reducible()
#             False
#             sage : p = GeneralizedPermutation('a b c', 'b a c')
#             sage : p.is_reducible()
#             True

#         AUTHORS:
#             - Vincent Delecroix (2008-12-20)
#         """
#         loser = 1 - winner
        
#         # the same letter at the right-end (False)
#         if self.__involution[winner] == (loser, len(self.__involution[loser]) - 1) : return False
        
#         # the winner (or loser) letter is repeated on the other interval (True)
#         if self.__involution[winner][-1][0] == loser : return True
#         if self.__involution[loser][-1][0] == winner : return True

#         # the loser letters is the only letter repeated in the loser interval (False)
#         if [i for i,_ in self.__involution[loser]].count(loser) == 2 :
#             return False

#         return True
        

#     def __involution_rauzy_move(self,winner) :
#         loser = 1 - winner

#         i_win = self.__involution[winner][-1] # position of the winner twin
#         i_los = self.__involution[loser][-1] # position of the loser twin

#         if i_win[0] == loser : incr = 1
#         else : incr = 0

#         # increment the twins in the winner interval
#         interval = [(self.__involution[i_win[0]][j], j)  for j in range(i_win[1] + incr, len(self.__involution[i_win[0]]))]
#         for (i,j),k in interval : self.__involution[i][j] = (i_win[0], k+1)
        
#         # reinsert the loser in the right position
#         self.__involution[i_los[0]][i_los[1]] = (i_win[0], i_win[1] + incr)

#         # remove the loser
#         i_los = self.__involution[loser][-1]
#         self.__involution[i_win[0]].insert(i_win[1] + incr, i_los)

#         del self.__involution[loser][-1]


# ###################
# ##### FLIPPED #####
# ###################
# def _labelize_flip(i,flip):
#     if flip == -1 : return '-'+str(i)
#     elif flip == 1 : return ' '+str(i)
#     else : raise TypeError("flip must be 1 or -1")
        



# def is_FlippedPermutation(obj):
#     r"""
#     Test of orientation.

#     EXAMPLES:
#         sage : p = GeneralizedPermutation('a b b', 'c c a', flips = 'c')
#         sage : is_FlippedPermutation(p)
#         True

#         sage : p = GeneralizedPermutation('a b b', 'c c a')
#         sage : is_FlippedPermutation(p)
#         False
#     """


        
# class FlippedPermutation(GeneralizedPermutation):
#     r"""
#     General template for all flipped types

#     ALGORITHM:
#         Fliped type always had :
#             __involution_list (heritance from GeneralizedPermutation)
#             a list of flips (corresponding to the Alphabet order)
#     """
#     def 

#     def __repr__(self) :
#         l = list(self)
#         return ' '.join(map(str,l[0])) + "\n" + ' '.join(map(str,l[1]))


#     def __len__(self) :
#         return (len(self.__involution[0]) + len(self.__involution[1])) / 2


#     def length_top(self) :
#         r"""
#         Returns the number of intervals in the top segment.

#         OUTPUT:
#             an integer

#         EXAMPLES:
#             sage : p = GeneralizedPermutation('a b c d', 'c a d b')
#             sage : p.lenght_top()
#             4

#             sage : p = GeneralizedPermutation('a b c b c d d', 'e e a')
#             p.length_top()
#             7
#         """
#         return len(self.__involution[0])


#     def length_bottom(self) :
#         r"""
#         Return the number of intervals in the bottom segment.

#         OUTPUT:
#             an integer

#         EXAMPLES:
#             sage : p = GeneralizedPermutation('a b c d', 'c a d b')
#             sage : p.length_bottom()
#             4

#             sage : p = GeneralizedPermutation('a b c b c d d','e e a')
#             sage : p.length_bottom()
#             3
#         """
#         return len(self.__involution[1])

#     def length(self) :
#         r"""
#         Returns a 2-uple of lengths.

#         p.length() is identical to (p.length_top(), p.length_bottom())

#         OUTPUT:
#             a 2-uple of integers

#         EXAMPLES :
#             sage : p = GeneralizedPermutation('a b c d', 'c a d b')
#             sage : p.length()
#             (4,4)

#             sage : p = GeneralizedPermutation('a b c b c d d','e e a')
#             sage : p.length()
#             (7,3)

#         """
#         return len(self.__involution[0]),len(self.__involution[1])


#     def __getitem__(self,i) :
#         r"""
#         Get the label of a specified interval

#         INPUT:
#             i -- integer 0 or 1
#               or 2-uple of integer and slice  0,1 and a slice between 0 and
#               length_top() (if 0) and between 0 and length_bottom() (if 1)
#               or 2-uple of integers : 0,1 and the other between 0 and length_top()
#               (if 0) and between 1 and length_bottom() (if 1)

#         EXAMPLES:
#             sage : p = GeneralizedPermutation('a b c d', 'd c b a')
#             sage : p[0]
#             ['a', 'b', 'c', 'd']
#             sage : p[1]
#             ['d', 'c', 'b', 'a']
#             sage : p[0][2:]
#             ['c', 'd']
#             sage : p[0][-1]
#             ['d']
#             sage : p[1][-1]
#             ['a']
#         """
#         s = self.__list__()
#         if type(i) == int :
#             return s[i]
#         if type(i) == tuple :
#             if (len(i) != 2) or (type(i[0]) != int) : raise IndexError
#             return s[i[0]][i[1]]



# def is_FlippedAbelianPermutation(FlippedPermutation, AbelianPermutation):
#     r"""
#     Returns True if the object is a FlippedAbelianPermutation
#     """
#     return isinstance(obj, FlippedAbelianPermutation)


        
# class FlippedAbelianPermutation(FlippedPermutation) :
#     """Everything concerning the twin list is here"""
#     pass



# def is_FlippedQuadraticPermutation(obj):
#     r"""
#     """
#     return isinstance(obj, FlippedQuadraticPermutation)



# class FlippedQuadraticPermutation(GeneralizedPermutation) :
#     """Everything concerning the twin list is here"""
#     pass


# ##############################
# ##      RAUZY DIAGRAMS      ##
# ##############################
# class RauzyDiagram(SageObject) :
#     r"""
#     General template for Rauzy Diagram
#     """
#     def __init__(self, p) :
#         self._permutations = [p.copy()]
#         self._neighbours = [[None,None]]

#         self.complete()

#         self.first_vertex(self._permutations[0])
#         self._permutations = map(self.permutation_to_vertex, self._permutations)


#     def __repr__(self) :
#         r"""
#         Representation of general Rauzy Diagram

#         Just use the functions vertex_to_one_line_str and edge_to_str that
#         must be defined for each child.

#         AUTHORS:
#             -Vincent Delecroix (2008-12-20)
#         """
#         s = ""
#         for i in range(len(self._permutations)-1) :
#             s += "%3d : " %(i) + self.vertex_to_one_line_str(i) + "  " + self.edges_to_str(i) + "\n"
#         i = len(self._permutations)-1
#         s += "%3d : " %(i) + self.vertex_to_one_line_str(i) + "  " + self.edges_to_str(i)
#         return s


#     def __getitem__(self,i) :
#         r"""
#         Translate the vertex to storage to permutation

#         Just use the function vertex_to_permutation that must be defined
#         in each child.

#         INPUT:
#             i -- integer

#         AUTHORS:
#             - Vincent Delecroix (2008-12-20)
#         """
#         if type(i) != int :
#             raise TypeError("must be an integer")
#         return self.vertex_to_permutation(i)


#     def __len__(self) :
#         r"""
#         Number of vertices.

#         OUTPUT:
#             an integer
#         """
#         return len(self._permutations)


#     def complete(self) :
#         r"""
#         Completion of the Rauzy diagram.

#         A Rauzy diagram is the reunion of all permutations that could be
#         obtained with successive rauzy moves. This function just use the
#         functions __getitem__ and is_rauzy_movable and rauzy_move which must
#         be defined for child and their corresponding permutation types.

#         AUTHORS:
#             - Vincent Delecroix (2008-12-20)
#         """
#         i = 0
#         N = len(self._permutations)

#         while i < N :
#             p = self._permutations[i]

#             for t in (0,1) :
#                 if p.is_rauzy_movable(t) :
#                     q = p.copy()
#                     q.rauzy_move(t)
#                     j = self.add_vertex(q)
#                     self._neighbours[i][t] = j
#                 else :
#                     self._neighbours[i][t] = -1
                
#             i += 1
#             N = len(self._permutations)


#     def add_vertex(self, p) :
#         r"""
#         Add a vertex if it's not yet in and return the corresponding index

#         (perhaps a try...except is less performant than a count)

#         INPUT:
#             A permutations

#         AUTHORS:
#             - Vincent Delecroix (2008-20-12)
#         """
#         try :
#             return self._permutations.index(p)

#         except ValueError :
#             self._permutations.append(p)
#             self._neighbours.append([None,None])
#             return len(self._permutations) - 1


#     def dot(self,
#             edge0_label = "", edge0_style = "dotted",
#             edge1_label = "", edge1_style = "bold",
#             opt=['overlap="scale"']) :
#         r"""
#         Return a dot graph string

#         a dot file is simply a formated text file containg a graph. Some
#         software uses this format to compute graph pictures. This function
#         treats the translation from Rauzy diagram to dot file.
        
#         INPUT:
#             there is a lot of options that should be parametrized, but most of
#             the time, nothing is a good solution. x means here 0 or 1.
#             * edgex_label : A label that will be print over each edge
#             * edgex_style : one between "bold" , "dotted" and "dashed" (defaut
#             is dotted)

#             TODO :
#             * winner_letter_on_edge : a boolean (defaut is False)
#             * loser_letter_on_edge : a boolean (defaut is False)

#         OUTPUT:
#             a string

#         EXAMPLES:
#             sage : d = RauzyDiagram('a b c', 'c b a')
#             sage : print d.dot()
#             digraph G {
#             	overlap="scale";
#             	/* nodes */
#             	node [];
#             	0 [label = "a b c\nc b a"];
#             	1 [label = "a b c\nc a b"];
#             	2 [label = "a c b\nc b a"];
            
#             	/* edges of type 0 */
#             	edge [style = dotted];
#             	0->1;
#             	1->0;
#             	2->2;
            
#             	/* edges of type 1 */
#             	edge [style = bold];
#             	0->2;
#             	1->1;
#             	2->0;
#             }
            

#         AUTHORS:
#             - Vincent Delecroix
#         """
#         s = ""
        
#         s += "digraph G {\n"

#         for c in opt:
#             s += "\t"+c+";"

#         # initialization of node and edges properties
#         node_properties = "";
#         edge0_properties = "style = %s" %(edge0_style)
#         if edge0_label != "" :
#             edge0_properties += ", label = '%s'" %(edge0_label)

#         edge1_properties = "style = %s" %(edge1_style)
#         if edge1_label != "" :
#             edge1_properties += ", label = '%s'" %(edge1_label)


#         # creation of nodes
#         s += "\n\t/* nodes */\n"
#         s += "\tnode [%s];\n" %(node_properties)

#         for k in range(len(self._permutations)) :
#             s += """\t%d [label = "%s"];\n""" %(k, self.vertex_to_str(k))

#         # creation of edges
#         # edges 0
#         s += "\n\t/* edges of type 0 */\n"
#         s += "\tedge [%s];\n" %(edge0_properties)
#         for i,n in enumerate(self._neighbours) :
#             if n[0] != -1 :
#                 s += """\t%d->%d;\n""" %(i,n[0])

#         #edges 1
#         s += "\n\t/* edges of type 1 */\n"
#         s += "\tedge [%s];\n" %(edge1_properties)
#         for i,n in enumerate(self._neighbours) :
#             if n[1] != -1 :
#                 s += """\t%d->%d;\n""" %(i,n[1])

#         # end
#         s += "}\n"

#         return s


