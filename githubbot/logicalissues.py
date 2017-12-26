# coding: utf-8

import repositories
import urls

class LogicalIssue(object):
    """
    A `LogicialIssue` is a container for an "logical issue" that does
    not exist yet or that exist on github but is not loaded yet.
    The fact is that we don't know when creating an new issue what
    the number will be.

    This class also supports templates and substitution when saving
    the issue.

    It supports also loading the issue if it exist.

    This class is a bit weird. Its design is quite close
    to the needs of scribesclasses.Work module. It might be a good
    idea to move it to scribesclasses.model package.


    """

    def __init__(self, orgName, repoName, titleTemplate, bodyTemplate,
                 issueNumber=None):

        #: str name of the organisation containing the issue
        self.orgName = orgName

        #: str name of the repository containing the issue
        self.repoName = repoName

        #: github repository object
        self.repo = repositories.repo(orgName, repoName)


        #: str  template for the title. May contain some substitution patterns
        self.titleTemplate = titleTemplate

        #: str  template for the body. May contain some substitution patterns
        self.bodyTemplate = bodyTemplate

        #: int|None  none if not bound. Otherwise the issue number
        self.issueNumber = issueNumber  # coudl be None

        #: github issue or None if not bound
        self.issue = None               # only available after save()


    @staticmethod
    def getSubstitutions(org, repo, substitutions=None):
        """
        Get the substitution computed by this logicial issue.
        This is a static method, so it can be called from outside
        without creating a logical issue.
        TODO: this method is not used yet outside. This is a mess.
        :param org:
        :param repo:
        :param substitutions:
        :return:
        """
        s = dict({} if substitutions is None else substitutions)
        s['org_name'] = org
        s['repo_name'] = repo
        s['org_repo'] = '%s/%s' % (org, repo)
        s['repo_url'] = urls.gitHubURL(s['org_repo'])
        s['repo_link'] = '[%s](%s)' % (s['repo_name'],s['repo_url'])
        s['repo_file'] = urls.gitHubFileURL(org, repo)
        return s

    def _substitute(self, text, substitutions=None):
        return text.format(**self.getSubstitutions(
                org=self.orgName,
                repo=self.repoName,
                substitutions=substitutions))

    def title(self, substitutions=None):
        """
        Title after substitutions
        :param substitutions:
        :return: the instanciated title
        """
        return self._substitute(self.titleTemplate, substitutions)

    def body(self, substitutions=None):
        """
        Body after substitutions
        :param substitutions:
        :return: the instanciated title
        """
        return self._substitute(self.bodyTemplate, substitutions)

    def text(self, substitutions=None):
        return \
            ('%s\n%s\n'+'='*80+'\n%s') % (
                self.url(),
                self.title(substitutions),
                self.body(substitutions)
            )

    def getIssue(self, forceLoad=False):
        """
        Return None if the issue number is not defined yet.
        Otherwise return the github issue if not already there.
        Reload the issue in all case if forceLoad.
        :return: github issue or None
        """
        if self.issueNumber is None:
            return None
        elif self.issue is not None and not forceLoad:
            return self.issue
        else:
            try:
                self.issue = self.repo.get_issue(self.issueNumber)
            except:
                raise EnvironmentError('getIssue(): issue #%s does not exist'
                                       % self.issueNumber )
            return self.issue

    def save(self, substitutions=None, verbose=False):
        title = self.title(substitutions)
        body = self.body(substitutions)
        if self.issueNumber is None:
            if verbose:
                print 'Creating new issue in %s/%s ... ' % (self.orgName, self.repoName),
            self.issue = self.repo.create_issue(title, body)
            self.issueNumber = self.issue.number
            if verbose:
                print '#%i created' % self.issueNumber
        else:
            if verbose:
                print 'Editing issue %s/%s#%i ... ' % (
                    self.orgName, self.repoName,    self.issueNumber),
            try:
                self.issue = self.repo.get_issue(self.issueNumber)
            except:
                # TODO: improve this case
                # this might be due because of an exception before
                # saving so the file is not synchronized or the repository
                # has been removed in the meantime.
                # One way to make it more robust is to search the
                # issue by name.
                raise EnvironmentError('save()! issue #%s does not exist'
                                       % self.issueNumber )
            self.issue.edit(title, body)
            print 'done'
        return self.issue



    def url(self):
        if self.issueNumber is None:
            return None
        return urls.gitHubURL('%s/%s/issues/%i' % (
            self.orgName,
            self.repoName,
            self.issueNumber ))

    def id(self, ifNone=None):
        if self.issueNumber is None and ifNone==None:
            return None
        else:
            num = ifNone if self.issueNumber is None else str(self.issueNumber)
            return \
                '%s/%s#%s' % (
                    self.orgName,
                    self.repoName,
                    num )

    def __str__(self):
        return self.id()

#
# """
# l = LogicalIssue('ScribesBotZone','root','titre{n}','body{b} repo_name is {repo_name}')
# l.save({'a':2, 'b':100, 'n':'qsd'})
# """

# class LogicalIssueGroup(object):
#     # TODO: This class seems unused. Could probably be removed because not maintained.
#     #       It should have been used by Work but actually it is not.
#     def __init__(self, keys,
#                  orgTemplate, repoTemplate, titleTemplate, bodyTemplate,
#                  keyName='group_num',
#                  issueNumbers=None):  # todo: change by a map towards issueNum
#         self.keyName = keyName
#         self.keys = keys
#         self.orgTemplate = orgTemplate
#         self.repoTemplate = repoTemplate
#         self.logicalIssueMap = {}
#         for key in keys:
#             org = self.orgName(key)
#             repo = self.repoName(key)
#             li = LogicalIssue(org, repo, titleTemplate, bodyTemplate)
#             self.logicalIssueMap[key] = li
#
#
#     def orgName(self, key):
#         return self.orgTemplate.format(**{self.keyName:key})
#
#     def repoName(self, key):
#         return self.repoTemplate.format(**{self.keyName:key})
#
#     def save(self, substitutions=None):
#         s = {} if substitutions is None else substitutions
#         print s
#         for key in self.keys:
#             # add the key to the substition list
#             s[self.keyName] = key
#             self.logicalIssueMap[key].save(s)
#
#     def logicalIssue(self, key):
#         return self.logicalIssueMap[key]
#
#     def idMap(self):
#         map = {}
#         for key in self.keys:
#             map[key] = self.logicalIssueMap[key].id()
#         return map
