# coding=utf-8

"""
Abstraction of the schema of a database case study.
As an input, the schema is either
* represented explictely as a ``*schema.sql`` file
* or inferred from the default state.

As an output the the following files and directories are build
* ``.build/<casename>.schema.sql``: the sql schema, either inferred or copied
* ``.build/<name>.schema.generated.rst``: rst description of the schema
* ``.build/schemaspy``: the schema spy documentation of the default state
"""

import os

import filehelpers
import sqlrst.parser
import sqlrst.printer
from filehelpers import saveContent

# TODO: activate pyschemaspy again
# import pyschemaspy

class Schema(object):
    """
    Schema.
    * name
    * case
    * sqlRst
    * sourceFilename
    * buildFilename
    * isGenerated
    * blocks
    * buildRstFile
    * build()
    """

    def __init__(self, name, case, sqlRstContent, schemaFilename=None, isGenerated=False):
        #: Name of the schema
        self.name = name

        #: Case
        self.case = case

        #: sqlrst text
        self.sqlRst = sqlRstContent

        #: str|None
        #: filename of the schema file if it is not generated.
        self.sourceFilename = schemaFilename

        #: str|None
        #: this file is in the .build directory. It will be set by build()
        self.buildFilename = None

        #: indicates if the schema has been generated.
        self.isGenerated = isGenerated

        #: list[sqlrst.structure.Blocks]|None.
        #: Schema text cut in logical blocks.
        self.blocks = sqlrst.parser.sqlRstToBlockSequence(self.sqlRst)

        #: str|None.
        #: filename of the generated rst file
        self.buildRstFile = None   # will be filled by build()

    def __saveSchemaFile(self, buildDirectory):
        print '    saving SQL Schema file',
        self.buildFilename = os.path.join(buildDirectory, self.name+'.schema.sql')
        saveContent(self.buildFilename, self.sqlRst)
        print ' ... done'

    def __buildSchemaRSTFile(self, buildDirectory):
        print '    generating RST Schema file ',
        self.buildRstFile = os.path.join(buildDirectory, self.name+'.schema.generated.rst')
        rst = sqlrst.printer.blockSequenceToRst(self.blocks, indentSQL=1)
        filehelpers.saveContent(self.buildRstFile, rst)
        print ' ... done'

    def __buildSchemaSpy(self, buildDirectory):
        print '    generating schemaspy documentation ',
        default_state_name = self.case.getDefaultState().name
        default_database = os.path.join(buildDirectory, '%s_%s.sqlite3' % (
            self.case.name, default_state_name))
        output_directory = os.path.join(
                buildDirectory,
                'schemaspy')
        e = pyschemaspy.Sqlite3SchemaSpyEngine(databaseFile=default_database)
        try:
            e.build(
                outputDirectory=output_directory)
        except ValueError:
            print '**** ERROR: ', e.lastExitCode
            print 'see ', e.lastCommandOutputFile

        print ' ... done'

    def build(self, buildDirectory):
        """
        Build the schema in the given directory
        :param buildDirectory: the directory where the schema must be build
        :return: None
        """
        print '  Building Schema ... '
        self.__saveSchemaFile(buildDirectory)
        self.__buildSchemaRSTFile(buildDirectory)
        # TODO: activate pyschemaspy again
        # self.__buildSchemaSpy(buildDirectory)
