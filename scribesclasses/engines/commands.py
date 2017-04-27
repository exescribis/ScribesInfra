# coding: utf-8

"""
Transform "template scripts" into expanded scripts containing
everything for all the group for a given classroom.
The template is instanciated for each classroom allowing
further manual customization, commenting, etc if required.
"""

import os

import githubbot


class ClassroomCommandsEngine(object):
    """
    Engine allowing to generate commands for classrooms from templates.
    The templates are processed by the `substitute` method of the `Classroom` class.
    The scripts can be either defined in files or as piece of text passed as parameter.
    'System' templates are defined in the ``scribesclass/res/commands`` directory
    but a user ``.commands`` directory can be specified.
    The `buildScript` method build a script and save it in the ``localHQBuildCommandsDirectory``
    of the headquarters.
    """

    def __init__(self, classroom):
        self.classroom = classroom

        #: Directory containing default script templates,
        #: These are stored in templates directory in this package.
        self.systemDirectory = os.path.join(
                os.path.join(os.path.dirname(os.path.realpath(__file__)),'..'),
                'res',
                'commands')

        #: Source directory for the classroom
        self.classroomSourceDirectory = classroom.localHQSourceCommandsDirectory()

        #: Sarget directory for the classroom
        self.classroomBuildDirectory = classroom.localHQBuildCommandsDirectory()


    def scriptTemplate(self, filename):
        """
        Return the absolute path to a script searching first in the
        classroom template directory and then in the system directory.
        :param filename: the filename of the template.
        :return: The absolute path to the script template.
        :raises: ValueError if the script template is not found.
        """
        #: search first in user directory
        if self.classroomSourceDirectory:
            f = os.path.join(self.classroomSourceDirectory, filename)
            if os.path.isfile(f):
                return f
        #: otherwise search in system directory
        f = os.path.join(self.systemDirectory, filename)
        if os.path.isfile(f):
            return f
        else:
            raise ValueError('template command %s not found' % filename )


    def scriptTemplates(self):
        """
        List of all templates in the classroom directory and system directories.
        The templates in classroom directory (if any) take precedence over the
        templates with the same name (if any) in the system directory.
        :return: list[str] list of template full path
        """

        def _filesAndPaths(directory):
            return { f : os.path.join(directory, f)
                     for f in os.listdir(directory)
                     if os.path.isfile(os.path.join(directory, f))}

        files_and_paths = _filesAndPaths(self.systemDirectory)
        if self.classroomSourceDirectory:
            files_and_paths.update(_filesAndPaths(self.classroomSourceDirectory))
        return files_and_paths.values()



    def buildScript(self,
                    scriptPattern=None, scriptFile=None,  # either scriptPattern or scriptFile
                    key=None, accountInfo=None, substs=None,
                    save = True,
                    stripLines=True):
        """
        Create a script from a given text (scriptPattern) or from a template file. The template
        is repeated for all the group specified.
        :param scriptPattern: str|None. A text to be used as a template or none if scriptFile is defined.
            This parameter must be None if scriptFile is used instead.
        :param scriptFile: str|None. A name of a script template to be searched in the system or user directory.
            This parameter must be None if the scriptPattern parameter is used instead.
        :param key: str|None. If a string is given this will be the group key and the script will be generated
            only for this group. If None is provide all the script will consider all groups, that is all the
            keys of all groups in the classroom.
        :param accountInfo: The github account used to generate the url or the default if None.
        :param substs: Additional substitutions that must take place.
        :param save: If true the template is saved in the classroom script directory. This is the default.
            If a script file was given, the same name is used. If a text was used as a scriptPattern then
            'script.sh' will be generated.
        :param stripLines: Indicates if lines should be strip during script generation.
        :return: None
        """
        if scriptPattern is None and scriptFile is None:
            raise Exception('Either scriptPattern or scriptFile must be set')

        if scriptFile is not None:
            # read scriptPattern from file
            filename = self.scriptTemplate(scriptFile)
            with open(filename,'r') as f:
                scriptPattern = f.read()
        else:
            # use a default name
            scriptFile  = 'script.sh'
            # scriptPattern is not changed, since it contains the pattern

        # define the keys: the one specified or all the group keys
        if key is None:
            keys = self.classroom.groupList.keys()
        else:
            keys = [key]

        # concatenate the template for all groups
        _ = ''
        for key in keys:
            text =  self.classroom.substitute(
                scriptPattern,
                key=key, accountInfo=self.classroom.account(accountInfo), substs=substs)
            text = '\n'.join([line.strip() for line in text.split('\n')])
            _ += text + '\n\n'

        if not save:
            print _
        else:
            githubbot.ensure_dir(self.classroomBuildDirectory)
            filename = os.path.join(self.classroomBuildDirectory,
                                    os.path.basename(scriptFile)).replace('.sh','-all.sh')
            print 'Generating %s' % filename
            with open(filename,'w') as f:
                f.write(_)



    def build(self, arguments=(), accountInfo=None, substs=None ):
        """
        Generate the all scripts from this script engine. All templates in classroom and system directory
        are used (unless overloading) and generate a script with the same name in the classroom .build directory.
        """
        for script in self.scriptTemplates():
            self.buildScript(scriptFile=script, accountInfo=self.classroom.account(accountInfo), substs=substs)