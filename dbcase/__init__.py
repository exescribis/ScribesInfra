# coding=utf-8

"""
Management of Database Case Studies (DBCase).

This package contains various modules providing abstractions over the directory
representation of a DBCase::
* dbcase.case
* dbcase.schema
* dbcase.state
* dbcase.queries
"""

from __future__ import print_function
import sys

def warning(*objs):
    s = str(*objs)
    print(indent(1, 'WARNING: %s' % s, '********'), file=sys.stderr)


def indent(n, s, prefix=''):
    return '\n'.join([prefix+' '*n*4+l for l in s.split('\n')])

