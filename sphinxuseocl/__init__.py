"""
sphinxuseocl extension to document `USE OCL`_ project with the
sphinx documentation generator.

..  _`USE OCL`: http://scribetools.readthedocs.io/en/latest/useocl/

"""
from useocllexer import UseOCLLexer

def setup(app):
    app.add_lexer('useocl', UseOCLLexer() )
