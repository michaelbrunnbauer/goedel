#!/usr/bin/python

from functions_proof import *
from prettyprint import prettyprint

print basic_definitions()
print

for f in config.functions:
    print f.definition_intro()
    print prettyprint(f.definition())
    print
    print
    if f.name=='bitslice':
        print """Assume you want to define a primitive recursive relation r(x) like this:
r(0) = expression returning 0 or 1
r(x) = expression returning 0 or 1 using r(a), r(b) where a,b < x

This cannot be done with the primitive recursion scheme where
r(x+1,...) is defined only in terms of r(x,...) - not some r(y,...) (y < x).

This can be solved by defining a primitive recursive h(x)
so that r(x) <-> bit x of h(x) is set. h(x) "codes" the information of r(y)
for all values y <= x:
h(0) = expression returning r(0) - which is 0 or 1
h(x+1) = h(x) + f(x+1,h(x))*(2**(x+1))
recursive_r(y,x) = bitset(y,x)
f(x,y) = expression returning r(x) using recursive_r(y,a) where a < x
"""

        print """Assume you want to define a primitive recursive function r(x) like this:
r(0) = expression
r(x) = expression using r(a), r(b) where a,b < x

This is like the recursive relation r(x) mentioned above, but returns
arbitrary values instead of 0 or 1. We can reduce this to primitice recursive
functions by defining a function h that codes arbitrary values using several
bits at once instead of a single bit. This is done by calculating the maximum
length in bits of the result for any given input.

bitstart(0) = 0
bitstart(x+1) = bitstart(x) + expression calculating length of r(x) in bits
h(0) = expression calculating value for r(0)
h(x+1) = h(x) + f(x+1,h(x))*(2**bitstart(x+1))
recursive_r(y,x) = bitslice(y,bitstart(x),bitstart(x+1)-1)
f(x,y) = expression calculating the value for r(x) using recursive_r(y,a)
         where a < x
r(x) = recursive_r(h(x),x)
"""
