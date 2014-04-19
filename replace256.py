
numbers={}
numbers[0]='n0'

for i in range(1,257):
    numbers[i]='sc('+numbers[i-1]+')'

def replace256(instream,outstream):
    word=''
    while True:
        buffer=instream.read(65536)
        if not buffer:
            break
        for c in buffer:
            if not c.isalnum():
                if word and word.startswith('n'):
                    try:
                        number=int(word[1:])
                        assert c in (',',')','&','='),c # c!='('
                        word=numbers[number]
                    except ValueError:
                        pass
                if word:
                    outstream.write(word)
                    word=''
                outstream.write(c)
            else:
                word+=c
