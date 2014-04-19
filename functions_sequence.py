from functions import *
from functions_subst import *

config.globals=globals()

find_pos=argmin_function(config,
 name='find_pos',
 desc='position of occurence of a in x, starting with p+1 - 0 if not found',
 max='lambda a,x,p: length(x)',
 relation='lambda y,a,x,p: and_f(equal(item(y,x),a),smaller(p,y))'
)

find=primitive_recursive_function(config,
 name='find',
 desc='position of nth occurence of a in x - 0 if not found',
 zero='lambda a,x: n0',
 next='lambda n,a,x: find_pos(a,x,find(n,a,x))'
)

occur=argmin_function(config,
 name='occur',
 desc='how often character a occurs in x',
 max='lambda a,x: length(x)',
 relation='lambda n,a,x: zero(find(sc(n),a,x))'
)

sitem=basic_function(config, 
 name='sitem',
 desc='nth statement in formula sequence x delimited by ;',
 define='lambda n,x: slice(sc(find(acfull(n),n59,x)),acfull(find(n,n59,x)),x)'
)

slength=basic_function(config,
 name='slength',
 desc='length of sequence n',
 define='lambda n: occur(n59,n)'
)

sequence_end=basic_function(config,
 name='sequence_end',
 desc='returns last item of a sequence',
 define='lambda n: sitem(slength(n),n)'
)

sequence_start=basic_function(config,
 name='sequence_start',
 desc='returns all but last item of a sequence, 0 if sequence has length 1',
 define='lambda n: slice(n1,find(acfull(slength(n)),n59,n),n)'
)

# every well formed sequence must end with '\n' and must be nonempty
issequence=recursive_relation(config,
 name='issequence',
 desc='n is a valid nonempty sequence of formulae ending with ;',
 zero='lambda: n0',
 relation='lambda n,y: and_f3(equal(item(length(n),n),n59),isformula(sequence_end(n)),or_f(zero(sequence_start(n)),recursive_issequence(y,sequence_start(n))))'
)

freeinsequence=recursive_relation(config,
 name='freeinsequence',
 desc='x is free in sequence n',
 zero='lambda x: n0',
 relation='lambda n,x,y: or_f(isfreeinformula(sequence_end(n),x),recursive_freeinsequence(y,sequence_start(n),x))'
)

leftfromslash=basic_function(config,
 name='leftfromslash',
 desc='return string1 if x has the form string1 / string2',
 define='lambda x: cond(smaller(find_pos(n47,x,n0),length(x)),slice(n1,acfull(find_pos(n47,x,n0)),x),n0)'
)

rightfromslash=basic_function(config,
 name='rightfromslash',
 desc='return string2 if x has the form string1 / string2',
 define='lambda x: cond(smaller(n1,find_pos(n47,x,n0)),slice(sc(find_pos(n47,x,n0)),length(x),x),n0)'
)

recombine=basic_function(config,
 name='recombine',
 desc='return a / b',
 define='lambda a,b: cond(and_f(notzero(a),notzero(b)),concat(concat(a,n47),b),n0)'
)

subst_sequence=recursive_relation(config,
 name='subst_sequence',
 desc='n has the form sequence1 / sequence2 and sequence2 is a substitution of t for x in sequence1',
 zero='lambda x,t: n0',
 relation='lambda n,x,t,y: and_f4(issequence(leftfromslash(n)),issequence(rightfromslash(n)),equal(subst_formula(sequence_end(leftfromslash(n)),x,t),sequence_end(rightfromslash(n))),or_f(and_f(zero(sequence_start(leftfromslash(n))),zero(sequence_start(rightfromslash(n)))),recursive_subst_sequence(y,recombine(sequence_start(leftfromslash(n)),sequence_start(rightfromslash(n))),x,t)))'
)

subst_sequence_termlist1=recursive_relation(config,
 name='subst_sequence_termlist1',
 desc='returns 1 if subst_sequence(n,x,t1) for any term t1 in t',
 zero='lambda n,x: n0',
 relation='lambda t,n,x,y: cond(isterm(t),or_f(subst_sequence(n,x,t),recursive_subst_sequence_termlist1(y,term_termlist(t),n,x)),or_f3(subst_sequence(n,x,termlist_end(t)),recursive_subst_sequence_termlist1(y,term_termlist(termlist_end(t)),n,x),recursive_subst_sequence_termlist1(y,termlist_start(t),n,x)))'
)

subst_sequence_formula1=recursive_relation(config,
 name='subst_sequence_formula1',
 desc='returns 1 if subst_sequence(n,x,t1) for any term t1 in f',
 zero='lambda n,x: n0',
 relation='lambda f,n,x,y: or_f7(subst_sequence_termlist1(proposition_termlist(f),n,x),subst_sequence_termlist1(equation_term1(f),n,x),subst_sequence_termlist1(equation_term2(f),n,x),recursive_subst_sequence_formula1(y,negation_formula(f),n,x),recursive_subst_sequence_formula1(y,conjunction_formula1(f),n,x),recursive_subst_sequence_formula1(y,conjunction_formula2(f),n,x),recursive_subst_sequence_formula1(y,generalization_formula(f),n,x))'
)

subst_sequence_sequence1=recursive_relation(config,
 name='subst_sequence_sequence1',
 desc='returns 1 if subst_sequence(n,x,t1) for any term t1 in s',
 zero='lambda n,x: n0',
 relation='lambda s,n,x,y: or_f(subst_sequence_formula1(sequence_end(s),n,x),recursive_subst_sequence_sequence1(y,sequence_start(s),n,x))'
)

subst_sequence_termlist=recursive_relation(config,
 name='subst_sequence_termlist',
 desc='returns 1 if subst_sequence_sequence1(s,n,x) for any variable x in t',
 zero='lambda s,n: n0',
 relation='lambda t,s,n,y: cond(isterm(t),or_f(subst_sequence_sequence1(s,n,t),recursive_subst_sequence_termlist(y,term_termlist(t),s,n)),or_f3(subst_sequence_sequence1(s,n,termlist_end(t)),recursive_subst_sequence_termlist(y,term_termlist(termlist_end(t)),s,n),recursive_subst_sequence_termlist(y,termlist_start(t),s,n)))'
)

subst_sequence_formula=recursive_relation(config,
 name='subst_sequence_formula',
 desc='returns 1 if subst_sequence_sequence1(s,n,x) for any variable x in f',
 zero='lambda s,n: n0',
 relation='lambda f,s,n,y: or_f7(subst_sequence_termlist(proposition_termlist(f),s,n),subst_sequence_termlist(equation_term1(f),s,n),subst_sequence_termlist(equation_term2(f),s,n),recursive_subst_sequence_formula(y,negation_formula(f),s,n),recursive_subst_sequence_formula(y,conjunction_formula1(f),s,n),recursive_subst_sequence_formula(y,conjunction_formula2(f),s,n),recursive_subst_sequence_formula(y,generalization_formula(f),s,n))'
)

subst_sequence_sequence=recursive_relation(config,
 name='subst_sequence_sequence',
 desc='returns 1 if subst_sequence_sequence1(s1,n,x) for any variable x in s',
 zero='lambda s1,n: n0',
 relation='lambda s,s1,n,y: or_f(subst_sequence_formula(sequence_end(s),s1,n),recursive_subst_sequence_sequence(y,sequence_start(s),s1,n))'
)

subst_sequence_any=basic_function(config,
 name='subst_sequence_any',
 desc='returns 1 if sequence2 is a substitution of any term in sequence2 for any variable in sequence 1',
 define='lambda sequence1,sequence2: subst_sequence_sequence(sequence1,sequence2,recombine(sequence1,sequence2))'
)

isinsequence=recursive_relation(config,
 name='isinsequence',
 desc='returns 1 if formula f is in sequence s',
 zero='lambda f: n0',
 relation='lambda s,f,y: or_f(equal(f,sequence_end(s)),recursive_isinsequence(y,sequence_start(s),f))'
)

allof=recursive_relation(config,
 name='allof',
 desc='returns 1 if sequence b contains all formulae of sequence a',
 zero='lambda b: n1',
 relation='lambda a,b,y: and_f(isinsequence(b,sequence_end(a)),recursive_allof(y,sequence_start(a),b))'
)

sequal=basic_function(config,
 name='sequal',
 desc='returns 1 if sequences a and b contain the same formulae',
 define='lambda a,b: and_f(allof(a,b),allof(b,a))'
)
