from functions import *
from functions_calculus import *

config.globals=globals()

slice_safe=basic_function(config,
 name='slice_safe',
 desc='like slice(a,b,x), but returns slice(1,b,x) if a = 0',
 define='lambda a,b,x: left(minusfull(sc(b),ifzero(a,n1)),right(ifzero(a,n1),x))'
)

isgeneralization2_help=argmin_function(config,
 name='isgeneralization2_help',
 desc='returns position of : if x has the form ! isnamelc : ... and isnamelc != y and isnamelc != n0',
 max='lambda x,y: length(x)',
 relation='lambda pos,x,y: and_f5(equal(item(n1,x),n33),equal(item(pos,x),n58),isnamelc(slice(n2,acfull(pos),x)),not_f(equal(slice(n2,acfull(pos),x),concat(n110,n48))),not_f(equal(slice(n2,acfull(pos),x),y)))'
)

isgeneralizationlistnotusing=recursive_relation(config,
 name='isgeneralizationlistnotusing',
 desc='s is a list of generalizations not using variable x or n0',
 zero='lambda x: n1',
 relation='lambda s,x,y: and_f(notzero(isgeneralization2_help(s,x)),recursive_isgeneralizationlistnotusing(y,slice(sc(ifzero(isgeneralization2_help(s,x),length(s))),length(s),s),x))'
)

isinductionpremise=basic_function(config,
 name='isinductionpremise',
 desc='f has the form (A & !x~(B&~C)) where n0 is free in A, B = subst_formula(A,n0,x) = f1, C = subst_formula(A,n0,sc(x))',
 define='lambda f,x,f1: and_f(and_f10(isconjunction(f),isnamelc(x),isfreeinformula(conjunction_formula1(f),concat(n110,n48)),isgeneralization(conjunction_formula2(f)),equal(generalization_namelc(conjunction_formula2(f)),x),isnegation(generalization_formula(conjunction_formula2(f))),isconjunction(negation_formula(generalization_formula(conjunction_formula2(f)))),equal(subst_formula(conjunction_formula1(f),concat(n110,n48),x),conjunction_formula1(negation_formula(generalization_formula(conjunction_formula2(f))))),isnegation(conjunction_formula2(negation_formula(generalization_formula(conjunction_formula2(f))))),equal(subst_formula(conjunction_formula1(f),concat(n110,n48),getsuccx(x)),negation_formula(conjunction_formula2(negation_formula(generalization_formula(conjunction_formula2(f))))))),equal(subst_formula(conjunction_formula1(f),concat(n110,n48),x),f1))'
)

induction_leftformula=basic_function(config,
 name='induction_leftformula',
 desc='get ( formula ) from sequence --- ( formula ) ; ... (--- does not contain "(")',
 define='lambda s: slice_safe(find_pos(n40,sitem(n1,s),n0),length(sitem(n1,s)),sitem(n1,s))'
)

induction_leftgeneralizations=basic_function(config,
 name='induction_leftgeneralizations',
 desc='get --- from sequence --- ( formula ) ; ... (--- does not contain "(")',
 define='lambda s: slice(n1,acfull(find_pos(n40,sitem(n1,s),n0)),sitem(n1,s))'
)

induction_rightformula=basic_function(config,
 name='induction_rightformula',
 desc='get string from sequence --- ( formula ) ; --- string (--- does not contain "(")',
 define='lambda s: slice_safe(sc(length(induction_leftgeneralizations(s))),length(sequence_end(s)),sequence_end(s))'
)

induction_rightgeneralizations=basic_function(config,
 name='induction_rightgeneralizations',
 desc='get right --- from sequence --- ( formula ) ; --- string (--- does not contain "(")',
 define='lambda s: slice(n1,length(induction_leftgeneralizations(s)),sequence_end(s))'
)

isinduction=basic_function(config,
 name='isinduction',
 desc='s is a sequence of the form --- (A&!x:~(B&~C)) ; --- !x:B where n0 is free in A, B = subst_formula(A,n0,x), C = subst_formula(A,n0,sc(x)), --- is empty or a list of generalizations not containing variable x or n0',
 define='lambda s: and_f7(issequence(s),equal(slength(s),n2),isgeneralization(induction_rightformula(s)),isproposition(generalization_formula(induction_rightformula(s))),equal(induction_rightgeneralizations(s),induction_leftgeneralizations(s)),isgeneralizationlistnotusing(induction_rightgeneralizations(s),generalization_namelc(induction_rightformula(s))),isinductionpremise(induction_leftformula(s),generalization_namelc(induction_rightformula(s)),generalization_formula(induction_rightformula(s))))'
)

from base256 import *
from goedelize import *
oldsetup=(config.caching,config.fastfunctions,config.optimize)
config.caching=True
config.fastfunctions=True
config.optimize=True

axiom1=gn('!x:~n0=sc(x);')
assert issequence(axiom1)
axiom1=base256(axiom1)

axiom2=gn('!x:!y:~(sc(x)=sc(y)&~x=y);')
assert issequence(axiom2)
axiom2=base256(axiom2)

axiom3=gn('!x:ad(x,n0)=x;')
assert issequence(axiom3)
axiom3=base256(axiom3)

axiom4=gn('!x:!y:ad(x,sc(y))=sc(ad(x,y));')
assert issequence(axiom4)
axiom4=base256(axiom4)

axiom5=gn('!x:mu(x,n0)=n0;')
assert issequence(axiom5)
axiom5=base256(axiom5)

axiom6=gn('!x:!y:mu(x,sc(y))=ad(mu(x,y),x);')
assert issequence(axiom6)
axiom6=base256(axiom6)

config.caching=oldsetup[0]
config.fastfunctions=oldsetup[1]
config.optimize=oldsetup[2]

isbasicpeanoaxiom=basic_function(config,
 name='isbasicpeanoaxiom',
 desc='s is a sequence of one of the six peano axioms',
 define='lambda s: or_f6(equal(s,'+axiom1+'),equal(s,'+axiom2+'),equal(s,'+axiom3+'),equal(s,'+axiom4+'),equal(s,'+axiom5+'),equal(s,'+axiom6+'))'
)
