# coding: utf-8

import os
import re
from string import center

import collections
import githubbot.issues
import githubbot.labels
import githubbot.logicalissues
import githubbot.urls
from githubbot import file_content, load_json
import scribesclasses.models.subtasks

WORK_DEFINITION_LABEL_INFO  = ('WorkDefinition','fbca04')
WORK_ITEM_LABEL_INFO        = ('WorkItem', 'f0c000')





class WorkItem(object):
    pass


class Work(object):
    """
    A `Work` made of one `WorkDefinition` and many `WorkItem`s.

    On the local disk a `work` is represented in a directory with:
    * a file ``work.text.md`` which contains the text for definition and items.
    * a file ``work.info.json`` which contains meta information about the work
    * a file ``work.issues.gen.txt`` when the work is created on GitHub as issues.
    * a file ''work.state.json'' when the work is synchronized (update from githhub)

    On GitHub a `work` is implmented by
    * one `Issue` in the `DefinitionRepository` labelled WORK_DEFINITION_LABEL_INFO
    * a set of `Issue`s in the `ItemRepository`s labbled WORK_ITEM_LABEL_INFO

    The mapping between the `WorkDefinition` and the `WorkItem`s created
    or modified is stored in a the ``work.issues.gen.txt`` file.

    The lines before '__________' in the ``work.text.md`` file describes the
    `WorkDefinitionIssue`. The remaining lines are for the `WorkItemIssue`s.
    These lines can contains subtasks lines with check boxes following the
    SUBTASKS_PATTERN.

    WARNING: A github session must be opened before creating a work.
    ---------------------------------------------------------------

    Creating a Work access to github issues of the respective repositories,
    just to check if but do not modify it. To save all issues use save().
    WARNING: if the group issues have been modified in the meantime by students
    their changes will be lost (in particular check boxes for progress).
    Use saveDefinition to update only the definition item.

    Use the show() method to see the status of a work.


    Example of work.info.json
    {
      "labels": {
        "CyberResidencesOCL":"bfd4f2",
        "CyberBibliotheque":"bfd4f2"

      },
      "substitutions": {
        "EXAMPLEOFSUBST": "Ceci est un exemple de substitution"
      },
      "milestone": {
        "v1":""
      }
    }


    """

    @staticmethod
    def textFilePath(workDirectory):
        return os.path.join(workDirectory, 'work.text.md')

    @staticmethod
    def infoFilePath(workDirectory):
        return os.path.join(workDirectory, 'work.info.json')

    @staticmethod
    def issuesFilePath(workDirectory):
        return os.path.join(workDirectory, 'work.issues.gen.txt')


    def __init__(self,
                 workDirectory,
                 orgName,
                 definitionRepoName,
                 itemKeys=None, itemRepoNamePattern=None,
                 verbose=False):
        """
        Create/read a work from the specified source. GitHub is accessed but
        not modified. Use the show() method to display the work.

        :param workDirectory:
            The directory where the work files are stored locally.
            e.g. /home/jmfavre/DEV/m2gi/m2gi-idm-hq/CyberBiblibliotheque/.assignments/USE
        :param orgName: e.g.
            The GitHub organization where issues are created/stored 'orgName'
            e.g. "m2gi"
        :param definitionRepoName:
            The GitHub repo name for the definition issue.
            e.g. 'm2r-aeis-root'
        :param itemKeys:
            The list of keys for the group repositories.
            e.g. ['01','02'],
        :param itemRepoNamePattern:
            The pattern for item repositories. The pattern must contain "{key}"
            e.g. 'm2r-aeis-G{key}'
        :return:
            The work object created (if new it is not saved yet on github)


        Substitutions available in definitionTitlePattern, definitionBodyPattern:

        * 'definition_org_name'  : 'm2r'
        * 'definition_repo_name' : 'm2r-aeis-root'
        * 'definition_org_repo'  : 'm2r/m2r-aeis-root'
        * 'definition_repo_url'  : 'https://github.com/m2r/m2r-aeis-root'
        * 'definition_repo_file' : 'https://github.com/m2r/m2r-aeis-root/blob/master/'
        * 'org_name': 'm2r'
        * 'repo_name': 'm2r-aeis-root'
        * 'org_repo': 'm2r/m2r-aeis-root'
        * 'repo_url': 'https://github.com/m2r/m2r-aeis-root'
        * 'repo_link': '[m2r-aeis-root](https://github.com/m2r/m2r-aeis-root)'
        * 'repo_file': 'https://github.com/m2r/m2r-aeis-root/blob/master/'

        Additional substitutions available in itemRepoNamePattern

        * 'key' : '02'

        Substitution for itemBodyPattern

        * 'definition_org_name'  : 'm2r'
        * 'definition_repo_name' : 'm2r-aeis-root'
        * 'definition_org_repo'  : 'm2r/m2r-aeis-root'
        * 'definition_repo_url'  : 'https://github.com/m2r/m2r-aeis-root'
        * 'definition_repo_file' : 'https://github.com/m2r/m2r-aeis-root/blob/master/'
        * 'definition_issue_ref' : 'm2r/m2r-aeis-root#12'
        * 'key' : '02'
        * 'org_name': 'm2r'
        * 'repo_name': 'm2r-aeis-G12'
        * 'org_repo': 'm2r/m2r-aeis-G12'
        * 'repo_url': 'https://github.com/m2r/m2r-aeis-G12'
        * 'repo_link': '[m2r-aeis-G12](https://github.com/m2r/m2r-aeis-G12)'
        * 'repo_file': 'https://github.com/m2r/m2r-aeis-G12/blob/master/'




        """
        if verbose:
            print 'Loading work from: %s' % workDirectory

        #----- save parameters ----------------------------------------------
        self.verbose = verbose
        self.workDirectory = workDirectory
        self.orgName = orgName
        self.definitionRepoName = definitionRepoName
        self.itemKeys = itemKeys
        self.itemRepoNamePattern = itemRepoNamePattern


        #----- compute local files locations --------------------------------
        # reads .work.md and .issues.md files and set corresponding parameters
        self.workDirectory = workDirectory
        self.workName = os.path.basename(self.workDirectory)
        self.textFile = Work.textFilePath(self.workDirectory)
        self.infoFile = Work.infoFilePath(self.workDirectory)
        self.issuesFile = Work.issuesFilePath(self.workDirectory)


        #----- substitutions --------------------------------------------------
        # The substitutions will be augment with the id of the definition issue
        # when it is saved and by key for items.
        #
        #
        # self._workSubstitutions = {}  # will be augemented via _addWorkSubstitutions
        # self.__addDefinitionSubstitutions(issueRef=None)  # will be defined later anyway


        #---- process info file --------------------------------------------
        # TODO: encapsulate this file management
        self.info = self.__loadInfoFile()
        self.infoFileSubstitutions = (
            {} if 'substitutions' not in self.info
            else self.info['substitutions'])
        #: labelsSpec : dictionary of labelsSpec to apply on the work
        #: defined in the json file

        #: dict(str,str) mapping label name -> color
        self.labelSpecifications = {}  #
        if 'labels' in self.info:
            self.labelSpecifications = self.info['labels']

        # TODO: add support for milestone here


        #---- process text file --------------------------------------------
        # TODO: encapsulate this file management
        self.definitionTitlePattern = None #defined by next method call
        self.definitionBodyPattern  = None #defined by next method call
        self.itemBodyPattern = None        #defined by next method call
        self.__loadTextFile()

        #---- process the issues file if any -------------------------------
        self.definitionIssueId = None         # initalized by __loadIssuesFile() or __saveDefinition()
        self.itemIssueIdMap = {}              # initalized by __loadIssuesFile() or __saveItems()
        self.isExistingWork = self.__loadIssuesFile()




        #---- attributes populated by bind()

        self.definitionIssueNumber = None     # will be set during bind()
        self.definitionLogicalIssue = None    # will be created by bind()

        self.itemLogicalIssueMap = {}         # will be populated by bind()
        self.allItemKeys = []                 # will be set during bind()
        self.oldItemKeys = []                 # will be set during bind()
        self.newItemKeys = []                 # will be set during bind()



        #---- check if there will be no problem with the patterns
        self.definitionTitlePreview = self.__trySubstitute(
                "Definition title of '%s'" % self.workName,
                self.definitionTitlePattern,
                self._getSubstitutionsForDefinition())
        self.definitionBodyPreview = self.__trySubstitute(
                "Definition title of '%s'" % self.workName,
                self.definitionBodyPattern,
                self._getSubstitutionsForDefinition())
        self.itemBodyPatternPreview = self.__trySubstitute(
                "Item body pattern od '%s'" % self.workName,
                self.itemBodyPattern,
                self._getSubstitutionsForItem(
                        key='00',
                        definitionIssueRef=None,
                        preview=True))

        self.hasBeenBoundWithGitHub = False             # does bind() has been executed?
        self.hasDefinitionBeenSavedToGitHub = False     # does the work has been saved?
        self.hasDefinitionLabelsBeenSavedToGitHub = False
        self.hasItemsBeenSavedToGitHub = False
        self.hasItemsLabelsBeenSavedToGitHub = False

        self.__WorkSubtasksProgress = None              # managed by WorkSubtasksProgress

        if self.verbose:
            print 'work specification loaded from: %s' % workDirectory



    #----- info file -------------------------------------------------------------------------

    def __loadInfoFile(self):
        if os.path.isfile(self.infoFile):
            return load_json(self.infoFile)
        else:
            return {}

    def __loadTextFile(self):
        work_content = file_content(self.textFile)
        sections = re.split('________*',work_content)

        # extract WorkDefinition
        def_lines = sections[0].strip().split('\n')
        self.definitionTitlePattern = def_lines[0]
        self.definitionBodyPattern = '\n'.join(def_lines[2:])

        # extract WorkItem
        self.itemBodyPattern =  sections[1].strip()

    #----- issue file -------------------------------------------------------------------------

    def __loadIssuesFile(self):
        """
        load the issue file if it exist and set definitionIssueId
        and itemIssueIdMap. If the file does not exist then
        definitionIssueId will be None and itemIssueIdMap will be {}
        :return:
        """
        if (os.path.isfile(self.issuesFile)):
            lines = file_content(self.issuesFile).split('\n')
            self.definitionIssueId = lines[0].strip()
            # print 'Definition issue found: %s' % self.definitionIssueId
            self.itemIssueIdMap = {}
            for line in lines[1:]:
                _ = line.strip()
                if _ <> '':
                    fields = line.strip().split('|')
                    key = fields[0]
                    id = fields[1]
                    self.itemIssueIdMap[key]=id
                    # print 'Item "%s" issue found: %s' % (key,id)
            return True  # the work is existing
        else:
            # print 'No existing issues found'
            self.definitionIssueId = None
            self.itemIssueIdMap = {}
            return False  # the work is not existing

    def __saveIssueIds(self):
        if self.definitionIssueId is None:
            return
        else:
            with open(self.issuesFile, 'w') as f:
                f.write(self.definitionIssueId+'\n')
                for (key,logical_issue) in self.itemLogicalIssueMap.items():
                    if logical_issue.id() is not None:
                        f.write('%s|%s\n' % (key,logical_issue.id()))




    #---- substitutions --------------------------------------------------------------

    def __get_def_substitutions(self):
        """ Internal method used below
        :param issueRef: this value will be defined only when the issue is saved
        :param preview: if this is a preview, do not generate an exception if issueRef is None
        :return: dict
        """
        return {
            'definition_org_name'  : self.orgName,
            'definition_repo_name' : self.definitionRepoName,
            'definition_org_repo'  : '%s/%s' % (self.orgName, self.definitionRepoName),
            'definition_repo_url'  : githubbot.urls.gitHubURL('%s/%s' % (
                                        self.orgName, self.definitionRepoName)),
            'definition_repo_file' : githubbot.urls.gitHubFileURL(
                                        self.orgName, self.definitionRepoName)
        }

    def _getSubstitutionsForDefinition(self):
        """
        Return the substitutions available in the work efinition parts
        * substitutions from info file
        * definition substitutions (see __get_def_substitutions)
        * substitutions defined by the corresponding logical issue
        """
        s = self.infoFileSubstitutions.copy()
        s.update(self.__get_def_substitutions())
        return githubbot.logicalissues.LogicalIssue.getSubstitutions(
                self.orgName, self.definitionRepoName)

    def _getSubstitutionsForRepoNamePattern(self, key):
        s = self._getSubstitutionsForDefinition()
        s['key']=key
        return s

    def _getSubstitutionsForItem(self, key, definitionIssueRef=None, preview=False):
        """
        Return the substitutions available in the work item parts
        * substitutions from info file
        * definition substitutions (see __get_def_substitutions)
        * 'key'
        * 'definition_issue_ref' with an exception if None and not preview
        * substitutions defined by the corresponding logical issue
        """
        s = self.infoFileSubstitutions.copy()
        s.update(self.__get_def_substitutions())

        # add key
        s['key'] = key

        # add definition_issue_ref
        if definitionIssueRef is None:
            if preview:
                s['definition_issue_ref'] = '***NOT_DEFINED_YET***'
            else:
                raise Exception('Attempt to substitute definition_issue_ref but not defined')
        else:
            s['definition_issue_ref'] = definitionIssueRef

        # add stuff from logical issue
        item_repo_name = self.itemRepoName(key=key)
        return githubbot.logicalissues.LogicalIssue.getSubstitutions(
            self.orgName,
            item_repo_name,
            s)

    def __trySubstitute(self, label, text, substitutions):
        try:
            return text.format(**substitutions)
        except:
            print '>>> ERROR %s: substitution failed for the following text.' % label
            print text
            raise

    #----

    def itemRepoName(self, key):
        return self.itemRepoNamePattern.format(
            **self._getSubstitutionsForRepoNamePattern(key=key))






    #---- binding with github --------------------------------------------------------------

    @staticmethod
    def __checkMatch(kind, issueFile, value1, value2):
        if value1 <> value2:
            raise Exception(
                    '%s: item %s does not match: %s<>%s' % (
                        issueFile, kind, value1, value2))

    def bind(self):
        """
        Read gitHub and check if the repositories and issues that have been
        defined in the issues file (if it was there) are existing.
        In this step GitHub is accessed but just in read only mode.
        """

        if self.verbose:
            print 'Binding work to GitHub: %s' % self.workDirectory

        self.__bindDefinition()

        #---- work items -------------------------------------------
        # Create the mapping of LogicalIssue.
        # First load the ones from the file with the existing ids.
        # Check if the repository is compatible with what is specified now
        #
        # Either take the issue id from the issue file if one exist.
        # Otherwise the issue id will be null.
        # Create a new logical issue in all cases.
        self.itemLogicalIssueMap = {}
        # keep all keys that are in the files + the keys generated now
        # check that issues in the files are in proper org/repo
        self.allItemKeys = sorted(set(self.itemKeys) | set (self.itemIssueIdMap.keys()))
        self.oldItemKeys = sorted(set(self.itemIssueIdMap.keys()) - set(self.itemKeys))
        self.newItemKeys = sorted(set(self.itemKeys) - set(self.itemIssueIdMap.keys()))
        # print 'Items keys -- total: %i,  new: %i,  old: %i' % (
        #    len(self.allItemKeys), len(self.newItemKeys), len(self.oldItemKeys))

        self.__bindOldItems()
        self.__bindAllItems()

        # TODO: extract to method
        for (key,id) in self.itemIssueIdMap.items():
            (o,r,ns) = githubbot.issues.issue_id_info(id)
            Work.__checkMatch('organization',self.issuesFile,self.orgName,o)
            # TODO: check if the issue should be check as well
            n = int(ns)
        if self.verbose:
            print 'work bound successfully'
        self.hasBeenBoundWithGitHub = True


    def __bindDefinition(self):
        # ---- work definition -------------------------------------------
        # Create a LogicalIssue.
        # Either take the issue id from the issue file if one exist.
        # Otherwise the issue id will be null.
        # Create a new logical issue in all cases/ .
        if self.definitionIssueId is None:
            # no .issues.md file -> never defined
            self.definitionIssueNumber = None
        else:
            # reads existing definition issue id from file
            (o, r, ns) = githubbot.issues.issue_id_info(self.definitionIssueId)
            Work.__checkMatch('organization',self.issuesFile,self.orgName,o)
            Work.__checkMatch('organization',self.issuesFile,self.definitionRepoName,r)
            self.definitionIssueNumber = int(ns)
        if self.verbose:
            print 'Initializing WD logical issue for %s/%s: "%s" -> ' % (
                self.orgName,
                self.definitionRepoName,
                self.definitionTitlePattern
            ),
        self.definitionLogicalIssue = githubbot.logicalissues.LogicalIssue(
                orgName=self.orgName,
                repoName=self.definitionRepoName,
                titleTemplate='[WD] %s' % self.definitionTitlePattern,
                bodyTemplate=self.definitionBodyPattern,
                issueNumber=self.definitionIssueNumber
        )
        n = self.definitionLogicalIssue.issueNumber
        if self.verbose:
            print 'issue #%s' % ('NOT SAVED YET' if n is None else n)

    def __bindAllItems(self):
        for key in self.allItemKeys:
            org = self.orgName
            repo = self.itemRepoName(key=key)
            title = '[WI] %s' % self.definitionTitlePattern
            prefix = (    '*See WorkDefinition {definition_issue_ref}.*\n'
                    '*Check the checkboxes below (use GitHub interface)'
                    'as soon as each task is completed.*\n'
                    '______\n')
            body = prefix+self.itemBodyPattern
            # check if there is already an issue for this key in the issue file
            if key in self.itemIssueIdMap.keys() and (self.itemIssueIdMap[key] is not "None"):
                # yes there is, so check it is compatible, and get issue number
                (o, r, ns) = githubbot.issues.issue_id_info(self.itemIssueIdMap[key])
                Work.__checkMatch('organization',self.issuesFile,o,org)
                Work.__checkMatch('repository',self.issuesFile,r,repo)
                issue_number = int(ns)
            else:
                # the item has no item issue yet
                issue_number = None
            # create the logical issue
            if self.verbose:
                print 'Initializing WI logical issue for %s/%s: "%s" -> ' % (org,repo,title),
            li = githubbot.logicalissues.LogicalIssue(
                    org, repo, title, body, issueNumber=issue_number
            )
            if self.verbose:
                print 'issue #%s' % ('NOT SAVED YET' if li.issueNumber is None else li.issueNumber)
            # Only logical issues in this map are saved.
            self.itemLogicalIssueMap[key] = li

    def __bindOldItems(self):
        for key in self.oldItemKeys:
            self.__bindOldItem(key)

    def __bindOldItem(self, key):
        print "Warning: the key '%s' is in .issues but not in list. Keep it anyway." % key


    #---- saving to github --------------------------------------------------------------



    def __saveDefinition(self):
        """
        Save the definition and associate corresponding labels.
        This method set self.definitionIssueId
        """
        if not self.hasBeenBoundWithGitHub:
            self.bind()

        if self.verbose:
            print '----- Saving definition ---------------------------'
        # save the definition issue
        self.definitionLogicalIssue.save(self._getSubstitutionsForDefinition())
        self.definitionIssueId = self.definitionLogicalIssue.id()
        self.__saveIssueIds()

        # associate labelsSpec
        all_labels = self.labelSpecifications.copy()
        (name,color)=WORK_DEFINITION_LABEL_INFO
        all_labels[name]=color
        self.__associateLabels(
            self.definitionLogicalIssue.repo,
            self.definitionLogicalIssue.issue,
            all_labels)
        self.hasDefinitionBeenSavedToGitHub = True
        # TODO: implement milestone here

    def __saveItems(self):
        if self.verbose:
            print '----- Saving items     ---------------------------'
        for (key, logical_issue) in sorted(self.itemLogicalIssueMap.items()):
            self.__saveItem(key, logical_issue)
        self.hasItemsLabelsBeenSavedToGitHub = True
        self.hasItemsBeenSavedToGitHub = True  # FIXME

    def __saveItem(self, key, logical_issue):
        # save the item issue
        id = logical_issue.save(
                self._getSubstitutionsForItem(
                        key=key,
                        definitionIssueRef=self.definitionIssueId,
                        preview=False))
        self.itemIssueIdMap[key] = id
        self.__saveIssueIds()

        # associate labelsSpec
        all_labels = self.labelSpecifications.copy()
        (name, color) = WORK_ITEM_LABEL_INFO
        all_labels[name] = color
        self.__associateLabels(
                logical_issue.repo,
                logical_issue.issue,
                all_labels)
        # TODO: implement milestone here

    def __associateLabels(self, repo, issue, labelInfos):
        """
        Associate all the given labels to the given issue in the given repo.
        First ensure that the labels exist.
        :param repo: the repository object
        :param issue: the issue object
        :param labelInfos: a map  name -> color
        :return: None
        """
        labels = []
        # save all labelsSpec to make sure they are defined on the repo
        for (name,color) in labelInfos.iteritems():
            labels.append(githubbot.labels.ensureLabel(repo, name, color))
        # associate all labelsSpec with the issue
        issue.set_labels(*labels)

    # TODO: implement __associateLabels

    def save(self, definitionOnly=False):
        if self.verbose:
            print center(' SAVING WORK ', 80, '=')
        self.__saveDefinition()
        if not definitionOnly:
            self.__saveItems()
        if self.verbose:
            print center(' WORK SAVED ', 80, '=')


    # ---- show --------------------------------------------------------------

    def updateWorkSubtasksProgress(self, publishProgress=True, forceUpdate=False):
        """
        load all workitem logical issues with getIssue()
        Parse all these issues with  WorkItemSubtasksProgress(groupKey, text, workItemClosed)
        Bind the work if not done previously.
        :return: WorkSubtasksProgress
        """
        if self.__WorkSubtasksProgress is not None and not forceUpdate:
            return self.__WorkSubtasksProgress
        if (not self.hasBeenBoundWithGitHub):
            self.bind()
        wp = scribesclasses.models.subtasks.WorkSubtasksProgress()
        for (key, logical_issue) in self.itemLogicalIssueMap.items():
            # print "Processing key '%s'" % key,
            issue = logical_issue.getIssue()
            wist = scribesclasses.models.subtasks.WorkItemSubtasksProgress(
                groupKey=key,
                text=issue.body,
                workItemClosed=(issue.state=='closed')
            )
            # print issue.body
            # print wist.subtaskIds
            wp.add(wist)
            # print issue.state, wp.groupKeys
        self.__WorkSubtasksProgress = wp
        if publishProgress:
            updateWorkProgressComment(
                githubIssue= self.definitionLogicalIssue.getIssue(),
                workSubtasksProgress= wp
            )
        return wp

    #---- show --------------------------------------------------------------


    def show(self, width=80, verbose=False):
        self.showSpec(width=width, verbose=verbose)
        self.showStatus(width=width, verbose=verbose)
        self.showDefinition(width=width, verbose=verbose)
        self.showItems(width=width, verbose=verbose)
        self.showIssues(width=width, verbose=verbose)

    def showSpec(self, width=80, verbose=False, cut=-50):
        print center(self.workName, width, '=')
        print '    workDirectory:     ... %s' % self.workDirectory[cut:]
        print '    workName:          ... %s' % self.workName[cut:]
        print '    textFile:          ... %s' % self.textFile[cut:]
        print '    infoFile:          ... %s' % self.infoFile[cut:]
        print '    issuesFile:        ... %s' % self.issuesFile[cut:]

    def showStatus(self, width=80,verbose=False):
        print center('status', width, '=')
        print '    isExistingWork:                  %s' % self.isExistingWork
        print '    hasBeenBoundWithGitHub:          %s' % self.hasBeenBoundWithGitHub
        print '    hasDefinitionBeenSavedToGitHub:  %s' % self.hasDefinitionBeenSavedToGitHub
        print '    hasItemsBeensavedToGitHub:       %s' % self.hasItemsBeenSavedToGitHub

    def showDefinition(self, width=80, verbose=False):
        print center('DEFINITION', width, '-')
        print '    '+self.definitionTitlePattern[:width]
        print '    '+'.'*width
        print '    '+self.definitionBodyPattern[:width]

    def showItems(self, width=80, verbose=False):
        print center('ITEM', width, '-')
        print '    '+self.itemBodyPattern[:width]

    def showIssues(self, width=80, verbose=False):
        print center('DEFINITION ISSUE',width, '-')
        if self.definitionIssueId is None:
            print 'NO DEFINITION ISSUE YET. definitionIssueId is None'
        elif self.definitionLogicalIssue is None:
            # TODO: Check why this is necessary
            # sometimes it goes through there but not sure if this is ok
            print 'NO DEFINITION ISSUE YET. definitionLogicalIssue is None'
        else:
            print self.definitionLogicalIssue.url()

        print center('ITEM ISSUES',width, '-')
        print '    New Item Keys: %s' % ', '.join(self.newItemKeys)
        print '    Old Item Keys: %s' % ', '.join(self.oldItemKeys)
        print '    All Item Keys: %s' % ', '.join(self.allItemKeys)
        print
        for (key, logical_issue) in sorted(self.itemLogicalIssueMap.items()):
            if logical_issue.issueNumber is None:
                print '%s -> ****NOT_SAVED****' % key
            else:
                print '%s -> %s' % (key, logical_issue.url())




import githubbot.users
import githubbot.issues
from time import gmtime, strftime

BOT_NAME='scribesbot'
__BOT_USER=None
def getBotUser():
    """
    Github bot user both cached and on demand.
    For performance but also avoid github connection if not needed.
    This module could be used offline (some features)
    """
    global __BOT_USER
    if __BOT_USER is None:
        __BOT_USER = githubbot.users.user(BOT_NAME)
    return __BOT_USER


def isWorkProgressComment(comment):
    """
    Used to search the work progress comment
    :param comment:
    :return:
    """

    return (
        comment.user == getBotUser()
        and comment.body.startswith(PROGESS_HEADER)
    )

PROGESS_HEADER = '## Work Progress'

def updateWorkProgressComment(githubIssue, workSubtasksProgress):
    """

    :return:
    """
    if workSubtasksProgress is None or githubIssue is None:
        return
    else:
        progressBody = '\n'.join(workSubtasksProgress.linesForSubtasks())
        updateText = 'Updated at '+ strftime("%d/%m/%Y %H:%M:%S", gmtime())

        githubbot.issues.ensureCommentWith(
            issuefun=isWorkProgressComment,
            issue=githubIssue,
            body=PROGESS_HEADER+'\n\n'+progressBody+'\n\n'+updateText,
            append=False)

