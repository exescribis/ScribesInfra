
from useocllexer import UseOCLLexer

def setup(app):
    app.add_lexer('useocl', UseOCLLexer() )
