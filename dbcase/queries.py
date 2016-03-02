# coding=utf-8

"""


    QuerySet
        * filename
        * name
        * sql
        * case
        * blocks
        * buildRstFile
        * v queryList

    Query
        * ^ querySet
        * key
        * queryIndex
        * block
        *
        * v queryEvaluationMap

        SelectQuery

        CreateViewQuery

    QueryEvaluation
        * ^ query
        * name
        * state
        * error
        * csvFile
        * rowNumber
        * outFile

        SelectQueryEvaluation

        CreateViewQueryEvaluation

"""





import os
import re
from collections import OrderedDict

import filehelpers
import sqlrst.parser
import sqlrst.printer
import sqlrst.structure
from filehelpers import fileContent


class QuerySet(object):

    def __init__(self, queriesFilename, case):

        #: filename of the queries file.
        self.filename = queriesFilename
        #: name of the query set, without numbering information at the beginning
        _ = os.path.basename(self.filename).replace('.queries.sql','')
        self.name = re.sub('^[0-9]+_','',_)
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
        print '    generating RST QuerySet file',
        outFileName = self.name+'.generated.rst'
        self.buildRstFile = os.path.join(buildDirectory,outFileName)
        rst = sqlrst.printer.blockSequenceToRst(self.blocks, indentSQL=1)

        filehelpers.saveContent(self.buildRstFile, rst)
        print outFileName,
        print ' ... done'

    def _buildQueries(self, buildDirectory):
        for query in self.queryList:
            query.build(buildDirectory)

    def build(self, buildDirectory):
        print '  Building QuerySet ... '
        self._buildRSTFile(buildDirectory)
        self._buildQueries(buildDirectory)

        # for state in self.case.stateMap.values():
        #     print 'Executing %s on state %s' % (self.filename, state.name)
        #     result = state.databaseEngine.execute(self.sql)
        #     print result


class Query(object):

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
        #: by the query set name.
        self.key = self._getKey()
        #: OrderedDict[State,QueryEvaluation]|None.
        #: Defined by the build method. There is one
        #: query evaluation for each state.
        self.queryEvaluationMap = self.__createEmptyQueryEvaluation()

    def _getKey(self):
        if hasattr(self.block, 'name'):
            return self.block.name
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

    def __init__(self, block, querySet, queryIndex):
        Query.__init__(self, block, querySet, queryIndex)

    def _createQueryEvaluation(self, state):
        return SelectQueryEvaluation(self, state)


class CreateViewQuery(Query):

    def __init__(self, block, querySet, queryIndex):
        Query.__init__(self, block, querySet, queryIndex)

    def _createQueryEvaluation(self, state):
        return CreateViewQueryEvaluation(self, state)


class QueryEvaluation(object):

    def __init__(self, query, state):
        self.query = query
        self.state = state
        self.name = self.query.key  # +'_'+self.state.name
        #: None if the evaluation was ok, the exception raise otherwise
        self.error = None # field by build(), None if error
        #: filled by build(), None if error
        self.csvFile = None
        #: filled by build(), None if error
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

    def __init__(self, query, state):
        QueryEvaluation.__init__(self, query, state)

    def build(self, buildDirectory):
        print '    SELECT %s ... ' % self.name,
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
            print  ' %s rows. done' % self.rowNumber


class CreateViewQueryEvaluation(QueryEvaluation):

    def __init__(self, query, state):
        QueryEvaluation.__init__(self, query, state)

    def build(self, buildDirectory):
        print '    CREATE VIEW %s ; ' % self.name,
        try:
            self.state.databaseEngine.execute(self.query.block.sqlText)
        except Exception as e:
            self._executionError(e)
        else:
            print 'SELECT * ',
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
                    print  ' %s rows. done' % self.rowNumber
