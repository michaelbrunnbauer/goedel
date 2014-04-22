# classes to generate primitive recursive functions

from StringIO import StringIO

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
        self.symbols=set(['sc','ad','mu'])
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
            params1=s[1][:-1].split(',')
            params=[]
            for param in params1:
                if param:
                    assert param not in ('sc','ad','mu'),s
                    params.append(param)
            s=' '.join(s[2:])
        else:
            assert False,s

        if s.endswith(','):
            s=s[:-1]
        return params,s

    def addsymbol(self,s):
        assert s not in self.config.symbols,s
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

    def getfunction(self,name):
        for f in self.config.functions:
            if f.name==name:
                return f
        assert False,name

    # return variable for term rm(a,b) = remainder of a / b
    # necessary assertions about variable are added to formulae
    # variables needing existential quantification are added to freevariables
    # ind is a structure holding the biggest variable index
    def getterm_rm(self,params,ind,formulae,freevariables):
        assert len(params)==2
        for param in params:
            assert parseterm.isbasicterm(param)
        id=ind.new()
        freevariables.append(id)
        ic=ind.new()
        zi=ind.new()
        rueck='~!'+ic+':!'+zi+':~('+params[0]+'=ad(mu('+params[1]+','+ic+'),'+id+')&ad('+id+',sc('+zi+'))='+params[1]+')'
        formulae.append(rueck)
        return id

    # return variable for term si(a,m,i) = rm(a,m*(i+1)+1)
    # necessary assertions about variable are added to formulae
    # variables needing existential quantification are added to freevariables
    # ind is a structure holding the biggest variable index
    def getterm_si(self,params,ind,formulae,freevariables):
        assert len(params)==3
        for param in params:
            assert parseterm.isbasicterm(param)
        y='sc(mu('+params[1]+',sc('+params[2]+')))'
        return self.getterm_rm([params[0],y],ind,formulae,freevariables)

    # return term/variable for parsed term
    # necessary assertions about variable are added to formulae
    # variables needing existential quantification are added to freevariables
    # ind is a structure holding the biggest variable index
    def getterm1(self,parsedterm,formulae,ind,freevariables):
        lcname,tlist=parsedterm
        if tlist is None:
            return lcname

        if lcname in ('sc','ad','mu'):
            rueck=lcname+'('
            for term in tlist:
                rueck+=self.getterm1(term,formulae,ind,freevariables)+','
            rueck=rueck[:-1]+')'
            return rueck
        else:
            params=[]
            for term in tlist:
                params.append(self.getterm1(term,formulae,ind,freevariables))
            if lcname=='si':
                return self.getterm_si(params,ind,formulae,freevariables)
            else:
                f=self.getfunction(lcname)
                return f.getterm(params,ind,formulae,freevariables)

    # return term/variable for lambda expression l
    # necessary assertions about variable are added to formulae
    # variables needing existential quantification are added to freevariables
    # ind is a structure holding the biggest variable index
    def getterm2(self,l,params,ind,formulae,freevariables):
        params1,source=self.lambdasource(l)
        assert len(params)==len(params1)
        parsedterm=parseterm.parseterm(source)
        parsedterm=parseterm.replaceparams(parsedterm,params1,params)
        return self.getterm1(parsedterm,formulae,ind,freevariables)

    # return formula composed of conjunction of formulae with existential 
    # quantification for a variables in freevariables
    def composeformula(self,formulae,freevariables):
        assert formulae
        rueck=StringIO()
        rueck.write('~')
        while freevariables:
            v=freevariables.pop()
            rueck.write('!'+v+':')
        rueck.write('~')
        rueck.write('('*(len(formulae)-1))
        first=True
        while formulae:
            formula=formulae.pop()
            if first:
                first=False
                rueck.write(formula)
            else:
                rueck.write('&'+formula+')')
        return rueck.getvalue()

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

    def definition(self):
        rueck=''
        params,source=self.lambdasource(self.define)
        params=','.join(params)
        rueck+=self.name+'('+params+')='+source
        return rueck

    def getterm(self,params,ind,formulae,freevariables):
        return self.getterm2(self.define,params,ind,formulae,freevariables)

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
            # we could compute n-1 with sc(), == and forward counting
            # recursion here but this seems pointless
            args=(n-1,) + args[1:]
            if self.config.optimize:
                return self.next_f_opt(*args)
            else:
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
        rueck+=self.name+'(n0'+restparams+')='+zerosource+'\n'
        rueck+=self.name+'(sc('+firstparam+')'+restparams+')='+nextsource
        return rueck

    def getterm(self,params,ind,formulae,freevariables):
        assert parseterm.isbasicterm(params[0]),params[0]
        ai=ind.new()
        mi=ind.new()
        freevariables.append(ai)
        freevariables.append(mi)
        si1=self.getterm_si([ai,mi,'n0'],ind,formulae,freevariables)
        si2=self.getterm_si([ai,mi,params[0]],ind,formulae,freevariables)
        ii=ind.new()
        myformulae=[]
        myfreevariables=[]
        si3=self.getterm_si([ai,mi,'sc('+ii+')'],ind,myformulae,myfreevariables)
        f0=self.getterm2(self.zero,params[1:],ind,myformulae,myfreevariables)
        
        nextparams,nextsource=self.lambdasource(self.next)
        nextcall=self.name+'('+','.join(nextparams)+')'
        nextsource=nextsource.replace(nextcall,'si('+ai+','+mi+','+ii+')')
        assert self.name+'(' not in nextsource,(self.name,nextsource)
        nextl='lambda '+','.join(nextparams)+': '+nextsource

        fx=self.getterm2(nextl,params,ind,myformulae,myfreevariables)

        myformulae.append(si3+'='+fx)
        rueck=self.composeformula(myformulae,myfreevariables)

        zi=ind.new()
        smallerf='~!'+zi+':~ad('+ii+',sc('+zi+'))='+params[0]

        rueck='!'+ii+':~('+smallerf+'&~'+rueck+')'
        formulae.append(rueck)
        formulae.append(si1+'='+f0)
        return si2

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
        self.me=self.gendefinition()

    def gendefinition(self):
        params,source=self.lambdasource(self.relation)
        assert len(params)
        firstparam=params[0]
        restparams=','.join(params[1:])
        if restparams:
            restparams=','+restparams

        relation=basic_function(self.config,
         name='relation_'+self.name,
         desc='part of definition for '+self.name,
         define='lambda '+firstparam+restparams+': '+source)

        argmin=primitive_recursive_function(self.config,
         name='argmin_'+self.name,
         desc='part of definition for '+self.name,
         zero='lambda '+restparams+': n0',
         next='lambda '+firstparam+restparams+': ifzero(argmin_'+self.name+'('+firstparam+restparams+'),cond(relation_'+self.name+'(sc('+firstparam+')'+restparams+'),sc('+firstparam+'),n0))')

        maxparams,maxsource=self.lambdasource(self.max)
        maxparams=','.join(maxparams)
        if maxparams:
            assert ','+maxparams==restparams
        else:
            assert maxparams==restparams

        me=basic_function(self.config,
         name=self.name,
         desc=self.desc,
         define='lambda '+maxparams+': argmin_'+self.name+'('+maxsource+restparams+')')
        popv=self.config.functions.pop(-1)
        return me

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

    def definition(self):
        return self.me.definition()

    def getterm(self,params,ind,formulae,freevariables):
        return self.me.getterm(params,ind,formulae,freevariables)

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
        self.me=self.gendefinition()

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

    def gendefinition(self):
        zeroparams1,zerosource=self.lambdasource(self.zero)
        relparams1,relsource=self.lambdasource(self.relation)
        assert len(relparams1) == len(zeroparams1)+2
        assert relparams1[1:-1] == zeroparams1

        params=[relparams1[-1]]+relparams1[:-1]

        firstparam=relparams1[0]
        lastparam=relparams1[-1]
        zeroparams=self.plist(zeroparams1)
        if zeroparams:
            zeroparams=','+zeroparams
        myparams1=relparams1[:-1]
        myparams=self.plist(myparams1)
        relparams=self.plist(relparams1)

        me_recursive=basic_function(self.config,
         name='recursive_'+self.name,
         desc='part of definition for '+self.name,
         define='lambda '+self.plist(params)+': bitset('+params[0]+','+params[1]+')')

        me_f=basic_function(self.config,
         name='f_'+self.name,
         desc='part of definition for '+self.name,
         define='lambda '+relparams+': '+relsource)

        me_h=primitive_recursive_function(self.config,
         name='h_'+self.name,
         desc='part of definition for '+self.name,
         zero='lambda '+zeroparams+': '+zerosource,
         next='lamda '+firstparam+zeroparams+': ad(h_'+self.name+'('+myparams+'),mu(f_'+self.name+'(sc('+firstparam+')'+zeroparams+',h_'+self.name+'('+myparams+')),pow(n2,sc('+firstparam+'))))')

        me=basic_function(self.config,
         name=self.name,
         desc=self.desc,
         define='lambda '+myparams+': bitset(h_'+self.name+'('+myparams+'),'+firstparam+')')
        popv=self.config.functions.pop(-1)
        return me

    def definition(self):
        return self.me.definition()

    def getterm(self,params,ind,formulae,freevariables):
        return self.me.getterm(params,ind,formulae,freevariables)

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
        source='lambda '+','.join(params)+': ad('+source+','+self.name_bitstart+'('+','.join(params)+'))'

        if len(params)==1:
            source0='lambda: n0'
        else:
            source0='lambda '+','.join(params[1:])+': n0'
        self.bitstart_f=primitive_recursive_function(self.config,
         name=self.name_bitstart,
         desc='part of definition for '+self.name,
         zero=source0,
         next=source
        )

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
        self.me=self.gendefinition()

    def gendefinition(self):
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

        me_recursive=basic_function(self.config,
         name='recursive_'+self.name,
         desc='part of definition for '+self.name,
         define='lambda '+self.plist(rparams)+': bitslice('+rparams[0]+','+self.name_bitstart+'('+self.plist(rparams[1:])+'),acfull('+self.name_bitstart+'(sc('+rparams[1]+')'+rparams1+')))')

        me_f=basic_function(self.config,
         name='f_'+self.name,
         desc='part of definition for '+self.name,
         define='lambda '+funcparams+': '+funcsource)

        me_h=primitive_recursive_function(self.config,
         name='h_'+self.name,
         desc='part of definition for '+self.name,
         zero='lambda '+zeroparams+': '+zerosource,
         next='lambda '+firstparam+zeroparams+': ad(h_'+self.name+'('+myparams+'),mu(f_'+self.name+'(sc('+firstparam+')'+zeroparams+',h_'+self.name+'('+myparams+')),pow(n2,'+self.name_bitstart+'(sc('+rparams[1]+')'+rparams1+'))))')

        me=basic_function(self.config,
         name=self.name,
         desc=self.desc,
         define='lambda '+myparams+': recursive_'+self.name+'(h_'+self.name+'('+myparams+'),'+myparams+')')

        popv=self.config.functions.pop(-1)
        return me

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

    def definition(self):
        return self.me.definition()

    def getterm(self,params,ind,formulae,freevariables):
        return self.me.getterm(params,ind,formulae,freevariables)
