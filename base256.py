
# express n as term using n0-n256, ad(), mu() and pow()
def base256(n):
    converted=''
    exp=0
    while n:
        m = n % 256
        if exp <= 256:
            expr_exp='n'+str(exp)
        else:
            expr_exp=base256(exp)
        if m:
            m=str(m)
            add='mu(n'+m+',pow(n256,'+expr_exp+'))'
            if converted:
                converted='ad('+converted+','+add+')'
            else:
                converted=add
        n = n / 256
        exp+=1
    return converted

# express n as formulae using n0-n256, ad(), mu()
def base256_formula(n,ind,formulae,freevariables):
    converted=''
    numbers={}
    last='n0'
    for i in range(1,257):
        mi=ind.new()
        freevariables.append(mi)
        numbers[i]=mi
        formulae.append(mi+'=succ('+last+')')
        last=mi

    vi=numbers[1]
    while n:
        m = n % 256
        if m:
            add='mu('+numbers[m]+','+vi+')'
            if converted:
                converted='ad('+converted+','+add+')'
            else:
                converted=add
        n = n / 256
        if n:
            vi1=ind.new()
            freevariables.append(vi1)
            formulae.append(vi1+'=mu('+numbers[256]+','+vi+')')
            vi=vi1
    vi=ind.new()
    freevariables.append(vi)
    formulae.append(vi+'='+converted)
    return vi
