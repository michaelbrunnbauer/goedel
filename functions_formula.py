from functions import *
from functions_string import *

config.globals=globals()

# isnamelc:
#  isalphalc
#  isnamelc isalnumlc
isnamelc=recursive_function(config,
 name='isnamelc',
 desc='lower case name [0-9,a-z,_] starting with a-z',
 zero='lambda: 0',
 relation='lambda x,y: OR(isalphalc(x),AND(isalnumlc(item(length(x),x)),recursive_isnamelc(y,slice(1,ac(length(x)),x))))'
)

# isnameuc:
#  isalphauc
#  isnameuc isalnumuc
isnameuc=recursive_function(config,
 name='isnameuc',
 desc='upper case name [0-9,A-Z,_] starting with A-Z',
 zero='lambda: 0',
 relation='lambda x,y: OR(isalphauc(x),AND(isalnumuc(item(length(x),x)),recursive_isnameuc(y,slice(1,ac(length(x)),x))))'
)

# istermlist:
#  isterm
#  istermlist , isterm

# needs termcode,termlistcode
istermlist1=argmin_function(config,
 name='istermlist1',
 desc='returns position of , if x has the form istermlist , isterm',
 max='lambda x,termcode,termlistcode: length(x)',
 relation='lambda pos,x,termcode,termlistcode: AND3(equal(item(pos,x),44),recursive_istermlist_help(termlistcode,slice(1,acfull(pos),x),termcode),recursive_isterm(termcode,slice(succ(pos),length(x),x)))'
)

# needs termcode
istermlist_help=recursive_function(config,
 name='istermlist_help',
 desc='x is a comma separated list of terms',
 zero='lambda termcode: 0',
 relation='lambda x,termcode,y: OR(recursive_isterm(termcode,x),notzero(istermlist1(x,termcode,y)))'
)

# isterm:
#  isnamelc
#  isnamelc ( istermlist )

# needs termcode
isterm1=argmin_function(config,
 name='isterm1',
 desc='returns position of ( if x has the form isnamelc ( istermlist )',
 max='lambda x,termcode: length(x)',
 relation='lambda pos,x,termcode: AND4(equal(item(length(x),x),41),equal(item(pos,x),40),isnamelc(slice(1,acfull(pos),x)),istermlist_help(slice(succ(pos),acfull(length(x)),x),termcode))'
)

isterm=recursive_function(config,
 name='isterm',
 desc='x is a term',
 zero='lambda: 0',
 relation='lambda x,y: OR(isnamelc(x),notzero(isterm1(x,y)))'
)

istermlist2=argmin_function(config,
 name='istermlist2',
 desc='returns position of , if x has the form istermlist , isterm (using the now defined isterm)',
 max='lambda x,termlistcode: length(x)',
 relation='lambda pos,x,termlistcode: AND3(equal(item(pos,x),44),recursive_istermlist(termlistcode,slice(1,acfull(pos),x)),isterm(slice(succ(pos),length(x),x)))'
)

istermlist=recursive_function(config,
 name='istermlist',
 desc='x is a comma separated list of terms (using the now defined isterm)',
 zero='lambda: 0',
 relation='lambda x,y: OR(isterm(x),notzero(istermlist2(x,y)))'
)

termlistpos=argmin_function(config,
 name='termlistpos',
 desc='returns position of ( if x has the form isnamelc ( istermlist )',
 max='lambda x: length(x)',
 relation='lambda pos,x: AND4(equal(item(length(x),x),41),equal(item(pos,x),40),isnamelc(slice(1,acfull(pos),x)),istermlist(slice(succ(pos),acfull(length(x)),x)))'
)

term_namelc=basic_function(config,
 name='term_namelc',
 desc='returns namelc if x has the form namelc ( termlist )',
 define='lambda x: cond(notzero(termlistpos(x)),slice(1,acfull(termlistpos(x)),x),0)'
)

term_termlist=basic_function(config,
 name='term_termlist',
 desc='returns termlist if x has the form namelc ( termlist )',
 define='lambda x: cond(notzero(termlistpos(x)),slice(succ(termlistpos(x)),acfull(length(x)),x),0)'
)

lasttermpos=argmin_function(config,
 name='lasttermpos',
 desc='returns position of , if x has the form termlist , term',
 max='lambda x: length(x)',
 relation='lambda pos,x: AND3(equal(item(pos,x),44),istermlist(slice(1,acfull(pos),x)),isterm(slice(succ(pos),length(x),x)))'
)

termlist_start=basic_function(config,
 name='termlist_start',
 desc='returns termlist if x has the form termlist, term',
 define='lambda x: cond(notzero(lasttermpos(x)),slice(1,acfull(lasttermpos(x)),x),0)'
)

termlist_end=basic_function(config,
 name='termlist_end',
 desc='returns term if x has the form termlist, term',
 define='lambda x: cond(notzero(lasttermpos(x)),slice(plus(2,acfull(lasttermpos(x))),length(x),x),0)'
)

# isproposition:
#  isnameuc ( termlist )
isproposition1=argmin_function(config,
 name='isproposition1',
 desc='returns position of ( if x has the form isnameuc ( termlist )',
 max='lambda x: length(x)',
 relation='lambda pos,x: AND4(equal(item(length(x),x),41),equal(item(pos,x),40),isnameuc(slice(1,acfull(pos),x)),istermlist(slice(succ(pos),acfull(length(x)),x)))'
)

isproposition=basic_function(config,
 name='isproposition',
 desc='x is a proposition',
 define='lambda x: notzero(isproposition1(x))'
)

proposition_nameuc=basic_function(config,
 name='proposition_nameuc',
 desc='returns nameuc if x has the form nameuc ( termlist )',
 define='lambda x: cond(isproposition(x),slice(1,acfull(isproposition1(x)),x),0)'
)

proposition_termlist=basic_function(config,
 name='proposition_termlist',
 desc='returns termlist if x has the form nameuc ( termlist )',
 define='lambda x: cond(isproposition(x),slice(succ(isproposition1(x)),acfull(length(x)),x),0)'
)

# isequation:
#  term = term
isequation1=argmin_function(config,
 name='isequation1',
 desc='returns position of = if x has the form term = term',
 max='lambda x: length(x)',
 relation='lambda pos,x: AND3(equal(item(pos,x),61),isterm(slice(1,acfull(pos),x)),isterm(slice(succ(pos),length(x),x)))'
)

isequation=basic_function(config,
 name='isequation',
 desc='x is an equation',
 define='lambda x: notzero(isequation1(x))'
)

equation_term1=basic_function(config,
 name='equation_term1',
 desc='returns term1 if x has the form term1 = term2',
 define='lambda x: cond(isequation(x),slice(1,acfull(isequation1(x)),x),0)'
)

equation_term2=basic_function(config,
 name='equation_term2',
 desc='returns term2 if x has the form term1 = term2',
 define='lambda x: cond(isequation(x),slice(succ(isequation1(x)),length(x),x),0)'
)

# needs formulacode
isnegation_help=basic_function(config,
 name='isnegation_help',
 desc='x has the form ~ formula (is a negation)',
 define='lambda x,formulacode: AND(equal(item(1,x),126),recursive_isformula(formulacode,slice(2,length(x),x)))'
)

# needs formulacode
# we need slice(2+x to avoid endless recursion in actual computation
isconjunction1_help=argmin_function(config,
 name='isconjunction1_help',
 desc='returns position of & if x has the form ( formula & formula )',
 max='lambda x,formulacode: length(x)',
 relation='lambda pos,x,formulacode: AND5(equal(item(1,x),40),equal(item(length(x),x),41),equal(item(pos,x),38),recursive_isformula(formulacode,slice(2,acfull(pos),x)),recursive_isformula(formulacode,slice(plus(2,acfull(pos)),acfull(length(x)),x)))'
)

# needs formulacode
isconjunction_help=basic_function(config,
 name='isconjunction_help',
 desc='x is a conjunction',
 define='lambda x,formulacode: notzero(isconjunction1_help(x,formulacode))'
)

# needs formulacode
# we need slice(2+x to avoid endless recursion in actual computation
isgeneralization1_help=argmin_function(config,
 name='isgeneralization1_help',
 desc='returns position of : if x has the form ! isnamelc : formula',
 max='lambda x,formulacode: length(x)',
 relation='lambda pos,x,formulacode: AND4(equal(item(1,x),33),equal(item(pos,x),58),isnamelc(slice(2,acfull(pos),x)),recursive_isformula(formulacode,slice(plus(2,acfull(pos)),length(x),x)))'
)

# needs formulacode
isgeneralization_help=basic_function(config,
 name='isgeneralization_help',
 desc='x is a generalization',
 define='lambda x,formulacode: notzero(isgeneralization1_help(x,formulacode))'
)

isformula=recursive_function(config,
 name='isformula',
 desc='x is a formula (proposition|equation|negation|conjunction|generalization)',
 zero='lambda: 0',
 relation='lambda x,y: OR5(isproposition(x),isequation(x),isnegation_help(x,y),isconjunction_help(x,y),isgeneralization_help(x,y))'
)

# redefinition of formula functions using isformula

isnegation=basic_function(config,
 name='isnegation',
 desc='x has the form ~ formula (is a negation)',
 define='lambda x: AND(equal(item(1,x),126),isformula(slice(2,length(x),x)))'
)

# we need slice(2+x to avoid endless recursion in actual computation
isconjunction1=argmin_function(config,
 name='isconjunction1',
 desc='returns position of & if x has the form ( formula & formula )',
 max='lambda x: length(x)',
 relation='lambda pos,x: AND5(equal(item(1,x),40),equal(item(length(x),x),41),equal(item(pos,x),38),isformula(slice(2,acfull(pos),x)),isformula(slice(plus(2,acfull(pos)),acfull(length(x)),x)))'
)

isconjunction=basic_function(config,
 name='isconjunction',
 desc='x is a conjunction',
 define='lambda x: notzero(isconjunction1(x))'
)

# we need slice(2+x to avoid endless recursion in actual computation
isgeneralization1=argmin_function(config,
 name='isgeneralization1',
 desc='returns position of : if x has the form ! isnamelc : formula',
 max='lambda x: length(x)',
 relation='lambda pos,x: AND4(equal(item(1,x),33),equal(item(pos,x),58),isnamelc(slice(2,acfull(pos),x)),isformula(slice(plus(2,acfull(pos)),length(x),x)))'
)

isgeneralization=basic_function(config,
 name='isgeneralization',
 desc='x is a generalization',
 define='lambda x: notzero(isgeneralization1(x))'
)

negation_formula=basic_function(config,
 name='negation_formula',
 desc='returns formula if x has the form ~ formula',
 define='lambda x: cond(isnegation(x),slice(2,length(x),x),0)'
)

conjunction_formula1=basic_function(config,
 name='conjunction_formula1',
 desc='returns formula1 if x has the form ( formula1 & formula2 )',
 define='lambda x: cond(isconjunction(x),slice(2,acfull(isconjunction1(x)),x),0)'
)

conjunction_formula2=basic_function(config,
 name='conjunction_formula2',
 desc='returns formula2 if x has the form ( formula1 & formula2 )',
 define='lambda x: cond(isconjunction(x),slice(plus(2,acfull(isconjunction1(x))),acfull(length(x)),x),0)'
)

generalization_namelc=basic_function(config,
 name='generalization_namelc',
 desc='returns namelc if x has the form ! isnamelc : formula',
 define='lambda x: cond(isgeneralization(x),slice(2,acfull(isgeneralization1(x)),x),0)'
)

generalization_formula=basic_function(config,
 name='generalization_formula',
 desc='returns formula if x has the form ! isnamelc : formula',
 define='lambda x: cond(isgeneralization(x),slice(plus(2,acfull(isgeneralization1(x))),length(x),x),0)'
)