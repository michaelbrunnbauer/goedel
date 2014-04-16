
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
