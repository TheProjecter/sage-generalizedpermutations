import constructor as gp


# ABELIAN PERMUTATION
a_list = (("a b","b a"),
          ("a b c","c b a"),
          ("a b c","b c a"),
          ("a b c","c a b"))

a_r_list = ((("a b","b a"),("a b","b a")),
            (("a b c","c a b"),("a c b","c b a")),
            (("a b c","b c a"),("a c b","b c a")),
            (("a b c","c b a"),("a b c","c a b")))

for a,(a0,a1) in zip(a_list, a_r_list) :
    p = gp.GeneralizedPermutation(a, reduced=True)

    if not p.is_rauzy_movable() :
        print "ERROR RAUZY MOVABILITY (ABELIAN)"
        print p
        
    p.rauzy_move(0)
    p0 = gp.GeneralizedPermutation(a0, reduced=True)
    
    if p != p0 :
        print "R0 ERROR"
        print p
        print "\n",p0


    p = gp.GeneralizedPermutation(a, reduced=True)
    p.rauzy_move(1)
    p1 = gp.GeneralizedPermutation(a1, reduced=True)

    if p != p1 :
        print "R1 ERROR"
        print p
        print "\n",p1
            

# QUADRATIC PERMUTATION
a_list = {}
a_r_list = {}

# only 0-Rauzy movable
a_list_0 = (("a a","b b c c"),
            ("1 2 2","3 1 3 4 4"),
            ("1 1","2 2 3 4 3 4")
            )
a_r_list_0 = (("c a a","b b c"),
              ("1 4 2 2","3 1 3 4"),
              ("4 1 1","2 2 3 4 3")
              )

# only 1-Rauzy movable
a_list_1 = (("a a b b","c c"),
            ("1 1 2 3 3","4 2 4"),
                
                )
a_r_list_1 = (("a a b","b c c"),
              ("1 1 2 3","3 4 2 4")
                  )

# Rauzy movable on 0 and 1
a_list_01 = (("a b b","c c a"),("a a b","b c c"),
               ("1 1 2","3 3 4 2 4")
               )

a_r_list_01 = ((("a a b b","c c"),("a b b","c c a")),(("a a b","b c c"),("a a","b b c c")),
                 (("1 1 2","3 3 4 2 4"),("1 1","3 3 2 4 2 4"))
                 )

reduction = ((True,"REDUCED : "),(False,"LABELED : ")) 

# ONLY 0
for a,a0 in zip(a_list_0, a_r_list_0) :
    for r, l in reduction :
        p = gp.GeneralizedPermutation(a, reduced=r)
        if p.is_rauzy_movable(1) or (not p.is_rauzy_movable(0)) :
            print l + "ERROR RAUZY MOVABILITY (QUADRATIC only 0)"
            print a
        
        p.rauzy_move(0)
        p0 = gp.GeneralizedPermutation(a0, reduced=r)
        if p != p0 :
            print l + "ERROR 0-RAUZY MOVE (QUADRATIC only 0)"
            print a, " -> ", a0
            print p

    
# ONLY 1
for a,a1 in zip(a_list_1, a_r_list_1) :
    for r,l in reduction :
        p = gp.GeneralizedPermutation(a, reduced=r)
        if p.is_rauzy_movable(0) or (not p.is_rauzy_movable(1)) :
            print l + "ERROR RAUZY MOVABILITY (QUADRATIC only 1)"
            print a

        p.rauzy_move(1)
        p1 = gp.GeneralizedPermutation(a1, reduced=r)
        if p != p1 :
            print l + "ERROR 1-RAUZY MOVE (QUADRATIC only 1)"
            print a, " -> ", a1
            print p

for a,(a0,a1) in zip(a_list_01, a_r_list_01) :
    for r,l in reduction :
        p = gp.GeneralizedPermutation(a, reduced=r)
        if not (p.is_rauzy_movable(0) and p.is_rauzy_movable(1)) :
            print l + "ERROR RAUZY MOVABILITY (QUADRATIC 0 and 1)"
            print a

        p.rauzy_move(0)
        p0 = gp.GeneralizedPermutation(a0, reduced=r)
        if p != p0 :
            print l + "ERROR 0-RAUZY MOVE (QUADRATIC 0 and 1)"
            print a, " -> ",a0
            print p
            
        p = gp.GeneralizedPermutation(a, reduced=r)
        p.rauzy_move(1)
        p1 = gp.GeneralizedPermutation(a1, reduced=r)
        
        if p != p1 :
            print l + "ERROR 1-RAUZY MOVE (QUADRATIC 0 and 1)"
            print a, " -> ", a1
            print p
    
