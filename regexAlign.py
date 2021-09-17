# regex aligner

# str1 is a regex
# str2 is another string to search in

import re

r = r'convolution[\W:-]*is not a.* crime'
s = r'convolution: --\tis not a fucking crime, but worse'

def regexAlign(regex,text):
    i = 0
    flex = []
    while re.search(r'\[[^\]]*\**\+*\]\+*\**',regex[i:]):
        tmp = re.search(r'\[[^\]]*\**\+*\]\+*\**',regex[i:])
        if regex[i+tmp.span()[0]-1]=='\\':
            i = tmp.span()[1]
            continue
        flex.append(tmp)
        i = flex[-1].span()[1]
    
    
    i = 0
    while re.search(r'\.\+*\**',regex[i:]):
        tmp = re.search(r'\.\+*\**',regex[i:])
        if regex[i+tmp.span()[0]-1]=='\\':
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

    s1,s2 = regtext,text

    scores   = [[0 for i in s2] for k in s1]
    pointers = [[None for i in s2] for k in s1]

    for r in range(1,len(s1)):
        if r in flexpos:
            i  = flexpos.index(r)
            rx = flex[i]
            if flextype[i] == 0:
                for c in range(len(s2)):
                

                    
            continue
        for c in range(1,len(s2)):
            s  = (scores[r-1][c-1]+(1 if regtext[r]==text[c] else -1),
                  scores[r-1][c]-1,
                  scores[r][c-1]-1)
            ms = max(s)
            pt = s.index(ms)
            if ms>0:
                scores[r][c]   = ms
                pointers[r][c] = pt







