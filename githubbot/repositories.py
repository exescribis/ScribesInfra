# coding: utf-8
from __future__ import print_function
import users
import githubbot
import refs
from githubbot import toNotSet

def repo(username="", reponame=""):
    if (username=="") and (reponame==""):
        if githubbot._repo_ is None:
            raise RuntimeError("Current repository (_repo_) is not defined")
        else:
            return githubbot._repo_
    else:
        o = users.user(username)
        r = o.get_repo(reponame)
        return r




def setRepo(username="", reponame=""):
    r = repo(username,reponame)
    githubbot._repo_ = r
    print('Default repository set to %s ' % refs.ref(r))




def ensureRepo(
        orgName,
        reponame,
        description=None,
        private=None,
        has_issues=None,
        has_wiki=None,
        has_downloads=None,
        doEnsureEmptyRepo=False,
        prefix='  '):
    try:
        o = githubbot.users.org(orgName)
    except:
        raise EnvironmentError(
                'Organisation "%s" is not reachable on github\n.'
                % orgName)
    try:
        r = o.get_repo(reponame)
    except:
        if prefix is not None:
            print(prefix+'Create repository %s/%s ... '
                  % (orgName, reponame),
                  end=''),
        r = o.create_repo(
                reponame,
                description=toNotSet(description),
                private=toNotSet(private), has_issues=toNotSet(has_issues),
                has_wiki=toNotSet(has_wiki), has_downloads=toNotSet(has_downloads))
        if prefix is not None:
            print(prefix+'done')
        return r
    else:
        if doEnsureEmptyRepo==666:
            if prefix is not None:
                print(prefix +'Delete repository %s/%s ... '
                      % (orgName, reponame),
                        end='')
            r.delete()
            r = o.create_repo(
                reponame,
                description=toNotSet(description),
                private=toNotSet(private), has_issues=toNotSet(has_issues),
                has_wiki=toNotSet(has_wiki), has_downloads=toNotSet(has_downloads))
        else:
            if prefix is not None:
                print(prefix+'Edit repository %s/%s ... '
                      % (orgName, reponame),
                      end='')
            r.edit(reponame,
                description=toNotSet(description),
                private=toNotSet(private),
                has_issues=toNotSet(has_issues),
                has_wiki=toNotSet(has_wiki),
                has_downloads=toNotSet(has_downloads))
            if prefix is not None:
                print('done')
        return r

