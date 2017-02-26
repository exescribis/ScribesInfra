"""
Description of problems and set of problems.
"""

import os
from collections import OrderedDict


def times(n,word,format='%s %s'):
    if n==0:
        return format % ('no',word)
    else:
        return format % (n,word)+('s' if n>1 else '')

def link(url, label):
    return '`%s <%s>`_' % (label, url)


class Problem(object):
    """
    A problem with a type, a potential line, a potential source, message and content.
    """

    def __init__(self, sphinxRootDirectory, type, line, source, message, content=''):
        #: Type of the message. SEVERE, ERROR, WARNING, ...
        self.type = type

        #: int|NoneType, line where the problem has been detected. Can be None
        self.line = line

        #: str|NoneType, source file where the problem has been detected. Can be None
        #: Sometime this is the full path name, sometimes a relative path name.
        #: This depends on which piece of code generated the message.
        #: Use fullFileName instead
        self.source = source

        #: Short message describing the kind of problem.
        self.message = message

        #: Remaining text with details about the problem.
        self.content = content

        #: Absolute path name of the rst file or None if the file cannot be found.
        #: This field is computed from the ``source`` attribute.
        #: Check if the file exists, otherwise it will be None.
        self.fullFileName = None   # computed by _computeFilenames

        #: Just like the ``fullFileName`` attribute but relative to the
        #: sphinx source directory. None if the file is not found.
        #: path to the source file, relative to the sphinx root directory
        self.relativeFileName = None # computed by _computeFilenames

        self._setFileNames(sphinxRootDirectory)


    def appendToContent(self, text):
        self.content += ('' if self.content == '' else '\n') + text



    def _setFileNames(self, sphinxRootDirectory):
        """

        :param sphinxRootDirectory:
        :return:
        """
        if self.source is None:
            self.fullFileName = None
            self.relativeFileName = None
            return
        root = os.path.realpath(sphinxRootDirectory)
        src = os.path.realpath(self.source)
        if src.startswith(root):
            # the source file is absolute and seems ok
            file = src
        else:
            # assume that the source file is relative to the root
            file = os.path.join(root,self.source)
        if not os.path.isfile(file):
            self.fullFileName = None
            self.relativeFileName = None
            return
        self.fullFileName = file
        self.relativeFileName = os.path.relpath(file, root)




class UnknownProblem(Problem):
    """
    Unknown problem, that is problem that can be parsed no information.
    """
    def __init__(self, sphinxRootDirectory, content=''):
        Problem.__init__(self, sphinxRootDirectory, type='UNKNOWN',
                         line=None, source=None, message='UNKNOWN',
                         content=content)


class ProblemManager(object):
    """
    A collection of problems.
    """

    def __init__(self, sphinxRootDirectory=None):
        #: The sphinx root directory where rst source lives
        #: This value is used to display short filename when possible
        self.sphinxRootDirectory=sphinxRootDirectory

        #: dict[str,list[Problem]]
        #: Problems found in the specified filename (absolute)
        self.problemListByFilename = OrderedDict()

        #: dict[str,list[Problem]]
        #: Problems for a given type (e.g. 'SEVERE').
        self.problemListByType = OrderedDict()

        #: dict[str,list[Problem]]
        #: Problems for a given message (e.g. 'Duplicate label')
        self.problemListByMessage = OrderedDict()

    def addProblem(self, problem):
        if problem.fullFileName not in self.problemListByFilename:
            self.problemListByFilename[problem.fullFileName] = []
        self.problemListByFilename[problem.fullFileName].append(problem)

        if problem.type not in self.problemListByType:
            self.problemListByType[problem.type] = []
        self.problemListByType[problem.type].append(problem)

        if problem.message not in self.problemListByMessage:
            self.problemListByMessage[problem.message] = []
        self.problemListByMessage[problem.message].append(problem)


    def nbOfProblems(self):
        return sum(map(len,[self.problemListByType[type] for type in self.problemListByType]))


    def shortStatus(self):
        n = self.nbOfProblems()
        return times(n,'problem')+' found'


    def summaryByFile(self):
        entries = map( lambda (file,list):(file,len(list)), self.problemListByFilename.items())
        sorted_entries = sorted(entries, key=lambda (file,nb): -nb)
        nb_total = sum(map(lambda entry:entry[1], sorted_entries))
        nb_files = len(sorted_entries)
        if nb_total == 0:
            return ''

        title =  times(nb_total,'problem')+' in '+times(nb_files,'file')
        _ =   [ title, '-'*len(title), '']
        # sort by nb of occurrence
        for (filename,nb) in sorted_entries:
            relative_file_name = self.problemListByFilename[filename][0].relativeFileName
            if relative_file_name is not None:
                    #             _.append('* %s in %s' % (
                    # times(nb,'problem','**%s** %s'),
                    # link(label=relative_file_name, url='file://'+filename)))
                _ += [ relative_file_name, '^'*len(relative_file_name), '']
                for problem in self.problemListByFilename[filename]:
                    line = '``line %d``' % problem.line if problem.line else ''
                    _ += ['.. admonition:: %s' % (problem.type)]
                    _ += ['']
                    _ += ['   %s *%s*' % (line, problem.message)]
                    _ += ['']
                    if (problem.content):
                        _ += ['    ::','']
                        for line in problem.content.split('\n'):
                            _+= ['        %s' % line]

                    _ += ['']

            else:
                _.append('NO LOCATION')
        return '\n'.join(_)


    def summary(self):
        # document_list = '\n'.join(
        #         ['* % 5d in %s' % (
        #             len(self.problemListByFilename[fullFilename]),
        #             self.problemListByFilename[fullFilename])
        #          for fullFilename in self.problemListByFilename])
        summary_by_file = self.summaryByFile()
        type_list = ', '.join(
                ['%s:%s' % (
                    type,
                    len(self.problemListByType[type]))
                for type in self.problemListByType])
        message_list = '\n'.join(
                ['* % 5d %s' % (
                    len(self.problemListByMessage[message]),
                    message,
                    )
                for message in self.problemListByMessage])
        if self.nbOfProblems() == 0:
            return ''
        else:

            return ('\n'.join([
                'Problems',
                '========',
                '',
                '%s: %s',
                '',
                'Categories',
                '----------',
                '',
                '%s',
                '',
                '%s'])
                % (
                self.shortStatus(),
                type_list,
                message_list,
                summary_by_file))





