
from __future__ import print_function

from typing import Text

import githubbot.repositories
import githubbot.teams

from scribesclasses.models.repositories import (
    Repository
)
from scribesclasses.engines.github.milestones import (
    ensureMilestonesAtGH
)
from scribesclasses.engines.github.labels import (
    ensureLablesAtGH
)

def ensureRepositoryAtGH(
        repo,
        ensureLabels=False,
        ensureMilestones=False,
        prefix='\n'):
    #type: (Repository, bool, bool, Text) -> None
    """
    Ensure that the repository exist and have the proper
    structure. Set repo.atGH.
    :return:
    """
    org_name=repo.classroom.org.name
    if prefix is not None:
        print(prefix+"==== Ensure repository %s/%s"
            % (org_name, repo.name))

    #---- ensure repo
    gh_repo = githubbot.repositories.ensureRepo(
        orgName=org_name,
        reponame=repo.name,
        description=repo.description,
        private=repo.repoConfig.private,
        has_issues=repo.repoConfig.hasIssue,
        has_wiki=repo.repoConfig.hasWiki,
        has_downloads=repo.repoConfig.hasDownloads)
    repo.atGH=gh_repo

    #---- ensure labels
    if ensureLabels:
        ensureLablesAtGH(repo, prefix=' '+prefix)

    # ---- ensure milestones
    if ensureMilestones:
        ensureMilestonesAtGH(repo, prefix='  '+prefix)

def deleteRepositoryAtGH(
        repo,
        deleteCode):
    assert deleteCode == 666
    assert repo.classroom.canBeDeleted
    assert repo.atGH is not None
    repo.atGH.delete()


