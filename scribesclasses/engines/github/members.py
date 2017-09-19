from typing import List, Text
from scribesclasses.models.teams import (
    Team,
)
from scribesclasses.models.members import Member
import github.NamedUser


def readTeamMembersFromGH(team, prefix='  '):
    #type: (Team, Text) -> None
    """
    Read the github members from the team. Create
    a Member for each user in the github team.
    """
    if prefix is not None:
        print('%sReading the list of members for team %s' %
              (prefix, team.name))
    # if team.atGH is None:
    #     ensureTeamAtGH(team, readMembers=False, prefix=None)
    gh_users=list(team.atGH.get_members())
    #type: List[github.NamedUser.NamedUser]

    if prefix is not None:
        print('%s%i member(s) found.' % (prefix, len(gh_users)))
    for gh_user in gh_users:
        if prefix is not None:
            print(prefix+'  Reading info from user %s'
                 % gh_user.login)
        _readMemberFromGHUser(team, gh_user)

def _readMemberFromGHUser(team, gh_user):
    #type: (Team, github.NamedUser.NamedUser) -> None
    """
    If the member with the login exists then do nothing,
    otherwise read info from gh_user and create a member.
    """
    login=gh_user.login
    if login in team.memberByLogin:
        return
    else:
        Member(
            team,
            login=login,
            email=gh_user.email,
            atGH=gh_user,
            firstName=None,
            lastName=None,
            trigram=None
        )