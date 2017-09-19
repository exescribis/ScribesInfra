# coding: utf-8
from __future__ import print_function
from typing import List, Text, Tuple, Optional

from github import UnknownObjectException
import github.Repository
import github.Label

import repositories

NameAndColor=Tuple[Text, Text]
GH_Repository=github.Repository.Repository


def label(username='',reponame='',labelname=None):
    ls = [ l for l in labels(username,reponame) if l.name==labelname ]
    if len(ls)==1:
        return ls[0]
    else:
        raise RuntimeError('%s label(s) named "%s" ' % (len(ls),labelname))


def labels(username='',reponame=''):
    r = repositories.repo(username,reponame)
    ls_ = r.get_labels()
    return ls_

def labelNames(repo):
    return { l.name for l in repo.get_labels() }

STD_LABEL_NAMES = {
    'bug',
    'duplicate',
    'enhancement',
    'help wanted',
    'invalid',
    'question',
    'wontfix'
}

def deleteStandardLabels(gh_repo, prefix='  '):
    #type: (GH_Repository, Optional[Text]) -> None
    for gh_label in gh_repo.get_labels():
        if gh_label.name in STD_LABEL_NAMES:
            if prefix is not None:
                print(prefix+'Deleting standard label (%s,%s)'
                      % (gh_label.name, gh_label.color))
            gh_label.delete()

def deleteAllLabels(gh_repo, code, prefix='  '):
    #type: (GH_Repository, int, Optional[Text]) -> None
    if code == 666:
        if prefix is not None:
            print(prefix +'Removing existing labelsSpec from '
                  % gh_repo.name)
        for gh_label in gh_repo.get_labels():
            if prefix is not None:
                print(prefix+'  deleting (%s,%s)'
                      % (gh_label.name, gh_label.color))
            gh_label.delete()

def defineAllLabels(
        gh_repo,
        namesAndColors,
        deleteExistingLabels=True,
        prefix='  '):
    #type: (GH_Repository, List[NameAndColor], bool, Optional[Text]) -> None
    if deleteExistingLabels:
        deleteAllLabels(gh_repo, 666)
    print(prefix+'Adding labelsSpec')
    for (name, color) in namesAndColors:
        if prefix is not None:
            print(prefix+'Creating (%s,%s)' % (name, color))
        gh_repo.create_label(name, color)


def ensureLabel(gh_repo, name, color, prefix='  '):
    #type: (GH_Repository, Text, Text, Optional[Text]) -> github.Label.Label
    try:
        gh_label = gh_repo.get_label(name)
    except UnknownObjectException as e:
        gh_label = None

    if gh_label is None:
        # no such label name
        if prefix is not None:
            print(
                prefix+'Creating label (%s,%s) in repo %s'
                % (name, color, gh_repo.name))
        gh_label = gh_repo.create_label(name, color)
    else:
        if prefix is not None:
            print(prefix +'Editing label (%s,%s) in repo %s ... '
                  % (name, color, gh_repo.name))
        gh_label.edit(name, color)
    return gh_label


def ensureAllLabels(
        gh_repo,
        namesAndColors,
        deleteStandardLabelsBefore):
    #type: (GH_Repository, List[NameAndColor], bool) -> None
    if deleteStandardLabelsBefore:
        deleteStandardLabels(gh_repo)
    for (name,color) in namesAndColors:
        ensureLabel(gh_repo, name, color)