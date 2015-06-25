# author   : Johann-Mattis List
# email    : mattis.list@uni-marburg.de
# created  : 2015-06-23 15:30
# modified : 2015-06-23 15:30
"""
<++>
"""

__author__="Johann-Mattis List"
__date__="2015-06-23"

from lingpyd import *

tr = Tree('(((a,b)ab,(c,d)cd)abcd,e)abcde;')

words = dict(
        a = 'tsa:n',
        b = 'tu:þ',
        c = 'dente',
        d = 'dã',
        ab = 'tanþ',
        cd = 'dente',
        abcd = 'dont',
        e = 'dint',
        abcde = 'dunt'
        )
txt = '<ul>{0}\n</ul>'
depth = -1
tlen = len(tr.getNodesDict())
pred = -1
for i,t in enumerate(tr.preorder()):
    n = t.Name
    v = words[n]
    
    try:
        d = tr.getDistanceToRoot(n)
    except AttributeError:
        d = 0
    print(n,d,pred,txt)
    contentX = '\n'+d * '  ' + '  <li>'+v+'</li>'
    if t.Children and d > pred:
        content = contentX+'\n'+d * '  ' + '  <ul>{0}\n'
        #content += '\n'+d * '  ' + '  </ul>'
        txt = txt.format(content)
    elif t.Children and d < pred:
        content = '\n' + (d+1) * '  '+'</ul>'
        content += '\n' + d * '  '+'x'+contentX
        content += '\n'+d * '  ' + '  <ul>{0}\n'#+ d * '  '+'  </ul>'
        txt = txt.format(content)
    else:
        content = contentX + '{0}'
        txt = txt.format(content)
    pred = d
    
print(txt)

txt = "{abcde}"
queue = [tr]
while queue:
    nn = queue.pop(0)
    if nn.Children:
        queue += nn.Children

    name = nn.Name
    v = words[name]
    try:
        d = tr.getDistanceToRoot(name)
    except:
        d = 0

    
    if True: #nn.Children:
        nv = '\n'+d * '  '
        nv += '<ul>\n'
    else:
        nv = '\n'
    nv += d * '  '+'<li>'+v+'\n'+''.join(['{'+n.Name+'}' for n in
        nn.Children])

    #nv += d * '  '+'<li>'+v+'\n'+''.join(['{'+n.Name+'}' for n in
    #    nn.Children])
    nv += '\n'+d * '  ' +'</li>\n'
    if True: #nn.Children:
        nv += d * '  '+'</ul>'
    txt = txt.replace('{'+name+'}',nv)
print(txt)

with open('test.html','w') as f:
    f.write(txt)
