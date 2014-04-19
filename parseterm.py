
def termlist_start_rest(s):
    start=''
    bracketbalance=0
    for c in s:
        if c==',' and bracketbalance==0:
            break
        if c=='(':
            bracketbalance+=1
        if c==')':
            bracketbalance-=1
        start+=c
    if bracketbalance:
        return None,None
    rest=s[len(start)+1:]
    return start,rest

def termlist(s):
    if not s:
        return []
    start,rest=termlist_start_rest(s)
    if not start:
        return []
    result1=parseterm(start)
    if result1 is None:
        return []
    if not rest:
        return [result1]
    result2=termlist(rest)
    if not result2:
        return []
    return [result1]+result2

def isvariable(s):
    if not s:
        return False
    if not s[0].isalpha():
        return False
    for c in s:
         if c.isalpha() and not c.islower():
             return False
         if not c.isalnum() and not c=='_':
             return False
    return True

def parseterm(s):
    if not s:
        return None
    if isvariable(s):
        return (s,None)
    if not s.endswith(')'):
        return None
    pos=s.find('(')
    if pos==-1:
        return None
    part1=s[:pos]
    if not isvariable(part1):
        return None
    part2=termlist(s[pos+1:-1])
    if part2:
        return (part1,part2)
    return None

def reformat(parsedterm,optimizeandor=False):
    if parsedterm[1] is None:
        return parsedterm[0]
    tlist=parsedterm[1]

    if optimizeandor and parsedterm[0].startswith('and_f'):
        rueck='1 if True'
        for term in tlist:
            rueck+=' and ('+reformat(term,optimizeandor=optimizeandor)+')'
        rueck+=' else 0'
        return rueck

    if optimizeandor and parsedterm[0].startswith('or_f'):
        rueck='1 if False'   
        for term in tlist:
            rueck+=' or ('+reformat(term,optimizeandor=optimizeandor)+')'
        rueck+=' else 0'
        return rueck

    if parsedterm[0].startswith('recursive_'):
        rueck=parsedterm[0][10:]+'('
        tlist=tlist[1:]
    else:
        rueck=parsedterm[0]+'('
    for term in tlist:
       rueck+=reformat(term,optimizeandor=optimizeandor)+','
    rueck=rueck[:-1]
    rueck+=')'
    return rueck

# variable generator
#class vindex(object):
#    def __init__(self):
#        self.index=0
#    def new(self):
#        self.index+=1
#        return 'x'+str(self.index)

# alternative variable generator, does not make things much shorter
class vindex(object):
    def __init__(self,donotuse=None):
        self.digits=[0]
        # not strictly necessary
        self.donotuse=set(['sc','ad','mu'])
        if donotuse:
            for v in donotuse:
                self.donotuse.add(v)

    def increment(self,digit):
        a=self.digits[digit]
        a+=1
        if digit==0:
            if a==25:
                self.digits[0]=0
                self.digits.append(0)
            else:
                self.digits[0]=a
        else:
            if a==35:
                self.digits[digit]=0
                self.increment(digit-1)
            else:
                self.digits[digit]=a

    def new(self):
        while True:
            # without n
            chars="abcdefghijklmopqrstuvwxyz0123456789"
            rueck=''
            for digit in self.digits:
                rueck+=chars[digit]
            self.increment(len(self.digits)-1)
            if rueck not in self.donotuse:
                break
        return rueck

def replaceparams(parsedterm,params,paramsnew):
    if parsedterm[1] is None:
        if parsedterm[0] not in params:
            return (parsedterm[0],None)
        i=0
        while i<len(params):
            if params[i]==parsedterm[0]:
                return (paramsnew[i],None)
            i+=1
    tlist1=[]
    for term in parsedterm[1]:
        tlist1.append(replaceparams(term,params,paramsnew))
    return (parsedterm[0],tlist1)

def isbasicterm1(parsedterm):
    if parsedterm is None:
        return False
    lcname,tlist=parsedterm
    if tlist is None:
        return True
    if lcname not in ('sc','ad','mu'):
        return False
    for term in tlist:
        if not isbasicterm1(term):
            return False
    return True

def isbasicterm(s):
    parsedterm=parseterm(s)
    assert parsedterm is not None,s
    return isbasicterm1(parsedterm)

def termvariables(parsedterm):
    lcname,tlist=parsedterm
    if tlist is None:
        return [lcname]
    rueck=[]
    for term in tlist:
        rueck+=termvariables(term)
    return rueck

