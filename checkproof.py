#!/usr/bin/python

import sys

# not safe! if you get a segmentation fault it's my fault
if sys.getrecursionlimit() < 2500:
    sys.setrecursionlimit(2500)

from functions_proof import *
from goedelize import *

config.caching=True
config.fastfunctions=True
config.optimize=True

def checkproof(s):
    s=s.replace(' ','')
    s=s.strip()
    s=s.split('\n')
    s1=[]
    for line in s:
        if not line.startswith('#'):
            s1.append(line)
    s=s1
    s1='\n'.join(s)
    s1+='\n'
    if isvalidproof(gn(s1)) == 1:
        print "correct!"
        return True
    for x in range(1,len(s)+1):
        s1='\n'.join(s[:x])
        s1+='\n'
        if isvalidproof(gn(s1)) == 0:
            print "not correct at last line:"
            print s1
            return False

if not len(sys.argv):
    print "usage: checkproof.py file1, file2, ..."
    sys.exit(1)

for filename in sys.argv[1:]:
    print "checking",filename
    f=open(filename,"r")
    s=f.read()
    f.close()
    if not checkproof(s):
        sys.exit(1)
