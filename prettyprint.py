
def termlist(s):
    if not s:
        return []
    result=parseterm(s)
    if result is not None:
        return [result]
    s=s.split(',')
    for i in range(1,len(s)):
        a=','.join(s[:i])
        b=','.join(s[i:])
        result1=parseterm(a)
        if result1 is not None:
            result2=termlist(b)
            if result2:
                return [result1]+result2
    return []

def isvariable(s):
    if not s:
        return False
    for c in s:
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

# this got much too involved
def prettyprint1(parsedterm,indent,forcenl):
    if parsedterm[1] is None:
        return parsedterm[0]
    tlist=parsedterm[1]
    rueck=parsedterm[0]+'('
    nl=parsedterm[0] in ('AND','OR','ifzero','cond') or forcenl
    indentnew=indent+len(parsedterm[0])+1
    if tlist[0][1] is None:
        rueck+=tlist[0][0]
        tlist=tlist[1:]
        if not tlist:
            return rueck+')'
        rueck+=','
        if not nl:
            indentnew+=len(tlist[0][0])+1
    if nl:
        rueck+='\n'+' '*indentnew
    for term in tlist:
        termpp=prettyprint1(term,indentnew,0)+','
        if '\n' in termpp or len(termpp) + indentnew > 79:
            forcenl_new=forcenl-1 if forcenl else forcenl
            termpp=prettyprint1(term,indentnew,forcenl_new)+','
        rueck+=termpp
        if nl:
            rueck+='\n'+' '*indentnew
        else:
            indentnew+=len(termpp)
    if nl:
        rueck=rueck[:-indentnew]
        rueck=rueck[:-1]
    rueck=rueck[:-1]
    rueck+=')'
    if nl:
        rueck+='\n'+' '*len(rueck.split('\n')[-1])
    return rueck

def toobig(s,max):
    for line in s.split('\n'):
        if len(line) > max:
            return True
    return False

def prettyprint0(source,indent):
    s=parseterm(source)
    assert s is not None,source
    forcenl=0
    while True:
        rueck=prettyprint1(s,indent,forcenl)
        if not toobig(rueck,79-indent) or forcenl==20:
            break
        forcenl+=1
    return rueck

def prettyprint(source):
    rueck=''
    for line in source.split('\n'):
        part1,part2 = line.split('=')
        part1+='= '
        part2=part2.strip()
        part2_pp=prettyprint0(part2,len(part1))
        if toobig(part2_pp,79):
            part1+='\n '
            part2_pp=prettyprint0(part2,1)
        rueck+=(part1+part2_pp).strip()+'\n'
    rueck=rueck[:-1]
    return rueck
