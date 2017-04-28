# coding=utf-8

"""
Wrapper to the USE engine. Call the 'use' command. This command should be in the
system path. Otherwise the value UseEngine.USE_OCL_COMMAND should be set explicitely.
"""

__all__ = [
    'USEEngine',
]


import logging
# logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('test.' + __name__)

import os
import tempfile
import operator
import re


class USEEngine(object):
    """
    Wrapper to the "use" command.

    .. note::

        "use" must be available in the system path, otherwize the
        USE_OCL_COMMAND class attribute should be modified.
    """


    #: Path of to the use command binary.
    #: If the default value (``"use"``) does not work, for instance if
    #: the use binary is not in the system path, you can change this
    #: value either in the source, or programmatically using something
    #: like ::
    #:
    #:     USEEngine.USE_OCL_COMMAND = r'c:\Path\To\UseCommand\bin\use'
    #:
    USE_OCL_COMMAND = 'use'

    #: Last command executed by the engine
    command = None

    #: Directory in which the last command was executed
    directory = None

    #: Exit code of last execution (or None for before any execution)
    commandExitCode = None

    #: Output of last execution in case of separated out/err
    out = None

    #: Errors of last execution in case of separated out/err
    err = None

    #: Combined output & errors for last execution if merged out/err
    outAndErr = None


    @classmethod
    def __soilHelper(cls, name):
        return os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'res', name)


    @classmethod
    def __execute(cls, useFile, soilFile, errWithOut=False,
                  executionDirectory=None):
        """
        Execute use command with the given model and given soil file.
        The soil file MUST terminate by a 'quit' statement so that the process
        finish.

        # it seems that this is not necessary. So remove this.
        #    The process is executed in the specified 'executionDirectory'.
        #    If not specified the execution directory is set to the directory
        #    of the use file given as a parameter. This directory could be
        #    important if the soil files contains references to relative path.
        #    This is in particular the case of 'open file.soil' statements.
        """
        def readAndRemove(filename):
            with open(filename, 'r') as f:
                _ = f.read()
            # FIXME os.remove(filename)
            return _

        if errWithOut:
            #-- one unique output file for output and errors
            (f, output_filename) = tempfile.mkstemp(suffix='.txt', text=True)
            os.close(f)
            errors_filename = None
            redirection = '>%s 2>&1' % output_filename
            cls.out = None
            cls.err = None
        else:
            # -- two temporary files for output and errors
            (f, output_filename) = tempfile.mkstemp(suffix='.use', text=True)
            os.close(f)
            # prepare temporary file for errors
            (f, errors_filename) = tempfile.mkstemp(suffix='.err', text=True)
            os.close(f)
            redirection = '>%s 2>%s' % (output_filename, errors_filename)
            cls.outAndErr = None


        commandPattern = '%s -nogui -nr %s %s '+ redirection
        cls.command = (commandPattern
                           % (cls.USE_OCL_COMMAND, useFile, soilFile))

        cls.directory = executionDirectory if executionDirectory is not None \
                     else os.getcwd()
        # cls.directory = executionDirectory if executionDirectory is not None \
        #             else os.path.dirname(os.path.abspath(useFile))
        previousDirectory = os.getcwd()

        # Execute the command
        log.info('Execute USE OCL in %s: %s', cls.directory, cls.command)
        os.chdir(cls.directory)
        cls.commandExitCode = os.system(cls.command)
        os.chdir(previousDirectory)
        log.info('        execution returned %s exit code', cls.commandExitCode)

        if errWithOut:
             if cls.commandExitCode != 0:
                 cls.outAndErr = None
             else:
                 cls.outAndErr = readAndRemove(output_filename)
        else:
            cls.out = readAndRemove(output_filename)
            log.info ('        with output of %s lines',
                      len(cls.out.split('\n')))
            # log.debug('----- output -----')
            # log.debug(cls.out)
            # log.debug('----- end of output ------')

            cls.err = readAndRemove(errors_filename)
            if len(cls.err) > 0:
                log.info(
                    '        WITH ERRORS of %s lines: (first lines below)',
                    len(cls.err.split('\n'))   )
                LINE_COUNT = 3
                for err_line in cls.err.split('\n')[:LINE_COUNT]:
                    if err_line != '':
                        log.debug('         ERROR: %s',err_line)
            else:
                log.info(
                    '        without anything in stderr'
                )

            # log.debug('----- errors -----')
            # log.debug(cls.err)
            # log.debug('----- end of errors ------')

        return cls.commandExitCode


    @classmethod
    def useVersion(cls):
        """
        Get the version of use by executing it.
        Raise an exception if use cannot be executed.

        Returns (str): The version number.
        """
        cls.__execute(
            cls.__soilHelper('emptyModel.use'),
            cls.__soilHelper('quit.soil'))
        first_line = cls.out.split('\n')[0]
        m = re.match( r'(use|USE) version (?P<version>[0-9\.]+),', first_line)
        if m:
            return m.group('version')
        else:
            msg = "Cannot execute USE OCL or get its version.\n" \

            raise EnvironmentError('Cannot execute USE OCL or get its version. Is this program installed?')

    @classmethod
    def withUseOCL(cls):
        """
        Indicates if use is installed and works properly.
        Returns (bool): True if use is installed properly, False otherwise.
        """
        try:
            cls.useVersion()
        except EnvironmentError:
            return False
        else:
            return True

    @classmethod
    def analyzeUSEModel(cls, useFileName):
        """
        Submit a ``.use`` model to use and indicates return the exit code.

        Args:
            useFileName (str): The path of the ``.use`` file to analyze.

        Returns (int):
            use command exit code.
        """
        cls.__execute(
            useFileName,
            cls.__soilHelper('infoModelAndQuit.soil'))
        return cls.commandExitCode


    @classmethod
    def checkSoilFileWithUSEModel(cls, modelFile, stateFile):
        driver_sequence = 'open %s \nquit' % stateFile
        (f, driver_filename) = tempfile.mkstemp(suffix='.soil', text=True)
        os.close(f)
        with open(driver_filename, 'w') as f:
            f.write(driver_sequence)

        cls.__execute(
            modelFile,
            driver_filename,
            errWithOut=False)

        return cls.commandExitCode


    @classmethod
    def evaluateSoilFilesWithUSEModel(cls, modelFile, stateFiles):

        def __generateSoilValidationDriver(stateFilePaths):
            """
            Create a soil sequence with the necessary statements to drive the
            sequence of state validation. That is, it loads and checks each
            state one after each other.

            The soil driver sequence generated looks like:
                    reset
                    open file1.soil
                    check
                    reset
                    open file2.soil
                    check
                    ...
                    quit

            The output with error messages can be found after the execution
            in the variable outAndErr.
            :param stateFilePaths: A list of .soil files corresponding
            to states.
            :type stateFilePaths: [str]
            :return: The soil text
            :rtype: str
            """
            if len(stateFiles) == 0:
                raise Exception('Error: no state file to evaluate')
            lines = reduce(operator.add,
                           map(
                               lambda file: ['reset', 'open ' + file,
                                             'check -d'],
                               stateFilePaths))
            lines.append('quit')
            return '\n'.join(lines)

        #-- generate soil driver
        if len(stateFiles) == 0:
            raise Exception('Error: no state file to evaluate')
        driver_sequence = __generateSoilValidationDriver(stateFiles)
        (f, driver_filename) = tempfile.mkstemp(suffix='.soil', text=True)
        os.close(f)
        with open(driver_filename, 'w') as f:
            f.write(driver_sequence)

        cls.__execute(
            modelFile,
            driver_filename,
            errWithOut=True)

        return cls.commandExitCode
