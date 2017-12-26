
from typing import Text, List, Optional
import os
from collections import OrderedDict
from abc import ABCMeta, abstractproperty

import githubbot.urls
import github.Repository
GH_Repository=github.Repository.Repository


from scribesclasses.models.labels import (
    LabelConfig,
    toLabelConfigList,
    Label
)
from scribesclasses.models.milestones import (
    MilestoneConfig,
    toMilestoneConfigList,
    Milestone
)
from scribesclasses.models.configurations import (
    toBool,
    toText
)

class RepositoryConfiguration(object):
    def __init__(self,
                 classroom,
                 id,
                 name,
                 description=None,
                 secret=None,
                 private=None,
                 hasIssue=None,
                 hasWiki=None,
                 hasDownloads=None,
                 labelConfigList=None,
                 noStandardLabels=None,
                 milestoneConfigList=None
                 ):

        def _choice(value, configpath, default=None, err=None, f=toText):
            return self.classroom.config.choice(
                value, configpath, default=default, err=err, f=f)

        self.classroom=classroom
        #type: 'Classroom'

        self.id=id
        #type: Text

        self.name=name
        #type: Text

        self.description=_choice(description, [id,'description'], '')
        #type: Text

        self.secret=_choice(secret, [id,'secret'], None)
        #type: Optional[Text]

        self.private=_choice(private, [id,'private'], True, f=toBool)
        #type: bool

        self.hasIssue=_choice(hasIssue, [id,'hasIssue'], True, f=toBool)
        #type: bool

        self.hasWiki=_choice(hasWiki, [id,'hasWiki'], True, f=toBool)
        #type: bool

        self.hasDownloads=\
            _choice(hasDownloads, [id,'hasDownloads'], True,  f=toBool)
        #type: bool

        self.noStandardLabels= \
            _choice(noStandardLabels, [id, 'noStandardLabels'], True, f=toBool)

        self.labelConfigList=\
            _choice(
                labelConfigList,
                ['labels'],
                default={},
                f=toLabelConfigList)
        #type: List[LabelConfig]

        self.milestoneConfigList=\
            _choice(
                milestoneConfigList,
                ['milestones'],
                default={},
                f=toMilestoneConfigList)
        #type: List[MilestoneConfig]




class Repository(object):
    __metaclass__ = ABCMeta

    def __init__(self,
                 classroom,
                 id,
                 repoConfig):
        self.classroom=classroom
        self._id=id
        self.repoConfig=repoConfig
            # (
            # repoConfig if repoConfig is not None
            # else RepositoryConfiguration(
            #     classroom, id))
        self.name=self.repoConfig.name
        self.description=self.repoConfig.description
        self.secret=self.repoConfig.secret
        self.private=self.repoConfig.private
        self.hasIssue=self.repoConfig.hasIssue
        self.hasWiki=self.repoConfig.hasWiki
        self.hasDownloads=self.repoConfig.hasDownloads
        self.secret=self.repoConfig.secret

        self.atGH=None #type: Optional[GH_Repository]
        # will be set by ensure repo

        self.noStandardLabels=self.repoConfig.noStandardLabels
        # create (unbound) labels
        self.labelNamed=OrderedDict()
        for lconf in self.repoConfig.labelConfigList:
            Label(
                repo=self,
                name=lconf.name,
                color=lconf.color,
                atGH=None)

        # create (unbound) milestones
        self.milestoneEntitled=OrderedDict()
        for mconf in self.repoConfig.milestoneConfigList:
            Milestone(
                repo=self,
                title=mconf.title,
                description=mconf.description,
                dueOn=mconf.due_on,
                atGH=None)



    @property
    def id(self):
        return self._id

    @property
    def labels(self):
        return self.labelNamed.values()

    @property
    def milestones(self):
        return self.milestoneEntitled.values()

    @property
    def secretLabel(self):
        if self.secret is None:
            return self.name
        else:
            return '%s-%s' % (self.name, self.secret)

    @property
    def url(self):
        """
        The repository URL
        (e.g. https://escribis@github.com/l3miage/l3miage-bdsi-hq.git
        # :param accountInfo: github login
        :return: url of the repo on github
        """
        return self.getURL()

    def getURL(self, relPath='', accountInfo=''):
        """
        The repository URL with the account name given
        (e.g. https://escribis@github.com/l3miage/l3miage-bdsi-hq/a/x.txt
        """
        path = '%s/%s/%s' % (
            self.classroom.org.name,
            self.name,
            relPath
        )
        return githubbot.urls.gitHubURL(path, accountInfo)

    def getFileURL(self, filePath='', accountInfo=''):
        """
        https://github.com/l3miage/l3miage-bdsi-hq/blob/master/a/x.txt
        """
        githubbot.urls.gitHubFileURL(
            org=self.classroom.org.name,
            repo=self.name,
            file=filePath
        )

    @abstractproperty
    def dir(self):
        pass

    def path(self, path):
        """
        Path to the specified item given as a relative path from the local directory.
        For instance for 'manage.py' this function will return something like
        /media/jmfavre/Windows/DEV/l3miage/l3miage-bdsi-hq/manage.py
        :param path: a relative path to the item (e.g. manage.py)
        :return: the absolute path to the item.
        """
        return os.path.join(
            self.dir,
            path)


class WebRepository(Repository):

    def __init__(self, classroom):
        id='web'
        super(WebRepository, self).__init__(
            classroom=classroom,
            id=id,
            repoConfig=(
                RepositoryConfiguration(
                    classroom=classroom,
                    id=id,
                    name='%s.github.io' % classroom.grade,
                    description='Web repository for %s'
                                % classroom.grade
                )),
        )

    @property
    def dir(self):
        """
        e.g. /media/jmfavre/Windows/DEV/l3miage/l3miage.github.io
        """
        return os.path.join(
            self.classroom.org.dir,
            self.name)

    @property
    def courseDir(self):
        """
        e.g. /media/jmfavre/Windows/DEV/l3miage/l3miage.github.io/l3miage-bdsi
        """
        return self.path(self.classroom.course)

    def coursePath(self, relpath=''):
        return os.path.join(self.courseDir, relpath)

    @property
    def courseURL(self):
        return self.getCourseURL()

    def getCourseURL(self, relPath=''):
        """
        https://github.com/l3miage/l3miage.github.io/l3miage-bdsi/x/y/z
        """
        return self.getURL('%s/%s' %
           (self.classroom.course,
            relPath))

    def localRepoWebPath(self, repo):
        #type: (Repository) -> Text
        return self.coursePath(repo.secretLabel)

    def repoURL(self, repo):
        #type: (Repository) -> Text
        return self.getCourseURL(
            repo.secretLabel
        )



class RegularRepository(Repository):

    def __init__(self, classroom, id, repoConfig=None):
        super(RegularRepository, self).__init__(
            classroom=classroom,
            id=id,
            repoConfig=repoConfig)

    @property
    def dir(self):
        """
        The directory on the local disk
        (e.g. /media/jmfavre/Windows/DEV/l3miage/l3miage-bdsi-hq)
        :return: the path to the local directory.
        """
        return os.path.join(
            self.classroom.org.dir,  #XXX
            self.name)

    @property
    def web(self):
        """
        The web repository
        """
        return self.classroom.web

    @property
    def webDir(self):
        return self.webPath()

    def webPath(self, relPath=''):
        #type: (Text) -> Text
        return self.web.coursePath(
            os.path.join(self.secretLabel, relPath))


class MainRepository(RegularRepository):
    pass


class RootRepository(MainRepository):
    def __init__(self, classroom):
        id='root'
        super(RootRepository, self).__init__(
            classroom=classroom,
            id=id,
            repoConfig=(
                RepositoryConfiguration(
                    classroom=classroom,
                    id=id,
                    name='%s-%s' % (
                        classroom.course,
                        id
                    ),
                    description='DO NOT FORK! This repository contains skeletons'
                )),
        )


class InfoRepository(MainRepository):
    def __init__(self, classroom):
        id='info'
        super(InfoRepository, self).__init__(
            classroom=classroom,
            id=id,
            repoConfig=(
                RepositoryConfiguration(
                    classroom=classroom,
                    id=id,
                    name='%s-%s' % (
                        classroom.course,
                        id
                    ),
                    description='Information about the course'
                )),
        )

class HQRepository(MainRepository):
    def __init__(self, classroom):
        id='hq'
        super(HQRepository, self).__init__(
            classroom=classroom,
            id=id,
            repoConfig=(
                RepositoryConfiguration(
                    classroom=classroom,
                    id=id,
                    name='%s-%s' % (
                        classroom.course,
                        id
                    ),
                    description='Headquarters. This repository is visible by staff only!'
                )),
        )

    @property
    def buildDir(self):
        return self.path('.build')

    @property
    def buildCommandsDir(self):
        """
        Path to the generated directory of script,
        """
        return os.path.join(self.buildDir, 'bin')

    @property
    def buildDocsDir(self):
        """
        Path to the generated documentation directory for the course
        """
        return os.path.join(self.buildDir, 'docs')

    @property
    def sourceCommandsDir(self):
        """
        Path to the local command template directory or None if the directory does not exist,
        :return: the directory name or None
        """
        directory = self.path('.commands')
        return directory if os.path.isdir(directory) else None


class GroupRepository(RegularRepository):
    def __init__(self, group):
        self.group=group
        id=self.group.key
        super(GroupRepository, self).__init__(
            classroom=self.group.classroom,
            id=id,
            repoConfig=(
                RepositoryConfiguration(
                    classroom=self.group.classroom,
                    id=id,
                    name=self.group.groupList.factory.repoName(self.group.key),
                    description=self.group.groupList.factory.repoDescription(
                    key=group.key)
                )),
        )

    @property
    def dir(self):
        """
        The directory on the local disk
        (e.g. /media/jmfavre/Windows/DEV/l3miage/groups/l3miage-bdsi-G12)
        :return: the path to the local directory.
        """
        return os.path.join(
            self.group.groupList.groupsDir,
            self.name)
