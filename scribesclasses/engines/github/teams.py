
from __future__ import print_function
from typing import Text, Optional

import githubbot.teams
from scribesclasses.models.teams import (
    Team,
)
from scribesclasses.engines.github.members import (
    readTeamMembersFromGH
)

def ensureTeamAtGH(team, readMembers=False, prefix='  '):
    #type: (Team, bool, Optional[Text]) -> None
    if prefix is not None:
        print('%sEnsure team %s' % (
            prefix, team.name))
    team.atGH = githubbot.teams.ensureTeam(
        team.classroom.org.name,
        team.name)
    if readMembers:
        readTeamMembersFromGH(team, prefix=prefix+'  ')
