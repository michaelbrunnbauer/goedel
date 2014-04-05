#!/usr/bin/python

from functions_proof import *
from prettyprint import prettyprint

for f in config.functions:
    print f.definition_intro()
    print prettyprint(f.definition())
    print
    print
    if f.name=='bitset':
        print """We introduce the notion of code functions to reduce more general forms of
recursion to primitive recursion.

Assume you want to define a primitive recursive relation r(x) like this:
r(0) = 1 <-> ...
r(x) = 1 <-> ... or ( r(a) and r(b) and ... ) where a,b < x
This cannot be done with the primitive recursion scheme where
r(x+1,...) is defined only in terms of r(x,...) - not some r(y,...) (y < x).

This can be solved by defining a primitive recursive h(x) (the code function)
so that r(x) <-> bit x of h(x) is set. h(x) "codes" the information of r(y)
for all values y <= x:
h(0) = 1 <-> ...
h(x+1) = h(x) + f(x+1,h(x))*(2**(x+1))
recursive_r(y,x) = bitset(y,x)
f(x,y) = 1 <-> ... or ( recursive_r(y,a) and recursive_r(y,b) and ... )
where a,b < x

All recursive_r(y,x) used later will be defined now. This way, a recursive
function can even be used before it is defined - if a suitable value of h(x)
is provided as parameter y. Computation of h(x) is not feasible so we will
replace all calls to recursive_r with calls to f(x,None) during computation.
"""
        for f1 in config.functions:
            if type(f1)==recursive_function:
                print 'Definition of recursive_'+f1.name+':'
                print prettyprint(f1.definition1())
                print
                print

