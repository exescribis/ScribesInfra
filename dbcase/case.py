# coding=utf-8

"""
A DBCase is represented as a directory with a structure like the following.
Most elements are optional:

    <Name>
        index.rst
        <Name>.schema.sql       Optional. Can be inferred from default state
        <Name>.queries.sql
        states
            default
                <R1>.csv
                <R2>.csv
                ...
                <Rn>.csv
            <StateName2>
                <R1>.csv
                ...

    Case
        * directory
        * name
        * hasSchema
        * stateMap
        * hasStates
        * defaultState
        * querySetMap
        * querySetIndexFilename
        * buildDirectory
        * sphinxRootDirectory

"""


from collections import OrderedDict

from dbcase.queries import QuerySet
from dbcase.schema import Schema
from dbcase.state import stateFactory
from filehelpers import directoryItemPaths, saveContent, ensureDirectory, fileContent, removeTrailingSeparator


class Case(object):
    def __init__(self, caseDirectory, sphinxRootDirectory):

        #: directory of the case.
        #: str.
        self.directory = removeTrailingSeparator(caseDirectory)
        assert os.path.isdir(self.directory)

        #: sphinx root directory (the one containing the makefile usually).
        #: This is required to have includes inside includes
        #: as they must be defined using a pseudo absolute root
        #: from this root (see _pathFromRootSphinxDirectory).
        #: str.
        self.sphinxRootDirectory = removeTrailingSeparator(sphinxRootDirectory)
        assert os.path.isdir(self.sphinxRootDirectory)

        #: name of the case.
        #: str.
        self.name = os.path.basename(self.directory)
        print '  case named %s' % self.name

        #: '.build' directory where all generated files go.
        #: This directory will be created in build()
        #: str.
        self.buildDirectory = os.path.join(self.directory, '.build')

        #: google credential file or None if this file does not exist
        #: This file allows to connect to google spreadsheet for states.
        self.googleCredentialsJsonFile = \
            self._tryToGetGoogleCredentials(self.sphinxRootDirectory)

        #: 'tmp' directory where temporary and debug files go.
        #: This directory will be created in build()
        # self.tmpDirectory = os.path.join(self.buildDirectory, 'tmp')

        #: dict[string,State]. Map stateName -> State.
        #: All states in the 'states' directory. These states
        #: can be easily conveted to 'INSERT' statements and
        #: a schema ('CREATE' statements) can be inferred as well.
        #: see :class:State.
        #: Can be empty if there is no states.
        self.stateMap = OrderedDict(sorted({
            os.path.basename(state_dir) : stateFactory(state_dir, self)
            for state_dir in self._getStateDirectories()
            }.items()))
        print '  %s state(s) found: %s' % (len(self.stateMap), self.stateMap.keys())

        #: A case may have no state.
        #! bool.
        self.hasStates = len(self.stateMap.keys()) > 0

        #: State|None
        #: default state. It is either named default or this will be
        #: the first one or None if there is no state at all.
        self.defaultState = self.getDefaultState()
        if self.defaultState is None:
            print '  No state found. No database will be build.'
        else:
            print '  %s is the default state.' % self.defaultState.name

        #: Schema object, either inferred from default state or taken from
        #: an explicit .schema.sql file.
        #: Schema|None
        self.schema = self._getSchema()   # should be done after stateMap

        #: Indicates if the case have a schema (either inferred or explicit)
        #: bool.
        self.hasSchema = self.schema is not None

        if self.hasSchema and self.schema.isGenerated:
            print '  schema inferred from default state'
        elif self.hasSchema and not self.schema.isGenerated:
            print '  explicit schema found'
        else:
            print '  no schema found or inferred'

        #: dict[string,QuerySet], Map queryiesName -> QuerySet
        #: All queries from the *.queries.sql in the case directory.
        self.querySetMap = OrderedDict(sorted({
            queries_file : QuerySet(queries_file, self)
            for queries_file in self._getQueriesFiles()
        }.items()))

        #: str|None
        #: Name of the index file for queries
        self.querySetIndexFilename = None  # defined by build

    def getDefaultState(self):
        if len(self.stateMap)==0:
            return None
        elif 'default' in self.stateMap.keys():
            return self.stateMap['default']
        else:
            return list(self.stateMap)[0]

    def _tryToGetGoogleCredentials(self, directory):
        credentials_file = os.path.join(directory,'GoogleScribesBot.json')
        if os.path.isfile(credentials_file):
            return credentials_file
        else:
            return None

    def _getSchema(self):
        """
        Get the schema if any:

        *   if there is an explicit "*.schema.sql" then copy it in the build
            directory and set self.schema.

        *   if there is a default state then try to infer the schema.

        *   otherwise return none.

        """

        explicit_schema_file = os.path.join(self.directory, '%s.schema.sql' % self.name)
        if os.path.isfile(explicit_schema_file):
            return Schema(
                    self.name,
                    self,
                    fileContent(explicit_schema_file),
                    schemaFilename=explicit_schema_file,
                    isGenerated=False)

        elif self.hasStates:
            sql_rst = self.defaultState.getInferredSchema()
            return Schema(
                    self.name,
                    self,
                    sql_rst,
                    schemaFilename=None,
                    isGenerated=True
            )
        else:
            return None

    def _getStateDirectories(self):
        states_directory = os.path.join(self.directory, 'states')
        if (os.path.isdir(states_directory)):
            # there is a 'states' directory, directories inside are states name
            return directoryItemPaths(
                    states_directory,
                    lambda x:os.path.isdir(x) and not x.startswith('.'))
        else:
            return []

    def _getQueriesFiles(self):
        return sorted(
                    directoryItemPaths(
                        self.directory,
                        predicate=
                            lambda f : f.endswith('.queries.sql') and os.path.isfile(f)))

    def _pathFromRootSphinxDirectory(self, filename):
        return os.sep+filename.replace(self.sphinxRootDirectory, '')

    def _buildQuerySetsIndexFile(self, subTitleCharacter='"'):
        index_filename = os.path.join(
                self.buildDirectory,
                '%s.queries.generated.rst' % self.name)
        index_content = ''
        for query_set in self.querySetMap.values():
            # add a subtitle if required
            if subTitleCharacter is not None:
                index_content += '%s\n%s\n\n' % (
                    query_set.name,
                    subTitleCharacter*len(query_set.name))
            # add an include
            index_content += (
                '..  include:: %s\n\n'% self._pathFromRootSphinxDirectory(query_set.buildRstFile)
            )
        print '    saving %s ... '  % index_filename
        saveContent(index_filename, index_content)
        print 'done'

    def _buildQuerySets(self):
        for querySet in self.querySetMap.values():
            querySet.build(self.buildDirectory)
        self._buildQuerySetsIndexFile()



    def build(self):
        ensureDirectory(self.buildDirectory)
        if self.hasSchema:
            # FIXME: called twice, why?
            self.schema.build(self.buildDirectory)
            if self.hasStates:
                for state in self.stateMap.values():
                    state.build(self.buildDirectory)

        # create the schema documentation in case.schema.rst
        if self.schema is not None:
            # FIXME: called twice, why?
            self.schema.build(self.buildDirectory)

        self._buildQuerySets()





if __name__ == "__main__":

    import os
    import sys

    SPHINX_DOCS_DIRECTORY=os.path.realpath(sys.argv[1])
    for case_directory in sys.argv[2:]:
        print 'Analysing case %s' % case_directory
        c = Case(case_directory, SPHINX_DOCS_DIRECTORY)
        print 'Building case %s' % case_directory
        c.build()
