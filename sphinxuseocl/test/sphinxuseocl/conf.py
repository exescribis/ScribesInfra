import sys
import os.path

DOC_DIR = os.path.dirname(os.path.realpath(__file__))
MAIN_DIR = os.path.join(os.path.abspath(DOC_DIR),'..','..','..')
sys.path.insert(0, MAIN_DIR)
sys.path.insert(0, os.path.join(MAIN_DIR,'libs'))
extensions = [
    'sphinxuseocl'
]

source_suffix = '.rst'
master_doc = 'index'

import sphinx_rtd_theme
html_theme = 'sphinx_rtd_theme'
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

project = u'SandboxDB'
copyright = u'2015, (CC)(SA)(BY)escribis'
author = u'escribis'
version = '0.1'
release = '0.1'
exclude_patterns = ['.build']
default_role = 'any'
pygments_style = 'sphinx'
keep_warnings = True
nitpicky = True #  %JFE+=  Does not seems to have an effect
# html_static_path = [os.path.join(DOC_DIR,'static')]
