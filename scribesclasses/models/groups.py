from __future__ import print_function
from typing import Text, Optional
import os
from collections import OrderedDict

from scribesclasses.models.repositories import (
    GroupRepository
)

def keyRange(min, max, numberOfDigits=2):
    """
    e.g. keyRange(0,3) = ['00', '01', '02', '03']
    """
    pattern = '{key:0%s}' % numberOfDigits
    return [pattern.format(key=i) for i in range(min,max+1)]



class GroupFactory(object):
    """
    Patterns for group and way to apply these patterns
    """

    def __init__(self,
                 groupList,
                 namePattern='G{key}',
                 repoDescriptionPattern=
                    '{namepat} group repository',
                 repoNamePattern=
                    '{course}-{namepat}'
                 ):
        self.groupList=groupList
        self.namePattern=namePattern
        self.repoDescriptionPattern=repoDescriptionPattern
        self.repoNamePattern=repoNamePattern

    def name(self, key=None):
        """
        The name of the group or the pattern
        If None return the key-based pattern
        such as 'G{key}'.
        Otherwise return something like 'G12'
        """
        p=self.namePattern
        print('=============',p)

        if key is None:
            return p
        else:
            return p.format(key=key)

    def repoName(self, key):
        """
        The repository name of the group or the pattern
        If None return the key-based pattern
        such as 'l3miage-bdsi-G{key}'.
        Otherwise return something like 'l3miage-bdsi-G12'
        """
        p=self.repoNamePattern.format(
            course=self.groupList.classroom.course,
            namepat=self.namePattern)
        print('=============',self.groupList.classroom.course)
        print('-------------', self.namePattern)
        print('--------------', self.repoNamePattern)
        exit(0)

        if key is None:
            return p
        else:
            return p.format(key=key)


    def repoDescription(self, key=None):
        """
        If None return the key-based pattern
        such as 'G{key} group repository'.
        Otherwise return something like
        'G12 group repository'
        """
        p=self.repoDescriptionPattern.format(
            namepat=self.namePattern)
        if key is None:
            return p
        else:
            return p.format(key=key)



class GroupList(object):
    def __init__(self,
                 classroom,
                 groupsInfo,
                 groupNamePattern):
        """
        Create group list given a python representation
        of json (dict/list) of the list of groups coming
        from the classroom info file.
        :param groupsInfo: dict/dict corresponding to json
        :return: GroupList with Group object created inside
        """
        self.classroom=classroom
        self.factory=GroupFactory(
            groupList=self,
            namePattern=groupNamePattern)
        self._groupByKey = OrderedDict()
        for key in sorted(groupsInfo.keys()):
            self._groupByKey[key] = Group(
                groupList=self,
                key=key,
                secret=groupsInfo[key]['secret']
            )

    def __getitem__(self, key):
        return self._groupByKey[key]

    def __len__(self):
        return len(self._groupByKey)

    def __iter__(self):
        for i in self._groupByKey:
            yield self._groupByKey[i]

    def keys(self):
        return self._groupByKey.keys()

    @property
    def nb(self):
        return len(self._groupByKey)

    @property
    def groupsDir(self):
        return os.path.join(
            self.classroom.org.dir,
            self.classroom.course+'-groups')


class Group(object):
    def __init__(self, groupList, key, secret, team=None):
        self.groupList = groupList #type: GroupList
        self.key = key #type: Text
        self.secret = secret #type: Text
        self.team = team #type: Optional['Team']
        #type: will be set in team constructor
        self.repo=GroupRepository(self)

    @property
    def classroom(self):
        #type: () -> 'Classroom'
        #: Direct access to class room for convenience
        return self.groupList.classroom










