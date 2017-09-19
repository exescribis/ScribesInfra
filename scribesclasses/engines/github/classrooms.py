# coding: utf-8
from __future__ import print_function
from typing import List, Text

from scribesclasses.engines.github.groups import (
    deleteGroupListAtGH,
    ensureGroupListAtGH
)
from scribesclasses.engines.github.repositories import (
    ensureRepositoryAtGH,
    deleteRepositoryAtGH
)

"""
Ensure that the classroom is represented propely on GitHub.
Currently this create only the repository of the group list.

"""


class ClassroomOnGHEngine(object):
    def __init__(self, classroom):
        self.classroom = classroom

    def ensureAtGH(
            self,
            repoIds=('root', 'hq', 'info', 'web', 'groups'),
            ensureTeams=False,
            ensureLabels=False,
            ensureMilestones=False,
            readMembers=False,
            prefix=''):
        #type: (List[Text], bool, bool, bool, bool) -> None
        for repo_id in repoIds:
            if repo_id=='groups':
                ensureGroupListAtGH(
                    self.classroom.groupList,
                    ensureLabels=ensureLabels,
                    ensureMilestones=ensureMilestones,
                    ensureTeams=ensureTeams,
                    readMembers=readMembers
                )
            else:
                ensureRepositoryAtGH(
                    repo=self.classroom.repoById[repo_id],
                    ensureLabels=ensureLabels,
                    ensureMilestones=ensureMilestones,
                    prefix='  '+prefix
                )



    def deleteAtGH(self,
                       repoIds=(),
                       deleteCode=None):
        """
        Delete the repositories at GitHub.
        This will only be possible with the proper deleteCode.
        This is to avoid accidental deletion.
        """
        assert deleteCode==666
        for repo_id in repoIds:
            assert repo_id in self.classroom.deletableRepositories
            if repo_id=='groups':
                deleteGroupListAtGH(
                    self.classroom.groupList,
                    deleteCode)
            else:
                if repo_id=='web':
                    deleteRepositoryAtGH(
                        self.classroom.web,
                        deleteCode)





# def ensureRootRepositoryAtGithub(
#         classroom,
#         ensureLabels=False,
#         ensureMilestones=False):
#     """
#     Ensure that the root repository exist and have the proper
#     structure. Set the attribute classroom.rootRepo
#     :param classroom: the classroom specifing the root
#     """
#     orgName=classroom.org()
#     repoName=classroom.root.name()
#     print("\n==== Ensure root repository %s/%s" % (orgName, repoName))
#
#     repo = githubbot.repositories.ensureRepo(
#         orgName=orgName,
#         reponame=repoName,
#         description=classroom.root.description(),
#         private=True,
#         has_issues=True,
#         has_wiki=False,
#         has_downloads=True)
#     if ensureLabels:
#         _ensureLabels(repo, classroom)
#     if ensureMilestones:
#         _ensureMilestones(repo, classroom)
#     classroom.rootRepo = repo
#     print("---- repository %s/%s is OK" % (orgName, repoName))
