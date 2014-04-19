from functions import *
from functions_calculus import *

config.globals=globals()

istautology=basic_function(config,
 name='istautology',
 desc='x is a tautological sequence',
 define='lambda x: or_f(isimplies_itself(x),istautologicalequation(x))'
)

isimplicationfromonesequence=basic_function(config,
 name='isimplicationfromonesequence',
 desc='sequence y is an implication of sequence x',
 define='lambda x,y: or_f7(ispermutation(x,y),isdeletionofconjunction1(x,y),isdeletionofconjunction2(x,y),isremovalofgeneralization(x,y),isintroductionofgeneralization(x,y),issubstitution(x,y),issubstitutionwithidentity(x,y))'
)

isimplicationfromtwosequences=basic_function(config,
 name='isimplicationfromtwosequences',
 desc='sequence z is an implication of sequence x and y',
 define='lambda x,y,z: or_f3(isintroductionofconjunction(x,y,z),isexhaustion(x,y,z),isquodlibet(x,y,z))'
)

proofitem=basic_function(config,
 name='proofitem',
 desc='nth statement in sequence of sequences x delimited by \\n',
 define='lambda n,x: slice(sc(find(acfull(n),n10,x)),acfull(find(n,n10,x)),x)'
)

prooflength=basic_function(config,
 name='prooflength',
 desc='length of sequence of sequences n',
 define='lambda n: occur(n10,n)'
)

proof_end=basic_function(config,
 name='proof_end',
 desc='returns last item of a sequence of sequences',
 define='lambda n: proofitem(prooflength(n),n)'
)

proof_start=basic_function(config,
 name='proof_start',
 desc='returns all but last item of a sequence of sequences, 0 if sequence of sequences has length 1',
 define='lambda n: slice(n1,find(acfull(prooflength(n)),n10,n),n)'
)

# every well formed sequence of sequences must end with '\n' and must be nonempty
isproof=recursive_relation(config,
 name='isproof',
 desc='n is a valid nonempty sequence of sequences ending with \\n',
 zero='lambda: n0',
 relation='lambda n,y: and_f3(equal(item(length(n),n),n10),issequence(proof_end(n)),or_f(zero(proof_start(n)),recursive_isproof(y,proof_start(n))))'
)

issimplyimplicatedbyone1=argmin_function(config,
 name='issimplyimplicatedbyone1',
 desc='returns a positive number if sequence y is implicated by one sequence in proof x',
 max='lambda x,y: prooflength(x)',
 relation='lambda nr,x,y: isimplicationfromonesequence(proofitem(nr,x),y)'
)

issimplyimplicatedbyone=basic_function(config,
 name='issimplyimplicatedbyone',
 desc='returns 1 if sequence y is implicated by one sequence in proof x',
 define='lambda x,y: notzero(issimplyimplicatedbyone1(x,y))'
)

issimplyimplicatedbytwo1=argmin_function(config,
 name='issimplyimplicatedbytwo1',
 desc='returns a positive number if sequence z is implicated by one sequence in proof x and sequence y',
 max='lambda x,y,z: prooflength(x)',
 relation='lambda nr,x,y,z: isimplicationfromtwosequences(proofitem(nr,x),y,z)'
)

issimplyimplicatedbytwo2=argmin_function(config,
 name='issimplyimplicatedbytwo2',
 desc='returns a positive number if sequence y is implicated by two sequences in proof x',
 max='lambda x,y: prooflength(x)',
 relation='lambda nr,x,y: notzero(issimplyimplicatedbytwo1(x,proofitem(nr,x),y))'
)

issimplyimplicatedbytwo=basic_function(config,
 name='issimplyimplicatedbytwo',
 desc='returns 1 if sequence y is implicated by two sequences in proof x',
 define='lambda x,y: notzero(issimplyimplicatedbytwo2(x,y))'
)

isvalidproof=recursive_relation(config,
 name='isvalidproof',
 desc='x is a valid proof (every sequence follows directly from zero, one or two preceding sequences)',
 zero='lambda: n0',
 relation='lambda x,y: and_f3(isproof(x),or_f3(istautology(proof_end(x)),issimplyimplicatedbyone(proof_start(x),proof_end(x)),issimplyimplicatedbytwo(proof_start(x),proof_end(x))),or_f(zero(proof_start(x)),recursive_isvalidproof(y,proof_start(x))))'
)

isvalidprooffor=basic_function(config,
 name='isvalidprooffor',
 desc='x is a valid proof for y',
 define='lambda x,y: and_f3(isvalidproof(x),isformula(y),equal(proof_end(x),concat(y,n59)))'
)
