"""Definition of labeled type permutation

  a labeled (generalized) permutation is better suited to study
  dynamics of a translation surface than reduced object. To study
  strata prefer reduced object (Rauzy diagrams are significantly
  smaller ex. for ('a b d b e','e d c a c') the labeled Rauzy diagram
  contains 8760 permutations, and the reduced only 73).
"""

#try :
#    import sage
#    try :
#        import Words
#    except ImportError :
#        from defaut import WordMorphism
#    
#except ImportError :
#    from defaut import WordMorphism
#    try :
#         import numpy.matlib
#         matrix = numpy.matlib.matrix
#         identity_matrix = lambda n : numpy.matlib.eye(n, dtype=int)
#     except ImportError :
#         print "No Matrix support found"

import template
# TODO
#  try to import the words package... (which is now under developpement)

SageObject = object


class NeighbourError(Exception) :
    def __init__(self, value) :
        self.value = value

    def __str__(self) :
        return self.value
    


class Permutation(SageObject) :
    """General template for labeled

    ...NOT A USABLE TYPE... JUST HERE FOR INHERITANCE MECHANISM..."""

    def __init__(self, a) :
        self._intervals = [a[0][:], a[1][:]]

        self._twin = [[],[]]
        self._init_twin(a)


    def __list__(self) :
        return [self._intervals[0][:], self._intervals[1][:]]

    def __eq__(self,other) :
        return (self._intervals == other._intervals)

    
    def __ne__(self,other) :
        return (self._intervals != other._intervals)



class AbelianPermutation(Permutation, template.AbelianPermutation) :
    """Class for labeled abelian permutation"""

    def copy(self) :
        p = AbelianPermutation(([],[]))
        p._twin[0].extend(self._twin[0])
        p._twin[1].extend(self._twin[1])
        p._intervals[0].extend(self._intervals[0])
        p._intervals[1].extend(self._intervals[1])
        return p


    def rauzy_move(self, winner) :
        """do a Rauzy move for this choice of winner

        The Rauzy move of a permutation is the type of a special
        induced on a sub-interval."""

        loser = 1 - winner

        i_win = self._twin[winner][-1]
        loser_letter = self._intervals[loser].pop()
        self._intervals[loser].insert(i_win+1, loser_letter)

        self._twin_rauzy_move(winner)


    def rauzy_move_substitution(self, winner) :
        """return a dictionnary on the alphabet of the
        permutation with codage on the upper interval

        (It should be transformed to a WordMorphism)"""

        loser = 1 - winner

        winner_letter = self._intervals[winner][-1]
        loser_letter = self._intervals[loser][-1]
        d = dict(zip(self._intervals[0],self._intervals[0]))
        
        if winner == 0 : d[loser_letter] = loser_letter + winner_letter
        else : d[loser_letter] = winner_letter + loser_letter

        return WordMorphism(d)

        
    def rauzy_diagram(self) :
        """return the Rauzy diagram of this permutation

        The permutation must be irreducible, because of the
        definability of the Rauzy induction."""
        return AbelianRauzyDiagram(self)


#####################################################################
##############    QUADRATIC LABELED PERMUTATIONS    #################
#####################################################################

class QuadraticPermutation(Permutation, template.QuadraticPermutation) :
    """Class for generalized permutations without flip"""

    def copy(self) :
        p = QuadraticPermutation(([],[]))
        p._twin[0].extend(self._twin[0])
        p._twin[1].extend(self._twin[1])
        p._intervals[0].extend(self._intervals[0])
        p._intervals[1].extend(self._intervals[1])
        return p
       

    def rauzy_move(self,winner) :
        loser = 1 - winner

        i_win = self._twin[winner][-1]

        if i_win[0] == loser : incr = 1
        else : incr = 0
        
        loser_letter = self._intervals[loser].pop()
        self._intervals[i_win[0]].insert(i_win[1] + incr, loser_letter)

        self._twin_rauzy_move(winner)

    def rauzy_diagram(self) :
        return QuadraticRauzyDiagram(self)


##################################
#####     RAUZY DIAGRAMS     #####
##################################
# TODO
#  - define a type Path which should be used to generate matrx or substitution or language or equations on lengths
# from a rauzy diagram. A path is simply (p,type,type,type,...,type) or (p,(type,n1),(type,n2),...,(type,n))
# it should be embeded in different diagrams but much of the method conern directly the diagrams :
#   diagram.path_is_loop(self, path)
#   diagram.path_composition(self, path, function, composition)
#   diagram.path_is_complete(self, path)  # if each letter wins
#
#
#
#
#
#  - perform rauzy_move on real lengths
#  - the alphabet must be set in an order one time for all (the order is only determine by the initial permutation)
#  (use alphabetize and numerize to know it)
#

class Path(SageObject) :
    def __init__(self, value=()) :
        l = []
        # syntax verification
        if len(value) == 0 : raise TypeError("a path as a start")
        if type(value[0]) != int : raise TypeError("the first element must be an integer")
        l.append(value[0])

        for i in value[1:] :
            if type(i) == int  :
               if (i != 0) and (i != 1) : raise TypeError("type must be 0 or 1")
               l.append(i)
            if type(i) == tuple :
                if len(i) != 2 : raise TypeError("syntax problem")
                if (type(i[0]) != int) or (type(i[1]) != int) : raise TypeError("syntax problem")
                if (i[0] != 0) and (i[0] != 1) : raise TypeError("type must be 0 or 1")
                l.extend([i[0]] * i[1])

        print l
        tuple.__init__(self, tuple(l))
                
                


class RauzyDiagram(SageObject) :
    """Class for Labeled Rauzy Diagram

        ...DO NOT USE... """
    
    # standard function for representation of the Rauzy Diagram
    def permutation_to_vertex(self, p) :
        l = list(p)
        return (' '.join(l[0]),' '.join(l[1]))

    def vertex_to_permutation(self, i) :
        a0 = self._permutations[i][0].split()
        a1 = self._permutations[i][1].split()
        return AbelianPermutation([a0,a1])


    def vertex_to_str_one_line(self, i) :
        return str(self._permutations[i])


    def vertex_to_str(self, i) :
        return self._permutations[i][0] + "\\n" + self._permutations[i][1]


    def edges_to_str(self, i) :
        return str(self._neighbours[i])


    # Composition function on edges.
    def path_composition(self, path, function, composition = None) :
        """compose an edge's function on a path
        function must be of the form :
          (i,type) -> element

        function(None) must be an identity element for initialization
        and the path as a path...

        ! MUST TRY TO SEARCH LOOPS INSIDE THE PATH !
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
                        result = result * function(i,step)
                    else :
                        result = composition(result, function(i,step[0]))
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
        """the path must be of the form :
        (i,type,type,type,...,type)
        or
        (i,(type,n1),(type,n2),...,(type,nk))
        or a mix
        (i,type,(type,n1),type,type,(type,n2),...)

        if an element is with (type,n) form the object must
        support a poweration with ** symbol"""
        
        return self.path_composition(args, self.edge_to_substitution)
        

    def path_to_matrix(self, *args) :
        """the path must be of the form :
        (i,type,type,type,...,type)
        or
        (i,(type,n1),(type,n2),...,(type,nk))"""

        return self.path_composition(args, self.edge_to_matrix)

        
class AbelianRauzyDiagram(RauzyDiagram, template.RauzyDiagram) :
    def first_vertex(self, p) :
        self._alphabet = p[0][:]
        self.numerize = lambda l : self._alphabet.index(l)
        self.alphabetize = lambda i : self._alphabet[i]



class QuadraticRauzyDiagram(RauzyDiagram, template.RauzyDiagram) :
    def first_vertex(self, p) :
        tmp_alphabet = []
        for letter in p[0]+p[1] :
            if letter not in tmp_alphabet : tmp_alphabet.append(letter)

        self._alphabet = tmp_alphabet
        self.numerize = lambda l : self._alphabet.index(i)
        self.alphabetize = lambda i : self._alphabet[i]

