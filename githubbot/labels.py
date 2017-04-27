# coding: utf-8

from github import UnknownObjectException

import repositories


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

def deleteStandardLabels(repo):
    for label in repo.get_labels():
        if label.name in STD_LABEL_NAMES:
            print '  deleting standard label (%s,%s)' % (label.name, label.color)
            label.delete()

def deleteAllLabels(repo, code):
    if code == 666:
        print 'Removing existing labelsSpec from ' % repo.name
        for label in repo.get_labels():
            print '  deleting (%s,%s)' % (label.name, label.color)
            label.delete()

def defineAllLabels(repo, namesAndColors, deleteExistingLabels=True):
    if deleteExistingLabels:
        deleteAllLabels(repo, 666)
    print 'Adding labelsSpec'
    for (name, color) in namesAndColors:
        print '  creating (%s,%s)' % (name, color)
        repo.create_label(name, color)


def ensureLabel(repo, name, color):
    try:
        label = repo.get_label(name)
    except UnknownObjectException as e:
        label = None

    if label is None:
        # no such label name
        print 'Creating label (%s,%s) in repo %s ... ' % (name, color, repo.name),
        label = repo.create_label(name, color)
    else:
        print 'Editing label (%s,%s) in repo %s ... ' % (name, color, repo.name),
        label.edit(name, color)
    print 'done'
    return label

def ensureAllLabels(repo, namesAndColors, deleteStandardLabelsBefore):
    if deleteStandardLabelsBefore:
        deleteStandardLabels(repo)
    for (name,color) in namesAndColors:
        ensureLabel(repo, name, color)