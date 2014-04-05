
# goedel number of a binary string (e.g. ASCII) without leading null character
def gn(s):
    assert type(s)==str
    number=0
    for c in s:
        number=number * 256
        number+=ord(c)
    return number

# reverse of goedelnumber()
def goedelstring(n):
    s=""
    for i in range(length(n)):
        s+=chr(item(i+1,n))
    return s

