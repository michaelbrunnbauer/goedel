from functions import *
from functions_formula import *

config.globals=globals()

# isfreeinterm_help needs freeintermlistcode
isfreeinterm_help=basic_function(config,
 name='isfreeinterm_help',
 desc='variable x is free in term t',
 define='lambda freeintermlistcode,x,t: and_f(isterm(t),or_f(equal(x,t),recursive_isfreeintermlist(freeintermlistcode,term_termlist(t),x)))'
)

isfreeintermlist=recursive_relation(config,
 name='isfreeintermlist',
 desc='x is a free variable of termlist',
 zero='lambda x: n0',
 relation='lambda termlist,x,y: or_f3(isfreeinterm_help(y,x,termlist),recursive_isfreeintermlist(y,termlist_start(termlist),x),isfreeinterm_help(y,x,termlist_end(termlist)))'
)

isfreeinterm=basic_function(config,
 name='isfreeinterm',
 desc='variable x is free in term t',
 define='lambda t,x: and_f(isterm(t),or_f(equal(x,t),isfreeintermlist(term_termlist(t),x)))'
)

isfreeinproposition=basic_function(config,
 name='isfreeinproposition',
 desc='variable x is free in proposition t',
 define='lambda t,x: isfreeintermlist(proposition_termlist(t),x)'
)

isfreeinequation=basic_function(config,
 name='isfreeinequation',
 desc='variable x is free in equation t',
 define='lambda t,x: or_f(isfreeinterm(equation_term1(t),x),isfreeinterm(equation_term2(t),x))'
)

# needs isfreeinformulacode
isfreeinnegation=basic_function(config,
 name='isfreeinnegation',
 desc='variable y is free in negation x',
 define='lambda x,y,isfreeinformulacode: recursive_isfreeinformula(isfreeinformulacode,negation_formula(x),y)'
)

# needs isfreeinformulacode
isfreeinconjunction=basic_function(config,
 name='isfreeinconjunction',
 desc='variable y is free in conjunction x',
 define='lambda x,y,isfreeinformulacode: or_f(recursive_isfreeinformula(isfreeinformulacode,conjunction_formula1(x),y),recursive_isfreeinformula(isfreeinformulacode,conjunction_formula2(x),y))'
)

# needs isfreeinformulacode
isfreeingeneralization=basic_function(config,
 name='isfreeingeneralization',
 desc='variable y is free in generalization x',
 define='lambda x,y,isfreeinformulacode: and_f(not_f(equal(generalization_namelc(x),y)),recursive_isfreeinformula(isfreeinformulacode,generalization_formula(x),y))'
)

isfreeinformula=recursive_relation(config,
 name='isfreeinformula',
 desc='variable z is free in formula x',
 zero='lambda z: n0',
 relation='lambda x,z,y: and_f(isformula(x),or_f5(isfreeinproposition(x,z),isfreeinequation(x,z),isfreeinnegation(x,z,y),isfreeinconjunction(x,z,y),isfreeingeneralization(x,z,y)))'
)
