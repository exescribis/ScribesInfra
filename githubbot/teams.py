# coding: utf-8

import githubbot.users

def getTeam(orgName, teamName):
    """
    Return a team by name
    :param orgName: the organization containing the team
    :param teamName: the team of the team to be searched.
    :return: the team
    :raise: EnvironmentError if the team does not exist
    """
    o = githubbot.users.org(orgName)
    for t in o.get_teams():
        if t.name == teamName:
            return t
    raise EnvironmentError(
        'No team %s/%s found on GitHub' % (orgName,teamName)
    )

def ensureTeam(orgName, teamName):
    """
    Make sure that the team exists.
    :param orgName: name of the organization or user
    :param teamName: name of the team
    :return: the team
    """
    try:
        t = getTeam(orgName, teamName)
    except:
        o = githubbot.users.org(orgName)
        t = o.create_team(teamName)
        return t
    else:
        return t

