

from collections import OrderedDict

from typing import Text, Dict
from scribesclasses.models.members import (
    Member
)

class TeamFactory(object):
    def __init__(self, teamNamePattern):
        self.teamNamePattern=teamNamePattern

    def name(self, key=None):
        """
        The team name of the group or the pattern
        If None return the key-based pattern
        such as 'GPI{key}'.
        Otherwise return something like 'l3miage-bdsi-GPI12'
        """
        p = self.teamNamePattern
        if key is None:
            return p
        else:
            return p.format(key=key)


class TeamList(object):
    def __init__(self,
                 groupList,
                 teamNamePattern):
        self.groupList=groupList
        self.factory=TeamFactory(teamNamePattern)
        self._teamsByKey=OrderedDict()
        for group in groupList:
            key=group.key,
            team=Team(self, group)
            self._teamsByKey[key]=team


    def __getitem__(self, key):
        return self._teamsByKey[key]

    def __len__(self):
        return len(self._teamsByKey)

    def __iter__(self):
        for i in self._teamsByKey:
            yield self._teamsByKey[i]

    def keys(self):
        return self._teamsByKey.keys()

    @property
    def nb(self):
        return len(self._teamsByKey)


    @property
    def classroom(self):
        #type: () -> 'Classroom'
        #: Direct access to class room for convenience
        return self.groupList.classroom


class Team(object):

    def __init__(self, teamList, group):
        self.teamList=teamList  #type: TeamList
        self.key=group.key #type: Text
        self.group=group #type: 'Group'
        self.group.team=self   # set backward reference
        self.name=self.teamList.factory.name(self.key) #type:Text
        self.atGH=None

        self.memberByLogin = OrderedDict() #type: Dict[Text, Member]

    @property
    def members(self):
        return self.memberByLogin.values()


    @property
    def classroom(self):
        #type: () -> 'Classroom'
        #: Direct access to class room for convenience
        return self.teamList.classroom