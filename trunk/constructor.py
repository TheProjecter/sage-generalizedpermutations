r"""
(Flipped) Generalized (Reduced or Labeled) Permutation and associated Rauzy
diagrams.

    This library is designed to define and use different types of permutations
    and generalized permutations which appears in interval exchange
    transformations and linear involutions (with or without flips). The module
    also provide special tools to work with Rauzy diagrams.


AUTHORS: 
    -- Vincent Delecroix (2008-12-20): initial version


EXAMPLES:
    To create all types of permutation there is a general class factory whose
    name is GeneralizedPermutation :

    Creation of labeled Abelian and quadratic permutation :
        sage : p1 =  GeneralizedPermutation('a b c', 'c b a')
        a b c
        c b a
        sage : p2 = GeneralizedPermutation('a a b', 'b c c')
        a a b
        b c c
       
    Creation of reduced Abelian and quadratic permutation :
        sage : p1 = GeneralizedPermutation('a b c', 'c b a', reduced = True)
        a b c
        c b a
        sage : p2 = GeneralizedPermutation('a b b', 'c c a', reduced = True)
        a b b
        c c a

    For flips you just have to precise the set of flipped intervals :
        sage : p1 = GeneralizedPermutation('a b c', 'c b a', flips = ['a','c'])
        -a b -c
        -c b -a
        sage : p2 = GeneralizedPermutation('a a b', 'b c c', flips = ['a'],
        reduced = True)
        -a -a  b
         b  c  c


    For Rauzy diagrams there is two construction methods. The first one is to
    use the class factory :
        sage : d = RauzyDiagram('a b c', 'c b a')
        0 : ('a b c', 'c b a')  [1,2]
        1 : ('a b c', 'c a b')  [0,1]
        2 : ('a c b',' c b a')  [2,0]

    The other one is to use the method of a generalized permutation :
        sage : p = GeneralizedPermutation('a b c', 'c b a')
        sage : d = p.rauzy_diagram()
        0 : ('a b c', 'c b a')  [1,2]
        1 : ('a b c', 'c a b')  [0,1]
        2 : ('a c b',' c b a')  [2,0]
       
    Both methods give rise to the same object.
"""

#*****************************************************************************
#       Copyright (C) 2008 Vincent Delecroix <delecroix@iml.univ-mrs.fr>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
#*****************************************************************************

from sage import SageObject
#from sage.structure.sage_object import SageObject

from labeled import *
from reduced import *

class WrongParameter(Exception):
    def __init__(self,value):
        self.value = value

    def __str__(self):
        return str(self.value)

class NoAdmissibleLength(Exception):
    def __init__(self,value):
        self.value = value

    def __str__(self):
        return str(self.value)

class NoMatchingTwin(Exception):
    def __init__(self,value):
        self.value = value

    def __str__(self):
        return str(self.value)



def GeneralizedPermutation(*args,**kargs):
    r"""
    Return an object representing a generalized permutation.

    Generalized permutations are the combinatoric part of an interval exchange
    transformation (IET). The combinatorial study of those objects starts with
    Gerard Rauzy and William Veech.

    INPUT:
        intervals -- two strings or a list of two strings or two lists
        (names of intervals) or a list of two lists or one string with form
        (top intervals) \\n (bottom intervals)

        flips -- list of letters (defaut: [])
        reduced -- a boolean (defaut: False) which specifies reduction


    OUTPUT:
        generalized permutation -- (eight possible types)

    EXAMPLES:
    Creation of labeled permutations (Abelian or quadratic) :
        sage : GeneralizedPermutation('a b c d','d c b a')
        a b c d
        d c b a
        sage : GeneralizedPermutation([['a','b','c','d'],['d','c','b','a']])
        a b c d
        d c b a
        sage : GeneralizedPermutation('a b b', 'c c a')
        a b b
        c c a

    Creation of reduced permutations (Abelian or quadratic)
        sage : GeneralizedPermutation('a b c', 'c b a', reduced = True)
        a b c
        c b a
        sage : GeneralizedPermutation('a b b' 'c c a', reduced = True)
        a b b
        c c a

    Creation of flipped permutations (Abelian or quadratic)
        sage : GeneralizedPermutation('a b c', 'c b a', flips = ['a','b'])  # todo: not yet implemented
        sage : GeneralizedPermutation('a b c', 'c b a', flips = ['a'], reduced = True)  # todo: not yet implemented

    NOTES:
        flipped permutations are not yet implemented


        REFERENCES :
            Corentin Boissy and Erwan Lanneau, "Dynamics and geometry
            of the Rauzy-Veech induction for quadratic differentials"
            (arxiv:0710.5614)

            Claude Danthony and Arnaldo Nogueira "Measured foliations
            on nonorientable surfaces", Annales scientifiques de
            l'Ecole Normale Superieure, Ser. 4, 23, no. 3 (1990),
            p 469-494

            Arnaldo Nogueira, "Almost all Interval Exchange
            Transformations with Flips are Nonergodic" (Ergod. Th. &
            Dyn. Systems, Vol 5., (1985), 257-271

            Anton Zorich, "Generalized Permutation software"
            (http://perso.univ-rennes1.fr/anton.zorich)

            Anton Zorich, "Explicit Jenkins-Strebel representatives of
            all strata of Abelian and quadratic differentials", Journal
            of Modern Dynamics, 2:1 (2008), 139-185

    AUTHORS :
        - Vincent Delecroix (2008-20-12)
    """

    a = [None,None]
    
    # verification of args, at the end of this verification a[0] and a[1]  are two lists
    # of strings which represent list of intervals
    if (len(args) == 0) or (len(args) > 2) : raise WrongParameter("At most two arguments")

    if len(args) == 1 :
        args = args[0]
        if (type(args) == list) or (type(args) == tuple) :
            # here args is one list (of string or list)
            if (len(args) != 2) : raise WrongParameter("Your list must contain two strings or two lists")
            for i in range(2):
                if type(args[i]) == str :
                    a[i] = args[i].split()
                elif type(args[i]) == list :
                    a[i] = args[i][:]
                    for j in a[i] :
                        if type(j) != str : raise TypeError("Must be strings in your list")
                else :
                    raise TypeError("Your list must be string or list")

        elif type(args) == str :
            # here args is one string
            strings = args.split('\n')
            if len(a) != 2 : raise WrongParameter("Your chain must contain exactly two lines")
            else :
                a[0] = strings[0].split()
                a[1] = strings[1].split()

        else :
            # here is a bad argument
            raise TypeErrorr("Non acceptable argument")

    else :
        # here args is composed of two elements
        for i in range(2):
            if type(args[i]) == str :
                a[i] = args[i].split()
            elif type(args[i]) == list : 
                a[i] = args[i][:]
                for j in a[i] :
                    if type(j) != str : raise TypeError("Must be strings in your list")
            else : raise TypeError("Your two arguments must be string or list")
    
    # verification of kargs
    if 'reduced' not in kargs :
        reduction = False
    elif not isinstance(kargs["reduced"], bool) :
        raise TypeError("reduced must be of type boolean")
    else :
        if kargs["reduced"] == True : reduction = True
        else : reduction = False

    if  'flips' not in kargs :
        flips = []
    else :
        flips = kargs['flips']
        
      
    # verification of the coherence of a and choose between normal or generalized
    l = a[0] + a[1]
    alphabet = set(l)

    for letter in alphabet :
        if l.count(letter) != 2 : raise NoMatchingTwin("Letters must reappear twice")

    for letter in alphabet :
        if (a[0].count(letter) == 2) or (a[1].count(letter) == 2) :
            generalized = True
            break
    else :
        generalized = False

    if generalized == True :
        # check exitence of admissible length
        b0 = a[0][:]
        b1 = a[1][:]
        for letter in alphabet :
            if b0.count(letter) == 1 :
                del b0[b0.index(letter)]
                del b1[b1.index(letter)]

        if (b0 == []) or (b1 == []):
            raise NoAdmissibleLength("There is no corresponding length")


    # verification of coherence of flips
    for flip in flips :
        if flip not in alphabet : raise WrongParameter("flips non element of the alphabet")


    # repartition to different objects
    if generalized == False :
        if reduction == True :
            if flips == [] :
                return ReducedAbelianPermutation(a)
            else :
                return FlippedReducedAbelianPermutation(a,flips)
        else :
            if flips == [] :
                return LabeledAbelianPermutation(a)
            else :
                return FlippedLabeledAbelianPermutation(a,flips)
    else :
        if reduction == True :
            if flips == [] :
                return ReducedQuadraticPermutation(a)
            else :
                return FlippedReducedQuadraticPermutation(a,flips)
        else :
            if flips == [] :
                return LabeledQuadraticPermutation(a)
            else :
                return FlippedLabeledQuadraticPermutation(a,flips)


def RauzyDiagram(*args, **kargs) :
    r"""
    Return an object coding a Rauzy diagram

    INPUT :
        intervals -- two list, or two strings
        reduced -- a boolean (defaut: False) to precise reduction
        flips -- a list (defaut: []) for flipped permutations
    
    OUTPUT :
        rauzy diagram -- eight possible types depending on input datas

    EXAMPLES :
        sage :  RauzyDiagram('a b c','c b a')
         0 : ('a b c', 'c b a')  [1,2]
         1 : ('a b c', 'c a b')  [0,1]
         2 : ('a c b', 'c b a')  [2,0]
        sage : RauzyDiagram('a b b', 'c c a', reduced = True)
         0 : ('a b b', 'c c a')  [1, 0]
         1 : ('a a b b', 'c c')  [-1, 2]
         2 : ('a a b', 'b c c')  [2, 3]
         3 : ('a a', 'b b c c')  [0, -1]
        

        Each line of the representation of RauzyDiagrams correspond to :
        'internal number' : 'permutation' ['0-neighbour', '1-neighbour']
              

    NOTES :
        flipped permutations are not yet implemented


        REFERENCES :
            Corentin Boissy and Erwan Lanneau, "Dynamics and geometry
            of the Rauzy-Veech induction for quadratic differentials"
            (arxiv:0710.5614)

            Claude Danthony and Arnaldo Nogueira "Measured foliations
            on nonorientable surfaces", Annales scientifiques de
            l'Ecole Normale Superieure, Ser. 4, 23, no. 3 (1990),
            p 469-494

            Arnaldo Nogueira, "Almost all Interval Exchange
            Transformations with Flips are Nonergodic" (Ergod. Th. &
            Dyn. Systems, Vol 5., (1985), 257-271

            Anton Zorich, "Generalized Permutation software"
            (http://perso.univ-rennes1.fr/anton.zorich)

            Anton Zorich, "Explicit Jenkins-Strebel representatives of
            all strata of Abelian and quadratic differentials", Journal
            of Modern Dynamics, 2:1 (2008), 139-185

    AUTHORS :
        - Vincent Delecroix (2008-20-12)
    """
    if not kargs.has_key("reduced") : kargs["reduced"] = False
    if not kargs.has_key("flips") : kargs["flips"] = []

    p = GeneralizedPermutation(args, reduced = kargs["reduced"], flips = kargs["flips"])
    return p.rauzy_diagram()
