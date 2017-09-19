import githubbot.labels

def ensureLablesAtGH(repo, prefix=''):
    if repo.noStandardLabels:
        githubbot.labels.deleteStandardLabels(
            repo.atGH,
            prefix=prefix + '  ')
    for label in repo.labels:
        gh_label = githubbot.labels.ensureLabel(
            gh_repo=repo.atGH,
            name=label.name,
            color=label.color,
            prefix=prefix + '  ')
        label.atGH = gh_label