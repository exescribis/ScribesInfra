# -*- coding: utf-8 -*-
project = u'CyberCompetition'
copyright = u'2016, (CC)(SA)(BY) UFRIMAG'
author = u'M2CCI'
version = '0.1'
release = '0.1'

import sys
import os.path

DOC_DIR = os.path.dirname(os.path.realpath(__file__))
CONF_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_DIR = os.path.join(CONF_DIR,'..','..')
TOP_PROJECTS_DIR = os.path.realpath(os.path.join(PROJECT_DIR,'..','..','..','..'))
SCRIBES_INFRA_DIR = os.path.realpath(os.path.join(TOP_PROJECTS_DIR,'ScribesInfra'))
SPHINX_ZONE_DIR = os.path.realpath(os.path.join(TOP_PROJECTS_DIR,'SphinxZone'))

if os.path.exists(SPHINX_ZONE_DIR):
    pass # print 'SphinxZone found'
else:
    if not os.path.isdir(SCRIBES_INFRA_DIR):
        print 'FATAL ERROR: directory %s does not exist' % SCRIBES_INFRA_DIR
        print '             You can try to install ScribesInfra as following:'
        print '             (1) cd %s' % TOP_PROJECTS_DIR
        print '             (2) git clone https//github.com/ScribesZone/ScribesInfra.git'
        print '             (3) you can try again.'
        raise EnvironmentError('ScribesInfra not found. See message above.')

path_dirs = [
    '.',
    CONF_DIR,
    SCRIBES_INFRA_DIR,
    os.path.join(SCRIBES_INFRA_DIR,'libs'),
    SPHINX_ZONE_DIR,
    os.path.join(SPHINX_ZONE_DIR,'libs'),
    ]

for dir in path_dirs:
    if os.path.isdir(dir):
        sys.path.insert(0, dir)

extensions = [
    # 'sphinxuseocl',
    # 'sphinxproblems',
    # 'sphinxgithub',
    # 'sphinx_git',
    # 'sphinxdata',
    'sphinxxrefs',
    # 'sphinxse',
    # 'sphinx.ext.intersphinx',
    # 'sphinx.ext.todo',
    #'sphinx.ext.viewcode',
]

templates_path = [DOC_DIR+os.sep+'templates']
source_suffix = '.rst'
master_doc = 'index'
language = 'fr'
exclude_patterns = [
    'README.rst',
    'CONTRIBUTORS.rst',
    'References/Glossaires.rst',
    '**/.build/*.generated.rst',
    ]
default_role = 'any'
show_authors = False
pygments_style = 'sphinx'
keep_warnings = True
nitpicky = True #  %JFE+=  Does not seems to have an effect


# -- Options for HTML output ----------------------------------------------
html_static_path = [os.path.join(CONF_DIR, 'static')]


# on_rtd is whether we are on readthedocs.org
on_rtd = os.environ.get('READTHEDOCS', None) == 'True'
local = not on_rtd
if local:
    tags.add('local')
else:
    tags.add('rtd')
    tags.add('RTD')
    tags.add('ReadTheDocs')
todo_include_todos = local
web = on_rtd
if local:  # only import and set the theme if we're building docs locally
    import sphinx_rtd_theme

    html_theme = 'sphinx_rtd_theme'
    html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
    #local = True
#     #web = False
#     rst_prolog = """
# .. |L| replace::
#     local
# """
# else:
#     rst_prolog = """
# .. |L| replace::
#
# """

htmlhelp_basename = project

# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {'https://docs.python.org/': None}
