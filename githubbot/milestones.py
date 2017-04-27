# coding: utf-8

import github.GithubObject

"""
Deal with "named" milestone. GitHub use number to reference milestone.
However GitHub ensure that the unicity of the title attribute in the
respository. Here the title is taken as the identifier. This does not
allows renaming but it should be ok for most uses.

WARNING:

*   It seems that there is a bug in the repo.create_milestone method.
    It does not work with the deadline parameter. The code below solve
    this problem.

*   The date due_on returns something with hours although hours cannot be
    set in the interface. It does not take into account hours in parameters.
    One should use   due_on.date() if comparison is required.

"""


def getMilestone(repo, title):
    """
    Return the milestone with the given title or None if there is no such milestone in the repository
    :param repo: repository
    :param title: title of the milestone to search
    :return str: the milestone object or None
    """
    milestones = repo.get_milestones()
    for m in milestones:
        if m.title==title :
            return m
    return None

def ensureMilestone(repo, title,
                    description = github.GithubObject.NotSet,
                    state = github.GithubObject.NotSet,  # 'open' | closed
                    dueOn = github.GithubObject.NotSet):
    m = getMilestone(repo, title)
    if m == None:
        print 'Creating milestone "%s"... ' % title,
        m = repo.create_milestone(title)
        # For some strange reason the method create_milestone
        # dos not work with the parameter due_on.
        # So after creating the milestone the code below
        # set additional parameters and in particular the due_on
        m.edit(title, state, description, dueOn)
        print '    milestone #%i created' % m.number
    else:
        print 'Editing milestone "%s" ... ' % title,
        m.edit(title, state, description, dueOn)
        print '    milestone #%i edited' % m.number
    return m
