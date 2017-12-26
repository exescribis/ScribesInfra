# coding: utf-8

from typing import Text, Optional, List
import os
from collections import OrderedDict

from scribesclasses.models.groups import (
    GroupList,
)
from scribesclasses.models.teams import (
    TeamList
)
from scribesclasses.models.repositories import (
    RootRepository,
    InfoRepository,
    HQRepository,
    WebRepository,
)
from scribesclasses.models.organizations import (
    Organization
)
from scribesclasses.models.configurations import (
    Configuration,
)



class Classroom(object):
    """
    Define the pattern for a classroom:
    - hq/root/info repositories
    - groups repositories

    The class provide also a template facility allowing
    to make substitutions like {org_name},
    {hq_repo_name}, [hq_root_repo_dir},
    {root_repo_account_url} in any text.
    """
    def __init__(self,
                 classroomFile='classroom.json',
                 topDir=None,
                 defaultAccountInfo=None,
                 ):
        #type: (Text, Optional[Text], Text) -> None
        self.config = Configuration(classroomFile)
        #type: Configuration

        #:  local directory containing grades/classrooms structure
        self.localTopDir=self._get_local_top_dir(topDir)
        #type: Text

        self.grade = self.config.param("grade", err=1) #type: Text
        """ Grade, e.g. 'l3miage' """

        self.course = self.config.param("course", err=1) #type: Text
        """ Course, e.g. 'l3miage-bdsi' """



        self.defaultAccountInfo = self.config.choice(
            defaultAccountInfo,
            'login',
            'scribesbot'
        ) #type: Text
        """ 
        Defaut for connecting to github, when not specified.
        """

        self.deletableRepositories = (
            self.config.param(
                'deletableRepositories', ()))
        #type: List[Text]


        self.org=Organization(self)  #type: Organization

        self.repoById=OrderedDict()

        self.repoById['hq']=HQRepository(self)
        self.repoById['info']=InfoRepository(self)
        self.repoById['root']=RootRepository(self)
        self.repoById['web']=WebRepository(self)

        self.groupList = GroupList(
            classroom=self,
            groupsInfo=self.config.param("groups", err=1),
            groupNamePattern=
                self.config.param('groupNamePattern', 'G{key}'))
        #type: GroupList

        self.teamList=TeamList(
            groupList=self.groupList,
            teamNamePattern=
                self.config.param('teamNamePattern', 'G{key}')
        )


    @property
    def hq(self):
        return self.repoById['hq']

    @property
    def info(self):
        return self.repoById['info']

    @property
    def root(self):
        return self.repoById['root']

    @property
    def web(self):
        return self.repoById['web']


    def _get_local_top_dir(self, dir=None):
        """
        Compute the top level directory. For instance DEV.
        This directory contains the different grades.
        For instance we can have DEV/l3miage/l3miage-bdsi-root
        """
        if dir is not None:
            # take the parameter if set
            top_dir=dir
        else:
            p=self.config.param('localRoot', None)
            if p is not None:
                top_dir=p
            else:
                # use the classroom file name and assume
                # it is like this grade/course-hq/classroom.py
                top_dir = os.path.join(
                    os.path.dirname(self.config.filename),
                    '..', '..')
        assert (os.path.isdir(top_dir))
        return top_dir


    def account(self, accountInfo=None):
        return (
            self.defaultAccountInfo if accountInfo is None
            else accountInfo)




    def substitutions(self, key=None, accountInfo=None, substs=None):
        """
        Generate a dictionary of substitutions. See the code for the
        name of substituions defined.
        :param key: optional. The key of the group. None otherwise.
        :param accountInfo: optional. The github access for githuub. None otherwise.
        :param substs: optional dict[str,str]. A lists of substitutions.
        :return: dict[str,str] All substitutions defined + the user defined subsitutions.
        """

        s = dict()

        # TODO: add web related variables

        s['org_name'] = self.org.name
        s['org_url'] = self.org.url
        s['local_org_dir'] = self.org.dir


        #------ hq ----------------------------------
        s['hq_repo_name'] = self.hq.name
        s['hq_repo_url'] = self.hq.url
        s['hq_repo_account_url'] = \
            self.hq.getURL(accountInfo=self.account(accountInfo))
        s['hq_root_repo_dir'] = self.hq.dir
        s['hq_build_dir'] = self.hq.buildDir


        #------ root --------------------------------
        s['root_repo_name'] = self.root.name
        s['root_repo_url'] = self.root.url
        s['root_repo_account_url'] = \
            self.root.getURL(accountInfo=self.account(accountInfo))
        s['local_root_repo_dir'] = self.root.dir


        s['local_groups_dir'] = self.groupList.groupsDir

        if key is not None:
            group=self.groupList[key]
            s['key'] = key
            s['group_repo_name']=group.repo.name
            s['group_repo_url'] = group.repo.url
            s['group_repo_account_url'] = group.repo.getURL(
                accountInfo=self.account(accountInfo))
            s['local_group_repo_dir'] = group.repo.dir

        if substs is not None:
            s.update(substs)
        return s

    def substitute(self, text, key=None, accountInfo=None, substs=None):
        """
        Replace subsitutions in the given template text.
        See the method substitutions.
        :param key: optional. The key of the group. None otherwise.
        :param accountInfo: optional. The github access for githuub. None otherwise.
        :param substs: optional dict[str,str]. A lists of substitutions.
        :return: dict[str,str] All substitutions defined + the user defined subsitutions.
        """
        s = self.substitutions(key=key, accountInfo=self.account(accountInfo), substs=substs)
        return text.format(**s)


    def __str__(self):
        _ = [
            "classroomFile = %s" % self.config.filename,
            "localTopDir = %s" % self.localTopDir,
            "grade = %s" % self.grade,
            "course = %s" % self.course,
            'groupNamePattern = %s' % self.groupList.factory.namePattern,
            'defaultAccountInfo = %s' % self.defaultAccountInfo]
        body = '\n'.join(["    "+s for s in _])
        return "classroom\n"+body

