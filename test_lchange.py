# author   : Johann-Mattis List
# email    : mattis.list@uni-marburg.de
# created  : 2015-06-24 14:03
# modified : 2015-06-24 14:03
"""
<++>
"""

__author__="Johann-Mattis List"
__date__="2015-06-24"

import numpy as np
from matplotlib import pyplot as plt
import matplotlib as mpl
from lingpyd import *
from lingpyd.compare.phylogeny import PhyBo
from lingpyd.align.sca import *

import json

# we test with aslian
alm = Alignments('basic.qlc')

alm.align()
alm.output('tsv', filename='.tmp', ignore='all')

# we load into phybo
phy = PhyBo('.tmp.tsv', ref='cogid', tree='common_chinese.tre')
phy.analyze()
phy.get_ACS(phy.best_model)


def get_colormap(amount, colormap=mpl.cm.jet):
    """
    Helper function to get a nice color range.
    """

    cfunc = np.array(np.linspace(10,256,amount),dtype='int')
    colors = [mpl.colors.rgb2hex(colormap(cfunc[i])) for i in
            range(amount)]
    return colors

def create_charhist(phy, concept, output='json', debug=False):
    """
    Create character history based on phylogeny object and concept.
    """
    
    # for convenience, get the relevant datapoints
    T = phy.tree
    G = phy.graph[phy.best_model]
    A = phy.acs[phy.best_model]
    E = phy.etd

    # get the paps
    paps = sorted(set([p for p in phy.get_list(
        row=concept,
        flat=True,
        entry='pap'
        )]))
    
    # get the color dict
    cdict = dict(zip(paps, get_colormap(len(paps))))

    # create the dictionary
    D = {}
    order = []
    previous = {}
    
    for t in T.preorder():
        name = t.Name
        node = G.node[name]
        states = [(s[0],s[1]) for s in A[name] if s[1] == concept]
        
        # select the reflexes
        taxa = t.taxa
        refs = []
        
        # iterate over states and assign reflexes
        for s1,s2 in states:
            indices = [
                    x[0] for x in E[s1] if x != 0 and phy[x[0],'doculect'] in
                    taxa]
            alm = [phy[idx,'alignment'] for idx in indices]
            txa = [phy[idx,'taxa'] for idx in indices]

            # get the consensus
            cns = get_consensus(alm, gaps=False)

            # check whether state is retention or innovation
            if t.Parent:
                if s1 in previous[t.Parent.Name]:
                    retention = '1'
                else:
                    retention = "0"
            else:
                retention = '0'
            refs += [[cns,s1,cdict[s1],alm,retention,txa,t.Parent.Name if
                t.Parent else '']]
        
        # 
        previous[name] = [s[0] for s in states]

        # get the siblings
        if t.Children:
            children = [x.Name for x in t.Children]
        else:
            children = []
            if not refs:
                
                try:
                    vals = phy.get_dict(
                            concept=concept,
                            )[name]
                except:
                    vals = []
                for v in vals:
                    refs += [[
                        phy[v,'tokens'],
                        phy[v,'pap'],
                        cdict[phy[v,'pap']],
                        phy[v,'tokens'],
                        '0',
                        phy[v,'taxon'],
                        t.Parent.Name
                        ]]

        D[name] = dict(
                children = children,
                consensus = [c[0] for c in refs],
                paps = [c[1] for c in refs],
                colors = [c[2] for c in refs],
                alignments = [c[3] for c in refs],
                retention = [c[4] for c in refs],
                taxa = [c[5] for c in refs],
                parent = [c[6] for c in refs]
                )
        order += [name]
    
    D['order'] = order
    D['colors'] = cdict
    
    if output == 'json':
        with open('json/'+concept + '.json','w') as f:
            f.write(json.dumps(D, indent=2))
    
    if debug:
        return previous

    return D
            
txt = ''
for c in phy.concepts:
    if not '/' in c:
        create_charhist(phy, c)
        txt += r"""<option value="{0}">{0}</option>""".format(c)

tmpl = open('template.html').read()
tmpj = open('template.js').read()
tmpc = open('template.css').read()
with open('index.html','w') as f:
    f.write(tmpl.format(INPUT=txt,SCRIPT=tmpj, STYLE=tmpc))

