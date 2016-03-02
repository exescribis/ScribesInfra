# coding=utf-8

"""
Pygment lexer for `USE OCL`_.

..  _`USE OCL`:
    https://sourceforge.net/projects/useocl/
"""

from pygments.lexer import RegexLexer, words
from pygments.token import *


class UseOCLLexer(RegexLexer):
    """
    Lexer for Structured Query Language. Currently, this lexer does
    not recognize any special syntax except ANSI SQL.
    """

    name = 'useocl'
    aliases = ['useocl']
    filenames = ['*.use','*.soil', '*.con']
    mimetypes = ['text/x-useocl']

    tokens = {
        'root': [
            (r'\s+', Text),
            (r'--.*?\n', Comment.Single),
            (r'/\*', Comment.Multiline, 'multiline-comments'),

            (words((
                    'abstract','aggregation','association','associationclass','begin',
                    'class','composition','constraints','context','end','enum',
                    'model',
                    'operations',
                    'statemachines'
                ), suffix=r'\b'),
             Keyword.Declaration),

            (words((
                    'attributes','between',
                    'derived','do','else','endif','enum',
                    'for','if','in','init','inv','let',
                    'ordered','post','pre','psm','qualifier','redefines','role',
                    'states','subsets','then','transitions'
                ), suffix=r'\b'),
             Keyword.Declaration),

            (words((
                'Bag','Boolean','Collection','Integer','OrderedSet','Real','Sequence','Set','String','TupleType'
                ), suffix=r'\b'),
             Keyword.Type),

            (words((
                'Tuple','allInstances','and','any','append','asBag','asOrderedSet','asSequence','asSet','at',
                'characters','closure','collecNested','collect','concat','count','div','equalsIgnoreCase','excludes',
                'excludesAll','excluding','exists','false','first','flatten','floor','forAll','forall','implies',
                'includes','includesAll','including','indexOf','insertAt','intersection','isEmpty','isUnique',
                'iterate','last','max','min','mod','not','notEmpty','oclAsType','oclIsInState','oclIsKindOf',
                'oclIsNew','oclIsTypeOf','one','or','prepend','product','reject','reverse','result','round','select',
                'selectByKind','selectByType','self','size','sortedBy','subOrderedSet','subSequence','substring',
                'sum','symmetricDifference','toBoolean','toInteger','toLowerCase','toReal','toString','toUpperCase',
                'true','union','xor'
                ), suffix=r'\b'),
              Name.Entity),

            (words((
                'ReadInteger','ReadLine','Write','WriteLine','between','create','declare','delete','destroy','from','insert','into','new'
                )),
             Keyword),

            # < > <= >= <> = :=    + * - /   @  ? !

            (r'(->|<=|>=|<|>|<>|=|:=|\+|\*|-|/|@)', Name.Entity),
            ('!|\?', Generic.Strong),
            ('\.', Operator.Word),
            (r'[0-9]+', Number),
            (r"'(''|[^'])*'", String.Single),
            (r'[A-Z]\w*', Name.Exception),
            (r'[a-z]\w*', Name.Attribute),
            (r'[;.:|()\[\]{},]', Punctuation)
        ],
        'multiline-comments': [
            (r'/\*', Comment.Multiline, 'multiline-comments'),
            (r'\*/', Comment.Multiline, '#pop'),
            (r'[^/*]+', Comment.Multiline),
            (r'[/*]', Comment.Multiline)
        ]
    }