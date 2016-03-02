# coding=utf-8

"""
    State
        * ^ case
        * sourceDirectory
        * name
        * typeTables
        * databaseEngine
        * stateBuildDirectory
"""


import os
import re
import shutil

import dbhelpers
from filehelpers import ensureDirectory, saveContent

import typedtable


class State(object):
    """
    Abstraction of a state. A state is represented by a directory.
    Various concrete representations are possibles.
    """
    def __init__(self, stateDirectory, case):

        #: source directory of the state.
        self.sourceDirectory = stateDirectory
        assert os.path.isdir(self.sourceDirectory)

        #: name of the state.
        self.name = os.path.basename(stateDirectory)

        #: DatabaseEngine or None.
        #: This value could be set by setDatabaseEngine()
        self.databaseEngine = None

        #: Case
        self.case = case

        #: str|None
        #: Build directory. Created with build()
        self.stateBuildDirectory = None



class TypedTablesState(State):

    def __init__(self, stateDirectory, case, typedTables):
        State.__init__(self, stateDirectory=stateDirectory, case=case)
        self.typedTables = typedTables

    def getSQLCreateStatements(self):
        return '\n\n'.join([
            typed_table.getSQLCreateStatement() for typed_table in self.typedTables.values()
        ])

    def getSQLInsertStatements(self):
        return '\n\n'.join([
            typed_table.getSQLInsertStatements() for typed_table in self.typedTables.values()
        ])

    def getInferredSchema(self):
        return self.getSQLCreateStatements()

    def setDatabaseEngine(self, engine):
        self.databaseEngine = engine

    def build(self, buildDirectory):

        def __createStateBuildDirectory():
            states_directory = os.path.join(buildDirectory, 'states')
            ensureDirectory(states_directory)
            self.stateBuildDirectory = os.path.join(states_directory, self.name)
            ensureDirectory(self.stateBuildDirectory)

        def __createEmptyDatabase():
            # create the database
            dbname = '%s_%s' % (self.case.name, self.name)
            e = dbhelpers.SQLiteDatabaseEngine(self.stateBuildDirectory, dbname, isNewDatabase=True)
            self.setDatabaseEngine(e)

        def __executeDatabaseSchema():
            self.databaseEngine.defineSQLSchema(self.case.schema.buildFilename)

        def __insertDatabaseContent():
            sql = self.getSQLInsertStatements()
            filename = '%s_%s.insert.sql' % (self.case.name, self.name)
            generated_content_file_name = os.path.join(self.stateBuildDirectory,filename)
            saveContent(generated_content_file_name, sql)
            self.databaseEngine.executeScript(generated_content_file_name)

        def __copyCSVFiles():
            # copy all source csv file in this directory
            for filename in os.listdir(self.sourceDirectory):
                m = re.match('(?P<name>\w+)\.csv',filename)
                if m:
                    source_file_name = os.path.join(self.sourceDirectory, filename)
                    target_file_name = os.path.join(self.stateBuildDirectory, filename)
                    shutil.copyfile(source_file_name, target_file_name)

        __createStateBuildDirectory()
        __createEmptyDatabase()
        __executeDatabaseSchema()
        __insertDatabaseContent()
        __copyCSVFiles()



class CSVFilesState(TypedTablesState):

    """
    State represented as a directory containing one csv file for each table.
    Name of files are assumed to be name of tables (+'.csv' extenstion).
    The files are read and a map of tableName -> typedTable is created.
    """
    def __init__(self, stateDirectory, case):
        TypedTablesState.__init__(self, stateDirectory, case, typedTables={})

        # fill the typedTables map by reading the csv files
        for filename in os.listdir(self.sourceDirectory):
            m = re.match('(?P<name>\w+)\.csv',filename)
            if m:
                # this is a csv file, add it to the list
                table_name = m.group('name')
                csv_file_name = os.path.join(self.sourceDirectory, filename)
                table = typedtable.TypedTable(csv_file_name, tableName=table_name, header=True)
                self.typedTables[table_name] = table


import googlehelpers

class GoogleSpreadsheetState(CSVFilesState):
    """
    State represented as a google spreadsheet with on sheet for each table.
    Name of sheets are assumed to be name of tables.
    The spreadsheet to be used is defined by a filename like '<key>.gs'.
    CSV files are loaded in the stateDirectory and will be used in case of
    a connection problem with google spreadsheet. This provides a cache
    mechanism that could be useful when working off line or withou appropriate credentials.
    The spreasheet is read, then CSV files are created, then everything work like
    a CSVFilesState.
    """
    def __init__(self, stateDirectory, case, spreadsheetReference):
        self.spreadsheetReference = spreadsheetReference
        self.updatedFromSpreadsheet = None  # set by _tryToDownloadGoogleSpreadsheet

        if case.googleCredentialsJsonFile is None:
            raise ValueError('No credential file to connect to Google Spreadsheet')
        else:
            self._tryToDownloadGoogleSpreadsheet(stateDirectory, case, spreadsheetReference, )
            CSVFilesState.__init__(self, stateDirectory, case)

    def _tryToDownloadGoogleSpreadsheet(self, stateDirectory, case, spreadsheetReference ):
        files_updated = []
        name = os.path.basename(stateDirectory)
        print '  State %s: downloading state from google %s...' % (name, spreadsheetReference),
        try:
            files_updated = googlehelpers.googleSpreadSheetToCSVFiles(
                                credentialsJsonFile=case.googleCredentialsJsonFile,
                                spreadSheetKey=spreadsheetReference,
                                outputDirectory=stateDirectory)
        except Exception as e:
            print
            print '    ***** DOWNLOAD FAILED'
            print '    Local .csv files used (if any)'
            self.updatedFromSpreadsheet = False
        else:
            print 'done'
            print '      Files updated: '+', '.join(map(os.path.basename,files_updated))
            self.updatedFromSpreadsheet = True
        return files_updated

def googleSpreadsheetReference(filename):
    if filename.endswith('.gs'):
        return filename[:-len('.gs')]
    else:
        return None

def stateFactory(stateDirectory, case):
    """
    Create a state from a stateDirectory. The actual type
    of the state depends on the actual content of the directory.
    If there is a '.gs' file then this is assumed to be a GoogleSpreadsheetState.
    If there is at least a '.csv' file (but no '.gs' file) this is a CSVFilesState.
    """
    for filename in os.listdir(stateDirectory):
        google_reference = googleSpreadsheetReference(filename)
        if google_reference:
            return GoogleSpreadsheetState(stateDirectory, case, google_reference)
    # There is no '.gs' file. Assume that this is a CSVFilesState
    return CSVFilesState(stateDirectory, case)



    # def _buildStateArtefact(self, buildDirectory):
    #     """
    #     Create a sqlite database in the build directory.
    #     :param state State: The state to convert in a database.
    #     :return: None
    #     """
    #
    #
    #
    #
    #     def __define_database_content():
    #         sql = state.getSQLInsertStatements()
    #         filename = '%s_%s.insert.sql' % (self.name,state.name)
    #         generated_content_file_name = os.path.join(self.buildDirectory,filename)
    #         saveContent(generated_content_file_name, sql)
    #         state.databaseEngine.executeScript(generated_content_file_name)
    #
    #
    #     # Define the database schema
    #         state.databaseEngine.defineSQLSchema(self.schema.filename)
    #
    #     ensureDirectory(self.buildDirectory)
    #

    #     __define_database_schema()
    #     __define_database_content()
    #     state.databaseEngine.close()










