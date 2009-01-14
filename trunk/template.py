"""General template for different types of permutation
and rauzy_diagram


Here is the main file concerning the storage of general permutations. It's useful
for each of the type reduced or labeled. Because it's almost the same thing. Almost
every method here start with the special word 'twin'.

list of general method :
  __repr__
  __len__
  __getitem__
  length_top
  length_bottom
  length


list of general abelian/quadratic and flipped/oriented method :
  _init_twin
  _twin_rauzy_move
  is_reducible
  is_rauzy_movable
  strata
  gender


list of labeled general method :
  __init__
  __eq__
  __ne__
  __list__
  rauzy_move_matrix


list of labeled specialized method (i.e. depends of the type) :
  rauzy_move_substitution



list of reduced general method :
  __init__
  get_alphabet, set_alphabet
  set_alphabetize
  rauzy_move (= _twin_rauzy_move)


list of reduced specialized method (i.e. depends of the type) :
  __eq__
  __ne__
  __list__
  _init_alphabet
  copy

"""


# from sage.ext.sage_object import SageObject
SageObject = object

def is_simple(s) :
    """s must be a list. Return True if each element is non repeated. """

    for i in s :
        if s.count(i) != 1 : return False
    return True


def is_double_set(s) :
    """s must be a list. Return true if each element is repeated exactly twice """

    t = s[:]
    while t != [] :
        if t.count(t[0]) != 2 : return False
        i = t[1:].index(t[0])
        t.pop(0)
        t.pop(i)

    return True



class Permutation(SageObject) :
    """General template for all types

    ...NOT A USABLE TYPE... JUST HERE FOR INHERITANCE MECHANISM..."""

    def __repr__(self) :
        l = list(self)
        return ' '.join(map(str,l[0])) + "\n" + ' '.join(map(str,l[1]))

    def __len__(self) :
        return (len(self._twin[0]) + len(self._twin[1])) / 2

    def length_top(self) :
        return len(self._twin[0])

    def length_bottom(self) :
        return len(self._twin[1])

    def length(self) :
        return len(self._twin[0]),len(self._twin[1])

    def __getitem__(self,i) :
        s = self.__list__()
        if type(i) == int :
            if i == 0 : return s[0]
            elif i == 1 : return s[1]
            else : raise IndexError
        if type(i) == tuple :
            if (len(i) != 2) or (type(i[0]) != int ) : raise IndexError
            return s[i[0]][i[1]]


class AbelianPermutation(Permutation) :
    """General template for AbelianPermutation

    ...NOT A USABLE TYPE... JUST HERE FOR INHERITANCE MECHANISM..."""


    def _init_twin(self,a):
        """initialisation of correspondance from the list in a"""
        self._twin = [a[0][:],a[1][:]]
        for i in range(len(self._twin[0])) :
            c = self._twin[0][i]
            j = self._twin[1].index(c)
            self._twin[0][i] = j
            self._twin[1][j] = i


    def _twin_rauzy_move(self, winner) :
        """do a Rauzy move for this choice of winner

        The Rauzy move of a permutation is the type of a special
        induced on a sub-interval."""

        loser = 1 - winner

        i_win = self._twin[winner][-1]
        i_los = self._twin[loser][-1]
        
        # move the loser
        del self._twin[loser][-1]
        self._twin[loser].insert(i_win+1, i_los)
        self._twin[winner][i_los] = i_win+1

        # increment the twins in the winner interval
        for j in range(i_win + 2, len(self._twin[loser])) :
            self._twin[winner][self._twin[loser][j]] += 1


    def is_reducible(self) :
        """test of reducibility

        An abelian permutation p = (p0,p1) is reducible if
        the set(p0[:i]) = set(p1[:i]) for an i < len(p0) """
        s0, s1 = 0, 0
        for i in range(len(self)-1) :
            s0 += i
            s1 += self._twin[0][i]
            if s0 == s1 : return True
        return False


    def is_rauzy_movable(self, winner) :
        """Return True if it's possible to perform a Rauzy move with this winner"""
        return self._twin[winner][-1] != len(self._twin[winner]) - 1


    def strata(self) :
        """Return the strata (i.e. indices of singularities of the suspension)"""
        raise NotImplemented


    def gender(self) :
        """Return the gender of the suspension"""
        raise NotImplemented
        
    
    
class QuadraticPermutation(Permutation) :
    """General template for QuadraticPermutation

    ...NOT A USABLE TYPE... JUST HERE FOR INHERITANCE MECHANISM..."""


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


    def is_reducible(self, return_decomposition=False) :
        """return True if the permutation is geometrically reducible (Boissy-Lanneau)

        i.e. there no decomposition as
        A1 u B1 | ... | B1 u A2
        A1 u B2 | ... | B2 u A2
        where no corners is empty, or exactly one corner is empty
        and it is on the left, or two and they are both on the
        right or on the left.

        if return_decomposition is set as True it return a 2-uple
        (test,decomposition) where test is the preceding test and
        decomposition is a 4-uple (A11,A12,A21,A22) where :
        A11 = A1 u BA
        A12 = B1 u A2
        A21 = A1 u B2
        A22 = B2 u A2"""

        # the loops could be reduced using special properties such that :
        #    - crossed twin (A11 and A22) or (A12 and A21)
        
        l0 = self.length_top()
        l1 = self.length_bottom()
        s = list(self)

        # testing no corner empty eventually one or two on the left
        for i1 in range(0, l0) :
            A11 = s[0][:i1]
            if not is_simple(A11) : break
            
            for i2 in range(l0 - 1, i1 - 1, -1) :
                A12 = s[0][i2:]
                if not is_simple(A12) : break
                
                for i3 in range(0, l1) :
                    A21 = s[1][:i3]
                    if not is_simple(A21) : break
                    
                    for i4 in range(l1 - 1, i3 - 1, -1) :
                        A22 = s[1][i4:]
                        if not is_simple(A22) : break

                        if sorted(A11 + A22) == sorted(A12 + A21) :
                            if return_decomposition :
                                return True, (A11,A12,A21,A22)
                            return True
        
        # testing two corners empty on the right (i2 = i4 = 0)
        A12, A22 = [], []

        for i1 in range(1, l0) :
            A11 = s[0][:i1]
            if not is_simple(A11) : break
            
            for i3 in range(0, l1) :
                A21 = s[1][:i3]
                if not is_simple(A21) : break

                if sorted(A11 + A22) == sorted(A12 + A21) :
                    if return_decomposition :
                        return True,(A11,A12,A21,A22)
                    return True
                
        if return_decomposition :
            return False, ()
        return False


    def is_rauzy_movable(self,winner) :
        """test of possibility of a Rauzy move with this winner.

        The possibility of a Rauzy move depends just of the length
        equation."""
        loser = 1 - winner
        
        # the same letter at the right-end (False)
        if self._twin[winner] == (loser, len(self._twin[loser]) - 1) : return False
        
        # the winner (or loser) letter is repeated on the other interval (True)
        if self._twin[winner][-1][0] == loser : return True
        if self._twin[loser][-1][0] == winner : return True

        # the loser letters is the only letter repeated in the loser interval (False)
        if [i for i,_ in self._twin[loser]].count(loser) == 2 :
            return False

        return True
        

    def _twin_rauzy_move(self,winner) :
        """perform the rauzy move on the permutation with the specified winner"""
        
        loser = 1 - winner

        i_win = self._twin[winner][-1] # position of the winner twin
        i_los = self._twin[loser][-1] # position of the loser twin

        if i_win[0] == loser : incr = 1
        else : incr = 0

        # increment the twins in the winner interval
        interval = [(self._twin[i_win[0]][j], j)  for j in range(i_win[1] + incr, len(self._twin[i_win[0]]))]
        for (i,j),k in interval : self._twin[i][j] = (i_win[0], k+1)
        
        # reinsert the loser in the right position
        self._twin[i_los[0]][i_los[1]] = (i_win[0], i_win[1] + incr)

        # remove the loser
        i_los = self._twin[loser][-1]
        self._twin[i_win[0]].insert(i_win[1] + incr, i_los)

        del self._twin[loser][-1]

###################
##### FLIPPED #####
###################
class FlippedAbelianPermutation(Permutation) :
    """Everything concerning the twin list is here"""
    pass

class FlippedQuadraticPermutation(Permutation) :
    """Everything concerning the twin list is here"""
    pass


##############################
##      RAUZY DIAGRAMS      ##
##############################
"""

general methods of rauzy diagrams
  __init__
  dot()
  add_vertex(p)


specialized methods of Abelian Rauzy diagram / Quadratic Rauzy Diagram / Flipped
  vertex_to_permutation
    translation from vertex type to the permutation type
  vertex_to_string
    translation from vertex type to a string
  permutation_to_vertex
    translation from permutation to vertex type


Abelian oriented :
   complete_loop
   complete_diagram


general methods of Labeled Diagram
  alphabetize
  add_edge

general methods of Reduced Diagram
  add_edge

"""


class RauzyDiagram(SageObject) :
    """General template

    ...DO NOT USE..."""
    
    def __init__(self, p) :
        self._permutations = [p.copy()]
        self._neighbours = [[None,None]]

        # complete the list
        self.complete()

        # store just essential data
        self.first_vertex(self._permutations[0])
        self._permutations = map(self.permutation_to_vertex, self._permutations)


    def __repr__(self) :
        s = ""
        for i in range(len(self._permutations)-1) :
            s += "%3d : " %(i) + self.vertex_to_str_one_line(i) + "  " + self.edges_to_str(i) + "\n"
        i = len(self._permutations)-1
        s += "%3d : " %(i) + self.vertex_to_str_one_line(i) + "  " + self.edges_to_str(i)
        return s


    def __getitem__(self,i) :
        if type(i) != int :
            raise TypeError("must be an integer")
        return self.vertex_to_permutation(i)


    def __len__(self) :
        return len(self._permutations)

    def permutation_to_vertex(self, p) :
        pass


    def vertex_to_permutation(self, i) :
        pass


    def vertex_to_str(self, i) :
        str(p)
    

    def vertex_to_str_one_line(self, i) :
        raise NotImplemented


    def first_vertex(self, p) :
        pass


    def complete(self) :
        """total completion of the diagram from i"""
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


    def add_vertex(self,p) :
        """add a vertex or return the current index"""
        try :
            return self._permutations.index(p)

        except ValueError :
            self._permutations.append(p)
            self._neighbours.append([None,None])
            return len(self._permutations) - 1


    def dot(self,
            edge0_label = "", edge0_style = "dotted",
            edge1_label = "", edge1_style = "bold",
            opt=['overlap="scale"']) :
        """print a dot graph string (which should be used to produce a jpg, bitmap or pdf...)
        The options should take the form :
        edge0_label = "0"
        edge0_style = "bold" || "dotted" || "dashed"
        idem for 1
        """
        print "digraph G {"

        for c in opt:
            print "\t"+c+";"

        # initialization of node and edges properties
        node_properties = "";
        edge0_properties = "style = %s" %(edge0_style)
        if edge0_label != "" :
            edge0_properties += ", label = '%s'" %(edge0_label)

        edge1_properties = "style = %s" %(edge1_style)
        if edge1_label != "" :
            edge1_properties += ", label = '%s'" %(edge1_label)


        # creation of nodes
        print "\n\t/* nodes */"
        print "\tnode [%s];" %(node_properties)

        for k in range(len(self._permutations)) :
            print """\t%d [label = "%s"]""" %(k, self.vertex_to_str(k))

        # creation of edges
        # edges 0
        print "\n\t/* edges of type 0 */"
        print "\tedge [%s];" %(edge0_properties)
        for i,n in enumerate(self._neighbours) :
            if n[0] != -1 :
                print """\t%d->%d;""" %(i,n[0])

        #edges 1
        print "\n\t/* edges of type 1 */"
        print "\tedge [%s];" %(edge1_properties)
        for i,n in enumerate(self._neighbours) :
            if n[1] != -1 :
                print """\t%d->%d;""" %(i,n[1])

        # end
        print "}"


