# coding: utf-8

import githubbot
import refs



def user(name=''):
    if name=='':
        return githubbot._user_
    else:
        user=githubbot._gh_.get_user(name)
        return user


def org(name=''):
    if name=='':
        return githubbot._org_
    else:
        return githubbot._gh_.get_organization(name)


def setOrg(name):
    o = org(name)
    githubbot._org_ = o
    print "Default organization set to %s" % refs.ref(o)