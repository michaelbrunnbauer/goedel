
import sys

# goedel number of a binary string (e.g. ASCII) without leading null character
def gn(s):
    assert type(s)==str
    number=0
    for c in s:
        number=number << 8
        number+=ord(c)
    return number

# optimized version for larger strings
chunksize=65536
def gn_chunked(s):
    assert type(s)==str
    l=len(s)
    if l <= chunksize:
        return gn(s)
    end=chunksize
    currentchunksize=chunksize
    number=0
    while True:
        chunk=s[end-currentchunksize:end]
        n=gn(chunk)
        number += n << ((l-end)*8)
        if end==l:
            break
        end+=currentchunksize
        if end > l:
            currentchunksize-=(end-l)
            end=l
    return number

# reverse of goedelnumber()
def goedelstring(n):
    s=""
    while n:
        n1=n/256
        s=chr(n-n1*256)+s
        n=n1
    return s
