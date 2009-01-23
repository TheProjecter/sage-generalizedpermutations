from generalized_permutation import GeneralizedPermutation

# reducible list
r_list_a = (("a b c", "b a c"),
            ("a b c", "a c b"),

            ("a a","b b"),
            
            ("a a","b c c b"),
            ("b c c b","a a"),          

            ("a a", "b c b c"),
            ("b c b c", "a a"),

            ("a b a c", "b d c d"),
            ("b d c d", "a b a c"),
            ("c a b a", "d c d b"),
            ("d c d b", "c a b a"),

            ("a b c a", "b d d c"),
            ("b d d c", "a b c a"),
            ("a c b a", "c d d b"),
            ("c d d b", "a c b a"),

            
            ("a b a b","c d d c"),

        # one empty and it is on the left !
            ("b a b c", "d e a c e d")
            )

# irreducible list
irr_list_a = (("a a b","b c c"),
              ("a a b b","c c"),
              ("a a","b b c c"),
              ("a b a c","b c d d"),
              ("a b a b","c c d d")
              )

#################################
#initialization
rp_list = []
for a in r_list_a :
    rp_list.append(GeneralizedPermutation(a[0],a[1],reduced=True))

irrp_list = []
for a in irr_list_a :
    irrp_list.append(GeneralizedPermutation(a[0],a[1],reduced=True))

#################################
#tests
for p in rp_list :
    test, d = p.is_reducible(return_decomposition=True)
    if test == False :
        print "REDUCIBILITY ERROR : "
        print p
    else :
        print p
        print d[0],d[1]
        print d[2],d[3]
    print "\n"

for p in irrp_list :
    if p.is_reducible() == True :
        print "IRREDUCIBILITY ERROR : "
        print p
        print "\n"
