from pygments.lexer import RegexLexer
from pygments.token import *

class RelationalAlgebraLexer(RegexLexer):
    name = 'RelationalAlgebra'
    aliases = ['relation_algebra']
    filenames = ['*.ra']

    tokens = {
        'root': [
            (r'--.*?\n', Comment.Singleline),
            (r'\'[^\']*\'', String.Single),
            (r'\"[^"]*"', String.Double),
            (r'\d+', Number.Integer),
            (r'[A-Z][A-Za-z0-9_]+', Name.Class),
            (r'[a-z][A-Za-z0-9_]+', Name.Attribute),
            (r':=', Operator),
            (r'[[\](){}<>,:nu\-=.\*x/]', Operator),
            (r'\s+', Whitespace),
        ]
    }