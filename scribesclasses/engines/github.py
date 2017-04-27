# coding: utf-8

"""
Ensure that the classroom is represented propely on GitHub.
Currently this create only the repository of the group list.

"""
import datetime

import githubbot.repositories
import githubbot.teams
import githubbot.labels
import githubbot.milestones

import scribesclasses.models.groups


# def getTeamMembers(group):
#     (group.ghOrgName, group.ghTeamName)


def _readMemberFromGithubUser(githubUser, group):
    """
    Create a Member object from the github and add this member into
    member list of the group given as parameter.
    :param githubUser: a github user
    :param group: a scribesclass group containing that new member
    :return Member: a fresh member object
    """
    member = scribesclasses.models.groups.Member()
    member.login = githubUser.login
    member.email = githubUser.email
    member.group = group
    group.members.add(member)
    return member

def _readMembersFromGithubTeam(group):
    """
    Read the github team associated with the given group, create
    a Member for each user in this list and add the group members field.
    :param group: a scribesclass group
    :return: None
    """
    print "Reading the list of members from github for team %s" % group.ghTeamName
    for user in group.ghTeam.get_members():
        print "  reading a new member from user '%s'" % user.login
        _readMemberFromGithubUser(user, group)


def _ensureLabels(repository, classroom):
    """
    Ensure that the label specifications (Classroom.labelSpecifications)
    corresponds to actual labels in the given repository
    :param repository: the repository where to ensure labels
    :param classroom: the classroom where labels are specified
    :return: None
    """
    githubbot.labels.ensureAllLabels(
        repository,
        classroom.labelSpecifications,
        True
    )

def _ensureMilestones(repository, classroom):
    """
    Ensure that the milestone specifications (Classroom.milestoneSpecifications)
    corresponds to actual milestones in the given repository
    :param repository: the repository where to ensure milestones
    :param classroom: the classroom where milestones are specified
    :return: None
    """
    for (title,info) in classroom.milestoneSpecifications:
        print title
        print info
        deadline = datetime.datetime.strptime(info['deadline'],"%d/%m/%Y")
        description = info['description']
        # print title, info['Description'],date
        githubbot.milestones.ensureMilestone(
            repository,
            title=title,
            description=description,
            dueOn=deadline
        )

def ensureRootRepositoryAtGithub(classroom, ensureLabels=False, ensureMilestones=False):
    """
    Ensure that the root repository exist and have the proper
    structure. Set the attribute classroom.rootRepo
    :param classroom: the classroom specifing the root
    """
    orgName=classroom.org()
    repoName=classroom.rootRepoName()
    print "ensure repository %s/%s" % (orgName, repoName)

    repo = githubbot.repositories.ensureRepo(
        orgName=orgName,
        reponame=repoName,
        description=classroom.rootRepoDescription(),
        private=True,
        has_issues=True,
        has_wiki=False,
        has_downloads=True)
    if ensureLabels:
        _ensureLabels(repo, classroom)
    if ensureMilestones:
        _ensureMilestones(repo, classroom)
    classroom.rootRepo = repo


def deleteRootRepositoryAtGithub(classroom, deleteCode):
    assert deleteCode == 666
    assert classroom.canBeDeleted
    assert classroom.rootRepo is not None
    classroom.rootRepo.delete()

def ensureGroupAtGitHub(group, ensureLabels=False, ensureMilestones=False):
    """
    Ensure that there is a repository and a team for the group.
    This function fill as well the group given as a parameter:
    it set the following github data fields :

    *   ghRepo
    *   ghTeam


    Currently the GitHub API permission is not published and pygithub do not
    implement what is needed. Currently the team and repository is not associated.

    See https://developer.github.com/v3/orgs/teams/#add-team-repo
    no permission seems to be change by PyGithub

        print 'Getting pull repositories %s ...' % (', '.join(pullRepoNames))
        pull_repos = [o.get_repo(name) for name in pullRepoNames ]
        In previous version this was: t = o.create_team(team_name, [r], teamPermission)
    """
    orgName=group.ghOrgName
    repoName=group.ghRepoName
    print "ensure repository %s/%s" % (orgName, repoName)

    group.ghRepo = githubbot.repositories.ensureRepo(
        orgName=orgName,
        reponame=repoName,
        description=group.ghRepoTitle,
        private=True,
        has_issues=True,
        has_wiki=False,
        has_downloads=True)

    group.ghTeam = githubbot.teams.ensureTeam(
        group.ghOrgName, group.ghTeamName)

    _readMembersFromGithubTeam(group)

    if ensureLabels:
        _ensureLabels(group.ghRepo, group.classRoom)
    if ensureMilestones:
        _ensureMilestones(group.ghRepo, group.classRoom)


def ensureGroupListAtGitHub(groupList, ensureLabels=False, ensureMilestones=False):
    for group in groupList:
        ensureGroupAtGitHub(
            group=group,
            ensureLabels=ensureLabels,
            ensureMilestones=ensureMilestones
        )



def deleteGroupListAtGitHub(groupList, deleteCode):
    assert deleteCode == 666
    assert groupList.classRoom.canBeDeleted
    for group in groupList:
        print "deleting group with key ",group.key
        deleteGroupAtGitHub(group, deleteCode)


def deleteGroupAtGitHub(group, deleteCode):
    assert deleteCode == 666
    assert group.groupList.classRoom.canBeDeleted
    group.ghRepo.delete()
    group.ghTeam.delete()
















class ClassroomOnGitHubEngine(object):
    def __init__(self, classroom):
        self.classroom = classroom

    def ensureAtGitHub(self,
                       ensureLabels=False,
                       ensureMilestones=False):
        """
        Create the repositories and teams on github thanks to scribesbot.createReposAndTeams
        but according to the particular patterns in Classroom.
        :return: None
        """

        # repository and teams for groups
        # labelsSpec and milestones
        ensureGroupListAtGitHub(
            self.classroom.groupList,
            ensureLabels=ensureLabels,
            ensureMilestones=ensureMilestones
        )

        ensureRootRepositoryAtGithub(
            classroom=self.classroom,
            ensureLabels=ensureLabels,
            ensureMilestones=ensureMilestones
        )

        # TODO hq-repository
        # TODO info-repository
        # TODO web-repository


    def deleteAtGitHub(self, deleteCode):
        """
        Delete the repositories at GitHub.
        This will only be possible with the proper deleteCode.
        This is to avoid accidental deletion.
        """
        assert deleteCode == 666
        assert self.classroom.canBeDeleted

        # TODO hq-repository
        # TODO info-repository
        # TODO web-repository

        deleteRootRepositoryAtGithub(self.classroom, deleteCode)

        deleteGroupListAtGitHub(
            self.classroom.groupList, deleteCode)


