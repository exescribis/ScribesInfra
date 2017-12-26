# coding=utf-8

"""
Model errors in source files either localized or not.
"""
from collections import OrderedDict
from typing import Optional, List, Text, Dict, Tuple

from modelscripts.base.annotations import (
    Annotations
)
from modelscripts.base.locations import (
    SourceLocation,
)

from modelscripts.config import Config

#TODO:4 it should be better to remove the printer dependency
from modelscripts.base.styles import Styles

DEBUG=1

class FatalError(Exception):
    def __init__(self, SourceError):
        super(FatalError, self).__init__()
        self.sourceError=SourceError

class Level(object):
    def __init__(self, label, rank, style):
        self.label=label
        self.rank=rank
        self.style=style

    def __le__(self, other):
        return self.rank <= other.rank

    def __ge__(self, other):
        return self.rank >= other.rank

    def __eq__(self, other):
        return self.rank == other.rank

    def cmp(self, other, op='='):
        #type: (Level, Text) -> bool
        if op=='=':
            return self == other
        elif op=='<=':
            return self <= other
        elif op=='>=':
            return self >= other
        else:
            raise NotImplementedError('Operation %s is not allowed'%op)

    def str(self, styled=False):
        return self.style.do(self.label, styled=styled)

    def __str__(self):
        return self.label

    def __repr__(self):
        return self.__str__()


class Levels(object):
    Hint=Level('HINT', 10, Styles.smallIssue)
    Info=Level('INFO', 20, Styles.smallIssue)
    Warning=Level('WARNING', 30, Styles.smallIssue)
    Error=Level('ERROR', 40, Styles.bigIssue)
    Fatal=Level('FATAL ERROR', 50, Styles.bigIssue)

    Levels=[Fatal, Error, Warning, Info, Hint]


class Issue(object):
    """
    An issue in a given entity with issue list (WithIssueList).
    Direct instances of Issue are not localized.
    The class LocalizedSourceIssue must be used if the error line
    is known.
    """
    def __init__(self, origin, level, message):
        #type: (WithIssueList, Level, 'Text') -> None
        """
        Create a source error and add it to the given SourceFile.
        Raise FatalError if the error is fatal and processing could not
        continue.
        """
        assert message is not None and message!=''

        self.origin = origin  #type: WithIssueList
        """ A source file or a model. """

        self.message = message
        """ The error message. """

        self.level=level  #type:Level

        self.origin._issueBox._add(self)

        if DEBUG>=1 or Config.realtimeIssuePrint>=1:
            print('iss: Issue: ' + str(self))

        if level==Levels.Fatal:
            raise FatalError(self)

    @property
    def fromModel(self):
        """
        Indicates if the issue comes from a model.
        """
        # Since importing the model type generate a cycle,
        # the trick below should be good enough.
        return type(self.origin).__name__.endswith('Model')

    @property
    def kind(self):
        """M for Model, S for source"""
        return 'M' if self.fromModel else 'S'

    def str(self,
            pattern=None,
            mode='fragment',
            displayOrigin=False,
            displayLocation=True,
            styled=False): # not used, but in subclasses

        """
        Display the issue.
        Since the issue is not localized
        direct instances of this class just display
        the level and the error message.
        Subclasses provide more information
        """
        # l=self.level.style.do(self.level.str(styled=styled))
        # return pattern.format(
        #     message=self.message,
        #     level=l)
        if pattern is None:
            pattern=(
                Annotations.prefix
                + '{origin}:{kind}:{level}:{location}:{message}')
        text=pattern.format(
            origin='ORIGIN',
            level=self.level.str(),
            kind=self.kind,
            location='LOCATION',
            message=self.message
        )
        return self.level.style.do(
            text,
            styled=styled)

    def __str__(self):
        return self.str()


    def __repr__(self):
        return self.__str__()


class LocalizedSourceIssue(Issue):

    def __init__(self,
                 sourceFile,
                 level,
                 message,
                 line,
                 column=None,
                 fileName=None):
        #type: ('SourceFile', Level, Text, int, Optional[int], Optional[Text]) -> None
        """
        Create a localized source file and add it to
        the given source file.

        :param sourceFile: The Source File
        :param message: The error message.
        :param line: The line number of the error
            starting at 1. If the error is before
            the first line, it is moved to (1,0)
            If the error is after the end
            of the file (typically the last line)
            the line recorded is assumed to be
            the last character of the last line.
        :param column: The column number of the
            error or None. If the errors is between
            the previous line and before the
            first column 0 is an acceptable value.
        :param fileName: An optional string
            representing the filename to be output
            with the error message. If None is
            given, then this value will be taken
            from the source file.
        """

        def __adjust(sourceFile, line, column):
            #type: ('SourceFile', int,int) -> Tuple[int,int]
            lines = sourceFile.sourceLines
            nblines = len(lines)
            if line == 0:
                # move error before first line to first line
                # this could be after the last line if empty
                l = 1
                c = 0
            elif nblines == 0:
                # if no line on the file, line will be 1
                # that is, after the last line
                l = 1
                c = 0
            elif line > nblines:
                # move error after last line to end
                # of last line
                l = nblines
                c = len(lines[nblines - 1])
            else:
                # regular location for a line
                l = line
                c = column
            return(l,c)

        (l, c) = __adjust(sourceFile, line, column)

        self.location=SourceLocation(
            sourceFile=sourceFile,
            fileName=fileName,
            line=l,
            column=c
        )

        # self.sourceFile = sourceFile
        # """ The source file. An instance of SourceFile. """
        #
        # self.fileName = (
        #     fileName if fileName is not None
        #     else self.sourceFile.fileName )
        #
        # #------ ajust line,col if necessary
        # (l,c)=__adjust(self.sourceFile, line, column)
        # lines=sourceFile.sourceLines
        #
        # self.line = l #type: int
        # """
        # The line number between 1 and the nb of lines.
        # This values may have been adjusted
        # """
        #
        # self.column = c #type: Optional[int]
        # """
        # The column number or None. If defined
        # it could be 0 or 1 more than the length
        # of the line
        # """

        super(LocalizedSourceIssue, self).__init__(
            origin=sourceFile,
            level=level,
            message=message)

    @property
    def line(self):
        return self.location.line

    @property
    def column(self):
        return self.location.column

    def str(self,
            pattern=None,
            mode='fragment',
            displayOrigin=False,
            displayLocation=True,
            styled=False):
        if pattern is None:
            pattern=(
                Annotations.prefix
                + '{kind}:{level}:{origin}:{line}:{message}')
        text=pattern.format(
            origin=self.location.sourceFile.basename,
            level=self.level.str(),
            kind=self.kind,
            line=str(self.location.line),
            message=self.message
        )
        return self.level.style.do(
            text,
            styled=styled)

        # l=self.level.style.do(self.level.str(styled=styled))
        # return pattern.format(
        #     message=self.message,
        #     level=l)

    def __str__(self):
        return self.str()

    def __repr__(self):
        return self.__str__()


class IssueBox(object):
    """
    A collection of issues. It allows to have nested issues box
    and have some query mecanisms.
    """

    def __init__(self, parents=()):
        #type: (List[IssueBox]) -> None
        self._issueList=[] #type: List[Issue]
        self.parents=list(parents) #type:List[IssueBox]

        self._issuesAtLine=OrderedDict()
        #type: Dict[Optional[int], List[Issue]]
        """ 
        Store for a given line the issues at this line.
        There is no  entry for lines without issues.
        _issuesAtLine[0] are for unlocalized issues.
        """

    def _add(self, issue):
        #type: (Issue) -> None
        # called by the issue constructor
        # Issue -> None
        self._issueList.append(issue)
        if isinstance(issue, LocalizedSourceIssue):
            index=issue.line
        else:
            index=0
        if index not in self._issuesAtLine:
            self._issuesAtLine[index]=[]
        self._issuesAtLine[index].append(issue)

    def addParent(self, issues):
        #type: (IssueBox) -> None
        """
        Add the issue box as the last parents.
        If it is already in the list, do nothing.
        """
        if not issues in self.parents:
            self.parents.append(issues)



    def at(self, lineNo, parentsFirst=True):
        """
        Return the list of issues at the specified line.
        If the line is 0 then return unlocalized issues.
        Return both local and parents issues recursively.
        """
        # int -> List[Issue]
        parent_issues=[
            i for p in self.parents
                for i in p.at(lineNo, parentsFirst=parentsFirst) ]
        self_issues=(
            [] if lineNo not in self._issuesAtLine
            else self._issuesAtLine[lineNo]
        )
        if parentsFirst:
            return parent_issues+self_issues
        else:
            return self_issues+parent_issues

    @property
    def allParents(self):
        #type: () -> List[IssueBox]
        """
        Return all parents recursively.
        """
        return list(
            x
            for p in self.parents
                for x in p.allParents+[p]
        )

    @property
    def all(self):
        """
        Return both local and parents issues recursively
        """
        return list(
            [ i for p in self.allParents
                    for i in p._issueList ]
            + self._issueList
        )

    @property
    def nb(self):
        """
        Return the nb of all issues (local and parents)
        """
        return len(self.all)

    def select(self,
               level=None, op='=',
               line=None ):
        #type: (Optional[Level], str, Optional[bool], Optional[int]) -> List[Issue]
        if level is None and line is None:
            return list(self.all)
        issues_at=(
            self.all if line is None
            else self.at(line))
        return [
            i for i in issues_at
            if i.level.cmp(level, op) ]

    @property
    def bigIssues(self, level=Levels.Error):
        return self.select(level=level,op='>=')

    @property
    def smallIssues(self, level=Levels.Warning):
        return self.select(level=level,op='<=')

    @property
    def isValid(self):
        # () -> bool
        return len(self.bigIssues)==0

    @property
    def hasIssues(self):
        return len(self.all) != 0

    @property
    def hasBigIssues(self):
        return len(self.bigIssues) >= 1

    @property
    def hasSmallIssues(self):
        return

    @property
    def summaryMap(self):
        #type: () -> Dict[Level, int]
        """
        A map that give for each level the
        number of corresponding issues at that level.
        This include levels with 0 issues.
        """
        map=OrderedDict()
        for l in Levels.Levels:
            n=len(self.select(level=l))
            map[l]=n
        return map


    @property
    def summaryLine(self):

        def times(n, word, pattern='%i %s'):
            if n==0:
                return ''
            else:
                return (pattern % (
                    n,
                    word + ('s' if n>=2 else '')
                ))

        if self.nb==0:
            return ''
        level_msgs=[]
        m=self.summaryMap
        for l in m:
            n=m[l]
            if n>0:
                level_msgs.append(
                    times(n, l.label))
        if len(level_msgs)==1:
            text=level_msgs[0]
        else:
            text= '%s (%s)' % (
                    times(self.nb, 'Issue'),
                    ', '.join(level_msgs)
                )
        return Annotations.fullLine(text)



    def str(self,
            level=None,
            op='=',
            mode='fragment',
            summary=True,
            styled=False):
        if not self.hasIssues:
            return ''
        header=(
            Annotations.full+'\n'
            +self.summaryLine+'\n'
            +Annotations.full) if summary else ''
        return '\n'.join(
            [header]
            + [
                i.str(mode=mode, styled=styled)
                for i in self.select(level,op)]
            + [Annotations.full+'\n' ])

    def __str__(self):
        return self.str()

    def __repr__(self):
        return self.__str__()



class WithIssueList(object):
    def __init__(self, parents=()):
        #type: (List[IssueBox]) -> None
        assert(isinstance(parents, list))
        self._issueBox=IssueBox(parents=parents)

    @property
    def issues(self):
        return self._issueBox

    @property
    def isValid(self):
        # () -> bool
        return self._issueBox.isValid

    @property
    def hasIssues(self):
        return self._issueBox.hasIssues

    def addIssue(self, sourceError):
        self._issueBox._add(sourceError)
