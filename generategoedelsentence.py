#!/usr/bin/python

import sys
import parseterm
from functions_proof import *
from goedelize import *
from base256 import *
from replace256 import replace256

config.caching=True
config.fastfunctions=True
config.optimize=True

def save(s,filename):
    f=open(filename,'w')
    f.write(s)
    f.close()

# generate p

# this is our variable generator
ind=parseterm.vindex()

# we need two variables
vx=ind.new()
vk=ind.new()

# the Goedel-number of variable vk
gvk=gn(vk)
assert gvk <= 256

# p = for all vx: not term=1
term='isvalidprooffor('+vx+',subst_formula('+vk+',n'+str(gvk)+',number('+vk+')))'

# now resolve all definitions in term to formulae

parsedterm=parseterm.parseterm(term)
formulae=[]
freevariables=[]
# this fills formulae+freevariables and returns a term/variable for the value
# of term
term1=ac.getterm1(parsedterm,formulae,ind,freevariables)
# the value of term should be 0
formulae.append(term1+'=n1')
# now build the conjunction of all generated formulae, bind all free
# variables to the existential quantifier and generalize over vx
p='!'+vx+':~'+ac.composeformula(formulae,freevariables)

# we have p, save it
save(p,'p_stage1.txt')

p=None

# replace n1 - n256 in p with n0 and sc()
infile=open('p_stage1.txt','r')
outfile=open('p_stage2.txt','w')
replace256(infile,outfile)
infile.close()
outfile.close()

# p is 19GB big, so we stop here
sys.exit(0)

# this is how we would go on 

f=open('p_stage2.txt','r')
p=f.read()
f.close()

# goedelize p
p=gn_chunked(p)

# generate [p] as term using n0-n256, ad(), mu() and pow()
# size factor > 38
ind=parseterm.vindex()
formulae=[]
freevariables=[]
vp=base256_formula(p,ind,formulae,freevariables)

# generate the goedel sentence
# size factor 1

vx=ind.new()
# the goedel sentence is for all vx: not term=1
term='isvalidprooffor('+vx+',subst_formula('+vp+',n'+str(gvk)+',number('+vp+')))'
parsedterm=parseterm.parseterm(term)
term1=ac.getterm1(parsedterm,formulae,ind,freevariables)
formulae.append(term1+'=n1')
g='!'+vx+':~'+ac.composeformula(formulae,freevariables)

save(g,'g_stage1.txt')

# replace n1 - n256 with n0 and sc()
# size factor 1
infile=open('g_stage1.txt','r')
outfile=open('g_stage2.txt','w')
replace256(infile,outfile)
infile.close()
outfile.close()
