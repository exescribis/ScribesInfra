# coding: utf-8

"""
Change specifications are specifications of valid changes for a given
set of files or directories (items) expressed as globpatterns.
For instance::

            U   README.md
            M   src/UMLClassMetamodel.use
            M   src/states/Company.soil
            D   src/states/TODOS
            *   **/*.olt
            *   **/*.clt
            *   **/*.pdf
            *   **/*.soil

This module is based on the module py:module:`comparison` and in particular
on the :py:class:`comparison.Flag` for the kind of changes, as well
as the class :py:class:`comparison.ItemStatus`.
"""

import re
import os

import pywildcard
from changecontrol.comparison import Flag


class Change(object):
    """
    Specification of valid changes for a given file.
    """

    ADDED='A'
    DELETED='D'
    MODIFIED='M'
    UNCHANGED='U'

    EXIST='E'

    ANY='*'

    #: mapping beetween change specification and valid flags actually found
    ACCEPT={
        ADDED:      (Flag.RIGHT_FILE, Flag.RIGHT_DIR),
        DELETED:    (Flag.DELETED_FILE, Flag.DELETED_DIR),
        MODIFIED:   (Flag.MODIFIED_FILE, Flag.FUNNY_FILE),
        UNCHANGED:  (Flag.SAME_FILE, Flag.COMMON_DIR),
        EXIST:      (Flag.RIGHT_FILE, Flag.RIGHT_DIR,
                     Flag.MODIFIED_FILE, Flag.FUNNY_FILE, Flag.SAME_FILE),
        ANY:        Flag.ALL
    }

    @staticmethod
    def accept(change, comparisonFlag):
        return comparisonFlag in Change.ACCEPT[change]


class ChangeSpecification(object):
    """
    Abstract change specification. Just contains the accept method.
    """

    def accept(self, itemStatus):
        """
        Indicates whether the itemStatus is accepted by this change specification
        or not. Can return three values:
        * True if the change is accepted
        * False if the change is rejected
        * None if the change specification provides no indication for this item
        """
        return None

    @staticmethod
    def fromString(text):
        """
        Build a change specification from a series of lines of the form:

            *   README.md
            U   states
            M   src/UMLClassMetamodel.use
            M   src/states/Company.soil
            D   src/states/TODOS
            *   **/*.olt
            *   **/*.clt
            *   **/*.pdf
            *   **/*.soil
        """
        composite = CompositeChangeSpecification()
        for line in text.split('\n'):
            if line.startswith('#') or line=='':
                pass
            else:
                m = re.match('(?P<letter>[A-Z\*]) +(?P<pattern>[^ ]+) *',line)
                if m:
                    pattern=m.group('pattern')
                    letter=m.group('letter')
                    composite.add(BasicChangeSpecification(pattern,letter))
                else:
                    print 'WARNING: ignoring line %s' % line
        return composite

    @staticmethod
    def fromFile(filename, emptyIfNotExist=True):
        if os.path.isfile(filename):
            with open(filename,'r') as f:
                content = f.read()
            return ChangeSpecification.fromString(content)
        else:
            if emptyIfNotExist:
                return EmptyChangeSpecification()
            else:
                raise ValueError('No file %s' % filename)

class EmptyChangeSpecification(ChangeSpecification):
    def accept(self, itemStatus):
        return None

class BasicChangeSpecification(ChangeSpecification):
    """
    Specification corresponding conceptually to a single item.
    It might be represented like that::

        M   CyberKebab/src/states/**.soil
    """

    def __init__(self, filePattern, validChange):
        #: glob pattern for matching files
        #: str
        self.filePattern = filePattern
        #: change to check
        #: str (Change value)
        self.validChange = validChange

    def accept(self, itemStatus):
        """
        Check if the itemStatus is compatible with the specification.
        return bool|NoneType
        """
        relativePath = itemStatus.relativePath
        matches=pywildcard.filter([relativePath],self.filePattern)
        if matches:
            return Change.accept(self.validChange,itemStatus.flag)
        else:
            return None

    def __str__(self):
        return self.validChange+'   '+self.filePattern


class CompositeChangeSpecification(ChangeSpecification):
    """
    Composite specification made a sequence of specification
    (basic, composite or whatever). Use ``add``  method to
    append a new specification. The ``accept`` method search
    the specification in order.
    """

    def __init__(self):
        self.specifications = []

    def add(self, specification):
        """
        Add a new specification at the end.
        """
        self.specifications.append(specification)

    def accept(self, itemStatus):
        """
        Evaluate each specification in sequential order until
        a specification return true or false. Return None if
        no specification match the item.
        return bool|NoneType
        """
        for spec in self.specifications:
            r = spec.accept(itemStatus)
            if r is not None:
                return r
        return None

    def __str__(self):
        return '\n'.join(map(str,self.specifications))


def directory2ChangeSpecificationFile(
        root, outputFile,
        outputprefix='*   ', force=False):
    """
    Read a directory and create a change specification file from the
    directory structure. This file can be later customized with
    appropriate specification.
    :param root: the root directory for which the specificiation is created
    :param outputFile: the file that will contain the result
    :param outputprefix: the prefix for each line. 
        Default to "*   " meaning whatever.
    :param force: indicate if the specification file should be overwritton. 
    :return: None
    """
    if os.path.exists(outputFile) and not force:
        raise ValueError('change specification file already exists: %s' % outputFile)
    with open(outputFile,"w") as output:
        for dir, subdirs, files in os.walk(root):
            relativeDir = os.path.relpath(dir, root)
            if dir != root:   # this test is to avoid having "." in the list
                output.write("%s%s\n" % (outputprefix, relativeDir))
            for file in files:
                output.write("%s%s\n" % (outputprefix, os.path.normpath(os.path.join(relativeDir, file))))
