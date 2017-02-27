"""
Engine that must be used as a replacement of sphinx binanry in order
to integrate problems documentation within the documentation itself.
Obviously this engine call sphinx-build, but do some other processing
as well.

"""


import os
import sys

import filehelpers
import sphinxproblems.problems
import sphinxproblems.parser
import sphinxproblems.patchhtml


debug=True
showOutputAndErrors=False

import sphinx

def default(value,defaultValue):
    return value if value is not None else defaultValue

class SphinxProblemsEngine(object):
    def __init__(self,
                 sourceDir,
                 targetDir,
                 clean=True,
                 docTrees=None,
                 confDir=None,
                 sphinxOutputPhase1=None,
                 sphinxOutputPhase3=None,
                 sphinxErrorsPhase1=None,
                 sphinxErrorsPhase3=None,
                 rawProblemFile=None,
                 rstProblemFile=None,
                 shortStatusProblemFile=None,
                 configValues=()):
        """
        Create the engine by settings its parameters.
        Do not perform any processing.

        :param sourceDir: The source directory where the rst files are.
        :param targetDir: The target directory where the .index.html will be generated
        :param clean: If true the target directory is cleaned.
        :param docTrees: default to <targetDir>/.doctrees
        :param confDir: directory containing conf.py. Default to <sourceDir>/.infra/docs
        :param sphinxOutputPhase1:
            File where to save the output of phase1.
            Default to <targetDir>/sphinx-output-phase1.txt.
        :param sphinxOutputPhase3:
            File where to save the output of phase3.
            Default to <targetDir>/sphinx-output-phase3.txt.
        :param sphinxErrorsPhase1:
            File where to save the errors generated during phase1.
            Default to <targetDir>/sphinx-errors-phase1.txt.
        :param sphinxErrorsPhase3:
            File where to save the errors generated during phase3.
            Default to <targetDir>/sphinx-errors-phase3.txt.
        :param rawProblemFile:
            File where the "problems" are saved in a raw mode.
            Default to <targetDir>/sphinx-problems.txt
        :param rstProblemFile:
        :param shortStatusProblemFile:
        :param configValues:
        """

        self.sourceDir = sourceDir

        self.targetDir = targetDir

        self.clean = clean

        self.docTrees = default(
                docTrees,
                os.path.join(self.targetDir, '.doctrees'))

        self.confDir = default(
                confDir,
                os.path.join(self.sourceDir, '.infra', 'docs'))

        #: pairs of config values that will override the config value
        self.configValues = configValues



        self.sphinxOutputPhase1 = default(
                sphinxOutputPhase1,
                os.path.join(self.targetDir, 'sphinx-output-phase1.txt'))

        self.sphinxOutputPhase3 = default(
                sphinxOutputPhase3,
                os.path.join(self.targetDir, 'sphinx-output-phase3.txt'))

        self.sphinxErrorsPhase1 = default(
                sphinxErrorsPhase1,
                os.path.join(self.targetDir, 'sphinx-errors-phase1.txt'))

        self.sphinxErrorsPhase3 = default(
                sphinxErrorsPhase3,
                os.path.join(self.targetDir, 'sphinx-errors-phase3.txt'))

        self.rawProblemFile = default(
                rawProblemFile,
                os.path.join(self.targetDir,'sphinx-problems.txt'))

        self.rstProblemFile = default(
                rstProblemFile,
                os.path.join(self.confDir, 'problems','sphinx-problems.rst'))

        self.shortStatusProblemFile = default(
                shortStatusProblemFile,
                os.path.join(self.targetDir, 'sphinx-problems-short-status.txt'))

        self.shortStatus = None # filled by _generateShortStatusProblemFile



    def build(self):

        # clean the directory if required
        if self.clean:
            filehelpers.ensureEmptyDir(self.targetDir)
        filehelpers.ensureDirectory(self.targetDir)
        # raw_input('cont')

        #------ execute phase #1
        exit_code = self._phase1ExecuteSphinxForNormalDocProduction()
        if debug:
            print('sphinxproblems: Phase #1 terminated with exit code %s' % exit_code)
        if exit_code != 0:
            print('**** ERROR ****: sphinx exit with code %s in phase #1' % exit_code)
            print(' '*8+'errors can be found in "%s"' %  self.sphinxErrorsPhase1)
            # raw_input('cont')
            return exit_code
        if not os.path.isfile(self.rawProblemFile):
            if debug:
                print ('sphinxproblems: no problems found. no file %s ' % self.rawProblemFile)
            # raw_input('cont')
            return 0
        else:

            #----- execute phase 2
            self._phase2ExtractAndGenerateProblemsDoc()
            # raw_input('cont')


            #----- execute phase 3
            exit_code = self._phase3ExecuteSphinxForProblemDocProduction()
            if exit_code != 0:
                print('**** ERROR ****: sphinx exit with code %s in phase #3' % exit_code)
                print(' ' * 8 + 'errors can be found in "%s"' % self.sphinxErrorsPhase3)
                # raw_input('cont')
                return exit_code
            # raw_input('cont')
            #----- execute phase 4
            self._phase4PatchHTMLFiles()
            print (self.shortStatus)
            # raw_input('cont')
            return 0



    #----- phases #1 to #4 --------------------------------------------------

    def _phase1ExecuteSphinxForNormalDocProduction(self):
        """
        Phase #1 : Execute sphinx for the first time. The goal is to
        generate regular documentation and collect the warnings.
        :return: exit code
        """
        if debug:
            print('sphinxproblems: Phase #1. Documentation generation')
        options = ['-q', '-w', self.rawProblemFile]
        exit_code =  self._executeSphinx(
            options=options,
            outputFile=self.sphinxOutputPhase1,
            errorsFile=self.sphinxErrorsPhase1
        )
        return exit_code

    def _phase2ExtractAndGenerateProblemsDoc(self):
        """
        Phase #2:  Extract the problems generated during phase #1
        and generate the files documenting them.
        """
        if debug:
            print ('sphinxproblems: Phase #2. Documenting problems')
        problem_manager = self._extractProblemsFromRawProblemFile()
        self._generateRstProblemFile(problem_manager)
        self._generateShortStatusProblemFile(problem_manager)


    def _phase3ExecuteSphinxForProblemDocProduction(self):
        """
        Phase #3: Execute sphinx for the second time. The goal is to
        generate the documentation of errors collected during phase 1.
        :return: exit code.
        """
        if debug:
            print ('sphinxproblems: Phase #3. Generating documentation for problems')
        # use a tag to inform the extension that this is phase 3
        options = ['-Q', '-t', 'sphinx-problems-rerun']
        exit_code = self._executeSphinx(
            options=options,
            outputFile=self.sphinxOutputPhase3,
            errorsFile=self.sphinxErrorsPhase3
        )
        return exit_code

    def _phase4PatchHTMLFiles(self):
        """
        Phase #4: Post processing of HTML file. The goal is
        to add a link to the problem documentation in all pages.
        :return:
        """
        if debug:
            print('sphinxproblems: Phase #4. Patching html files to add link to problem documents.')
        with open(self.shortStatusProblemFile,'r') as f:
            self.shortStatus = f.read()
        sphinxproblems.patchhtml.processFiles(self.targetDir, self.shortStatus)






    #----- execution of sphinx --------------------------------------------------

    def _executeSphinx(self, options, outputFile, errorsFile):
        """
        General execution of sphinx. This method is used by:
        * phase #1: by _phase1ExecuteSphinxForNormalDocProduction
        * phase #3: by _phase3ExecuteSphinxForProblemDocProduction
        The options are different in each case.
        :param options: particular options depending on the phase
        :return: exit code
        """
        # config_arguments = []
        # map(config_arguments.extend,
        #    [ '-D%s=%s' % (name, value)]  for (name, value) in self.configValues] )
        # print '===',config_arguments
        additional_arguments = [
            '-T',                   # Display the full traceback when an unhandled exception occurs.
            '-b', 'html',           # Build HTML pages. This is the default builder.
            # '-d', self.docTrees,    # Directory of the doctree pickles
            '-c', self.confDir,     # Directory containing the conf.py file
            self.sourceDir,         # Source directory
            self.targetDir,         # target directory
            ]
        #arguments=config_arguments+options+additional_arguments
        arguments=options+additional_arguments
        if debug:
            print('   sphinxproblems: Executing sphinx as following')
            print(' '*8+'sphinx-build %s' % ' '.join(arguments) )
        if showOutputAndErrors:
            exit_code = sphinx.build_main(argv=arguments)
        else:
            stdout = sys.stdout
            stderr = sys.stderr
            with open(outputFile, 'w') as sys.stdout:
                with open(errorsFile, 'w') as sys.stderr:
                    exit_code = sphinx.build_main(argv=arguments)
            sys.stdout = stdout
            sys.stderr = stderr
        return exit_code



    #----- extraction of problems ----------------------------------------------------


    def _extractProblemsFromRawProblemFile(self, problemManager=None):
        """
        Extract problems from the raw problem file. Fill a problem manager
        and return it. If a problem manager is provided fill this one
        otherwise create a new one. Always returned the problem manager.
        :return: ProblemManager. Either created or completed.
        """
        if problemManager is None:
            problem_manager = sphinxproblems.problems.ProblemManager(
                    sphinxRootDirectory=self.sourceDir)
        else:
            problem_manager = problemManager
        new_problem_founds = sphinxproblems.parser.parseErrorFile(
                self.sourceDir,
                self.rawProblemFile,
                problem_manager)
        return problem_manager


    #----- generation of problems documents --------------------------------------------

    def _generateRstProblemFile(self, problemManager):
        """
        Generate the documentation of problems in RST
        :return: None
        """
        content = problemManager.summary()  # TODO: change the name of the method
        with open(self.rstProblemFile, 'w') as f:
            f.write(content)
        if debug:
            print("%s saved (%d bytes)" % (self.rstProblemFile, len(content)))

    def _generateShortStatusProblemFile(self, problemManager):
        """
        Generate the short status file with the number of errors
        :param problemManager: the problem manager to be used
        """
        content = problemManager.shortStatus()  # TODO: change the name of the method
        with open(self.shortStatusProblemFile, 'w') as f:
            f.write(content)
        if debug:
            print("%s saved (%d bytes)" % (self.shortStatusProblemFile, len(content)))


