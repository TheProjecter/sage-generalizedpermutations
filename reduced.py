"""Definition of reduced object

  a reduced (generalized) permutation is better suitted to study
  strata of abelian (or quadratic) holomorphic forms on Riemann
  surfaces. The Rauzy diagram is an invariant of such a
  component. Corentin  Boissy proved the identification between
  Rauzy diagrams and connected components of strata. But the
  geometry of the diagram is not yet totally understood.
"""

import template
SageObject = object

class Permutation(SageObject) :
    """Template for reduced objects"""

    ### INITIALIZATION
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


class FlippedPermutation(SageObject) :
    pass

class FlippedAbelianPermutation(FlippedPermutation, template.FlippedAbelianPermutation) :
    pass

######################################
#####     ABELIAN PERMUTATION    #####
######################################
class AbelianPermutation(Permutation, template.AbelianPermutation):
    """Reduced abelian permutation

    Class for Abelian Permutation without numerotation of intervals.
    For initialization, you should use GeneralizedPermutation which
    is the class factory for all permutation types.
    """

    def copy(self) :
        p = AbelianPermutation(([],[]))
        p._twin[0].extend(self._twin[0])
        p._twin[1].extend(self._twin[1])
        p._alphabet = self._alphabet
        return p

    
    def _init_alphabet(self,a) :
        self._alphabet = tuple(a[0][:])


    def __list__(self) :
        """mutation of the permutation to a list of two lists"""
        a0 = map(self._alphabetize, range(0,len(self)))
        a1 = map(self._alphabetize, self._twin[1])
        return [a0,a1]
        

    def __eq__(self,other) :
        """test of equality"""
        return self._twin[0] == other._twin[0]


    def __ne__(self,other) :
        """test of difference"""
        return self._twin[0] != other._twin[0]
    

    def copy(self) :
        """return a copy of himself"""
        q = AbelianPermutation(("",""))
        q._twin = [self._twin[0][:], self._twin[1][:]]
        if hasattr(self,"_alphabet") :
            q._alphabet = self._alphabet
            q._alphabetize = lambda i : self._alphabet[i]
        else :
            q._alphabetize = self._alphabetize

        return q
        
        
    def rauzy_diagram(self) :
        """return the Rauzy diagram of this permutation

        The permutation must be irreducible, because of the
        definability of the Rauzy induction."""
        return AbelianRauzyDiagram(self)


###############################################
#####     FLIPPED ABELIAN PERMUTATION     #####
###############################################

class FlippedAbelianPermutation(Permutation, template.AbelianPermutation):
    pass


#####################################################################
##############    QUADRATIC REDUCED PERMUTATIONS    #################
#####################################################################

class QuadraticPermutation(Permutation, template.QuadraticPermutation):
    """Quadratic (or generalized) reduced permutation """

    def copy(self) :
        p = QuadraticPermutation(([],[]))
        p._twin[0].extend(self._twin[0])
        p._twin[1].extend(self._twin[1])
        p._alphabet = self._alphabet
        return p

    def _init_alphabet(self,a) :
        """initialization of alphabet"""
        tmp_alphabet = []
        for letter in a[0]+a[1] :
            if letter not in tmp_alphabet :
                tmp_alphabet.append(letter)

        self._alphabet = tuple(tmp_alphabet)


    def __list__(self) :
        """return a list of letter """
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
        return (self._twin[0] == other._twin[0]) and (self._twin[1] == other._twin[1])


    def __ne__(self, other) :
        return (self._twin[0] != other._twin[0]) or (self._twin[1] != other._twin[1])


    def rauzy_diagram(self) :
        return QuadraticRauzyDiagram(self)

#################################################
#####     FLIPPED QUADRATIC PERMUTATION     #####
#################################################
class FlippedQuadraticPermutation(FlippedPermutation, template.FlippedQuadraticPermutation) :
    pass

###################################################
#############    RAUZY DIAGRAMS    ################
###################################################


class AbelianRauzyDiagram(template.RauzyDiagram) :
    """Class for rauzy diagram of abelian permutations"""
    
    def permutation_to_vertex(self, p) :
        return ' '.join(list(p)[1])
        

    def vertex_to_permutation(self, i) :
        a0 = self._a0.split()
        a1 = self._permutations[i].split()
        return AbelianPermutation([a0,a1])


    def vertex_to_str_one_line(self, i) :
        """return a string that represent a vertex"""
        return self._permutations[i]


    def vertex_to_str(self, i) :
        """return a 'real' representation on two lines"""
        return self._a0 + "\\n" + self._permutations[i]


    def edges_to_str(self, i) :
        """return a string that represent a couple of edge"""
        return str(self._neighbours[i])
        

    def first_vertex(self, p) :
        """The special initialization"""
        self._a0 = ' '.join(list(p)[0])


#####################################################
###########    QUADRATIC RAUZY DIAGRAM    ###########
#####################################################
# A Rauzy Diagram is here a static abject. Nothing can be changed. You
# can hust have information, such that :
#  - strata (gender, singularity, spin)
#  - property of the graph

class QuadraticRauzyDiagram(template.RauzyDiagram) :
    """Class for rauzy diagram of abelian permutations"""
    
    def permutation_to_vertex(self, p) :
        l = list(p)
        return (' '.join(l[0]), ' '.join(l[1]))
        

    def vertex_to_permutation(self, i) :
        a0 = self._permutations[i][0].split()
        a1 = self._permutations[i][1].split()
        return QuadraticPermutation([a0,a1])


    def vertex_to_str_one_line(self, i) :
        """return a string that represent a vertex"""
        return str(self._permutations[i])


    def vertex_to_str(self, i) :
        """return a 'real' representation on two lines"""
        return self._permutations[i][0] + "\\n" + self._permutations[i][1]


    def edges_to_str(self, i) :
        """return a string that represent a couple of edge"""
        return str(self._neighbours[i])

