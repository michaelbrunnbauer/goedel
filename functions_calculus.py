from functions import *
from functions_sequence import *

config.globals=globals()

isimplies_itself=basic_function(config,
 name='isimplies_itself',
 desc='x is a sequence of the form formula formula',
 define='lambda x: and_f3(issequence(x),equal(slength(x),n2),equal(sitem(n1,x),sitem(n2,x)))'
)

istautologicalequation=basic_function(config,
 name='istautologicalequation',
 desc='x is a sequence of the form term = term',
 define='lambda x: and_f4(issequence(x),equal(slength(x),n1),isequation(sitem(n1,x)),equal(equation_term1(sitem(n1,x)),equation_term2(sitem(n1,x))))'
)

isintroductionofconjunction=basic_function(config,
 name='isintroductionofconjunction',
 desc='x is a sequence ... a, y is a sequence --- b, z is ... --- ( a & b )',
 define='lambda x,y,z: and_f7(issequence(x),issequence(y),issequence(z),isconjunction(sequence_end(z)),sequal(sequence_start(z),concat(sequence_start(x),sequence_start(y))),equal(conjunction_formula1(sequence_end(z)),sequence_end(x)),equal(conjunction_formula2(sequence_end(z)),sequence_end(y)))'
)

isdeletionofconjunction1=basic_function(config,
 name='isdeletionofconjunction1',
 desc='x is a sequence ... ( a & b ), y is a sequence ... a',
 define='lambda x,y: and_f4(issequence(x),isconjunction(sequence_end(x)),sequal(sequence_start(x),sequence_start(y)),equal(sequence_end(y),conjunction_formula1(sequence_end(x))))'
)

isdeletionofconjunction2=basic_function(config,
 name='isdeletionofconjunction2',
 desc='x is a sequence ... ( a & b ), y is a sequence ... b',
 define='lambda x,y: and_f4(issequence(x),isconjunction(sequence_end(x)),sequal(sequence_start(x),sequence_start(y)),equal(sequence_end(y),conjunction_formula2(sequence_end(x))))'
)

isexhaustion=basic_function(config,
 name='isexhaustion',
 desc='x is a sequence ... a b, y is a sequence --- ~a b, z is a sequence ... --- b',
 define='lambda x,y,z: and_f10(issequence(x),issequence(y),issequence(z),smaller(n1,slength(x)),smaller(n1,slength(y)),isnegation(sitem(acfull(slength(y)),y)),equal(negation_formula(sitem(acfull(slength(y)),y)),sitem(acfull(slength(x)),x)),equal(sequence_end(x),sequence_end(y)),equal(sequence_end(x),sequence_end(z)),sequal(sequence_start(z),concat(sequence_start(sequence_start(x)),sequence_start(sequence_start(y)))))'
)

isquodlibet=basic_function(config,
 name='isquodlibet',
 desc='x is a sequence ... a, y is a sequence --- ~a, z is a sequence ... --- b',
 define='lambda x,y,z: and_f6(issequence(x),issequence(y),issequence(z),isnegation(sequence_end(y)),equal(negation_formula(sequence_end(y)),sequence_end(x)),sequal(sequence_start(z),concat(sequence_start(x),sequence_start(y))))'
)

isremovalofgeneralization=basic_function(config,
 name='isremovalofgeneralization',
 desc='x is a sequence ... !x:a, y is a sequence ... a',
 define='lambda x,y: and_f5(issequence(x),issequence(y),isgeneralization(sequence_end(x)),sequal(sequence_start(x),sequence_start(y)),equal(generalization_formula(sequence_end(x)),sequence_end(y)))'
)

isintroductionofgeneralization=basic_function(config,
 name='isintroductionofgeneralization',
 desc='x is a sequence ... a, y is a sequence ... !x:a, x is not free in ...',
 define='lambda x,y: and_f6(issequence(x),issequence(y),isgeneralization(sequence_end(y)),sequal(sequence_start(x),sequence_start(y)),equal(sequence_end(x),generalization_formula(sequence_end(y))),or_f(zero(sequence_start(x)),not_f(freeinsequence(sequence_start(x),generalization_namelc(sequence_end(y))))))'
)

issubstitution=basic_function(config,
 name='issubstitution',
 desc='x is a sequence, y is a sequence, y is a substitution of a term in y for a variable in x in x',
 define='lambda x,y: and_f4(issequence(x),issequence(y),not_f(equal(x,y)),subst_sequence_any(x,y))'
)

issubstitutionwithidentity=basic_function(config,
 name='issubstitutionwithidentity',
 desc='x is a sequence ... a, y is a sequence --- x=t b, b is a substitution of t for x in a',
 define='lambda x,y: and_f5(issequence(x),issequence(y),smaller(n1,slength(y)),isequation(sequence_end(sequence_start(y))),equal(sequence_end(y),subst_formula(sequence_end(x),equation_term1(sequence_end(sequence_start(y))),equation_term2(sequence_end(sequence_start(y))))))'
)

ispermutation=basic_function(config,
 name='ispermutation',
 desc='x is a sequence ... a, y is a sequence ... a',
 define='lambda x,y: and_f5(issequence(x),issequence(y),smaller(n2,slength(x)),equal(sequence_end(x),sequence_end(y)),sequal(sequence_start(x),sequence_start(y)))'
)
