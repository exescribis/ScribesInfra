# coding: utf-8

def gitHubURL(path, accountInfo=''):
    if accountInfo is '':
        return 'https://github.com/%s' % path
    else:
        return 'https://%s@github.com/%s' % (accountInfo,path)

def gitHubFileURL(org, repo, file=None):
    f = '' if file is None else file
    return gitHubURL('%s/%s/blob/master/%s' % (org, repo, f))

def gitHubRepoURL(orgName, repoName, accountInfo='', gitSuffix=False):
    return gitHubURL (
        path = '%s/%s' % (orgName, repoName) + ('.git' if gitSuffix else ''),
        accountInfo = accountInfo
    )


def gitHubWebURL(org, path):
    return 'https://%s.github.io/%s' % (org,path)