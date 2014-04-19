from functions import *
from functions_basic import *

config.globals=globals()

rshift=basic_function(config,
 name='rshift',
 desc='right shift by b bytes',
 define='lambda a,b: div(a,pow(n2,mu(n8,b)))',
 #fast='lambda a,b: a >> b*8'
)

lshift=basic_function(config,
 name='lshift',
 desc='left shift by b bytes',
 define='lambda a,b: mu(a,pow(n2,mu(n8,b)))',
 #fast='lambda a,b: a << b*8'
)

length=argmin_function(config,
 name='length',
 desc='length of a string',
 max='lambda x: x',
 relation='lambda y,x: zero(rshift(x,y))',
 #fast='lambda x: 0 if x==0 else (x.bit_length()/8)+1'
)

item=basic_function(config,
 name='item',
 desc='n-th character of a string',
 define='lambda n,x: cond(smallereq(n,length(x)),minusfull(rshift(x,minusfull(length(x),n)),lshift(rshift(x,sc(minusfull(length(x),n))),n1)),n0)',
)

concat=basic_function(config,
 name='concat',
 desc='concatenation of strings',
 define='lambda x,y: ad(lshift(x,length(y)),y)'
)

concat3=basic_function(config,
 name='concat3',
 desc='concatenation of strings',
 define='lambda x1,x2,x3: concat(x1,concat(x2,x3))'
)

concat4=basic_function(config,
 name='concat4',
 desc='concatenation of strings',
 define='lambda x1,x2,x3,x4: concat(x1,concat3(x2,x3,x4))'
)

concat5=basic_function(config,
 name='concat5',
 desc='concatenation of strings',
 define='lambda x1,x2,x3,x4,x5: concat(x1,concat4(x2,x3,x4,x5))'
)

concat6=basic_function(config,
 name='concat6',
 desc='concatenation of strings',
 define='lambda x1,x2,x3,x4,x5,x6: concat(x1,concat5(x2,x3,x4,x5,x6))'
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
 define='lambda a,b,x: left(minusfull(sc(b),a),right(a,x))',
 asserts='lambda a,b,x: a!=0'
)

bitset=basic_function(config,
 name='bitset',
 desc='bit b of a is set (starting with bit 0)',
 define='lambda a,b: minus(div(a,pow(n2,b)),mu(div(a,pow(n2,sc(b))),n2))'
)

bitslice=basic_function(config,
 name='bitslice',
 desc='returns the number corresponding to bit b-c of a (from right to left starting with 0)',
 define='lambda a,b,c: minusfull(div(a,pow(n2,b)),mu(div(a,pow(n2,sc(c))),pow(n2,minusfull(sc(c),b))))'
)

isalphalc=basic_function(config,
 name='isalphalc',
 desc='x is a-z',
 define='lambda x: and_f(smaller(n96,x),smaller(x,n123))'
)

isalphauc=basic_function(config,
 name='isalphauc',
 desc='x is A-Z',
 define='lambda x: and_f(smaller(n64,x),smaller(x,n91))'
)

isdigit=basic_function(config,
 name='isdigit',
 desc='x is 0-9',
 define='lambda x: and_f(smaller(n47,x),smaller(x,n58))'
)

isalnumlc=basic_function(config,
 name='isalnumlc',
 desc='x is a-z or 0-9 or _',
 define='lambda x: or_f3(equal(x,n95),isalphalc(x),isdigit(x))'
)

isalnumuc=basic_function(config,
 name='isalnumuc',
 desc='x is A-Z or 0-9 or _',
 define='lambda x: or_f3(equal(x,n95),isalphauc(x),isdigit(x))'
)
