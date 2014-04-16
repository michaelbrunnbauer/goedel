# classes to generate primitive recursive functions

import parseterm

class configuration(object):
    __slots__ = 'fastfunctions','debugfunctions','caching','symbols','functions','globals','optimize'

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
        # default is no optimization for and_f/or_f
        self.optimize=False

        self.functions=[]
        self.symbols=set(['succ'])
        for x in range(257):
            self.symbols.add('n'+str(x))

class basefunction(object):
    def __init__(self,*args,**kwargs):
        self._cache = {}
        self._ser = 0
        self._cache_size=100000
        self.init(*args,**kwargs)
        if self.fast is not None:
            self.fast_f=self.getf(self.fast,reformat=False)
        else:
            self.fast_f=None
        if self.asserts is not None:
            self.asserts_f=self.getf(self.asserts,reformat=False)
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

        if self.fast is not None and (self.config.fastfunctions==True or self.name in self.config.fastfunctions):
            return self.fast_f(*args)
        else:
            result=self.call(*args)

        if self.config.caching:
            self.cache_put(args,result)

        return result

    # get eval of source of lambda function with
    # recursive_<name>(<firstparameter>,...) replaced by <name>(...)
    def getf(self,s,reformat=True,optimize=False):
        if reformat:
            params,source=self.lambdasource(s)
            parsedterm=parseterm.parseterm(source)
            assert parsedterm is not None,source
            s=parseterm.reformat(parsedterm,optimizeandor=optimize)
            s='lambda '+','.join(params)+': '+s
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
        self.define_f_opt=self.getf(define,optimize=True)
        self.fast=fast
        self.asserts=asserts
        self.checksymbols(define)
        self.addsymbol(self.name)

    def call(self,*args):
        if self.config.optimize:
            return self.define_f_opt(*args)
        else:
            return self.define_f(*args)

    def definition(self,formal=False):
        rueck=''
        params,source=self.lambdasource(self.define)
        if formal:
            for param in params:
                rueck+='!'+param+':'
        params=','.join(params)
        rueck+=self.name+'('+params+')='+source
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
        self.zero_f_opt=self.getf(zero,optimize=True)
        self.next=next
        self.next_f=self.getf(next)
        self.next_f_opt=self.getf(next,optimize=True)
        self.fast=fast
        self.asserts=asserts
        self.checksymbols(zero)
        self.addsymbol(self.name)
        self.checksymbols(next)

    def call(self,*args):
        n=args[0]
        if n==0:
            args=args[1:]
            if self.config.optimize:
                return self.zero_f_opt(*args)
            else:
                return self.zero_f(*args)
        else:
            # we could compute n-1 with succ(), == and forward counting
            # recursion here but this seems pointless
            args=(n-1,) + args[1:]
            if self.config.optimize:
                return self.next_f_opt(*args)
            else:
                return self.next_f(*args)

    def definition(self,formal=False):
        rueck=''
        zeroparams,zerosource=self.lambdasource(self.zero)
        nextparams,nextsource=self.lambdasource(self.next)
        assert zeroparams==nextparams[1:],(zeroparams,nextparams)
        firstparam=nextparams[0]
        restparams=','.join(nextparams[1:])
        if restparams:
            restparams=','+restparams
        if formal:
            for param in zeroparams:
                rueck+='!'+param+':'
        rueck+=self.name+'(n0'+restparams+')='+zerosource+'\n'
        if formal:
            for param in nextparams:
                rueck+='!'+param+':'
        rueck+=self.name+'(succ('+firstparam+')'+restparams+')='+nextsource
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
        self.max_f_opt=self.getf(max,optimize=True)
        self.relation=relation
        self.relation_f=self.getf(relation)
        self.relation_f_opt=self.getf(relation,optimize=True)
        self.fast=fast
        self.asserts=asserts
        self.checksymbols(max)
        self.checksymbols(relation)
        self.addsymbol(self.name)

    def call(self,*args):
        if self.config.optimize:
            m=self.max_f_opt(*args)
        else:
            m=self.max_f(*args)
        x = 0
        while x <= m:
            if self.config.optimize:
                result=self.relation_f_opt(x,*args)
            else:
                result=self.relation_f(x,*args)
            assert type(result)==int
            assert result in (1,0)
            if result:
                return x
            x+=1
        return 0

    def definition(self,formal=False):
        rueck=''

        params,source=self.lambdasource(self.relation)
        assert len(params)
        firstparam=params[0]
        restparams=','.join(params[1:])
        if restparams:
            restparams=','+restparams   

        if formal:
            for param in params:
                rueck+='!'+param+':'
        rueck+='relation_'+self.name+'('+firstparam+restparams+')='+source+'\n'
        if formal:
            for param in params[1:]:
                rueck+='!'+param+':'
        rueck+='argmin_'+self.name+'(n0'+restparams+')=n0\n'
        if formal:
            for param in params:
                rueck+='!'+param+':'
        rueck+='argmin_'+self.name+'(succ('+firstparam+')'+restparams+')='
        rueck+='ifzero(argmin_'+self.name+'('+firstparam+restparams+'),cond(relation_'+self.name+'(succ('+firstparam+')'+restparams+'),succ('+firstparam+'),n0))\n'
        maxparams,maxsource=self.lambdasource(self.max)
        maxparams=','.join(maxparams)
        if maxparams:
            assert ','+maxparams==restparams
        else:
            assert maxparams==restparams
        if formal:
            for param in params[1:]:
                rueck+='!'+param+':'
        rueck+=self.name+'('+maxparams+')=argmin_'+self.name+'('+maxsource+restparams+')'
        return rueck

# see explanation contained in / printed by printdefinitions
class recursive_relation(basefunction):

    def init(self,config,name,desc,zero,relation,fast=None,asserts=None):
        assert zero and next
        self.config=config
        self.name=name
        self.desc=desc
        self.zero=zero
        self.zero_f=self.getf(zero)
        self.zero_f_opt=self.getf(zero,optimize=True)
        self.relation=relation
        self.relation_f=self.getf(relation)
        self.relation_f_opt=self.getf(relation,optimize=True)
        self.fast=fast
        self.asserts=asserts
        self.checksymbols(zero)
        self.checksymbols(relation)
        self.addsymbol(self.name)

    def call(self,*args):
        n=args[0]
        if n==0:
            args=args[1:]
            if self.config.optimize:
                result=self.zero_f_opt(*args)
            else:
                result=self.zero_f(*args)
            assert result in (0,1),result
            return result
        else:
            args+=(None,)
            if self.config.optimize:
                result=self.relation_f_opt(*args)
            else:
                result=self.relation_f(*args)
            assert result in (0,1),result
            return result

    def definition(self,formal=False):
        zeroparams1,zerosource=self.lambdasource(self.zero)
        relparams1,relsource=self.lambdasource(self.relation)
        assert len(relparams1) == len(zeroparams1)+2
        assert relparams1[1:-1] == zeroparams1

        firstparam=relparams1[0]
        lastparam=relparams1[-1]
        zeroparams=self.plist(zeroparams1)
        if zeroparams:
            zeroparams=','+zeroparams
        myparams1=relparams1[:-1]
        myparams=self.plist(myparams1)
        relparams=self.plist(relparams1)
        rueck=''
        if formal:
            for param in relparams1:
                rueck+='!'+param+':'
        rueck+='f_'+self.name+'('+relparams+')='+relsource+'\n'
        if formal:
            for param in zeroparams1:
                rueck+='!'+param+':'
        rueck+='h_'+self.name+'(n0'+zeroparams+')='+zerosource+'\n'
        if formal:
            for param in myparams1:
                rueck+='!'+param+':'
        rueck+='h_'+self.name+'(succ('+firstparam+')'+zeroparams+')=plus(h_'+self.name+'('+myparams+'),mul(f_'+self.name+'(succ('+firstparam+')'+zeroparams+',h_'+self.name+'('+myparams+')),pow(n2,succ('+firstparam+'))))\n'
        if formal:
            for param in myparams1:
                rueck+='!'+param+':'
        rueck+=self.name+'('+myparams+')=bitset(h_'+self.name+'('+myparams+'),'+firstparam+')'
        return rueck

    # definition of recursive_r(y,a,...). separate because may be printed
    # earlier
    def definition1(self,formal=True):
        relparams,relsource=self.lambdasource(self.relation)
        params=[relparams[-1]]+relparams[:-1]
        rueck=''
        if formal:
            for param in params:
                rueck+='!'+param+':'
        rueck+='recursive_'+self.name+'('+self.plist(params)+')=bitset('+params[0]+','+params[1]+')'
        return rueck

# see explanation contained in / printed by printdefinitions
class recursive_function(basefunction):

    def init(self,config,name,desc,resultlen,zero,function,fast=None,asserts=None):
        assert zero and next
        self.config=config
        self.name=name
        self.desc=desc

        self.resultlen=resultlen
        self.resultlen_f=self.getf(resultlen)
        self.resultlen_f_opt=self.getf(resultlen,optimize=True)
        self.name_bitstart='bitstart_'+self.name
        params,source=self.lambdasource(resultlen)
        source='lambda '+','.join(params)+': plus('+source+','+self.name_bitstart+'('+','.join(params)+'))'

        if len(params)==1:
            source0='lambda: n0'
        else:
            source0='lambda '+','.join(params[1:])+': n0'
        self.bitstart_f=primitive_recursive_function(self.config,
         name=self.name_bitstart,
         desc='',
         zero=source0,
         next=source
        )
        popv=self.config.functions.pop(-1)
        assert popv.name == self.name_bitstart,popv

        self.zero=zero
        self.zero_f=self.getf(zero)
        self.zero_f_opt=self.getf(zero,optimize=True)
        self.function=function
        self.function_f=self.getf(function)
        self.function_f_opt=self.getf(function,optimize=True)
        self.fast=fast
        self.asserts=asserts
        self.checksymbols(zero)
        self.checksymbols(function)
        self.addsymbol(self.name)

    def call(self,*args):
        n=args[0]
        if n==0:
            if self.config.optimize:
                bits_this=self.resultlen_f_opt(*args)
            else:
                bits_this=self.resultlen_f(*args)
            args=args[1:]
            if self.config.optimize:
                result=self.zero_f_opt(*args)
            else:
                result=self.zero_f(*args)
            assert result.bit_length() <= bits_this,(result.bit_length(),bits_this)
            return result
        else:
            if self.config.optimize:
                bits_this=self.resultlen_f_opt(*args)
            else:
                bits_this=self.resultlen_f(*args)
            args+=(None,)
            if self.config.optimize:
                result=self.function_f_opt(*args)
            else:
                result=self.function_f(*args)
            assert result.bit_length() <= bits_this,(result.bit_length(),bits_this)
            return result

    def definition(self,formal=False):
        zeroparams1,zerosource=self.lambdasource(self.zero)
        funcparams1,funcsource=self.lambdasource(self.function)
        assert len(funcparams1) == len(zeroparams1)+2
        assert funcparams1[1:-1] == zeroparams1

        firstparam=funcparams1[0]
        lastparam=funcparams1[-1]
        zeroparams=self.plist(zeroparams1)
        if zeroparams:
            zeroparams=','+zeroparams
        myparams1=funcparams1[:-1]
        myparams=self.plist(myparams1)
        funcparams=self.plist(funcparams1)

        rparams=[funcparams1[-1]]+funcparams1[:-1]
        rparams1=rparams[2:]
        rparams1=','.join(rparams1)
        if rparams1:
            rparams1=','+rparams1

        rueck=''
        if formal:
            for param in funcparams1:
                rueck+='!'+param+':'
        rueck+='f_'+self.name+'('+funcparams+')='+funcsource+'\n'
        if formal:
            for param in zeroparams1:
                rueck+='!'+param+':'
        rueck+='h_'+self.name+'(n0'+zeroparams+')='+zerosource+'\n'
        if formal:
            for param in myparams1:
                rueck+='!'+param+':'
        rueck+='h_'+self.name+'(succ('+firstparam+')'+zeroparams+')=plus(h_'+self.name+'('+myparams+'),mul(f_'+self.name+'(succ('+firstparam+')'+zeroparams+',h_'+self.name+'('+myparams+')),pow(n2,'+self.name_bitstart+'(succ('+rparams[1]+')'+rparams1+'))))\n'
        if formal:
            for param in myparams1:
                rueck+='!'+param+':'
        rueck+=self.name+'('+myparams+')=recursive_'+self.name+'(h_'+self.name+'('+myparams+'),'+myparams+')'
        return rueck


    def definition1(self,formal=False):
        funcparams1,funcsource=self.lambdasource(self.function)
        rparams=[funcparams1[-1]]+funcparams1[:-1]
        rparams1=rparams[2:]
        rparams1=','.join(rparams1)
        if rparams1:
            rparams1=','+rparams1

        rueck=self.bitstart_f.definition(formal=formal)+'\n'
        if formal:
            for param in rparams:
                rueck+='!'+param+':'
        rueck+='recursive_'+self.name+'('+self.plist(rparams)+')=bitslice('+rparams[0]+','+self.name_bitstart+'('+self.plist(rparams[1:])+'),acfull('+self.name_bitstart+'(succ('+rparams[1]+')'+rparams1+')))'
        return rueck
