
from typing import (
    Text,

)

from scribesclasses.engines.github.repositories import (
    ensureRepositoryAtGH
)
from scribesclasses.engines.github.teams import (
    ensureTeamAtGH
)
from scribesclasses.models.repositories import GroupRepository


def ensureGroupRepositoryAtGH(
        repo,
        ensureLabels=False,
        ensureMilestones=False,
        ensureTeam=False,
        readMembers=False,
        prefix=''):
    #type: (GroupRepository, bool, bool, bool, bool, Text) -> None
    """
    Ensure that there is a repository and a team for the group.

    This function fill as well the group given as a parameter:
    it set the following github data fields :

    *   repo.atGH
    *   repo.team.atGH

    Currently the GitHub API permission is not published and
    pygithub do not implement what is needed. Currently the team
    and repository is not associated.

    See https://developer.github.com/v3/orgs/teams/#add-team-repo
    no permission seems to be change by PyGithub

        print 'Getting pull repositories %s ...' % (', '.join(pullRepoNames))
        pull_repos = [o.get_repo(name) for name in pullRepoNames ]
        In previous version this was: t = o.create_team(team_name, [r], teamPermission)
    """
    assert isinstance(repo, GroupRepository)
    # org_name=repo.classroom.org.name
    # repo_name=repo.name
    # team_name=repo.group.team.name
    # if prefix is not None:
    #     print('\n%s==== Ensure group repository %s/%s'
    #           % (prefix, org_name, repo_name))

    ensureRepositoryAtGH(
        repo=repo,
        ensureLabels=ensureLabels,
        ensureMilestones=ensureMilestones,
        prefix=prefix+'  ')

    if ensureTeam:
        ensureTeamAtGH(
            team=repo.group.team,
            readMembers=readMembers,
            prefix=prefix+'  ')

def ensureGroupListAtGH(
        groupList,
        ensureLabels=False,
        ensureMilestones=False,
        ensureTeams=False,
        readMembers=False):
    for group in groupList:
        ensureGroupRepositoryAtGH(
            repo=group.repo,
            ensureLabels=ensureLabels,
            ensureMilestones=ensureMilestones,
            ensureTeam=ensureTeams,
            readMembers=readMembers
        )


def deleteGroupAtGH(repo, deleteCode):
    #type: (GroupRepository, int) -> None
    assert isinstance(repo, GroupRepository)
    assert deleteCode == 666
    repo.atGH.delete()
    repo.group.team.atGH.delete()


def deleteGroupListAtGH(groupList, deleteCode, prefix='  '):
    assert deleteCode == 666
    assert groupList.classroom.canBeDeleted
    assert 'groups' in groupList.classroom.deletableRepositories
    for group in groupList:
        if prefix is not None:
            print(prefix+"deleting group with key %s" % group.key)
        deleteGroupAtGH(group.repo, deleteCode)