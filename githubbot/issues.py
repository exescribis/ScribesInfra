# coding: utf-8

"""
Helpers for issues.
Use the "Issue" class of pygithub.
See http://pygithub.readthedocs.io/en/latest/github_objects/Issue.html for documentation
"""

import re

import users
import repositories
import githubbot

def repos(username="", reporegexpr=None):
    o = users.org(username)
    rs = [_r for _r in o.get_repos() if githubbot.nameFilter(reporegexpr)(_r) ]
    return rs


def issue(userorgname='', reponame='', issuenb=None):
    r = repositories.repo(userorgname, reponame)
    i = r.get_issue(issuenb)
    return i


def issues(userorgname='',reponame=''):
    r = repositories.repo(userorgname, reponame)
    is_ = r.get_issues()
    return is_

def text_str(text):
    return '\n'.join(text.split('\r\n'))

def issue_str(issue):
    header = '#%i : %s' % (issue.number, issue.title)
    _ = [ header ]
    _.append( "="*len(header))
    _.append( "" )
    _.append(issue.body)

    # for
    return '\n'.join(_)





def id_issue(issue):
    return '%s/%s#%i' % (issue.user.login, issue.repository.name, issue.number)

def issue_id_info(issueid):
    m = re.match('(.*)/(.*)#(.*)', issueid)
    if m:
        return m.groups()
    else:
        raise Exception('Invalid issue id:%s' % issueid)



#-------------------------------------------------------------------------
#                               issue comments
#-------------------------------------------------------------------------

def firstCommentWith(issuefun, issue):
    for c in issue.get_comments():
        if issuefun(c):
            return c
    return None

def ensureCommentWith(issuefun, issue, body, append=False):
    c = firstCommentWith(issuefun, issue)
    if c is None:
        c = issue.create_comment(body)
    else:
        if append:
            txt = c.body+'\n'+body
        else:
            txt = body
        c.edit(txt)
    return c

    # get_comments()
    # create_comment(body)