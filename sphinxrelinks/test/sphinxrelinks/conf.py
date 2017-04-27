import sys
import os.path

DOC_DIR = os.path.dirname(os.path.realpath(__file__))
MAIN_DIR = os.path.join(os.path.abspath(DOC_DIR),'..','..','..')
sys.path.insert(0, MAIN_DIR)
sys.path.insert(0, os.path.join(MAIN_DIR,'libs'))
extensions = [
    'sphinxrelinks'
]


# TODO: this list should be checked and consolidated
sphinxrelinks = {

    # links to github objects
    'gh_user': (
        'https://github.com/{0}',
        '{0}'
    ),
    'gh_org': (
        'https://github.com/{0}',
        '{0}'
    ),
    'gh_team': (
        'https://github.com/orgs/{0}/teams/{1}',
        '{1}'
    ),
    'gh_repo': (
        'https://github.com/{0}/{1}',
        '{0}/{1}'
    ),
    'gh_wiki': (
        'https://github.com/{0}/{1}/wiki',
        '{0}/{1} wiki'
    ),
    'gh_repo_history': (
        'https://github.com/{0}/{1}/commits/master',
        '{0}/{1}'
    ),
    'gh_commit': (
        'https://github.com/{0}/{1}/commits/{2}',
        '{2}'
    ),
    'gh_branches': (
        'https://github.com/{0}/{1}/branches',
        '{0}/{1} branches'
    ),
    'gh_all_branches': (
        'https://github.com/{0}/{1}/branches/all',
        'all {0}/{1} branches'
    ),
    'gh_active_branches': (
        'https://github.com/{0}/{1}/branches/active',
        '{0}/{1} active branches'
    ),
    'gh_stale_branches': (
        'https://github.com/{0}/{1}/branches/active',
        '{0}/{1} stale branches'
    ),
    'gh_file': ( #FIXME: this will not work currenly as paths with / will be splitted and {2} yield only 1st component
        'https://github.com/{0}/{1}/blob/master/{2}',
        '{2}'
    ),
    # could add a parameter for the branch
    'gh_history': (
        'https://github.com/{0}/{1}/blob/master/{2}',
        '{2}'
    ),
    'gh_tags': (
        'https://github.com/{0}/{1}/tags',
        'tags'
    ),
    'gh_releases': (
        'https://github.com/{0}/{1}/releases',
        'releases'
    ),
    'gh_release': (
        'https://github.com/{0}/{1}/releases/tag/{2}',
        'release #{2}'
    ),
    'gh_zip_archive': (
        'https://github.com/{0}/{1}/archives/{2}.zip',
        '{2}.zip'
    ),
    'gh_tgz_archive': (
        'https://github.com/{0}/{1}/archives/{2}.tar.gz',
        '{2}.tar.gz'
    ),
    'gh_issue': (
        'https://github.com/{0}/{1}/issues/{2}',
        'issue #{2}'
    ),
    'gh_pr': (
        'https://github.com/{0}/{1}/issues/{2}',
        'pull request #{2}'
    ),
    'gh_label': (
        'https://github.com/{0}/{1}/labels/{2}',
        '{2}'
    ),
    'gh_milestone': (
        'https://github.com/{0}/{1}/milestone/{2}',
        '{2}'
    )   ,
    'gh_project': (
        'https://github.com/{0}/{1}/projects/{2}',
        'project #{2}'
    ),

    # links to readthedocs

    'rtfd_project': (
        'http://{0}.readthedocs.io/en/latest/index.html',
        '{0}'
    ),
    # TODO the structure of the project are not regular. The pash should be given
    # but this is not supported currently because separator is /
    # additionnaly one should add someway to express #xxx stuff
    'rtfd_page': (
        'http://{0}.readthedocs.io/en/latest/{1}.html',
        '{1}'
    ),



    # links to scribes quality documentation

    'sq_package': (
        'http://scribesquality.readthedocs.io/en/latest/packages/{0}.html',
        '{0} package'
    ),
    'sq_rule': (
        'http://scribesquality.readthedocs.io/en/latest/packages/{0}.html#{1}',
        '{0}/{1} rule'
    ),

    # links to scribes tool documentation

    'st_tool': (
        'http://scribestools.readthedocs.io/en/latest/{0}/index.html',
        '{0}'
    ),
    'st_tool_section': (
        'http://scribestools.readthedocs.io/en/latest/{0}/index.html#{1}',
        '{1}'
    ),



}




source_suffix = '.rst'
master_doc = 'index'

import sphinx_rtd_theme
html_theme = 'sphinx_rtd_theme'
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

project = u'sphinxrelinks'
copyright = u'2017, (CC)(SA)(BY)escribis'
author = u'escribis'
version = '0.1'
release = '0.1'
exclude_patterns = ['.build']
default_role = 'any'
pygments_style = 'sphinx'
keep_warnings = True
nitpicky = True #  %JFE+=  Does not seems to have an effect
# html_static_path = [os.path.join(DOC_DIR,'static')]
