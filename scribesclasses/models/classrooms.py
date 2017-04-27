# coding: utf-8

"""
Deals with Classrooms.
A classroom is described as a triplet (grade, course, nbOfGroups) e.g. ('l3miage','l3miage-bdsi',7).
This class implements the patterns to name repo, given access to local storage, to github storage, etc.


This could go in scribesbot, but seems to be more specific with the notion of Classroom
and more importantly -root -G conventions.
"""

import os

import githubbot
import githubbot.urls
import scribesclasses.models.groups


class Classroom(object):
    """
    Define the pattern for a classroom:
    - hq for headquarters
    - root for root repository
    - groups repositories

    For each of these repository different kind methods allow to get:
    - the name of the repository
    - its location on the local disk
    - a convenience method to transform a relative path into a absolute path on the local disk

    The class provide also a template facility allowing to make substitutions like {org_name},
    {hq_repo_name}, [hq_root_repo_dir}, {root_repo_account_url} in any text.
    """
    def __init__(self, classRoomFile='classroom.json', testingKey=None, localTopDir=None, defaultAccountInfo='scribesbot'):
        #: Filename for the classroom information file
        self.classRoomFile = classRoomFile

        #: str|NoneType
        #: If None, this is not a test, all groups are concerned
        #: If this is a string, this is the key of the test group (usually '00')
        self.testingKey = testingKey

        #: python/json representation of classroom information
        #: This information is taken from classroom.py but if testingKey
        #: is set, only a group remains.
        self.info = self._getInfo()

        #:  directory containing grades/classrooms structure
        self.localTopDir = None
        if localTopDir is not None:
            # take the parameter if set
            self.localTopDir = localTopDir
        elif 'localRoot' in self.info:
            # take the localRoot from json if set
            self.localTopDir = self.info['localRoot']
        else:
            # use the classroom file name and assume it is like this grade/course-hq/classroom.py
            self.localTopDir = os.path.join(os.path.dirname(classRoomFile),'..', '..')
        assert(os.path.isdir(self.localTopDir))

        self.grade = self.info["grade"]
        """ Grade, e.g. 'l3miage' """

        self.course = self.info["course"]
        """ Course, e.g. 'l3miage-bdsi' """

        self.hqSecret = self.info['headquarters']['secret']

        #: pattern for group names. By default 'G{key}' unless specified in json
        self.groupNamePattern = None
        if 'groupNamePattern' in self.info:
            self.groupNamePattern = self.info['groupNamePattern']
        else:
            self.groupNamePattern = 'G{key}'

        #: groups as a GroupList
        self.groupList = scribesclasses.models.groups.GroupList(self, self.info["groups"])

        self.nbOfGroups = len(self.groupList)  # TODO: remove this. Left during refactoring to avoid pb.
        """ Number of groups, excluding G00. This is the last number """

        self.defaultAccountInfo = defaultAccountInfo
        """ defaut for connecting to github, when not specified otherwize """

        self.canBeDeleted = \
            'canBeDeleted' in self.info \
            and self.info['canBeDeleted'] == '666'


        #: labelsSpec pairs, List[(label:string,color:string)]
        if 'labels' in self.info:
            self.labelSpecifications = self.info['labels'].items()
        else:
            self.labelSpecifications = []

        #: milestone maps
        # dict(labelsSpec(string->
        #    ["description":string, "deadline":string]
        if 'milestones in self.info' :
            self.milestoneSpecifications = self.info['milestones'].items()
        else:
            self.milestoneSpecifications = {}

        #: github respository for the root
        # This object will be set by ensureGroupAtGitHub
        self.rootRepo = None

    def account(self, accountInfo=None):
        return self.defaultAccountInfo if accountInfo is None else accountInfo

    def _getInfo(self):
        info = githubbot.load_json(self.classRoomFile)
        if self.testingKey is not None:
            # keep only the group corresponding to the testing Key
            for key in info['groups'].keys():
                if key != self.testingKey:
                    del info['groups'][key]
        return info

    #------ org ------------------------------------------------------------------------
    def org(self):
        """
        The github organization or grade such as "m2r"
        :return: grade
        """
        return self.grade

    def orgURL(self):
        """
        The URL of github organization (e.g. "http://github.com/l3miage")
        :return: url
        """
        return githubbot.urls.gitHubURL(path=self.org())

    def localOrgDirectory(self):
        """
        The directory of the organization on the local disk
        (e.g. /media/jmfavre/Windows/DEV/l3miage)
        :return: directory path
        """
        return os.path.join(self.localTopDir, self.org())


    #------ hq repository --------------------------------------------------------------
    def hqRepoName(self):
        """
        The headquarters repository (e.g. l3miage-bdsi-hq)
        :return:
        """
        return self.course + '-hq'

    def hqRepoURL(self, accountInfo=None, gitSuffix=False):
        """
        The headquarters repository URL with the account name given
        (e.g. https://escribis@github.com/l3miage/l3miage-bdsi-hq.git
        :param accountInfo: github login
        :return: url of the repo on github
        """
        return githubbot.urls.gitHubRepoURL(
            self.org(), self.hqRepoName(),
            gitSuffix=gitSuffix,
            accountInfo= self.account(accountInfo))

    def localHQRepoDirectory(self):
        """
        The headquarters directory on the local disk
        (e.g. /media/jmfavre/Windows/DEV/l3miage/l3miage-bdsi-hq)
        :return: the path to the local directory.
        """
        return os.path.join(self.localOrgDirectory(), self.hqRepoName())

    def localHQRepoPath(self, path):
        """
        Path to the specified item given as a relative path from the HQ directory.
        For instance for 'manage.py' this function will return something like
        /media/jmfavre/Windows/DEV/l3miage/l3miage-bdsi-hq/manage.py
        :param path: a relative path to the item (e.g. manage.py)
        :return: the absolute path to the item.
        """
        return os.path.join(self.localHQRepoDirectory(),path)

    def localHQBuildDirectory(self):
        return self.localHQRepoPath(os.path.join('.build'))

    def localHQBuildCommandsDirectory(self):
        """
        Path to the generated directory of script,
        """
        return self.localHQRepoPath(os.path.join('.build','bin'))

    def localHQBuildDocsDirectory(self):
        """
        Path to the generated documentation directory for the course
        """
        return self.localHQRepoPath(os.path.join('.build','docs'))

    def localHQSourceCommandsDirectory(self):
        """
        Path to the local command template directory or None if the directory does not exist,
        :return: the directory name or None
        """
        directory = self.localHQRepoPath('.commands')
        return directory if os.path.isdir(directory) else None


    #------ root repository ------------------------------------------------------------
    def rootRepoName(self):
        """
        Name of the "root" repository, e.g. l3miage-bdsi-root
        :return: name of the repository.
        """
        return self.course + '-root'

    def rootRepoURL(self, gitSuffix=False, accountInfo=None):
        """
        The root repository URL with the account name given
        (e.g. https://escribis@github.com/l3miage/l3miage-bdsi-root.git )
        :param accountInfo: github login
        :return: url of the repo on github
        """
        return githubbot.urls.gitHubRepoURL(
            self.org(), self.rootRepoName(),
            gitSuffix=gitSuffix,
            accountInfo=self.account(accountInfo))

    def localRootRepoDirectory(self):
        """
        Path to the root repo on the local disk,
        e.g. /media/jmfavre/Windows/DEV/l3miage/l3miage-bdsi-root
        :return: path of to the local repository.
        """
        return os.path.join(self.localOrgDirectory(),self.rootRepoName())

    def localRootRepoPath(self, path):
        """
        Path to the specified item given as a relative path from the root directory.
        For instance for 'README.rst' this function will return something like
        /media/jmfavre/Windows/DEV/l3miage/l3miage-bdsi-root/README.rst
        :param path: a relative path to the item (e.g. manage.py)
        :return: the absolute path to the item.
        """
        return os.path.join(self.localRootRepoDirectory(),path)

    def rootRepoDescription(self):
        return 'This repository provides skeletons for group repositories. DO NOT FORK!'

    #------ group repository ------------------------------------------------------------

    # TODO: Check if the group methods should go to groups package


    def groupRepoNamePattern(self):
        """
        Pattern for group repo. Could be refined by subclassing Classroom.
        The pattern must contain the string "{key}" for the key of the group.
        :return: a pattern like l3miage-bdsi-G{key}
        """
        return self.course + '-'+self.groupNamePattern

    def groupRepoName(self, key):
        """
        Repository name with for the group specified.
        :param key: The key of the group (e.g. '02')
        :return: the repository name (e.g.'l3miage-bdsi-G02')
        """
        return self.groupRepoNamePattern().format(key=key)

    def groupRepoURL(self, key, gitSuffix=False, accountInfo=None):
        """
        Repository URL to the specified group and with the specified account.
        :param key: The key of the group (e.g. '02')
        :param accountInfo: github account used to access to the repository
        :return: the repository URL (e.g. 'https://escribis@github.com/l3miage/l3miage-bdsi-G02.git')
        """
        return githubbot.urls.gitHubRepoURL(
            self.org(), self.groupRepoName(key=key),
            gitSuffix=gitSuffix,
            accountInfo=self.account(accountInfo))

    def localGroupsDirectory(self):
        return os.path.join(self.localOrgDirectory(),self.course+'-groups')

    def localGroupRepoDirectory(self, key):
        return os.path.join(self.localGroupsDirectory(),self.groupRepoName(key))

    def localGroupRepoPath(self, key, path):
        return os.path.join(self.localGroupRepoDirectory(key),path)

    def groupRepoTitlePattern(self):
        return self.groupNamePattern+' group repository'

    #------ teams -----------------------------------------------------------------------
    def groupTeamNamePattern(self):
        """
        Pattern for teams. Could be refined via subclassing. The pattern must contains
        the string '{key}' for the key of the group.
        :return:
        """
        return self.groupNamePattern

    # ------ labelsSpec -----------------------------------------------------------------------




    #------ web -------------------------------------------------------------------------



    def webGroupSecretDirectory(self, key):
        """
        Name of the subdirectory for the group web information.
        :param key: e.g. 03
        :return: something like 'groups/GPI03-m92334Gj'
        """
        group_name = self.groupNamePattern.format(key=key)
        return '%s-%s' % (group_name, self.groupList[key].secret)

    def localWebRepoDirectory(self):
        """
        Path to the web repo on the local disk,
        There is only one for the grade, not one for each course.
        e.g. /media/jmfavre/Windows/DEV/l3miage/l3miage.github.io
        :return: path of to the local web repository.
        """
        return os.path.join(self.localOrgDirectory(),self.webRepoName())

    def localWebGradePath(self, path=''):
        """
        Path to the specified item given as a relative path from grade web directory.
        For instance for 'README.rst' this function will return something like
        /media/jmfavre/Windows/DEV/l3miage/l3miage.github.io/README.rst
        :param path: a relative path to the item (e.g. manage.py)
        :return: the absolute path to the item.
        """
        return os.path.join(self.localOrgDirectory(),self.webRepoName(),path)

    def localWebCoursePath(self, path=''):
        """
        Path to the specified item given as a relative path from the **course** web directory.
        While most other functions are independent from the course, this one
        is specific to the course of the current classroom.
        For instance for 'README.rst' this function will return something like
        /media/jmfavre/Windows/DEV/l3miage/l3miage.github.io/l3miage-bdsi/README.rst
        :param path: a relative path to the item (e.g. manage.py)
        :return: the absolute path to the item.
        """
        return os.path.join(self.localOrgDirectory(),self.webRepoName(),os.path.join(self.course,path))

    def localWebHQPath(self, path=''):
        hq_dir = 'headquarters-%s' % self.hqSecret
        return self.localWebCoursePath(os.path.join(hq_dir, path))

    def localWebGroupPath(self, key, path=''):
        group_directory = self.webGroupSecretDirectory(key)
        return self.localWebCoursePath(os.path.join('groups',group_directory,path))




    def webRepoName(self):
        """
        Repository name for the web repo.
        There is only one for the grade, not one for each course.
        :return: the repository name (e.g.'l3miage.github.io')
        """
        return '%s.github.io' % self.grade

    def webRepoURL(self, path='', gitSuffix=False):
        """
        The web repository URL with the account name given.
        There is only one for the grade, not one for each course.
        (e.g. https://escribis@github.com/l3miage/l3miage.github.io.git )
        :param accountInfo: github login
        :return: url of the repo on github
        """
        return githubbot.urls.gitHubWebURL(
            self.grade,
            path)

    def webCourseURL(self, path=''):
        return self.webRepoURL(
                path=self.course+'/'+path)

    def webGroupURL(self, key, path='', accountInfo=None):
        return self.webCourseURL(
                path='groups/'+self.webGroupSecretDirectory(key)+'/'+path)


    def substitutions(self, key=None, accountInfo=None, substs=None):
        """
        Generate a dictionnary of substitutions. See the code for the
        name of substituions defined.
        :param key: optional. The key of the group. None otherwise.
        :param accountInfo: optional. The github access for githuub. None otherwise.
        :param substs: optional dict[str,str]. A lists of substitutions.
        :return: dict[str,str] All substitutions defined + the user defined subsitutions.
        """

        s = dict()

        # TODO: add web related variables

        s['org_name'] = self.org()
        s['org_url'] = self.orgURL()
        s['local_org_dir'] = self.localOrgDirectory()

        s['hq_repo_name'] = self.hqRepoName()
        s['hq_repo_url'] = self.hqRepoURL()
        s['hq_repo_account_url'] = \
            self.hqRepoURL(accountInfo=self.account(accountInfo))
        s['hq_root_repo_dir'] = self.localHQRepoDirectory()
        s['hq_build_dir'] = self.localHQBuildDirectory()

        s['root_repo_name'] = self.rootRepoName()
        s['root_repo_url'] = self.rootRepoURL()
        s['root_repo_account_url'] = \
            self.rootRepoURL(accountInfo=self.account(accountInfo))
        s['local_root_repo_dir'] = self.localRootRepoDirectory()


        s['local_groups_dir'] = self.localGroupsDirectory()

        if key is not None:
            s['key'] = key
            s['group_repo_name']= self.groupRepoName(key=key)
            s['group_repo_url'] = self.groupRepoURL(key=key)
            s['group_repo_account_url'] = \
                self.groupRepoURL(key=key, accountInfo=self.account(accountInfo))
            s['local_group_repo_dir'] = self.localGroupRepoDirectory(key=key)

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
            "classRoomFile = %s" % self.classRoomFile,
            "localTopDir = %s" % self.localTopDir,
            "grade = %s" % self.grade,
            "course = %s" % self.course,
            'groupNamePattern = %s' % self.groupNamePattern,
            'defaultAccountInfo = %s' % self.defaultAccountInfo]
        body = '\n'.join(["    "+s for s in _])
        return "classroom\n"+body

# print '='*80
# print __name__ + ' reloaded'
# print '='*80
