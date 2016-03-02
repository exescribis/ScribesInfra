"""
`SchemaSpy`_ wrapper.



..  _`SchemaSpy`:
    http://scribestools.readthedocs.org/en/latest/schemaspy/
"""

import os
import filehelpers

class SchemaSpyEngine(object):

    def __init__(self, schemaSpyCommand='schemaspy'):
        self.schemaSpyCommand = schemaSpyCommand


THIS_DIR = os.path.dirname(os.path.realpath(__file__))
SCHEMASPY_SQLITE_PROPERTY = os.path.join(THIS_DIR,'sqlite.properties')

class Sqlite3SchemaSpyEngine(SchemaSpyEngine):

    def __init__(self,
                 databaseFile,
                 schemaSpyCommand='schemaspy',
                 ):
        SchemaSpyEngine.__init__(self, schemaSpyCommand=schemaSpyCommand)
        self.dataBaseFile = databaseFile
        self.lastExitCode = None
        self.lastCommandOutputFile = None

    def build(self,
              outputDirectory='schemaspy',
              options='-hq -noads -nologo',
              schemaSpyOutput='/dev/null'
        ):
        filehelpers.ensureDirectory(outputDirectory)
        self.lastCommandOutputFile = os.path.join(outputDirectory, 'schemaspy.out.txt')
        command = '%s -t %s -db %s -sso -o %s %s >>%s' % (
            self.schemaSpyCommand,
            SCHEMASPY_SQLITE_PROPERTY,
            self.dataBaseFile,
            outputDirectory,
            options,
            self.lastCommandOutputFile
            )
        filehelpers.saveContent(self.lastCommandOutputFile, command+'\n\n')
        self.lastExitCode = os.system(command)
        if self.lastExitCode != 0:
            raise ValueError(
                    'SchemaSpy Error: exit code=%s. See %s for details'
                    % (self.lastExitCode, self.lastCommandOutputFile))