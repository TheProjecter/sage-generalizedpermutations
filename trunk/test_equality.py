import constructor as gp

##################
# EQUALITY TESTING

a_list = ((("a b","b a"),[]), (("a b","b a"),['a']),(("a b","b a"),['b']),(("a b","b a"),['a','b']),
          (("a b c","a b c"),[]),
          (("a b c","c b a"),[]),
          (("a b c","c a b"),[]),
          (("a b c","b c a"),[]),
          (("a a","b b"),[]),
          (("a b b","a c c"),[]),
          (("a b b","a c c"),[]))

b_list = ((("g h","h g"),[]),(("g h","h g"),['g']),(("g h","h g"),['h']),(("g h","h g"),['g','h']),
          (("g h i","g h i"),[]),
          (("g h i","i h g"),[]),
          (("g h i","i g h"),[]),
          (("g h i","h i g"),[]),
          (("g g","h h"),[]),
          (("g h h","g i i"),[]),
          (("g h h","g i i"),[]))

c_list = ((("a b","a b"),[]),(("a b","b a"),['b']),(("a b","a b"),['b']),(("a b","a b"),['a']),
          (("a b c","a c b"),[]),
          (("a b c","c a b"),[]),
          (("a b c","c b a"),[]),
          (("a c b","b c a"),[]),
          (("a b a","c c b"),[]),
          (("a b b","c a c"),[]),
          (("a b a","b c c"),[]))

for (a,a_flips),(b,b_flips),(c,c_flips) in zip(a_list, b_list, c_list) :
    pr = gp.GeneralizedPermutation(a, reduced=True, flips=a_flips)
    qr = gp.GeneralizedPermutation(b, reduced=True, flips=b_flips)
    rr = gp.GeneralizedPermutation(c, reduced=True, flips=c_flips)

    pl = gp.GeneralizedPermutation(a, reduced=False, flips=a_flips)
    ql = gp.GeneralizedPermutation(b, reduced=False, flips=b_flips)


    if not (pr == pr) :
        print "REDUCED EQUALITY ERROR WITH THE SAME PERMUTATION"
        print pr

    if (pr != pr) :
        print "REDUCED NON EQUALITY ERROR WITH THE SAME PERMUTATION"
        
    if not (pr == qr) :
        print "ab REDUCED EQUALITY ERROR"
        print pr
        print qr
    if pr != qr :
        print "ab REDUCED NON EQUALITY ERROR"
        print pr
        print qr
    if pr == rr :
        print "ac REDUCED EQUALITY ERROR"
        print p
        print r
    if not (pr != rr) :
        print "ac REDUCED NON EQUALITY ERROR"
        print pr
        print rr

    # labeled testing equality and difference
    if not (pl == pl) :
        print "LABELED EQUALITY ERROR WITH SAME PERMUTATION"
        print pl

    if (pl != pl) :
        print "LABELED NON EQUALITY ERROR WITH SAME PERMUTATION"
        print PL

    if (pl == ql) :
        print "LABELED EQUALITY ERROR"
        print pl
        print ql

    if not (pl != ql) :
        print "LABELED NON EQUALITY ERROR"
        print pl
        print ql



