from collections import OrderedDict


class Member(object):
    # Not used Yet
    def __init__(self):

        self.firstName = None
        self.lastName = None

        #: github login
        self.login = None

        #: email
        self.email = None

        #: group, the group containing this member
        self.group = None



def keyRange(min, max, numberOfDigits=2):
    """
    e.g. keyRange(0,3) = ['00', '01', '02', '03']
    """
    pattern = '{key:0%s}' % numberOfDigits
    return [pattern.format(key=i) for i in range(min,max+1)]






class Group(object):
    def __init__(self, groupList, key, secret):
        self.key = key

        #: Direct access to class room for convenience
        self.classRoom = groupList.classRoom
        self.secret = secret

        # will be set by ensure Group if called. Github object
        # FIXME: this should be fixed. It should be executed even when deleting the group (see manage.py)
        self.members = set()
        self.groupList = groupList

        #---- representation on github ------------------------
        self.ghOrgName = self.classRoom.org()

        # group repository
        self.ghRepoName = self.classRoom.groupRepoName(key=key)
        self.ghRepoTitle = \
            self.classRoom.groupRepoTitlePattern().format(key=key)

        # will be set by ensure Group if called. Github object
        # FIXME: this should be fixed. It should be executed even when deleting the group (see manage.py)
        self.ghRepo = None

        # group team
        self.ghTeamName = \
            self.classRoom.groupTeamNamePattern().format(key=key)

        # will be set by ensure Group if called. Github object
        # FIXME: this should be fixed. It should be executed even when deleting the group (see manage.py)
        self.ghTeam = None


class GroupList(object):
    def __init__(self, classRoom, groupsInfo):
        """
        Create group list given a python representation of json (dict/list)
        of the list of groups coming from the classroom info file.
        :param groupsInfo: dict/dict corresponding to json
        :return: GroupList with Group object created inside
        """
        self.classRoom = classRoom
        self._groupMap = OrderedDict()
        for key in sorted(groupsInfo.keys()):
            self._groupMap[key] = Group(
                groupList=self,
                key=key,
                secret=groupsInfo[key]['secret']
            )

    def __getitem__(self, key):
        return self._groupMap[key]

    def __len__(self):
        return len(self._groupMap)

    def __iter__(self):
        for i in self._groupMap:
            yield self._groupMap[i]

    def keys(self):
        return self._groupMap.keys()