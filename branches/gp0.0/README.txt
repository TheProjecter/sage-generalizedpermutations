Those files define general tools for usage and manipulation of
(generalized) permutations under SAGE. Those mathematical objects 
are encountered in the theory of translations surfaces (and also 
word combinatorics) and more generally in the theory measured 
foliations of surfaces.

To integrate this beta version to SAGE follow this steps :

1. Go to the main branch
    sage -b main

2. Create a clone of this main branch 
   sage -clone generalizedpermutations

(the name generalizedpermutations could be anything else. The
creation of this clone allow different 'version' of SAGE. If an
error occur with the new configuration, just do 'sage -b main'
following by 'sage -br')

3. Go to this new branch
   sage -b generalizedpermutations

4. Create a new sage directory for the generalizedpermutations
   mkdir $SAGE_ROOT/devel/sage/sage/generalizedpermutations

4. Copy all the files in this directory

5. Modify the $SAGE_ROOT/devel/sage/setup.py file
   adding 'generalizedpermutations' in the package list

6. Modify the $SAGE_ROOT/devel/sage/sage/all.py file adding the line
   from generalizedpermutations.all import *

7. Try this new version of SAGE with
   sage -br

(To get information on the package just try 'GeneralizedPermutation?'
in SAGE command line)

It's distribution is under GPLv2+
Copyright Vincent Delecroix 2008
