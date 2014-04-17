from functions import *

# we assume n0, succ() and = are symbols of the theory 

def succ(a):
    return a+1

def plus(a,b):
    return a+b

def mul(a,b):
    return a*b

for a in range(257):
    exec('n'+str(a)+'='+str(a))

def basic_definitions():
    rueck=''
    for a in range(1,257):
        rueck+='n'+str(a)+'=succ(n'+str(a-1)+')\n'
    return rueck[:-1]

config=configuration(globals())

ac=primitive_recursive_function(config,
 name='ac',
 desc='antecessor function - with assert for 0',
 zero='lambda: n0',
 next='lambda n: n',
 asserts='lambda n: n!=0'
)

# antecessor function without assert for cases where the antecessor of 0
# (defined as 0) actually has to be computed
acfull=primitive_recursive_function(config,
 name='acfull',
 desc='antecessor function - without assert for 0',
 zero='lambda: n0',
 next='lambda n: n'
)

zero=primitive_recursive_function(config,
 name='zero',
 desc='1 for n=0, else 0',
 zero='lambda: n1',
 next='lambda n: n0'
)

notzero=primitive_recursive_function(config,
 name='notzero',
 desc='0 for n=0, else 1',
 zero='lambda: n0',
 next='lambda n: n1'
)

minus_rev=primitive_recursive_function(config,
 name='minus_rev',
 desc='proper subtraction b-a',   
 zero='lambda b: b',
 next='lambda a,b: ac(minus_rev(a,b))'
)
 
minus=basic_function(config,
 name='minus',
 desc='subtraction',
 define='lambda a,b: minus_rev(b,a)',
 fast='lambda a,b: a-b',   
 asserts='lambda a,b: a >= b'
)

minusfull=basic_function(config,
 name='minusfull',
 desc='proper subtraction',
 define='lambda a,b: minus_rev(b,a)',
 fast='lambda a,b: a-b if a >= b else 0'
)

and_f=basic_function(config,
 name='and_f',
 desc='logical and',
 define='lambda a,b: mul(notzero(a),notzero(b))'
)

and_f3=basic_function(config,
 name='and_f3',
 desc='logical and',
 define='lambda a1,a2,a3: and_f(a1,and_f(a2,a3))'
)

and_f4=basic_function(config,
 name='and_f4',
 desc='logical and',
 define='lambda a1,a2,a3,a4: and_f(a1,and_f3(a2,a3,a4))'
)

and_f5=basic_function(config,
 name='and_f5',
 desc='logical and',
 define='lambda a1,a2,a3,a4,a5: and_f(a1,and_f4(a2,a3,a4,a5))'
)

and_f6=basic_function(config,
 name='and_f6',
 desc='logical and',
 define='lambda a1,a2,a3,a4,a5,a6: and_f(a1,and_f5(a2,a3,a4,a5,a6))'
)

and_f7=basic_function(config,
 name='and_f7',
 desc='logical and',
 define='lambda a1,a2,a3,a4,a5,a6,a7: and_f(a1,and_f6(a2,a3,a4,a5,a6,a7))'
)

and_f8=basic_function(config,
 name='and_f8',
 desc='logical and',
 define='lambda a1,a2,a3,a4,a5,a6,a7,a8: and_f(a1,and_f7(a2,a3,a4,a5,a6,a7,a8))'
)

and_f9=basic_function(config,
 name='and_f9',
 desc='logical and',
 define='lambda a1,a2,a3,a4,a5,a6,a7,a8,a9: and_f(a1,and_f8(a2,a3,a4,a5,a6,a7,a8,a9))'
)

and_f10=basic_function(config,
 name='and_f10',
 desc='logical and',
 define='lambda a1,a2,a3,a4,a5,a6,a7,a8,a9,a10: and_f(a1,and_f9(a2,a3,a4,a5,a6,a7,a8,a9,a10))'
)

or_f=basic_function(config,
 name='or_f',
 desc='logical or',
 define='lambda a,b: notzero(plus(a,b))'
)

or_f3=basic_function(config,
 name='or_f3',
 desc='logical or',
 define='lambda a1,a2,a3: or_f(a1,or_f(a2,a3))'
)

or_f4=basic_function(config,
 name='or_f4',
 desc='logical or',
 define='lambda a1,a2,a3,a4: or_f(a1,or_f3(a2,a3,a4))'
)

or_f5=basic_function(config,
 name='or_f5',
 desc='logical or',
 define='lambda a1,a2,a3,a4,a5: or_f(a1,or_f4(a2,a3,a4,a5))'
)

or_f6=basic_function(config,
 name='or_f6',
 desc='logical or',
 define='lambda a1,a2,a3,a4,a5,a6: or_f(a1,or_f5(a2,a3,a4,a5,a6))'
)

or_f7=basic_function(config,
 name='or_f7',
 desc='logical or',
 define='lambda a1,a2,a3,a4,a5,a6,a7: or_f(a1,or_f6(a2,a3,a4,a5,a6,a7))'
)

or_f8=basic_function(config,
 name='or_f8',
 desc='logical or',
 define='lambda a1,a2,a3,a4,a5,a6,a7,a8: or_f(a1,or_f7(a2,a3,a4,a5,a6,a7,a8))'
)

or_f9=basic_function(config,
 name='or_f9',
 desc='logical or',
 define='lambda a1,a2,a3,a4,a5,a6,a7,a8,a9: or_f(a1,or_f8(a2,a3,a4,a5,a6,a7,a8,a9))'
)

or_f10=basic_function(config,
 name='or_f10',
 desc='logical or',
 define='lambda a1,a2,a3,a4,a5,a6,a7,a8,a9,a10: or_f(a1,or_f9(a2,a3,a4,a5,a6,a7,a8,a9,a10))'
)

not_f=basic_function(config,
 name='not_f',
 desc='logical not',
 define='lambda a: zero(a)'
)

cond=basic_function(config,
 name='cond',   
 desc='returns a if c != 0, else b',
 define='lambda c,a,b: plus(mul(notzero(c),a),mul(zero(c),b))',
 fast='lambda c,a,b: b if c==0 else a'
)

ifzero=basic_function(config,
 name='ifzero',
 desc='returns a if a!=0, else b',
 define='lambda a,b: cond(a,a,b)'
)

smaller=primitive_recursive_function(config,
 name='smaller',
 desc='1 if a smaller b, else 0',
 zero='lambda b: notzero(b)',
 next='lambda a,b: smaller(a,acfull(b))',
 fast='lambda a,b: 1 if a < b else 0'
)

equal=primitive_recursive_function(config,
 name='equal',
 desc='1 if a==b, else 0',
 zero='lambda b: zero(b)',
 next='lambda a,b: cond(b,equal(a,acfull(b)),n0)',
 fast='lambda a,b: 1 if a==b else 0'
)

smallereq=basic_function(config,
 name='smallereq',
 desc='a smaller or equal b',
 define='lambda a,b: or_f(equal(a,b),smaller(a,b))',
 fast='lambda a,b: 1 if a<=b else 0'
)

div=argmin_function(config,
 name='div',
 desc='division',
 max='lambda a,b: a',
 relation='lambda x,a,b: and_f(notzero(smallereq(mul(x,b),a)),zero(smallereq(mul(succ(x),b),a)))',
 fast='lambda a,b: a / b',
 asserts='lambda a,b: b!=0'
)

modulo=basic_function(config,
 name='modulo',
 desc='modulo operator',
 define='lambda a,b: minus(a,mul(div(a,b),b))',
 fast='lambda a,b: a % b',
 asserts='lambda a,b: b!=0'
)

pow_rev=primitive_recursive_function(config,
 name='pow_rev',
 desc='b**a',
 zero='lambda b: n1',
 next='lambda a,b: mul(b,pow_rev(a,b))',
 fast='lambda a,b: b**a'
)

pow=basic_function(config,
 name='pow',
 desc='a**b',
 define='lambda a,b: pow_rev(b,a)'
)

