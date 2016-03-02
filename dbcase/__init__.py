# coding=utf-8

from __future__ import print_function
import sys

def warning(*objs):
    s = str(*objs)
    print(indent(1, 'WARNING: %s' % s, '********'), file=sys.stderr)


def indent(n, s, prefix=''):
    return '\n'.join([prefix+' '*n*4+l for l in s.split('\n')])

