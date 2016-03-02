import os

def touchFile(file, times=None):
    with open(file, 'a'):
        os.utime(file, times)

def getHTMLBuildDirectory(app):
    return

def addNoJekyll(app):
    """
    Add a .jekyll in the outfile for githubpages

    Here we assume that we generate the html for a private repository.
    In this case the directory is with a code name and .nojekyll should be
    on the top directory (hence the ``..`` parent directory below)

    See https://github.com/sphinx-doc/sphinx/blob/master/sphinx/ext/githubpages.py

    :param app: the sphinx app
    """
    touchFile(os.path.join(app.builder.outdir,'..','.nojekyll'))