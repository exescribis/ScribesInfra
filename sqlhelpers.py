# coding=utf-8

import csv
import os
import sqlite3

import sqlalchemy
import sqlalchemy.exc
import sqlalchemy_utils

import typedtable
from filehelpers import fileContent, ensureNoFile


def sqlAlchemyResultToCSVFile(result, filename):
    """
    Save a SQLAlchemy result to a .csv file
    :param result: (
    :param filename:
    :return:
    """
    with open(filename, 'wb') as f:
        outcsv = csv.writer(f)
        # dump header
        outcsv.writerow(result.keys())
        # dump rows
        outcsv.writerows(result.fetchall())


class DatabaseEngine(object):
    """ Super class of multiple database engine.
    """

    def __init__(self):
        #: URI of the database. Details depends on the RDBMS.
        #: This value is set by subclasses.
        self.dbURI = None

        #: SQL Alchemy Engine if open, or None.
        #: This value is set by ensureConnection()
        self.sqlAlchemyEngine = None

        #: Connection if open, or None
        #: This value is set by ensureConnection()
        self.connection = None

        #: SQL representation of the Schema or None.
        #: This value can be set by setSchema or can be inferred
        #: when a CSVFile is imported.
        self.schemaFile = None

        #: This value is the content of self.schemaFile unless
        #: the method addToSchema is used. In this case the sql
        #: statement may be appended at the end.
        self.schemaText = None

    def ensureEngine(self):
        """
        Make sure that an engine is available.
        """
        if self.sqlAlchemyEngine is None:
            self.sqlAlchemyEngine = sqlalchemy.create_engine(self.dbURI)

    # def ensureConnection(self):
    #     if self.sqlAlchemyEngine is None or self.connection is None:
    #         self.sqlAlchemyEngine = sqlalchemy.create_engine(self.dbURI)
    #         self.connection = self.sqlAlchemyEngine.connect()
    #
    # def closeConnection(self):
    #     if self.connection is not None:
    #         self.connection.close()
    #     self.connection = None
    #
    #     if self.sqlAlchemyEngine is not None:
    #         self.sqlAlchemyEngine.dispose()
    #     self.sqlAlchemyEngine = None

    def execute(self, sql, outputCSVFile=None):
        """
        Execute a query with the engine.
        :param sql:  The SQL query to be executed.
        :param outputCSVFile:
        :return:
        """
        self.ensureEngine()
        result = self.sqlAlchemyEngine.execute(sql)
        if outputCSVFile is not None:
            sqlAlchemyResultToCSVFile(result, outputCSVFile)
        return result

    def executeScript(self, sqlFile):
        self.execute(fileContent(sqlFile))

    def defineSQLSchema(self, sqlFile):
        assert(self.schemaFile is None)
        self.executeScript(sqlFile)
        self.schemaFile = sqlFile
        self.schemaText = fileContent(self.schemaFile)

    def addToSchema(self, sql):
        self.execute(sql)
        if self.schemaText is None:
            self.schemaText = ''
        self.schemaText += '\n\n' + sql

    def importCSVFile(self, csvFile,
                      tableName=None, columnNames=None,
                      autoCreateInferredTableSchema=False, truncateTable=False,
                      hasHeader=True, delimiter=',', quotechar='"'):

        t = typedtable.TypedTable(
                csvFile,
                tableName=tableName, columnNames=columnNames,
                header=hasHeader, delimiter=delimiter, quotechar=quotechar)

        if autoCreateInferredTableSchema:
            sql = t.getSQLCreateStatement()
            self.addToSchema(sql)

        if truncateTable:
            self.execute('TRUNCATE TABLE %s' % t.tableName )

        sql = t.getSQLInsertStatements()
        self.execute(sql)

    def close(self):
        if self.sqlAlchemyEngine is not None:
            self.sqlAlchemyEngine.dispose()
            self.sqlAlchemyEngine = None


class SQLiteDatabaseEngine(DatabaseEngine):

    def __init__(self, dbDirectory, dbName, isNewDatabase=False):
        """
        Open or create a sqlite database.
        :param dbDirectory: Directory where the sqlite database should be created.
        :param dbName: Name of the database without .sqlite3 extension.
        :param isNewDatabase: Should the database be created?
        :return:
        """
        super(SQLiteDatabaseEngine,self).__init__()
        self.dbName = dbName
        self.dbDirectory =  dbDirectory
        self.dbFile = os.path.join(self.dbDirectory, self.dbName+'.sqlite3')
        self.dbURI = 'sqlite:///'+self.dbFile
        if isNewDatabase:
            ensureNoFile(self.dbFile)
            sqlalchemy_utils.create_database(self.dbURI)
        self.schema = None

    def executeScript(self, sqlFile):
        # sqlite3 cannot execute multiple statement at the same time
        # close the existing engine if it exist
        if self.sqlAlchemyEngine is not None:
            self.sqlAlchemyEngine.dispose()
            self.sqlAlchemyEngine = None
        # use sqlite3 interface
        sqlite3_connection = sqlite3.connect(self.dbFile)
        # with tempfile.NamedTemporaryFile(mode='w',suffix='.sql') as f:
        #     f.write(self.dbFile)
        try:
            sqlite3_connection.executescript(fileContent(sqlFile))
        except:
            print (
                'Exception raised when executing Script "%s":\n%s'
                % (sqlFile, fileContent(sqlFile)) )
            raise
        sqlite3_connection.close()

