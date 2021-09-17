# regex aligner

# str1 is a regex
# str2 is another string to search in

import re

r = r'when [Ii] tasked my mom[, iI]* didnt flinch to fuck .. ass'
s = 'when i asked my, mom, I didn\'t even flinch to fuck an ass'

def regexAlign(regex,text):
    class Flex:
        def __init__(self,match,offset=0):
            self.g = match.group()
            self.s = match.span()[0]+offset,match.span()[1]+offset
        def group(self):
            return self.g
        def span(self):
            return self.s
    
    i = 0
    flex = []
    while re.search(r'\[[^\]]*\**\+*\]\+*\**',regex[i:]):
        tmp = Flex(re.search(r'\[[^\]]*\**\+*\]\+*\**',regex[i:]),i)
        if regex[tmp.span()[0]-1]=='\\':
            i = tmp.span()[1]
            continue
        flex.append(tmp)
        i = flex[-1].span()[1]
    
    i = 0
    while re.search(r'\.\+*\**',regex[i:]):
        tmp = Flex(re.search(r'\.\+*\**',regex[i:]),i)
        if regex[tmp.span()[0]-1]=='\\':
            i = tmp.span()[1]
            continue
        flex.append(tmp)
        i = flex[-1].span()[1]

    snippets = []
    
    if flex:
        snippets.append(regex[:flex[0].span()[0]])
        for i in range(len(flex)-1):
            snippets.append(regex[flex[i].span()[1]:flex[i+1].span()[0]])
        snippets.append(regex[flex[-1].span()[1]:])
    else:
        snippets.append(regex)

    flexpos  = []
    flextype = []
    regtext  = '\x00'

    for i in range(len(snippets)-1):
        regtext += snippets[i] + '*'
        flexpos.append(len(regtext)-1)
        lc = flex[i].group()[-1]
        flextype.append(0 if lc=='*' else (2 if lc=='+' else 1))
    regtext += snippets[-1]

    text = '\x00' + text

    ################################################
    global scores,pointers

    s1,s2 = regtext,text

    scores   = [[0 for i in s2] for k in s1]
    pointers = [[None for i in s2] for k in s1]
    flex     = [f.group() for f in flex]
    R,C,M = 0,0,0

    for r in range(1,len(s1)):
        if r in flexpos:
            i  = flexpos.index(r)
            rx = flex[i]
            if flextype[i] == 1:
                for c in range(len(s2)):
                    mt = 0 if re.search(rx,s2[c]) else -1
                    s  = (scores[r-1][c-1]+mt,
                          scores[r-1][c]-1,
                          scores[r][c-1]-1)
                    ms = max(s)
                    pt = s.index(ms)
                    if ms>0:
                        scores[r][c]   = ms
                        pointers[r][c] = pt
                        if M<=ms: M,R,C = ms,r,c
            elif flextype[i] == 2:
                rx = rx[:-1]
                for c in range(len(s2)):
                    mt = 0 if re.search(rx,s2[c]) else -1
                    s  = (scores[r-1][c-1]+mt,
                          scores[r-1][c]-1,
                          scores[r][c-1]+mt)
                    ms = max(s)
                    pt = s.index(ms)
                    if ms>0:
                        scores[r][c]   = ms
                        pointers[r][c] = pt
                        if M<=ms: M,R,C = ms,r,c
            else:
                rx = rx[:-1]
                for c in range(len(s2)):
                    mt = 0 if re.search(rx,s2[c]) else -1
                    s  = (scores[r-1][c-1]+mt,
                          scores[r-1][c]+mt,
                          scores[r][c-1]+mt)
                    ms = max(s)
                    pt = s.index(ms)
                    if ms>0:
                        scores[r][c]   = ms
                        pointers[r][c] = pt
                        if M<=ms: M,R,C = ms,r,c
        else:
            for c in range(1,len(s2)):
                s  = (scores[r-1][c-1]+(1 if regtext[r]==text[c] else -1),
                      scores[r-1][c]-1,
                      scores[r][c-1]-1)
                ms = max(s)
                pt = s.index(ms)
                if ms>0:
                    scores[r][c]   = ms
                    pointers[r][c] = pt
                    if M<=ms: M,R,C = ms,r,c

    t1,t2 = '',''

    while pointers[R][C] is not None:
        pt = pointers[R][C]
        if pt==0:
            t1,t2 = s1[R]+t1,s2[C]+t2
            R -= 1
            C -= 1
        elif pt==1:
            t1,t2 = s1[R]+t1,'_'+t2
            R -= 1
        elif pt==2:
            t1,t2 = '*'+t1,s2[C]+t2
            C -= 1
    
    return t1,t2
