# coding: utf-8

"""
Generate sphinx documentation for each group and push it on the web.
Generate as well a documentation for the headquarters.
"""

import os

import sphinx
import sphinxproblems.engine

import githubbot

debug = True
showOutputAndErrors = True

RES_DIRECTORY = os.path.join(os.path.dirname(os.path.realpath(__file__)),'..','res')
assert(os.path.isdir(RES_DIRECTORY))



class ClassroomOnWebEngine(object):

    def __init__(self, classroom):
        self.classroom = classroom
        assert os.path.isdir(self.classroom.localWebGradePath()), \
            'webengine: %s directory does not exist' % self.classroom.localWebGradePath()

    def _ensureEmptyGroupDirectory(self, key):
        dir = self.classroom.localWebGroupPath(key)
        if not os.path.isdir(dir):
            print 'Creating web group directory: %s' % dir
        githubbot.ensure_empty_dir(dir)

    def _buildSphinxDocWithProblems(self, key):
        source_dir = self.classroom.localGroupRepoDirectory(key=key)
        target_dir = self.classroom.localWebGroupPath(key=key)
        team_name = self.classroom.groupTeamNamePattern().format(key=key)
        e = sphinxproblems.engine.SphinxProblemsEngine(
                source_dir,
                target_dir,
                clean=True,
                configValues=[('project',team_name)] )#('author',team_name)])
        exit_code = e.build()
        if exit_code != 0:
            print '***** ERROR with sphinx for group %s' % key

    def _generateHQDocs(self):


        def _generateHQDocsDir():
            githubbot.ensure_empty_dir(self.classroom.localHQBuildDocsDirectory())

        def _generateHQDocsConf():
            hq_docs_template_dir = os.path.join(RES_DIRECTORY, 'hq-docs-template')
            conf_template = os.path.join(hq_docs_template_dir, 'conf.py')
            conf_target = os.path.join(self.classroom.localHQBuildDocsDirectory(),'conf.py')
            with open(conf_template, 'r') as f:
                content=f.read()
            content = content.format(project=self.classroom.course)
            with open(conf_target, 'w') as f:
                f.write(content)

        def _generateHQDocsIndex():
            index_file = os.path.join(self.classroom.localHQBuildDocsDirectory(),'index.rst')
            title = self.classroom.course
            lines = [ title, '='*len(title), '']
            lines += [
                '*   `%s <%s>`_' % (key, self.classroom.webGroupURL(key))
                for key in self.classroom.groupList.keys()
                if key != '00'
            ]
            with open(index_file, 'w') as f:
                f.write('\n'.join(lines))


        def _sphinxHQDocs():
            """
            Execute sphinx to generate html file for HQ documentation.
            """
            source = self.classroom.localHQBuildDocsDirectory()
            target = self.classroom.localWebHQPath()
            arguments = [
                '-T',
                '-q',
                '-b', 'html',
                '-d', os.path.join(target,'.doctrees'),
                '-c', source,
                source,
                target,
                ]
            exit_code = sphinx.build_main(argv=arguments)
            return exit_code

        _generateHQDocsDir()
        _generateHQDocsConf()
        _generateHQDocsIndex()
        _sphinxHQDocs()




    def _commitAndPushWeb(self):
        cmd_patterns = [
            'git -C {localwebrepodir} add .',
            'git -C {localwebrepodir} commit --quiet -a -m "add new sphinx build"',
            'git -C {localwebrepodir} push --quiet origin master'
        ]
        dir = self.classroom.localWebRepoDirectory()
        for cmd_pattern in cmd_patterns:
            cmd = cmd_pattern.format(localwebrepodir=dir)
            exit_code = os.system(cmd)
            if exit_code != 0:
                print '***** ERROR %s while executing:\n  %s' % (exit_code,cmd)

    def generateGroupDocs(self, key):
        self._ensureEmptyGroupDirectory(key=key)
        self._buildSphinxDocWithProblems(key=key)

    def generateAllGroupDocs(self):
        for key in self.classroom.groupList.keys():
            self.generateGroupDocs(key)

    def generatedHQDocs(self):
        self._generateHQDocs()

    def publishAllDocs(self):
        self._commitAndPushWeb()

    def build(self):
        self.generateAllGroupDocs()
        self.generatedHQDocs()
        self.publishDocs()




