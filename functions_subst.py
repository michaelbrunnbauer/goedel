from functions import *
from functions_freevariable import *

config.globals=globals()

# needs subst_termlistcode
subst_term_help=basic_function(config,
 name='subst_term_help',
 desc='return substitution of t for x in term n',
 define='lambda subst_termlistcode,n,x,t: cond(and_f3(isnamelc(x),isterm(t),isterm(n)),cond(isnamelc(n),cond(equal(n,x),t,n),concat(term_namelc(n),concat(n40,concat(recursive_subst_termlist(subst_termlistcode,term_termlist(n),x,t),n41)))),n0)'
)

subst_termlist=recursive_function(config,
 name='subst_termlist',
 desc='returns substitution of t for x in termlist n',
 resultlen='lambda n,x,t: succ(mul(n8,mul(length(n),length(t))))',
 zero='lambda x,t: n0',
 function='lambda n,x,t,y: cond(and_f3(istermlist(n),isnamelc(x),isterm(t)),cond(isterm(n),subst_term_help(y,n,x,t),concat3(recursive_subst_termlist(y,termlist_start(n),x,t),n44,subst_term_help(y,termlist_end(n),x,t))),n0)'
)

subst_term=basic_function(config,
 name='subst_term',
 desc='returns substitution of t for x in term n',
 define='lambda n,x,t: cond(and_f3(isnamelc(x),isterm(t),isterm(n)),cond(isnamelc(n),cond(equal(n,x),t,n),concat4(term_namelc(n),n40,subst_termlist(term_termlist(n),x,t),n41)),n0)'
)

subst_proposition=basic_function(config,
 name='subst_proposition',
 desc='returns substitution of t for x in proposition n',
 define='lambda n,x,t: cond(and_f3(isnamelc(x),isterm(t),isproposition(n)),concat4(proposition_nameuc(n),n40,subst_termlist(proposition_termlist(n),x,t),n41),n0)'
)

subst_equation=basic_function(config,
 name='subst_equation',
 desc='returns substitution of t for x in equation n',
 define='lambda n,x,t: cond(and_f3(isnamelc(x),isterm(t),isequation(n)),concat3(subst_term(equation_term1(n),x,t),n61,subst_term(equation_term2(n),x,t)),n0)'
)

# needs subst_formulacode
subst_negation=basic_function(config,
 name='subst_negation',
 desc='return substitution of t for x in negation n',
 define='lambda subst_formulacode,n,x,t: cond(and_f3(isnamelc(x),isterm(t),isnegation(n)),concat(n126,recursive_subst_formula(subst_formulacode,negation_formula(n),x,t)),n0)'
)

# needs subst_formulacode
subst_conjunction=basic_function(config,
 name='subst_conjunction',
 desc='returns substitution of t for x in conjunction n',
 define='lambda subst_formulacode,n,x,t: cond(and_f3(isnamelc(x),isterm(t),isconjunction(n)),concat5(n40,recursive_subst_formula(subst_formulacode,conjunction_formula1(n),x,t),n38,recursive_subst_formula(subst_formulacode,conjunction_formula2(n),x,t),n41),n0)'
)

# needs subst_formulacode
subst_generalization=basic_function(config,
 name='subst_generalization',
 desc='returns substitution of t for x in generalization n',
 define='lambda subst_formulacode,n,x,t: cond(and_f3(isnamelc(x),isterm(t),isgeneralization(n)),cond(isfreeinformula(n,x),cond(isfreeinterm(t,generalization_namelc(n)),n0,concat4(n33,generalization_namelc(n),n58,recursive_subst_formula(subst_formulacode,generalization_formula(n),x,t))),n),n0)'
)

subst_formula=recursive_function(config,
 name='subst_formula',
 desc='returns substitution of t for x in formula n',
 resultlen='lambda n,x,t: succ(mul(n8,mul(length(n),length(t))))',
 zero='lambda x,t: n0',
 function='lambda n,x,t,y: cond(and_f3(isnamelc(x),isterm(t),isformula(n)),concat5(subst_proposition(n,x,t),subst_equation(n,x,t),subst_negation(y,n,x,t),subst_conjunction(y,n,x,t),subst_generalization(y,n,x,t)),n0)'
)
