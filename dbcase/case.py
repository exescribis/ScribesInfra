# coding=utf-8

"""
Management of "Database Case Studies".

A DBCase is represented by a directory with a structure like the following.
See documentation of SandboxDB_.
Most elements are optional::

    <DBCaseName>
        index.rst
        <DBCaseName>.schema.sql     Optional. Can be inferred from default state
        *.queries.sql               SQL files containing SELECT or CREATE VIEW queries
        states                      Directory containing database states
            default                 Default state used for instance to infer schema if needed
                <R1>.csv            CSV representation of the relation R1
                <R2>.csv            CSV representation of the relation R2
                ...
                <Rn>.csv
            <StateName2>            Another CSV-based state
                <R1>.csv
                ...
            <StateName3>            Google spreadsheet state
                <googlecode>.gs     Reference to the google spreadsheet


This generates::

    .build/
        <DBCaseName>.schema.sql             Schema either inferred or copies from source directory
        <DBCaseName>.schema.generated.rst   Corresponding schema documentation
        <DBCaseName>.queries.generated.rst  Documentation of all queries
        <QUERY>.generated.rst  ...          Individual documentation of queries

"""



from collections import OrderedDict

from dbcase.queries import QuerySet
from dbcase.schema import Schema
from dbcase.state import stateFactory
from filehelpers import directoryItemPaths, saveContent, ensureDirectory, fileContent, removeTrailingSeparator


class Case(object):
    """
    (Database) Case. This is the main class of the package. It represents the whole
    case study. This class has the following attributes:

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
    def __init__(self, caseDirectory, sphinxRootDirectory, buildDirectory=None, verbose=False):
        """

        Args:
            caseDirectory: directory representingthe database case

            sphinxRootDirectory: Sphinx root directory (the one containing the makefile usually)

            buildDirectory:
                build directory where output go. If None is specified then
                goes to '.build'

        Returns: None

        """

        self.verbose = verbose

        # "d""
        # :param caseDirectory (str): The directory containing the database case.
        # :param sphinxRootDirectory (str):
        #     The root directory for the sphinx documentation.
        #     This parameter is required because sphinx include statements are generated
        #     and are relative to this directory.
        #
        # :return: The DBCase created.

        #: Directory of the case.
        #: str.
        self.directory = removeTrailingSeparator(caseDirectory)
        assert os.path.isdir(self.directory)

        #: Sphinx root directory (the one containing the makefile usually).
        #: This is required to have includes inside includes
        #: as they must be defined using a pseudo absolute root
        #: from this root (see _pathFromRootSphinxDirectory).
        #: str.
        self.sphinxRootDirectory = removeTrailingSeparator(sphinxRootDirectory)
        assert os.path.isdir(self.sphinxRootDirectory)

        #: Name of the case.
        #: str.
        self.name = os.path.basename(self.directory)
        if verbose:
            print('  case named %s' % self.name)

        #: '.build' directory where all generated files go.
        #: This directory will be created in the build() operation.
        #: str.
        self.buildDirectory = self._buildDirectory(buildDirectory)

        #: Google credential file or None if this file does not exist
        #: This file allows to connect to google spreadsheet for states.
        #: str.
        self.googleCredentialsJsonFile = \
            self._tryToGetGoogleCredentials(self.sphinxRootDirectory)

        #: 'tmp' directory where temporary and debug files go.
        #: This directory will be created in build()
        # self.tmpDirectory = os.path.join(self.buildDirectory, 'tmp')

        #: All states in the 'states' directory. These states
        #: can be easily conveted to 'INSERT' statements and
        #: a schema ('CREATE' statements) can be inferred as well.
        #: see :class:State.
        #: Can be empty if there is no states.
        #: dict[string,State]. Map stateName -> State.
        self.stateMap = OrderedDict(sorted({
            os.path.basename(state_dir) : stateFactory(state_dir, self)
            for state_dir in self._getStateDirectories()
            }.items()))
        if self.verbose:
            print('  %s state(s) found: %s' % (len(self.stateMap), self.stateMap.keys()))

        #: A case may have no state.
        #: bool.
        self.hasStates = len(self.stateMap.keys()) > 0

        #: State|None
        #: default state. It is either named default or this will be
        #: the first one or None if there is no state at all.
        self.defaultState = self.getDefaultState()
        if self.verbose:
            if self.defaultState is None:
                print('  No state found. No database will be build.')
            else:
                print('  %s is the default state.' % self.defaultState.name)

        #: Schema object, either inferred from default state or taken from
        #: an explicit .schema.sql file.
        #: Schema|None
        self.schema = self._getSchema()   # should be done after stateMap

        #: Indicates if the case have a schema (either inferred or explicit)
        #: bool.
        self.hasSchema = self.schema is not None

        if self.verbose:
            if self.hasSchema and self.schema.isGenerated:
                print ('  schema inferred from default state')
            elif self.hasSchema and not self.schema.isGenerated:
                print ('  explicit schema found')
            else:
                print ('  no schema found or inferred')

        #: All queries from the *.queries.sql in the case directory.
        #: dict[string,QuerySet], Map queryiesName -> QuerySet
        self.querySetMap = OrderedDict(sorted({
            queries_file : QuerySet(queries_file, self, verbose=self.verbose)
            for queries_file in self._getQueriesFiles()
        }.items()))

        #: Name of the index file for queries
        #: str|None
        self.querySetIndexFilename = None  # defined by build

    def getDefaultState(self):
        """
        Return the "default" state for this case.
        :return: State
        """
        if len(self.stateMap)==0:
            return None
        elif 'default' in self.stateMap.keys():
            return self.stateMap['default']
        else:
            return list(self.stateMap)[0]

    def _buildDirectory(self, buildDirectory=None):
        if buildDirectory is None:
            return os.path.join(self.directory, '.build')
        else:
            return buildDirectory

    def _tryToGetGoogleCredentials(self, directory):
        """
        Try to get google credentials from ``GoogleScribesBot.json`` file.
        This is necessary to be able to get access if needed to google
        spreadsheets in the case of google spreadsheet states.
        :param directory: The directory containing ``GoogleScribesBot.json``.
        :return: Pathname of the file ``GoogleScribesBot.json`` or None
        """
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
                    isGenerated=False,
                    verbose=self.verbose)

        elif self.hasStates:
            sql_rst = self.defaultState.getInferredSchema()
            return Schema(
                    self.name,
                    self,
                    sql_rst,
                    schemaFilename=None,
                    isGenerated=True,
                    verbose = self.verbose)
        else:
            return None

    def _getStateDirectories(self):
        """
        Get the list of state directories
        :return (list[str]):
        """
        # TODO: change "states" to "States to get uniform naming"
        states_directory = os.path.join(self.directory, 'states')
        if (os.path.isdir(states_directory)):
            # there is a 'states' directory, directories inside are states name
            return directoryItemPaths(
                    states_directory,
                    lambda x:os.path.isdir(x) and not x.startswith('.'))
        else:
            return []

    def _getQueriesFiles(self):
        """
        Get the list of queries files, those ending with ``.queries.sql``.
        :return (list[str]):
        """
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
        if self.verbose:
            print('    saving %s ... '  % index_filename)
        saveContent(index_filename, index_content)
        if self.verbose:
            print('done')

    def _buildQuerySets(self):
        for querySet in self.querySetMap.values():
            querySet.build(self.buildDirectory)
        self._buildQuerySetsIndexFile()



    def build(self):
        """
        Build derived artefacts for this case in the build directory.
        :return: None
        """
        ensureDirectory(self.buildDirectory)
        if self.hasSchema:
            # FIXME: called twice, why?  Code below commebted  self.hasSchema = self.schema is not None
            self.schema.build(self.buildDirectory)
            if self.hasStates:
                for state in self.stateMap.values():
                    state.build(self.buildDirectory)

        # # create the schema documentation in case.schema.rst
        # if self.schema is not None:
        #     # FIXME: called twice, why?
        #     self.schema.build(self.buildDirectory)

        self._buildQuerySets()


if __name__ == "__main__":

    import os
    import sys

    verbose= '-v' in sys.argv
    if verbose:
        sys.argv.remove('-v')

    # print '-----',verbose
    # exit(0)

    SPHINX_DOCS_DIRECTORY=os.path.realpath(sys.argv[1])
    for case_directory in sys.argv[2:]:
        if verbose:
            print('Analysing case %s' % case_directory)
        c = Case(case_directory, SPHINX_DOCS_DIRECTORY, verbose=verbose)
        if verbose:
            print('Building case %s' % case_directory)
        c.build()
