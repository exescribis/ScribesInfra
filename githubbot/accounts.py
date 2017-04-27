# coding: utf-8

import os.path

import github

import githubbot


def gitHubAccounts():
    home = os.path.expanduser("~")
    file = os.path.join(home, '.github_account')
    lines = [line.rstrip('\n') for line in open(file)]
    accounts = {}
    for line in lines:
        (login,passwd) = line.split(' ')
        accounts[login]=passwd
    return accounts


def gitHubSession(login):
    """
    Open a session with the given user login.
    The password is searched in ~/.github_account
    :param login: the github login
    :return: the session github session object
    """
    accounts=gitHubAccounts()
    password = accounts[login]
    session = github.Github(login, password)
    githubbot._gh_ = session
    githubbot._login_ = login
    githubbot._password_ = password
    return session


def currentLogin():
    return githubbot._login_


def currentPassword():
    return githubbot._password_