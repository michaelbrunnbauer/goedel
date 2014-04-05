from functions import *
from functions_freevariable import *

config.globals=globals()

find_pos=argmin_function(config,
 name='find_pos',
 desc='position of occurence of a in x, starting with p+1 - 0 if not found',
 max='lambda a,x,p: length(x)',
 relation='lambda y,a,x,p: AND(equal(item(y,x),a),smaller(p,y))'
)

leftfromslash=basic_function(config,
 name='leftfromslash',
 desc='return string1 if x has the form string1 / string2',
 define='lambda x: cond(smaller(find_pos(47,x,0),length(x)),slice(1,acfull(find_pos(47,x,0)),x),0)'
)

rightfromslash=basic_function(config,
 name='rightfromslash',
 desc='return string2 if x has the form string1 / string2',
 define='lambda x: cond(smaller(1,find_pos(47,x,0)),slice(succ(find_pos(47,x,0)),length(x),x),0)'
)

recombine=basic_function(config,
 name='recombine',
 desc='return a / b',
 define='lambda a,b: cond(AND(notzero(a),notzero(b)),concat(concat(a,47),b),0)'
)

# subst_term_help needs subst_termlistcode
subst_term_help=basic_function(config,
 name='subst_term_help',
 desc='n has the form term1 / term2 and term2 is a substitution of t for x in term1',
 define='lambda subst_termlistcode,n,x,t: AND3(isterm(leftfromslash(n)),isterm(rightfromslash(n)),OR3(AND(NOT(isfreeinterm(leftfromslash(n),x)),equal(leftfromslash(n),rightfromslash(n))),AND(equal(leftfromslash(n),x),equal(rightfromslash(n),t)),AND(equal(term_namelc(leftfromslash(n)),term_namelc(rightfromslash(n))),recursive_subst_termlist(subst_termlistcode,recombine(term_termlist(leftfromslash(n)),term_termlist(rightfromslash(n))),x,t))))'
)

subst_termlist=recursive_function(config,
 name='subst_termlist',
 desc='n has the form termlist1 / termlist2 and termlist2 is a substitution of t for x in termlist1',
 zero='lambda x,t: 0',
 relation='lambda n,x,t,y: AND3(istermlist(leftfromslash(n)),istermlist(rightfromslash(n)),OR(subst_term_help(y,n,x,t),AND(recursive_subst_termlist(y,recombine(termlist_start(leftfromslash(n)),termlist_start(rightfromslash(n))),x,t),subst_term_help(y,recombine(termlist_end(leftfromslash(n)),termlist_end(rightfromslash(n))),x,t))))'
)

subst_term=basic_function(config,
 name='subst_term',
 desc='n has the form term1 / term2 and term2 is a substitution of t for x in term1',
 define='lambda n,x,t: AND3(isterm(leftfromslash(n)),isterm(rightfromslash(n)),OR3(AND(NOT(isfreeinterm(leftfromslash(n),x)),equal(leftfromslash(n),rightfromslash(n))),AND(equal(leftfromslash(n),x),equal(rightfromslash(n),t)),AND(equal(term_namelc(leftfromslash(n)),term_namelc(rightfromslash(n))),subst_termlist(recombine(term_termlist(leftfromslash(n)),term_termlist(rightfromslash(n))),x,t))))'
)

subst_proposition=basic_function(config,
 name='subst_proposition',
 desc='n has the form proposition1 / proposition2 and proposition2 is a substitution of t for x in proposition1',
 define='lambda n,x,t: AND(equal(proposition_nameuc(leftfromslash(n)),proposition_nameuc(rightfromslash(n))),subst_termlist(recombine(proposition_termlist(leftfromslash(n)),proposition_termlist(rightfromslash(n))),x,t))'
)

subst_equation=basic_function(config,
 name='subst_equation',
 desc='n has the form equation1 / equation2 and equation2 is a substitution of t for x in equation1',
 define='lambda n,x,t: AND(subst_term(recombine(equation_term1(leftfromslash(n)),equation_term1(rightfromslash(n))),x,t),subst_term(recombine(equation_term2(leftfromslash(n)),equation_term2(rightfromslash(n))),x,t))'
)

# needs subst_formulacode
subst_negation=basic_function(config,
 name='subst_negation',
 desc='n has the form negation1 / negation2 and negation2 is a substitution of t for x in negation1',
 define='lambda subst_formulacode,n,x,t: recursive_subst_formula(subst_formulacode,recombine(negation_formula(leftfromslash(n)),negation_formula(rightfromslash(n))),x,t)'
)

# needs subst_formulacode
subst_conjunction=basic_function(config,
 name='subst_conjunction',
 desc='n has the form conjunction1 / conjunction2 and conjunction2 is a substitution of t for x in conjunction1',
 define='lambda subst_formulacode,n,x,t: AND(recursive_subst_formula(subst_formulacode,recombine(conjunction_formula1(leftfromslash(n)),conjunction_formula1(rightfromslash(n))),x,t),recursive_subst_formula(subst_formulacode,recombine(conjunction_formula2(leftfromslash(n)),conjunction_formula2(rightfromslash(n))),x,t))'
)

# needs subst_formulacode
subst_generalization=basic_function(config,
 name='subst_generalization',
 desc='n has the form generalization1 / generalization2 and generalization2 is a substitution of t for x in generalization1',
 define='lambda subst_formulacode,n,x,t: OR(AND3(isgeneralization(leftfromslash(n)),NOT(isfreeinformula(leftfromslash(n),x)),equal(leftfromslash(n),rightfromslash(n))),AND4(isfreeinformula(leftfromslash(n),x),equal(generalization_namelc(leftfromslash(n)),generalization_namelc(rightfromslash(n))),NOT(isfreeinformula(t,generalization_namelc(leftfromslash(n)))),recursive_subst_formula(subst_formulacode,recombine(generalization_formula(leftfromslash(n)),generalization_formula(rightfromslash(n))),x,t)))'
)

subst_formula=recursive_function(config,
 name='subst_formula',
 desc='n has the form formula1 / formula2 and formula2 is a substitution of t for x in formula1',
 zero='lambda x,t: 0',
 relation='lambda n,x,t,y: OR5(subst_proposition(n,x,t),subst_equation(n,x,t),subst_negation(y,n,x,t),subst_conjunction(y,n,x,t),subst_generalization(y,n,x,t))'
)
