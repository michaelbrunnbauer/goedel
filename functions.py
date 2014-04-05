# classes to generate primitive recursive functions

# todo:
# work with getpartof...()

class configuration(object):
    __slots__ = 'fastfunctions','debugfunctions','caching','symbols','functions','globals'

    def __init__(self,globals):
        self.globals=globals
        # set to set of names or True to use all available fast variants
        # default is to compute all the hard way
        self.fastfunctions=set()
        # set to set of names or True to debug all calls
        # default is debugging for no function
        self.debugfunctions=set()
        # default is no caching
        self.caching=False

        self.functions=[]
        self.symbols=set(['succ'])
        for x in range(256):
            self.symbols.add(str(x))

class basefunction(object):
    def __init__(self,*args,**kwargs):
        self._cache = {}
        self._ser = 0
        self._cache_size=100000
        self.init(*args,**kwargs)
        if self.fast is not None:
            self.fast_f=self.getf(self.fast)
        else:
            self.fast_f=None
        if self.asserts is not None:
            self.asserts_f=self.getf(self.asserts)
        else:
            self.asserts_f=None
        self.config.functions.append(self)
        assert self.config is not None and self.name is not None
        # may contain consistency checks
        self.definition()

    def __call__(self,*args):
        if self.config.caching:
            result=self.cache_get(args)
            if result is not None:
                return result

        if self.config.debugfunctions==True or self.name in self.config.debugfunctions:
            print self.name,args

        for arg in args:
            if arg is not None:
                assert type(arg) in (int,long),(self.name,args)

        if self.asserts is not None:
            assert self.asserts_f(*args),(self.name,args)

        if self.fast is not None:
            if self.config.fastfunctions==True or self.name in self.config.fastfunctions:
                return self.fast_f(*args)

        result=self.call(*args)

        if self.config.caching:
            self.cache_put(args,result)

        return result

    # get eval of source of lambda function with
    # recursive_<name>(<firstparameter>,...) replaced by <name>(...)
    def getf(self,s):
        while True:
            pos=s.find('recursive_',0)
            if pos==-1:
                break
            pos1=s.find('(',pos)
            assert pos1>pos
            pos2=s.find(',',pos)
            assert pos2>pos1
            fname=s[pos+10:pos1]
            s=s[:pos]+fname+'('+s[pos2+1:]
        return eval(s,self.config.globals)

    # get parameters and definition from source of lambda function
    def lambdasource(self,s):
        s=s.strip()
        s=s.split()
        assert len(s) > 1
        if s[0].endswith(':'):
            params=[]
            s=' '.join(s[1:])
        elif s[1].endswith(':'):
            params=s[1][:-1].split(',')
            for param in params:
                assert param,params
            s=' '.join(s[2:])
        else:
            assert False,s

        if s.endswith(','):
            s=s[:-1]
        return params,s

    def addsymbol(self,s):
        assert s not in self.config.symbols
        self.config.symbols.add(s)

    # check that a symbol is defined
    def checksymbol(self,params,s):
        if not s or s in params:
            return
        # FIXME: this is ugly
        if s.startswith('recursive_'):
            return
        assert s in self.config.symbols,s

    # check that all symbols in a lambda function source are defined or
    # parameters of the function
    def checksymbols(self,source):
        params,s=self.lambdasource(source)
        symbol=''
        for x in s:
            if x in ('(',')',','):
                self.checksymbol(params,symbol)
                symbol=''
            else:
                symbol+=x
        self.checksymbol(params,symbol)

    def cache_get(self,k):
        v = self._cache.get(k)
        if v is None:
            return None
        v = v[1]
        self._cache[k] = self._ser, v
        self._ser += 1
        return v

    def cache_put(self,k, v):
        self._cache[k] = self._ser, v
        self._ser += 1
        if len(self._cache) >= self._cache_size * 2:
            for k in list(self._cache):
                ser = self._cache[k][0]
                if self._ser - ser > self._cache_size:
                    del self._cache[k]

    def plist(self,params):
        return ','.join(params)

    def definition_intro(self):
        rueck='Definition of '+self.name
        if self.desc:
            rueck+=' ('+self.desc+')'
        rueck+=':'
        if self.asserts is not None:
            asparams,assource=self.lambdasource(self.asserts)
            rueck+='\nPython asserts: '+assource
        if self.fast is not None:
            fastparams,fastsource=self.lambdasource(self.fast)
            rueck+='\nPython fast computation: '+fastsource
        return rueck

# function defined by expression define(...)
class basic_function(basefunction):

    def init(self,config,name,desc,define,fast=None,asserts=None):
        assert define
        self.config=config
        self.name=name
        self.desc=desc
        self.define=define
        self.define_f=self.getf(define)
        self.fast=fast
        self.asserts=asserts
        self.checksymbols(define)
        self.addsymbol(self.name)

    def call(self,*args):
        return self.define_f(*args)

    def definition(self):
        rueck=''
        params,source=self.lambdasource(self.define)
        params=','.join(params)
        rueck+=self.name+'('+params+') = '+source
        return rueck

# function f defined by primitive recursion
# zero = value for f(0,...) (first parameter omitted)
# next = value for f(n+1,...) (can call f(n,...))
# the first parameter does not have to be named n
class primitive_recursive_function(basefunction):

    def init(self,config,name,desc,zero,next,fast=None,asserts=None):
        assert zero and next
        self.config=config
        self.name=name
        self.desc=desc
        self.zero=zero
        self.zero_f=self.getf(zero)
        self.next=next
        self.next_f=self.getf(next)
        self.fast=fast
        self.asserts=asserts
        self.checksymbols(zero)
        self.addsymbol(self.name)
        self.checksymbols(next)

    def call(self,*args):
        n=args[0]
        if n==0:
            args=args[1:]
            return self.zero_f(*args)
        else:
            # we could compute n-1 with succ(), == and forward counting
            # recursion here but this seems pointless
            args=(n-1,) + args[1:]
            return self.next_f(*args)

    def definition(self):
        rueck=''
        zeroparams,zerosource=self.lambdasource(self.zero)
        nextparams,nextsource=self.lambdasource(self.next)
        assert zeroparams==nextparams[1:],(zeroparams,nextparams)
        firstparam=nextparams[0]
        restparams=','.join(nextparams[1:])
        if restparams:
            restparams=','+restparams
        rueck+=self.name+'(0'+restparams+') = '+zerosource+'\n'
        rueck+=self.name+'('+firstparam+'+1'+restparams+') = '+nextsource
        return rueck

# returns the smallest x <= max(...) for which relation(x,...) == 1
class argmin_function(basefunction):

    def init(self,config,name,desc,max,relation,fast=None,asserts=None):
        assert relation
        self.config=config
        self.name=name
        self.desc=desc
        self.max=max
        self.max_f=self.getf(max)
        self.relation=relation
        self.relation_f=self.getf(relation)
        self.fast=fast
        self.asserts=asserts
        self.checksymbols(max)
        self.checksymbols(relation)
        self.addsymbol(self.name)

    def call(self,*args):
        m=self.max_f(*args)
        x = 0
        while x <= m:
            result=self.relation_f(x,*args)
            assert type(result)==int
            assert result in (1,0)
            if result:
                return x
            x+=1
        return 0

    def definition(self):
        rueck=''

        params,source=self.lambdasource(self.relation)
        assert len(params)
        firstparam=params[0]
        restparams=','.join(params[1:])
        if restparams:
            restparams=','+restparams   

        rueck+='relation_'+self.name+'('+firstparam+restparams+') = '+source+'\n'
        rueck+='argmin_'+self.name+'(0'+restparams+') = 0\n'
        rueck+='argmin_'+self.name+'('+firstparam+'+1'+restparams+') = '
        rueck+='ifzero(argmin_'+self.name+'('+firstparam+restparams+'),cond(relation_'+self.name+'(succ('+firstparam+')'+restparams+'),succ('+firstparam+'),0))\n'
        maxparams,maxsource=self.lambdasource(self.max)
        maxparams=','.join(maxparams)
        if maxparams:
            assert ','+maxparams==restparams
        else:
            assert maxparams==restparams
        rueck+=self.name+'('+maxparams+') = argmin_'+self.name+'('+maxsource+restparams+')'
        return rueck

# Assume you want to define a primitive recursive relation r(x) like this:
# r(0) = 1 <-> ...
# r(x) = 1 <-> ... or ( r(a) and r(b) and ... ) where a,b < x
# This cannot be done with the primitive recursion scheme where
# r(x+1,...) is defined only in terms of r(x,...) - not some r(y,...) (y < x).
#
# This can be solved by defining a primitive recursive h(x) so that 
# r(x) <-> bit x of h(x) is set:
# h(0) = 1 <-> ...
# h(x+1) = h(x) + f(x+1,h(x))*(2**(x+1))
# recursive_r(y,x) = bitset(y,x)
# f(x,y) = 1 <-> ... or ( recursive_r(y,a) and recursive_r(y,b) and ... )
# where a,b < x
#
# This class will define h(x,...), and r(x,...) = bitset(h(x,...),x)
# You just have to specify h(0,...) and f(x,...,y) as functions with result 0
# or 1 and you have to define recursive_r(y,a,...) as bitset(y,a).
# You can use calls to recursive_r(y,a,...) in the definition of
# f(x,...,y). The computation will not use h(x,...) but replace calls to
# recursive_r(y,a,...) with calls to r(a,...) to stay feasible.
class recursive_function(basefunction):

    def init(self,config,name,desc,zero,relation,fast=None,asserts=None):
        assert zero and next
        self.config=config
        self.name=name
        self.desc=desc
        self.zero=zero
        self.zero_f=self.getf(zero)
        self.relation=relation
        self.relation_f=self.getf(relation)
        self.fast=fast
        self.asserts=asserts
        self.checksymbols(zero)
        self.checksymbols(relation)
        self.addsymbol(self.name)

    def call(self,*args):
        n=args[0]
        if n==0:
            args=args[1:]
            result=self.zero_f(*args)
            assert result in (0,1),result
            return result
        else:
            args+=(None,)
            result=self.relation_f(*args)
            assert result in (0,1),result
            return result

    def definition(self):
        zeroparams,zerosource=self.lambdasource(self.zero)
        relparams,relsource=self.lambdasource(self.relation)
        assert len(relparams) == len(zeroparams)+2
        assert relparams[1:-1] == zeroparams

        firstparam=relparams[0]
        lastparam=relparams[-1]
        zeroparams=self.plist(zeroparams)
        if zeroparams:
            zeroparams=','+zeroparams
        myparams=self.plist(relparams[:-1])
        relparams=self.plist(relparams)
        rueck='f_'+self.name+'('+relparams+') = '+relsource+'\n'
        rueck+='h_'+self.name+'(0'+zeroparams+') = '+zerosource+'\n'
        rueck+='h_'+self.name+'('+firstparam+'+1'+zeroparams+') = plus(h_'+self.name+'('+myparams+'),mul(f_'+self.name+'(succ('+firstparam+')'+zeroparams+',h_'+self.name+'('+myparams+')),pow(2,succ('+firstparam+'))))\n'
        rueck+=self.name+'('+myparams+') = bitset(h_'+self.name+'('+myparams+'),'+firstparam+')'
        return rueck

    # definition of recursive_r(y,a,...). separate because may be printed
    # earlier
    def definition1(self):
        relparams,relsource=self.lambdasource(self.relation)
        params=[relparams[-1]]+relparams[:-1]
        rueck='recursive_'+self.name+'('+self.plist(params)+') = bitset('+params[0]+','+params[1]+')'
        return rueck
