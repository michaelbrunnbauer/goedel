
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
