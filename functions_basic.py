from functions import *

# we assume 0, succ() and = are symbols of the theory and that 1-255 have been
# defined using succ()

def succ(a):
    return a+1

config=configuration(globals())

ac=primitive_recursive_function(config,
 name='ac',
 desc='antecessor function - with assert for 0',
 zero='lambda: 0',
 next='lambda n: n',
 asserts='lambda n: n!=0'
)

# antecessor function without assert for cases where the antecessor of 0
# (defined as 0) actually has to be computed
acfull=primitive_recursive_function(config,
 name='acfull',
 desc='antecessor function - without assert for 0',
 zero='lambda: 0',
 next='lambda n: n'
)

zero=primitive_recursive_function(config,
 name='zero',
 desc='1 for n=0, else 0',
 zero='lambda: 1',
 next='lambda n: 0'
)

notzero=primitive_recursive_function(config,
 name='notzero',
 desc='0 for n=0, else 1',
 zero='lambda: 0',
 next='lambda n: 1'
)

plus=primitive_recursive_function(config,
 name='plus',
 desc='addition',
 zero='lambda b: b',
 next='lambda a,b: succ(plus(a,b))',
 fast='lambda a,b: a+b'
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

mul=primitive_recursive_function(config,
 name='mul',
 desc='multiplication',
 zero='lambda b: 0',
 next='lambda a,b: plus(mul(a,b),b)',
 fast='lambda a,b: a*b'
)

AND=basic_function(config,
 name='AND',
 desc='logical and',
 define='lambda a,b: mul(notzero(a),notzero(b))'
)

AND3=basic_function(config,
 name='AND3',
 desc='logical and',
 define='lambda a1,a2,a3: AND(a1,AND(a2,a3))'
)

AND4=basic_function(config,
 name='AND4',
 desc='logical and',
 define='lambda a1,a2,a3,a4: AND(a1,AND3(a2,a3,a4))'
)

AND5=basic_function(config,
 name='AND5',
 desc='logical and',
 define='lambda a1,a2,a3,a4,a5: AND(a1,AND4(a2,a3,a4,a5))'
)

AND6=basic_function(config,
 name='AND6',
 desc='logical and',
 define='lambda a1,a2,a3,a4,a5,a6: AND(a1,AND5(a2,a3,a4,a5,a6))'
)

AND7=basic_function(config,
 name='AND7',
 desc='logical and',
 define='lambda a1,a2,a3,a4,a5,a6,a7: AND(a1,AND6(a2,a3,a4,a5,a6,a7))'
)

AND8=basic_function(config,
 name='AND8',
 desc='logical and',
 define='lambda a1,a2,a3,a4,a5,a6,a7,a8: AND(a1,AND7(a2,a3,a4,a5,a6,a7,a8))'
)

AND9=basic_function(config,
 name='AND9',
 desc='logical and',
 define='lambda a1,a2,a3,a4,a5,a6,a7,a8,a9: AND(a1,AND8(a2,a3,a4,a5,a6,a7,a8,a9))'
)

AND10=basic_function(config,
 name='AND10',
 desc='logical and',
 define='lambda a1,a2,a3,a4,a5,a6,a7,a8,a9,a10: AND(a1,AND9(a2,a3,a4,a5,a6,a7,a8,a9,a10))'
)

OR=basic_function(config,
 name='OR',
 desc='logical or',
 define='lambda a,b: notzero(plus(a,b))'
)

OR3=basic_function(config,
 name='OR3',
 desc='logical or',
 define='lambda a1,a2,a3: OR(a1,OR(a2,a3))'
)

OR4=basic_function(config,
 name='OR4',
 desc='logical or',
 define='lambda a1,a2,a3,a4: OR(a1,OR3(a2,a3,a4))'
)

OR5=basic_function(config,
 name='OR5',
 desc='logical or',
 define='lambda a1,a2,a3,a4,a5: OR(a1,OR4(a2,a3,a4,a5))'
)

OR6=basic_function(config,
 name='OR6',
 desc='logical or',
 define='lambda a1,a2,a3,a4,a5,a6: OR(a1,OR5(a2,a3,a4,a5,a6))'
)

OR7=basic_function(config,
 name='OR7',
 desc='logical or',
 define='lambda a1,a2,a3,a4,a5,a6,a7: OR(a1,OR6(a2,a3,a4,a5,a6,a7))'
)

OR8=basic_function(config,
 name='OR8',
 desc='logical or',
 define='lambda a1,a2,a3,a4,a5,a6,a7,a8: OR(a1,OR7(a2,a3,a4,a5,a6,a7,a8))'
)

OR9=basic_function(config,
 name='OR9',
 desc='logical or',
 define='lambda a1,a2,a3,a4,a5,a6,a7,a8,a9: OR(a1,OR8(a2,a3,a4,a5,a6,a7,a8,a9))'
)

OR10=basic_function(config,
 name='OR10',
 desc='logical or',
 define='lambda a1,a2,a3,a4,a5,a6,a7,a8,a9,a10: OR(a1,OR9(a2,a3,a4,a5,a6,a7,a8,a9,a10))'
)

NOT=basic_function(config,
 name='NOT',
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
 next='lambda a,b: cond(b,equal(a,acfull(b)),0)',
 fast='lambda a,b: 1 if a==b else 0'
)

smallereq=basic_function(config,
 name='smallereq',
 desc='a smaller or equal b',
 define='lambda a,b: OR(equal(a,b),smaller(a,b))',
 fast='lambda a,b: 1 if a<=b else 0'
)

div=argmin_function(config,
 name='div',
 desc='division',
 max='lambda a,b: a',
 relation='lambda x,a,b: AND(notzero(smallereq(mul(x,b),a)),zero(smallereq(mul(succ(x),b),a)))',
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
 zero='lambda b: 1',
 next='lambda a,b: mul(b,pow_rev(a,b))',
 fast='lambda a,b: b**a'
)

pow=basic_function(config,
 name='pow',
 desc='a**b',
 define='lambda a,b: pow_rev(b,a)'
)

