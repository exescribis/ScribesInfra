import githubbot.milestones


def ensureMilestonesAtGH(repo, prefix=''):
    for milestone in repo.milestones:
        gh_milestone = githubbot.milestones.ensureMilestone(
            repo=repo.atGH,
            title=milestone.title,
            description=milestone.description,
            dueOn=milestone.color,
            prefix=prefix + '  ')
        milestone.atGH = gh_milestone

#
# from __future__ import print_function
#
# from typing import Text
# from githubbot.labels import (
#     ensureLabel,
#     deleteStandardLabels
# )
# from scribesclasses.models.repositories import (
#     Repository
# )
# from scribesclasses.models.labels import (
#     LabelConfig,
#     Label
# )
#
#
# def ensureLabelAtGH(
#         repo,
#         labelConfig,
#         prefix
#     ):
#     #type: (Repository, LabelConfig) -> None
#     """
#     Make sure that the given label is registered in the repository.
#     If not create a 'Label' object, register it, and ensure that
#     it is at GH.
#     In all case return the Label object
#     :return:
#     """
#     assert repo.atGH is not None
#     name=labelConfig.name
#     color=labelConfig.color
#     gh_label=ensureLabel(
#         gh_repo=repo.atGH,
#         name=name,
#         color=color,
#         prefix=prefix)
#     Label(repo, name, color, atGH=gh_label)
#
# def ensureLabelsAtGH(
#         repo
#     ):
#     #type: (Repository) -> None
#     assert repo.atGH is not None
#     for lc in repo.repoConfig.labelConfigList:
#         Label(repo, lc.name, lc.color)