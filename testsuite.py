#!/usr/bin/python

import sys

# not safe! if you get a segmentation fault it's my fault
if sys.getrecursionlimit() < 2500:
    sys.setrecursionlimit(2500)

from functions_proof import *
from goedelize import *

def checkproof(filename):
    f=open(filename,"r")
    s=f.read()
    f.close()

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
    assert isvalidproof(gn(s1)) == 1

def testsuite():
    config.caching=True
    assert goedelstring(0)==''
    s='123'
    assert goedelstring(gn(s))==s

    assert ac(1) == 0
    assert plus(11,5) == 16
    assert mul(11,5) == 55
    assert cond(3,1,2) == 1
    assert cond(0,1,2) == 2
    assert minus(2,2) == 0
    assert minus(11,6) == 5
    assert smaller(1,1) == 0
    assert smaller(0,1) == 1
    assert smaller(1,0) == 0
    assert smaller(2,3) == 1
    assert smaller(3,2) == 0
    assert equal(0,0) == 1
    assert equal(1,0) == 0
    assert equal(0,1) == 0
    assert equal(2,2) == 1
    assert smallereq(1,1) == 1
    assert smallereq(0,1) == 1
    assert smallereq(1,0) == 0
    assert div(11,3) == 3
    assert modulo(11,3) == 2
    assert pow(2,3) == 8
    assert rshift(0,1) == 0  
    assert rshift(8,1) == 0
    assert rshift(255,1) == 0
    assert rshift(256,1) == 1
    assert lshift(1,0) == 1
    assert lshift(1,1) == 256
    assert length(0) == 0
    assert length(2) == 1
    assert length(255) == 1 

    # doing this by hand from now on would break our neck (or stack)
    config.fastfunctions=set(['plus','minus','minusfull','smaller','equal'])

    assert length(256) == 2
    s=gn('ab')
    assert length(s) == 2
    assert item(1,s) == ord('a')
    assert item(2,s) == ord('b')
    assert concat(ord('a'),ord('b')) == s
    assert concat(s,0) == s
    assert concat(0,s) == s

    # from now on, do everything fast that can be done fast
    config.fastfunctions=True

    assert bitset(3,0) == 1
    assert bitset(3,1) == 1
    assert bitset(3,2) == 0

    assert bitslice(0,0,0) == 0
    assert bitslice(0,0,10) == 0
    assert bitslice(1,0,0) == 1
    assert bitslice(1,0,10) == 1
    assert bitslice(423895,0,2) == 7
    assert bitslice(423895,2,8) == 117
    assert bitslice(423895,0,80) == 423895

    assert isnamelc(0) == 0
    assert isnamelc(gn('c')) == 1
    assert isnamelc(gn('C')) == 0
    assert isnamelc(gn('3')) == 0
    assert isnamelc(gn('c3')) == 1
    assert isnamelc(gn('abc')) == 1
    assert isnamelc(gn('aBc')) == 0

    assert isnameuc(0) == 0
    assert isnameuc(gn('C')) == 1
    assert isnameuc(gn('c')) == 0
    assert isnameuc(gn('3')) == 0
    assert isnameuc(gn('C3')) == 1
    assert isnameuc(gn('ABC')) == 1
    assert isnameuc(gn('AbC')) == 0

    assert isterm(0) == 0
    assert isterm(gn('a')) == 1
    assert isterm(gn('f(a)')) == 1
    assert isterm(gn('f()')) == 0
    assert isterm(gn('f(a')) == 0
    assert isterm(gn('a)')) == 0
    assert isterm(gn('a,b')) == 0
    assert isterm(gn('f(a,b)')) == 1
    assert isterm(gn('f(a,b,c)')) == 1
    assert isterm(gn('f(a,b,)')) == 0
    assert isterm(gn('f(a,b,1c)')) == 0
    assert isterm(gn('f(a,b,c)a')) == 0
    assert isterm(gn('f(a,,b,c)')) == 0
    assert isterm(gn('f(a,b,c)(d)')) == 0
    assert isterm(gn('f(a,e(b),g(c))')) == 1

    assert isproposition(0) == 0
    assert isproposition(gn('P(a)')) == 1
    assert isproposition(gn('P(f(a))')) == 1
    assert isproposition(gn('P()')) == 0
    assert isproposition(gn('P(a')) == 0
    assert isproposition(gn('a)')) == 0
    assert isproposition(gn('a,b')) == 0
    assert isproposition(gn('P(a,b)')) == 1
    assert isproposition(gn('P(a,b,c)')) == 1
    assert isproposition(gn('P(a,b,)')) == 0
    assert isproposition(gn('P(a,b,1c)')) == 0
    assert isproposition(gn('P(a,b,c)a')) == 0
    assert isproposition(gn('P(a,,b,c)')) == 0
    assert isproposition(gn('P(a,b,c)(d)')) == 0
    assert isproposition(gn('P(a,e(b),g(c))')) == 1

    assert isequation(0) == 0
    assert isequation(gn('a=b')) == 1
    assert isequation(gn('=b')) == 0
    assert isequation(gn('a=')) == 0
    assert isequation(gn('=')) == 0
    assert isequation(gn('f(a)=b')) == 1
    assert isequation(gn('f(a=b')) == 0
    assert isequation(gn('fa)=b')) == 0
    assert isequation(gn('(a)=b')) == 0
    assert isequation(gn('f(a,g(c))=t(b,g)')) == 1

    assert isformula(0) == 0
    assert isformula(gn('a=b')) == 1
    assert isformula(gn('P(a)')) == 1
    assert isformula(gn('~a=b')) == 1
    assert isformula(gn('!a=b')) == 0
    assert isformula(gn('~a&b')) == 0
    assert isformula(gn('~~a=b')) == 1
    assert isformula(gn('~P(a)')) == 1
    assert isformula(gn('(P(a)&a=b)')) == 1
    assert isformula(gn('P(a)&a=b')) == 0
    assert isformula(gn('!x:P(a)')) == 1
    assert isformula(gn('!x:a=b')) == 1
    assert isformula(gn('!:a=b')) == 0
    assert isformula(gn('!x(P(a)&a=b)')) == 0
    assert isformula(gn('!x:(P(a)&a=b)')) == 1
    assert isformula(gn('!!x:(P(a)&a=b)')) == 0
    assert isformula(gn('~!x:(P(a)&a=b)')) == 1
    assert isformula(gn('(P(x)&(P(y)&P(z)))')) == 1
    assert isconjunction(0) == 0

    assert number(0) == gn('n0')
    assert number(1) == gn('succ(n0)')
    assert number(2) == gn('succ(succ(n0))')

    x=gn('x')
    assert isfreeintermlist(0,x) == 0
    assert isfreeintermlist(0,0) == 0 
    assert isfreeintermlist(gn('x'),x) == 1
    assert isfreeintermlist(gn('xx'),x) == 0
    assert isfreeintermlist(gn('y'),x) == 0
    assert isfreeintermlist(gn('x,y'),x) == 1
    assert isfreeintermlist(gn('y,f(x)'),x) == 1
    assert isfreeintermlist(gn('a,x(b)'),x) == 0

    assert isfreeinterm(0,x) == 0
    assert isfreeinterm(0,1) == 0
    assert isfreeinterm(gn('f(x)'),x) == 1
    assert isfreeinterm(gn('f(xx)'),x) == 0
    assert isfreeinterm(gn('x(y)'),x) == 0
    assert isfreeinterm(gn('f(x,y)'),x) == 1
    assert isfreeinterm(gn('f(y,f(x))'),x) == 1
    assert isfreeinterm(gn('x(a,x(b))'),x) == 0

    assert isfreeinproposition(0,x) == 0
    assert isfreeinproposition(0,0) == 0
    assert isfreeinproposition(gn('F(x)'),x) == 1
    assert isfreeinproposition(gn('F(xx)'),x) == 0
    assert isfreeinproposition(gn('X(y)'),x) == 0
    assert isfreeinproposition(gn('F(x,y)'),x) == 1
    assert isfreeinproposition(gn('F(y,f(x))'),x) == 1
    assert isfreeinproposition(gn('X(a,x(b))'),x) == 0

    assert isfreeinequation(0,x) == 0
    assert isfreeinequation(0,0) == 0
    assert isfreeinequation(gn('f(x)=y'),x) == 1
    assert isfreeinequation(gn('y=f(x)'),x) == 1
    assert isfreeinequation(gn('x(y)=z'),x) == 0
    assert isfreeinequation(gn('f(x,y)=x(g)'),x) == 1
    assert isfreeinequation(gn('x(g)=f(x,y)'),x) == 1
    assert isfreeinequation(gn('f(y,f(x))=z'),x) == 1
    assert isfreeinequation(gn('x(a,x(b))=z'),x) == 0

    assert isfreeinformula(0,x) == 0
    assert isfreeinformula(0,0) == 0 
    assert isfreeinformula(gn('f(x)=y'),x) == 1
    assert isfreeinformula(gn('y=f(x)'),x) == 1
    assert isfreeinformula(gn('x(y)=z'),x) == 0
    assert isfreeinformula(gn('f(x,y)=x(g)'),x) == 1
    assert isfreeinformula(gn('x(g)=f(x,y)'),x) == 1
    assert isfreeinformula(gn('f(y,f(x))=z'),x) == 1
    assert isfreeinformula(gn('x(a,x(b))=z'),x) == 0
    assert isfreeinformula(gn('P(x)'),x) == 1
    assert isfreeinformula(gn('!x:P(x)'),x) == 0
    assert isfreeinformula(gn('!y:P(x)'),x) == 1
    assert isfreeinformula(gn('(P(y)&P(x))'),x) == 1
    f=gn('(!x:(Q(x)&~R(x,y))&~!y:S(y,z))')
    assert isfreeinformula(f,gn('x')) == 0
    assert isfreeinformula(f,gn('y')) == 1   
    assert isfreeinformula(f,gn('z')) == 1
    assert isfreeinformula(f,gn('a')) == 0
    f=gn('(!xx:(Q(xx)&~R(xx,y))&~!y:S(y,z))')
    assert isfreeinformula(f,gn('xx')) == 0
    assert isfreeinformula(f,gn('y')) == 1
    assert isfreeinformula(f,gn('z')) == 1
    assert isfreeinformula(f,gn('x')) == 0

    f=gn('x')
    x=gn('x')
    t=gn('z(a)')
    assert subst_termlist(f,x,t) == gn('z(a)')
    f=gn('b,y')
    assert subst_termlist(f,x,t) == gn('b,y')
    f=gn('y,g(a,x)')
    assert subst_termlist(f,x,t) == gn('y,g(a,z(a))')

    f=gn('P(x)')
    assert subst_proposition(f,x,t) == gn('P(z(a))')
    f=gn('P(b,y)')
    assert subst_proposition(f,x,t) == f

    f=gn('a=b')
    assert subst_equation(f,x,t) == f
    f=gn('x=b')
    assert subst_equation(f,x,t) == gn('z(a)=b')

    f=gn('(!x:(Q(x)&~R(x,y))&~!y:S(y,z))')
    assert subst_formula(f,x,t) == f
    x=gn('y')
    assert subst_formula(f,x,t) == gn('(!x:(Q(x)&~R(x,z(a)))&~!y:S(y,z))')
    x=gn('z')
    assert subst_formula(f,x,t) == gn('(!x:(Q(x)&~R(x,y))&~!y:S(y,z(a)))')

    x=gn('!z:P(x,y,x)')
    y=gn('x')
    z=gn('f(a)')
    assert subst_formula(x,y,z)==gn('!z:P(f(a),y,f(a))')

    s=gn('This is a test')
    assert find_pos(ord(' '),s,0) == 5
    assert find_pos(ord(' '),s,5) == 8
    assert find_pos(ord(' '),s,8) == 10
    assert find_pos(ord(' '),s,10) == 0
    assert find(1,ord('T'),s) == 1
    assert find(0,ord(' '),s) == 0
    assert find(1,ord(' '),s) == 5
    assert find(2,ord(' '),s) == 8
    assert find(3,ord(' '),s) == 10
    assert find(4,ord(' '),s) == 0
    assert find(2,ord('t'),s) == 14
    assert find(3,ord('t'),s) == 0
    assert occur(ord(' '),s) == 3
    assert occur(ord('-'),s) == 0
    s=gn("111;222;333;")
    assert slength(s) == 3
    assert sitem(1,s) == gn('111')
    assert sitem(3,s) == gn('333')
    assert sequence_end(s) == gn('333')
    assert sequence_start(s) == gn('111;222;')
    s=gn('111;')
    assert sequence_end(s) == gn('111')
    assert sequence_start(s) == 0

    assert issequence(0) == 0
    assert issequence(gn(';')) == 0
    f=gn('a=b;')
    assert issequence(f) == 1
    f=gn('a=b')
    assert issequence(f) == 0
    f=gn('a=b;~P(a);!x:P(x);')
    assert issequence(f) == 1
    f=gn('a=b;~P(a);!x:P(x)')
    assert issequence(f) == 0
    f=gn('a=b;~P(a);!x:p(x);')
    assert issequence(f) == 0

    x=gn('P(x);')
    y=gn('P(f(y));')
    assert issubstitution(x,y) == 1
    y=gn('T(y);')
    assert issubstitution(x,y) == 0
    x=gn('!x:P(x);')
    y=gn('!x:P(y);')
    assert issubstitution(x,y) == 0

    assert isvalidproof(0) == 0
    f=gn('P(x);P(x)')
    assert isvalidproof(f) == 0
    f=gn('P(x);P(x);\n')
    assert isvalidproof(f) == 1
    f=gn('P(x);T(x);\n')
    assert isvalidproof(f) == 0

    checkproof('proofs/1')
    checkproof('proofs/2')
    checkproof('proofs/3')
    checkproof('proofs/4')
    checkproof('proofs/5')
    checkproof('proofs/6')
    checkproof('proofs/7')
    checkproof('proofs/8')

testsuite()
print "All tests OK!"
