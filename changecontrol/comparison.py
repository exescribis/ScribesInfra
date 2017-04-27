# coding: utf-8

"""
This module provides abstract representation for directory comparisons. A directory
comparisons is a pair of directory compared. The first directory is called left,
the second directory if called right. If there is a sequence the comparisons
can be considered as changed (e.g. added, deleted).

This module is based on the standard :module:`filecmp` module.

"""
import filecmp
import os
import fnmatch
from collections import OrderedDict

from termcolor import colored


def removePrefix(prefix,x):
    if x.startswith(prefix):
        return x[len(prefix):]
    else:
        return x


class Flag(object):
    """
    Flags constants for describing the result of comparison.
    Flags ADDED_*, DELETED_*, MODIFIED_* can be used when the
    comparisons actually represent changes between old and new version
    of a directory.
    """
    LEFT_FILE=0
    RIGHT_FILE=1
    DIFF_FILE=2
    FUNNY_FILE=3
    SAME_FILE=4

    LEFT_DIR=10
    RIGHT_DIR=11
    COMMON_DIR=12

    ADDED_FILE=RIGHT_FILE
    DELETED_FILE=LEFT_FILE
    MODIFIED_FILE=DIFF_FILE

    ADDED_DIR=RIGHT_DIR
    DELETED_DIR=LEFT_DIR

    FILE_FLAGS=[LEFT_FILE, RIGHT_FILE, DIFF_FILE, FUNNY_FILE, SAME_FILE]
    DIR_FLAGS=[LEFT_DIR, RIGHT_DIR, COMMON_DIR]
    ALL=FILE_FLAGS+DIR_FLAGS


#:    Convenience information for each flag/
#:    used by the method in this class.
#
PATTERNS = {

    Flag.LEFT_FILE: {
        'change.name':      'Deleted files',
        'change.letter':    'D',
        'text' : '- %s',
        'color' : 'red',
        'background' : None
    },
    Flag.RIGHT_FILE: {
        'change.name':      'Added files',
        'change.letter':    'A',
        'text' : '+ %s',
        'color' : 'green',
        'background' : None
    },
    Flag.DIFF_FILE: {
        'change.name':      'Modified files',
        'change.letter':    'M',
        'text' : 'M %s',
        'color' : 'blue',
        'background' : None
    },
    Flag.FUNNY_FILE: {
        'change.name':      'Uncomparable files',
        'change.letter':    '?',
        'text' : '? %s',
        'color' : 'cyan',
        'background' : None
    },
    Flag.SAME_FILE: {
        'change.name':      'Unchanged files',
        'change.letter':    '=',
        'text' : '= %s',
        'color' : 'grey',
        'background' : None
    },
    Flag.LEFT_DIR: {
        'change.name':      'Deleted directories',
        'change.letter':    'D',
        'text' : '- %s/',
        'color' : 'red',
        'background' : None
    },
    Flag.RIGHT_DIR: {
        'change.name':      'Added directories',
        'change.letter':    'A',
        'text' : '+ %s/',
        'color' : 'green',
        'background' : None
    },
    Flag.COMMON_DIR: {
        'change.name':      'Common directories',
        'change.letter':    '.',
        'text' : 'o %s/',
        'color' : 'grey',
        'background' : None
    },
}


ACCEPTANCE_LABELS = {
    True:   colored('..OK.. ',on_color='on_green'),
    False:  colored('..KO.. ',on_color='on_red'),
    None:   colored('..??.. ',on_color='on_white')
}



class ItemStatus(object):
    """
    Status of a directory or a file (here called an item).
    This class provides a convenient structure to analyze change in files.
    """

    def __init__(self, name, parentDirCmp, relativeParentList, flag):
        #: short name of the file or directory
        self.name = name
        #: dirCmp
        #: the dirCmp object of the parent. This is never null
        self.parentDirCmp = parentDirCmp
        #: list[str]
        #: the list of subdirectories name leading from the
        #: top level directories to this item
        self.relativeParentList = relativeParentList
        #: flag, value either from File or Dir classes
        self.flag = flag

    @property
    def leftPath(self):
        return os.path.join(self.parentDirCmp,self.name)

    @property
    def rightPath(self):
        return os.path.join(self.parentDirCmp,self.name)

    @property
    def relativePath(self):
        names = list(self.relativeParentList)+[self.name]
        return os.path.join(*names)

    @property
    def prefix(self):
        return '|   '*len(self.relativeParentList)

    @property
    def coloredTreeLine(self):
        pattern = PATTERNS[self.flag]
        text = pattern['text'] % self.name
        color = pattern['color']
        background = pattern['background']
        # if pattern['background'] == 'on_white':
        #     message = colored(text, color)
        # else:
        message = colored(text, color, background)
        return self.prefix+message

    @property
    def coloredRelativePath(self):
        parents = list(self.relativeParentList)
        path = os.path.sep.join(parents)
        if path != '':
            path = path+os.path.sep
        p = PATTERNS[self.flag]
        colored_letter = colored(p['change.letter'],p['color'],p['background'])
        return colored_letter+'   '+path+colored(self.name, p['color'], p['background'])


class FileStatus(ItemStatus):
    """
    Status for a file.
    """
    def __init__(self, name, parentDirCmp, relativeParentList, flag):
        ItemStatus.__init__(self, name, parentDirCmp, relativeParentList, flag)
    # Currently this class is not really used. It is instanciated but
    # No difference are defined for files and directories.
    # This could change in the future.

class DirectoryStatus(ItemStatus):
    """
    Status for a directory.
    """
    def __init__(self, name, parentDirCmp, relativeParentList, flag):
        ItemStatus.__init__(self, name, parentDirCmp, relativeParentList, flag)
    # Currently this class is not really used. It is instanciated but
    # No difference are defined for files and directories.
    # This could change in the future.


class DirectoryComparison(object):
    """
    Collection of item status resulting from the comparaison of two directories.
    Item statuses can be accessed in different ways:
    * in sequence, using the attribute `itemStatusList`. The list is sorted according
      to the top to bottom traversal of the directory. Convenient for displaying
      an indented tree for instance.
    * through the relative path name, using the map `itemStatusByRelativePath`.
      Convenient to get directly the status of an item.
    * by flags, using the map `itemStatusListByFlag`. Convenient to get directly
      all changed files for instance.
    """
    def __init__(self, dirLeft, dirRight, ignoreNames=('.git',)):

        #: The left directory
        self.dirLeft = dirLeft

        #: Whether the left directory exists or not
        self.dirLeftMissing = not os.path.isdir(self.dirLeft)

        #: The right directory
        self.dirRight = dirRight

        #: Whether the right directory exists or not
        self.dirRightMissing = not os.path.isdir(self.dirRight)

        if self.dirLeftMissing and self.dirRightMissing:
            raise ValueError(
                    'No comparison possible.'
                    + 'both directories are missing:\n'
                    + self.dirLeft+'\n'
                    + self.dirRight)

        #: A map containing for each flag, the list of item status
        #: with this status.
        #: dict[Flag.key,list|ItemStatus]]
        self.itemStatusListByFlag = {}
        for flag in Flag.ALL:
            self.itemStatusListByFlag[flag] = []

        #: A map if item status indexed by relative path
        #: dict[str,ItemStatus]
        self.itemStatusByRelativePath = OrderedDict()

        #: Indicates if at least one of the directory specified is missing.
        #: No comparison is possible in this case.
        self.missingDirectory = (
            self.dirLeftMissing
            or self.dirRightMissing)

        #: The instance of :py:class:`filecmp.dircmp` class or None if
        #: missingTopDirectory.
        self.dirCmp = None
        if not self.missingDirectory:
            self.dirCmp = filecmp.dircmp(dirLeft,dirRight,ignoreNames)
            # create the structure
            self._walk()

    @property
    def itemStatusList(self):
        return self.itemStatusByRelativePath

    def _path(self, dir, item):
        return os.path.join(dir, item)

    def _isdir(self, dir, item):
        return os.path.isdir(self._path(dir, item))

    def _addFile(self, filename, parentDirCmp, relativeParentList,  flag):
        """
        Create a new FileStatus and register it to the different lists.
        """
        assert isinstance(parentDirCmp,filecmp.dircmp)
        itemStatus = FileStatus(filename, parentDirCmp, relativeParentList, flag)
        self.itemStatusListByFlag[flag].append(itemStatus)
        self.itemStatusByRelativePath[itemStatus.relativePath]=itemStatus

    def _addDir(self, filename, parentDirCmp, relativeParentList,  flag):
        """
        Create a new FileStatus and register it to the different lists.
        """
        itemStatus = FileStatus(filename, parentDirCmp, relativeParentList, flag)
        self.itemStatusListByFlag[flag].append(itemStatus)
        self.itemStatusByRelativePath[itemStatus.relativePath]=itemStatus

    def _walk(self, currentDirCmp=None, relativeParentList=()):
        if currentDirCmp is None:
            currentDirCmp = self.dirCmp

        # same_files:
        for filename in currentDirCmp.same_files:
            self._addFile(filename, currentDirCmp, relativeParentList, Flag.SAME_FILE)

        # diff_files:
        for filename in currentDirCmp.diff_files:
            self._addFile(filename, currentDirCmp, relativeParentList, Flag.DIFF_FILE)

        # funny_files:
        for filename in currentDirCmp.funny_files:
            self._addFile(filename, currentDirCmp, relativeParentList, Flag.FUNNY_FILE)

        # left_only:  files or directory
        for item in currentDirCmp.left_only:
            p = self._path(currentDirCmp.left, item)
            if self._isdir(currentDirCmp.left, item):
                self._addDir(item, currentDirCmp, relativeParentList, Flag.LEFT_DIR)
            else:
               self._addFile(item, currentDirCmp, relativeParentList, Flag.LEFT_FILE)

        # right_only:  files or directorys
        for item in currentDirCmp.right_only:
            p = self._path(currentDirCmp.right, item)
            if self._isdir(currentDirCmp.right, item):
                self._addDir(item, currentDirCmp, relativeParentList, Flag.RIGHT_DIR)
            else:
                self._addFile(item, currentDirCmp, relativeParentList, Flag.RIGHT_FILE)

        # process and walk in common subdirectories
        for directory_name in currentDirCmp.subdirs.keys():
            self._addDir(directory_name, currentDirCmp, relativeParentList, Flag.COMMON_DIR)
            self._walk(currentDirCmp.subdirs[directory_name], list(relativeParentList)+[directory_name])

    def showSummary(self):
        """
        Print a summary of the difference with the number of items in each
        category.
        """
        if self.dirLeftMissing:
            print('Left directory missing: '+self.dirLeft)
        elif self.dirRightMissing:
            print('Right directory missing: '+self.dirRight)
        else:
            for flag in Flag.ALL:
                p = PATTERNS[flag]
                nb = len(self.itemStatusListByFlag[flag])
                if nb>=1:
                    print('%s: %s' % (p['change.name'], nb))

    def _acceptance(self, itemStatus, acceptFun=None):
        """
        Return a pair (str,bool|None). If acceptance is not important
        the string will be ''. Otherwise it will be a label to display
        and the second parameter is the acceptance value (True,False,None)
        """
        if acceptFun is None:
            return ('',True)
        else:
            acceptance = acceptFun(itemStatus)
            return (ACCEPTANCE_LABELS[acceptance],acceptance)

    def showTree(self, acceptFun=None):
        """
        Print a nested tree with color and text indicated the differences in
        the tree.
        """
        if self.dirLeftMissing:
            print('Left directory missing: '+self.dirLeft)
        elif self.dirRightMissing:
            print('Right directory missing: '+self.dirRight)
        else:
            for item_status in self.itemStatusByRelativePath.values():
                (accept_label, acceptance) = self._acceptance(item_status, acceptFun)
                print( "%s %s" % (
                    accept_label,
                    item_status.coloredTreeLine))

    def showFlatList(self, acceptFun=None, ignoreAccept=True, filter='*'):
        """
        Print a flat list of files/directories with relative path and change indicator.
        Items are printed only if matching the glob filter 
        """
        if self.dirLeftMissing:
            print('Left directory missing: '+self.dirLeft)
        elif self.dirRightMissing:
            print('Right directory missing: '+self.dirRight)
        else:
            ignored = 0
            for item_status in self.itemStatusByRelativePath.values():
                (accept_label, acceptance) = self._acceptance(item_status, acceptFun)
                if ignoreAccept and (acceptance is True):
                    ignored += 1
                else:
                    if fnmatch.fnmatch(item_status.relativePath, filter):
                        print("%s %s" % (
                            accept_label,
                            item_status.coloredRelativePath))
            if ignoreAccept and ignored>=1:
                print('Hidding %s items accepted' % ignored)

