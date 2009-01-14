r"""
(Flipped) Generalized (Reduced or Labeled) Permutation software


   This library is designed to define and use different types of
   permutations and generalized permutations which appears in interval
   exchange transformations or linear involutions (with or without
   flips). The module also provide works with Rauzy Diagram.



AUTHORS: 
    -- Vincent Delecroix (2008-12-20): initial version


   To create all types of permutation there is a general class factory
   whose name is GeneralizedPermutation :

   For labeled permutation :
   Creation of labeled abelian and quadratic permutation :
       sage : p1 =  GeneralizedPermutation('a b c', 'c b a')
       a b c
       c b a
       sage : p2 = GeneralizedPermutation('a a b', 'b c c')
       a a b
       b c c
       
   Creation of reduced abelian and quadratic permutation :
       sage : p1 = GeneralizedPermutation('a b c', 'c b a', reduced=True)
       a b c
       c b a
       sage : p2 = GeneralizedPermutation('a b b', 'c c a', reduced=True)
       a b b
       c c a

   For flips you just have to precise the set of flipped intervals :
       sage : p1 = GeneralizedPermutation('a b c', 'c b a', flips=['a','c'])
       -a b -c
       -c b -a
       sage : p2 = GeneralizedPermutation('a a b', 'b c c', flips=['a'], reduced=True)
       -a -a b
       b c c


   Remark :
     - flips are not yet implemented
   

   For Rauzy diagrams there is two methods. The first one is to use the class
   factory :
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


#from sage.all import *

import labeled
import reduced

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
    Class factory for Generalized Permutation objects

    INPUT :
        arguments must be in one of the following forms :
          - two strings (names of intervals)
          - a list of two strings (idem)
          - two lists (names of intervals)
          - a list of two lists (idem)
          - one string of the form (names of intervals in 0) \n (names of intervals in 1)

       Special arguments are specified with the argument=value syntax :
          - to specify flips : flips = list_of_letters
          - to specify reduction : reduced = True (False is the defaut)

    OUTPUT :
       a generalized permutation (eight possible types)

    EXAMPLES :
       sage : p = GeneralizedPermutation('a b c d','d c b a')


    NOTES


    REFERENCES :


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
    if not kargs.has_key("reduced") :
        reduction = False
    elif type(kargs["reduced"]) != bool :
        raise TypeError("reduced must be of type boolean")
    else :
        if kargs["reduced"] == True : reduction = True
        else : reduction = False

    if not kargs.has_key("flips") :
        flips = []
    elif type(kargs["flips"]) != list :
        raise TypeError("flips must be a list")
    else :
        flips = kargs["flips"]
        for j in flips :
            if type(j) != str : raise TypeError("flips must be a list of strings")

      
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
        if flips == [] :
            if reduction == True :
                return reduced.AbelianPermutation(a)
            else :
                return labeled.AbelianPermutation(a)
        else :
            if reduction == True :
                print "flipped reduced abelian"
                # return reduced.FlippedAbelianPermutation(a,flips)
            else :
                print "flipped labeled abelian"
                # return labeled.FlippedAbelianPermutation(a,flips)
            return None
    else :
        if flips == [] :
            if reduction == True :
                return reduced.QuadraticPermutation(a)
            else :
                return labeled.QuadraticPermutation(a)
        else :
            if reduction == True :
                print "flipped reduced quadratic"
                # return reduced.FlippedQuadraticPermutation(a,flips)
            else :
                print "flipped labeled quadratic"
                # return labeled.FlippedQuadraticPermutation(a,flips)



def RauzyDiagram(*args, **kargs) :
    r"""
    Class factory for Rauzy Diagram


    """

    if not kargs.has_key("reduced") : kargs["reduced"] = False
    if not kargs.has_key("flips") : kargs["flips"] = []

    p = GeneralizedPermutation(args, reduced = kargs["reduced"], flips = kargs["flips"])
    return p.rauzy_diagram()
