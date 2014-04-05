from functions import *
from functions_calculus import *

config.globals=globals()

istautology=basic_function(config,
 name='istautology',
 desc='x is a tautological sequence',
 define='lambda x: OR(isimplies_itself(x),istautologicalequation(x))'
)

isimplicationfromonesequence=basic_function(config,
 name='isimplicationfromonesequence',
 desc='sequence y is an implication of sequence x',
 define='lambda x,y: OR7(ispermutation(x,y),isdeletionofconjunction1(x,y),isdeletionofconjunction2(x,y),isremovalofgeneralization(x,y),isintroductionofgeneralization(x,y),issubstitution(x,y),issubstitutionwithidentity(x,y))'
)

isimplicationfromtwosequences=basic_function(config,
 name='isimplicationfromtwosequences',
 desc='sequence z is an implication of sequence x and y',
 define='lambda x,y,z: OR3(isintroductionofconjunction(x,y,z),isexhaustion(x,y,z),isquodlibet(x,y,z))'
)

proofitem=basic_function(config,
 name='proofitem',
 desc='nth statement in sequence of sequences x delimited by \\n',
 define='lambda n,x: slice(succ(find(acfull(n),10,x)),acfull(find(n,10,x)),x)'
)

prooflength=basic_function(config,
 name='prooflength',
 desc='length of sequence of sequences n',
 define='lambda n: occur(10,n)'
)

proof_end=basic_function(config,
 name='proof_end',
 desc='returns last item of a sequence of sequences',
 define='lambda n: proofitem(prooflength(n),n)'
)

proof_start=basic_function(config,
 name='proof_start',
 desc='returns all but last item of a sequence of sequences, 0 if sequence of sequences has length 1',
 define='lambda n: slice(1,find(acfull(prooflength(n)),10,n),n)'
)

# every well formed sequence of sequences must end with '\n' and must be nonempty
isproof=recursive_function(config,
 name='isproof',
 desc='n is a valid nonempty sequence of sequences ending with \\n',
 zero='lambda: 0',
 relation='lambda n,y: AND3(equal(item(length(n),n),10),issequence(proof_end(n)),OR(zero(proof_start(n)),recursive_isproof(y,proof_start(n))))'
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

isvalidproof=recursive_function(config,
 name='isvalidproof',
 desc='x is a valid proof (every sequence follows directly from zero, one or two preceding sequences)',
 zero='lambda: 0',
 relation='lambda x,y: AND3(isproof(x),OR3(istautology(proof_end(x)),issimplyimplicatedbyone(proof_start(x),proof_end(x)),issimplyimplicatedbytwo(proof_start(x),proof_end(x))),OR(zero(proof_start(x)),recursive_isvalidproof(y,proof_start(x))))'
)
