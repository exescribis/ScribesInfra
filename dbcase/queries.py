# coding=utf-8

"""
Management of datatbase queries and their evaluation on states.

This package contains the following class hierarchy::

    QuerySet

    Query
        SelectQuery
        CreateViewQuery

    QueryEvaluation
        SelectQueryEvaluation
        CreateViewQueryEvaluation

"""

from __future__ import print_function

import os
import re
from collections import OrderedDict

import filehelpers
import sqlrst.parser
import sqlrst.printer
import sqlrst.structure
from filehelpers import fileContent


class QuerySet(object):
    """
    QuerySet
        * filename
        * name
        * sql
        * case
        * blocks
        * buildRstFile
        * v queryList
    """

    def __init__(self, queriesFilename, case, verbose=False):

        #: filename of the queries file.
        self.filename = queriesFilename

        _ = os.path.basename(self.filename).replace('.queries.sql','')
        #: name of the query set, without numbering information at the beginning
        # self.name = re.sub('^[0-9]+_','',_)
        self.name = _

        #: SQL Text correspoding to the query files
        self.sql = fileContent(self.filename)

        #: Case containing this QuerySet
        self.case = case

        #: Schema text cut in logical blocks.
        #: list[sqlrst.structure.Block]
        self.blocks = sqlrst.parser.sqlRstToBlockSequence(self.sql)

        #: list[Query].
        #: List of queries extracted from the query set.
        self.queryList = self.__extractQueries()

        #: str|None.
        #: filename of the generated rst file
        self.buildRstFile = None   # will be filled by build()

        self.verbose = verbose

    def __extractQueries(self):
        """
        Transforms the block list into queries of appropriate type.
        :return: list|Query]
        """
        result = []
        queryIndex = 0
        for block in self.blocks:
            if isinstance(block, sqlrst.structure.SelectStatementBlock):
                result.append(SelectQuery(block, self, queryIndex+1))
                queryIndex += 1
            elif isinstance(block, sqlrst.structure.CreateViewStatementBlock):
                result.append(CreateViewQuery(block, self, queryIndex+1))
                queryIndex += 1

            else:
                pass
        return result

    def _buildRSTFile(self, buildDirectory):
        """
        Generate RST query set file named ``*.generated.rst``
        :param buildDirectory (str): path to the str directory.
        :return: None
        """
        if self.verbose:
            print( '    -> file', end=" ")
        outFileName = self.name+'.generated.rst'
        self.buildRstFile = os.path.join(buildDirectory,outFileName)
        rst = sqlrst.printer.blockSequenceToRst(self.blocks, indentSQL=1)

        filehelpers.saveContent(self.buildRstFile, rst)
        if self.verbose:
            print(outFileName, end=" ")
            print(' ... done')

    def _buildQueries(self, buildDirectory):
        for query in self.queryList:
            query.build(buildDirectory)

    def build(self, buildDirectory):
        if self.verbose:
            print('  '
                  '%s ... ' % self.name)
        self._buildRSTFile(buildDirectory)
        self._buildQueries(buildDirectory)

        # for state in self.case.stateMap.values():
        #     print 'Executing %s on state %s' % (self.filename, state.name)
        #     result = state.databaseEngine.execute(self.sql)
        #     print result


class Query(object):
    """
    Query
        * ^ querySet
        * key
        * queryIndex
        * block
        *
        * v queryEvaluationMap

        SelectQuery

        CreateViewQuery
    """

    def __init__(self, block, querySet, queryIndex):

        #: int
        #: The index in the list of queries  of the querySet
        self.queryIndex = queryIndex

        #: sqlrst.structure.Block
        #: Reference to the file block where this query is defined.
        self.block = block

        #: QuerySet
        #: QuerySet in which this query is defined.
        self.querySet = querySet

        #: str
        #: Either the name of the block or the index of the key prefixed
        #: by the query set name. See _getKey for more accurate specficiation.
        self.key = self._getKey()

        #: OrderedDict[State,QueryEvaluation]|None.
        #: Defined by the build method. There is one
        #: query evaluation for each state.
        self.queryEvaluationMap = self.__createEmptyQueryEvaluation()

    def _getKey(self):
        """
        The key is :
        - the name if the block is named (use SELECT /*:name*/ for SELECT stmts
        - the name of the key for the first block in the file
        - the name 
        Returns:

        """
        if self.block.name is not None:
            if self.block.name == '.':
                return self.querySet.name
            else:
                return self.block.name
        else:
            if self.queryIndex == 1:
                return self.querySet.name
            else:
                return self.querySet.name+'_'+str(self.queryIndex)

    def _createQueryEvaluation(self, state):
        raise NotImplementedError('Each subclass must implement this method')


    def __createEmptyQueryEvaluation(self):
        result = OrderedDict()
        for state in self.querySet.case.stateMap.values():
            result[state] = self._createQueryEvaluation(state)
        return result

    def build(self, buildDirectory):
        for query_evaluation in self.queryEvaluationMap.values():
            query_evaluation.build(buildDirectory)


class SelectQuery(Query):
    """
    SELECT queries.
    """
    def __init__(self, block, querySet, queryIndex):
        Query.__init__(self, block, querySet, queryIndex)

    def _createQueryEvaluation(self, state):
        return SelectQueryEvaluation(self, state)


class CreateViewQuery(Query):
    """
    CREATE VIEW queries.
    """
    def __init__(self, block, querySet, queryIndex):
        Query.__init__(self, block, querySet, queryIndex)

    def _createQueryEvaluation(self, state):
        return CreateViewQueryEvaluation(self, state)


class QueryEvaluation(object):
    """
    QueryEvaluation
        * ^ query
        * name
        * state
        * error
        * csvFile
        * rowNumber
        * outFile
    """

    def __init__(self, query, state):
        #: Query that is evaluated
        self.query = query

        #: State used to evaluate the query
        self.state = state

        #: Name of the state evaluation
        self.name = self.query.key  # +'_'+self.state.name

        #: Error raised during the evaluation, if any.
        #: None if the evaluation was ok, the exception raise otherwise
        self.error = None # filled by build(), None if error

        #: Path of the csvfile resulting from the query evaluation or None
        #: in case
        #: Filled by build(), None if error
        self.csvFile = None

        #: Filled by build(), None if error
        self.rowNumber = None

        # None before build, but always exists otherwise.
        # Either contains an error or some message such as the number of rows.
        # The file could be empty as well.
        self.outFile = None

        #: Exception|None

    def _computeCSVAndOutputFileNames(self, buildDirectory):
        self.csvFile = os.path.join(
                self.state.stateBuildDirectory,
                '%s.csv' % self.name)
        self.outFile = os.path.join(
                self.state.stateBuildDirectory,
                '%s.out' % self.name)

    def _executionError(self, e):
        self.error = e
        self.rowNumber = None
        self.csvFile = None
        message = (
            "ERROR in '%s/%s.queries.sql'.\nWhen evaluating %s for state '%s':\n\n%s" % (
                self.query.querySet.case.name,
                self.query.querySet.name,
                self.query.key,
                self.state.name,
                unicode(self.error))).replace(r'\n','\n')
        sphinx_message = '\n..  error::\n\n%s\n\n' % dbcase.indent(1, message)
        saveContent(self.outFile, sphinx_message)
        dbcase.warning(message)

    def build(self, buildDirectory):
        pass




import dbcase
from filehelpers import saveContent

class SelectQueryEvaluation(QueryEvaluation):
    """
    Evaluation of a :class:`SelectQuery`.
    """
    def __init__(self, query, state):
        QueryEvaluation.__init__(self, query, state)

    def build(self, buildDirectory):
        print('    SELECT {:<50}'.format(self.name), end=' ')
        self._computeCSVAndOutputFileNames(buildDirectory)
        query = self.query.block.sqlText
        try:
            result = self.state.databaseEngine.execute(query, self.csvFile)
        except Exception as e:
            self._executionError(e)
        else:
            try:
                result = self.state.databaseEngine.execute(query)
            except:
                # we don't care two much
                self.rowNumber = 0
                dbcase.warning('Cannot count results. Not really important in fact.')
                saveContent(self.outFile,'unkown number of rows.')
            else:
                self.rowNumber = len(list(result))
                saveContent(self.outFile,'%s row(s)' % self.rowNumber)
            print(' {:>5}'.format(self.rowNumber) )


class CreateViewQueryEvaluation(QueryEvaluation):
    """
    Evaluation of a :class:`CreateViewQuery`.
    """
    def __init__(self, query, state):
        QueryEvaluation.__init__(self, query, state)

    def build(self, buildDirectory):
        print('    *VIEW* {:<48}**'.format(self.name), end=' ')
        try:
            self.state.databaseEngine.execute(self.query.block.sqlText)
        except Exception as e:
            self._executionError(e)
        else:
            self._computeCSVAndOutputFileNames(buildDirectory)
            query = 'SELECT * FROM %s; ' % self.query.block.name
            try:
                result = self.state.databaseEngine.execute(query, self.csvFile)
            except Exception as e:
                self._executionError(e)
            else:
                try:
                    result = self.state.databaseEngine.execute(query)
                except:
                    # we don't care two much
                    self.rowNumber = 0
                    dbcase.warning('Cannot count results. Not really important in fact.')
                    saveContent(self.outFile,'unkown number of rows.')
                else:
                    self.rowNumber = len(list(result))
                    saveContent(self.outFile,'%s row(s)' % self.rowNumber)
                    print(' {:>5}'.format(self.rowNumber))

