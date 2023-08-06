
import os
import re
from importlib import import_module
from .genuslist import genus_list
from .exceptions import NonCanonicalError, SurplusTreeError
from .rulefiles import rule2files

def obtain_genus(rulestring):

    for g in genus_list:
        m = re.match(g['regex'] + '$', rulestring)
        if m is not None:
            return g['name']

    raise ValueError('Rule "%s" does not belong to any genus' % rulestring)

def genus_to_module(genus):

    m = import_module('.' + genus, __name__)

    return m

def rule_property(rulestring, attribute):

    m = genus_to_module(obtain_genus(rulestring))
    attr = getattr(m, attribute)
    if callable(attr):
        attr = attr(rulestring)
    return attr

def create_rule(rulestring):

    rule_property(rulestring, 'create_rule')

def decode_ltl(rulestring):

    rparts = rulestring.lower().split(',')

    d = {'c': 2, 'm': 1, 'n': 'm'}
    p = ['r', 'bmin', 'bmax', 'smin', 'smax']

    for r in rparts:
        if (r[0] >= 'a') and (r[0] <= 'z'):
            if '..' in r[1:]:
                a, b = r[1:].split('..')
                d[r[0] + 'min'] = a
                d[r[0] + 'max'] = b
            else:
                d[r[0]] = r[1:]
        else:
            d[[x for x in p if x not in d][0]] = r

    if d['n'] != 'm':
        raise ValueError("Unsupported LtL neighbourhood type")

    d = {k : int(d[k]) for k in ['r', 'c', 'm', 'smin', 'smax', 'bmin', 'bmax']}

    d['smin'] += (1 - d['m'])
    d['smax'] += (1 - d['m'])

    rulestring = 'r%db%dt%ds%dt%d' % (d['r'], d['bmin'], d['bmax'], d['smin'], d['smax'])
    if d['c'] > 2:
        rulestring = 'g%d%s' % (d['c'], rulestring)
    return rulestring

def sanirule(rulestring, drop_history=False):

    if ',' in rulestring:
        rulestring = decode_ltl(rulestring)

    if '.' in rulestring:
        try:
            rulestring = rule2files(rulestring)
            if (rulestring[0] != 'x'):
                raise ValueError("Rules specified by table/tree/code files must begin with a capital letter.")
        except SurplusTreeError as e:
            rulestring = str(e)

    rulestring = rulestring.lower()

    if (len(rulestring) > 7) and (rulestring[-7:] == 'history'):
        return sanirule(rulestring[:-7], drop_history) + ('' if drop_history else 'History')

    if '/' in rulestring:
        rparts = rulestring.split('/')
        if (len(rparts) <= 3):
            p = ['s', 'b', 'g'] # default parsing order == survivals/births/generations
            d = {}
            for r in rparts:
                if (len(r) > 0) and (r[0] in p):
                    d[r[0]] = r[1:]
                    p = [x for x in p if (x != r[0])]
                else:
                    d[p[0]] = r
                    p = p[1:]
            if ('g' in d) and (int(d['g']) >= 3):
                rulestring = 'g%sb%ss%s' % (d['g'], d['b'], d['s'])
            else:
                rulestring = 'b%ss%s' % (d['b'], d['s'])
        else:
            rulestring = rulestring.replace('/', '')

    commonnames = {'life': 'b3s23', 'pedestrianlife': 'b38s23', 'drylife': 'b37s23', 'highlife': 'b36s23'}

    if rulestring in commonnames:
        rulestring = commonnames[rulestring]

    return rulestring
