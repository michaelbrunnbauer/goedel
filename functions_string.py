from functions import *
from functions_basic import *

config.globals=globals()

rshift=basic_function(config,
 name='rshift',
 desc='right shift by b bytes',
 define='lambda a,b: div(a,pow(2,mul(8,b)))'
)

lshift=basic_function(config,
 name='lshift',
 desc='left shift by b bytes',
 define='lambda a,b: mul(a,pow(2,mul(8,b)))'
)

length=argmin_function(config,
 name='length',
 desc='length of a string',
 max='lambda x: x',
 relation='lambda y,x: zero(rshift(x,y))'
)

item=basic_function(config,
 name='item',
 desc='n-th character of a string',
 define='lambda n,x: cond(smallereq(n,length(x)),minusfull(rshift(x,minusfull(length(x),n)),lshift(rshift(x,succ(minusfull(length(x),n))),1)),0)',
)

concat=basic_function(config,
 name='concat',
 desc='concatenation of strings',
 define='lambda x,y: plus(lshift(x,length(y)),y)'
)

left=basic_function(config,
 name='left',
 desc='substring of x ending at position a',
 define='lambda a,x: rshift(x,minusfull(length(x),a))'
)

right=basic_function(config,
 name='right',
 desc='substring of x starting at position a',
 define='lambda a,x: minus(x,lshift(left(ac(a),x),minusfull(length(x),ac(a))))',
 asserts='lambda a,x: a!=0'
)

slice=basic_function(config,
 name='slice',
 desc='substring of x starting at position a and ending at position b',
 define='lambda a,b,x: left(minusfull(succ(b),a),right(a,x))',
 asserts='lambda a,b,x: a!=0'
)

bitset=basic_function(config,
 name='bitset',
 desc='bit b of a is set (starting with bit 0)',
 define='lambda a,b: minus(div(a,pow(2,b)),mul(div(a,pow(2,succ(b))),2))'
)

isalphalc=basic_function(config,
 name='isalphalc',
 desc='x is a-z',
 define='lambda x: AND(smaller(96,x),smaller(x,123))'
)

isalphauc=basic_function(config,
 name='isalphauc',
 desc='x is A-Z',
 define='lambda x: AND(smaller(64,x),smaller(x,91))'
)

isdigit=basic_function(config,
 name='isdigit',
 desc='x is 0-9',
 define='lambda x: AND(smaller(47,x),smaller(x,58))'
)

isalnumlc=basic_function(config,
 name='isalnumlc',
 desc='x is a-z or 0-9 or _',
 define='lambda x: OR3(equal(x,95),isalphalc(x),isdigit(x))'
)

isalnumuc=basic_function(config,
 name='isalnumuc',
 desc='x is A-Z or 0-9 or _',
 define='lambda x: OR3(equal(x,95),isalphauc(x),isdigit(x))'
)
