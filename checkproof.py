#!/usr/bin/python

import sys
from functions_proof import *
from goedelize import *

config.caching=True
config.fastfunctions=True

def checkproof(s):
    s=s.replace(' ','')
    if isvalidproof(gn(s)) == 1:
        return
    s=s.strip()
    s=s.split('\n')
    for x in range(1,len(s)+1):
        s1='\n'.join(s[:x])
        s1+='\n'
        assert isvalidproof(gn(s1)) == 1,'\n'+s1

if not len(sys.argv):
    print "usage: checkproof.py file1, file2, ..."
    sys.exit(1)

for filename in sys.argv[1:]:
    print "checking",filename
    f=open(filename,"r")
    s=f.read()
    f.close()
    checkproof(s)

