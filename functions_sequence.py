from functions import *
from functions_subst import *

config.globals=globals()

find=primitive_recursive_function(config,
 name='find',
 desc='position of nth occurence of a in x - 0 if not found',
 zero='lambda a,x: 0',
 next='lambda n,a,x: find_pos(a,x,find(n,a,x))'
)

occur=argmin_function(config,
 name='occur',
 desc='how often character a occurs in x',
 max='lambda a,x: length(x)',
 relation='lambda n,a,x: zero(find(succ(n),a,x))'
)

sitem=basic_function(config, 
 name='sitem',
 desc='nth statement in formula sequence x delimited by ;',
 define='lambda n,x: slice(succ(find(acfull(n),59,x)),acfull(find(n,59,x)),x)'
)

slength=basic_function(config,
 name='slength',
 desc='length of sequence n',
 define='lambda n: occur(59,n)'
)

sequence_end=basic_function(config,
 name='sequence_end',
 desc='returns last item of a sequence',
 define='lambda n: sitem(slength(n),n)'
)

sequence_start=basic_function(config,
 name='sequence_start',
 desc='returns all but last item of a sequence, 0 if sequence has length 1',
 define='lambda n: slice(1,find(acfull(slength(n)),59,n),n)'
)

# every well formed sequence must end with '\n' and must be nonempty
issequence=recursive_function(config,
 name='issequence',
 desc='n is a valid nonempty sequence of formulae ending with ;',
 zero='lambda: 0',
 relation='lambda n,y: AND3(equal(item(length(n),n),59),isformula(sequence_end(n)),OR(zero(sequence_start(n)),recursive_issequence(y,sequence_start(n))))'
)

freeinsequence=recursive_function(config,
 name='freeinsequence',
 desc='x is free in sequence n',
 zero='lambda x: 0',
 relation='lambda n,x,y: OR(isfreeinformula(sequence_end(n),x),recursive_freeinsequence(y,sequence_start(n),x))'
)

subst_sequence=recursive_function(config,
 name='subst_sequence',
 desc='n has the form sequence1 / sequence2 and sequence2 is a substitution of t for x in sequence1',
 zero='lambda x,t: 0',
 relation='lambda n,x,t,y: AND4(issequence(leftfromslash(n)),issequence(rightfromslash(n)),subst_formula(recombine(sequence_end(leftfromslash(n)),sequence_end(rightfromslash(n))),x,t),OR(AND(zero(sequence_start(leftfromslash(n))),zero(sequence_start(rightfromslash(n)))),recursive_subst_sequence(y,recombine(sequence_start(leftfromslash(n)),sequence_start(rightfromslash(n))),x,t)))'
)

subst_sequence_termlist1=recursive_function(config,
 name='subst_sequence_termlist1',
 desc='returns 1 if subst_sequence(n,x,t1) for any term t1 in t',
 zero='lambda n,x: 0',
 relation='lambda t,n,x,y: cond(isterm(t),OR(subst_sequence(n,x,t),recursive_subst_sequence_termlist1(y,term_termlist(t),n,x)),OR3(subst_sequence(n,x,termlist_end(t)),recursive_subst_sequence_termlist1(y,term_termlist(termlist_end(t)),n,x),recursive_subst_sequence_termlist1(y,termlist_start(t),n,x)))'
)

subst_sequence_formula1=recursive_function(config,
 name='subst_sequence_formula1',
 desc='returns 1 if subst_sequence(n,x,t1) for any term t1 in f',
 zero='lambda n,x: 0',
 relation='lambda f,n,x,y: OR7(subst_sequence_termlist1(proposition_termlist(f),n,x),subst_sequence_termlist1(equation_term1(f),n,x),subst_sequence_termlist1(equation_term2(f),n,x),recursive_subst_sequence_formula1(y,negation_formula(f),n,x),recursive_subst_sequence_formula1(y,conjunction_formula1(f),n,x),recursive_subst_sequence_formula1(y,conjunction_formula2(f),n,x),recursive_subst_sequence_formula1(y,generalization_formula(f),n,x))'
)

subst_sequence_sequence1=recursive_function(config,
 name='subst_sequence_sequence1',
 desc='returns 1 if subst_sequence(n,x,t1) for any term t1 in s',
 zero='lambda n,x: 0',
 relation='lambda s,n,x,y: OR(subst_sequence_formula1(sequence_end(s),n,x),recursive_subst_sequence_sequence1(y,sequence_start(s),n,x))'
)

subst_sequence_termlist=recursive_function(config,
 name='subst_sequence_termlist',
 desc='returns 1 if subst_sequence_sequence1(s,n,x) for any variable x in t',
 zero='lambda s,n: 0',
 relation='lambda t,s,n,y: cond(isterm(t),OR(subst_sequence_sequence1(s,n,t),recursive_subst_sequence_termlist(y,term_termlist(t),s,n)),OR3(subst_sequence_sequence1(s,n,termlist_end(t)),recursive_subst_sequence_termlist(y,term_termlist(termlist_end(t)),s,n),recursive_subst_sequence_termlist(y,termlist_start(t),s,n)))'
)

subst_sequence_formula=recursive_function(config,
 name='subst_sequence_formula',
 desc='returns 1 if subst_sequence_sequence1(s,n,x) for any variable x in f',
 zero='lambda s,n: 0',
 relation='lambda f,s,n,y: OR7(subst_sequence_termlist(proposition_termlist(f),s,n),subst_sequence_termlist(equation_term1(f),s,n),subst_sequence_termlist(equation_term2(f),s,n),recursive_subst_sequence_formula(y,negation_formula(f),s,n),recursive_subst_sequence_formula(y,conjunction_formula1(f),s,n),recursive_subst_sequence_formula(y,conjunction_formula2(f),s,n),recursive_subst_sequence_formula(y,generalization_formula(f),s,n))'
)

subst_sequence_sequence=recursive_function(config,
 name='subst_sequence_sequence',
 desc='returns 1 if subst_sequence_sequence1(s1,n,x) for any variable x in s',
 zero='lambda s1,n: 0',
 relation='lambda s,s1,n,y: OR(subst_sequence_formula(sequence_end(s),s1,n),recursive_subst_sequence_sequence(y,sequence_start(s),s1,n))'
)

subst_sequence_any=basic_function(config,
 name='subst_sequence_any',
 desc='returns 1 if sequence2 is a substitution of any term in sequence2 for any variable in sequence 1',
 define='lambda sequence1,sequence2: subst_sequence_sequence(sequence1,sequence2,recombine(sequence1,sequence2))'
)

isinsequence=recursive_function(config,
 name='isinsequence',
 desc='returns 1 if formula f is in sequence s',
 zero='lambda f: 0',
 relation='lambda s,f,y: OR(equal(f,sequence_end(s)),recursive_isinsequence(y,sequence_start(s),f))'
)

allof=recursive_function(config,
 name='allof',
 desc='returns 1 if sequence b contains all formulae of sequence a',
 zero='lambda b: 1',
 relation='lambda a,b,y: AND(isinsequence(b,sequence_end(a)),recursive_allof(y,sequence_start(a),b))'
)

sequal=basic_function(config,
 name='sequal',
 desc='returns 1 if sequences a and b contain the same formulae',
 define='lambda a,b: AND(allof(a,b),allof(b,a))'
)
