# coding: utf-8

import github.Organization
import github.NamedUser
import github.Repository
import github.Issue

def ref_named_user(named_user):
    return '%s' % named_user.name

def ref_organization(org):
    return org.login

def ref_repo(repo):
    return '%s/%s' % (
        ref_named_user(repo.owner),
        repo.name
    )

def ref_issue(issue):
    return '%s/issues/%s' % (
        ref_repo(issue.repository),
        issue.number
    )

def ref_label(label):
    return '%s/labelsSpec/%s' % (
        ref_repo(label.repository),
        label.name
    )

def ref_milestone(milestone):
    return milestone.url[len('https://api.github.com/repos/'):]
    # fixme: to be tested

def ref(obj):
    if isinstance(obj, github.Organization.Organization):
        return ref_organization(obj)
    if isinstance(obj, github.NamedUser.NamedUser ):
        return ref_named_user(obj)
    elif isinstance(obj, github.Repository.Repository ):
        return ref_repo(obj)
    elif isinstance(obj, github.Issue.Issue ):
        return ref_issue(obj)
    # elif isinstance(obj, github.Label.Label ):
    #     return ref_label(obj) # FIXME
    # elif isinstance(obj, github.Milestone.Milestone ):
    #     return ref_milestone(obj) # FIXME
    #
    # # TODO continue



def obj(name):
    # TODO continue
    segments = name.split('/')
    if len(segments)>=1:
        username=segments[0]
    # TODO continue

