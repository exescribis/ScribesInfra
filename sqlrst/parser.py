# coding=utf-8

"""
Take a SQL text with some RST comments and convert it to a sequence
of blocks according to the module :module:`structure`.
"""

import re

import sqlparse

import sqlrst.structure

__all__ = ('sqlRstToBlockSequence',)

def sqlSplit(sqlText):
    return sqlparse.split(sqlText)

BLOCK_COMMENT_RE = '/\*.*?\*/'
BLOCK_COMMENT_BLOCK = \
    r'^(?P<before>\s*)(?P<comment>/\*.*?\*/)(?P<after>\s*\n|$)(?P<rest>.*)'
LINES_COMMENT_BLOCK = \
    r'^(?P<before>\s*)(?P<comment>(?:--[^\n]*(?:\n|$))+)(?P<after>\s*)(?P<rest>.*)'
# SPACES_AND_LINE_COMMENT = '\s*(?P<comment>--[^\n]*(\n|$))(?P<rest>.*)'
CREATE_TABLE_RE = r'\s*CREATE\s+(?:\w+\s*)?TABLE\s*(?:IF\s+NOT\s+EXISTS\s+)?(?P<name>\w+)'
CREATE_VIEW_RE = r'\s*CREATE\s+(?:\w+\s*)?VIEW\s+(?P<name>\w+)'
SELECT_RE = r'\s*SELECT\s'

# match something like:
# ..  table:: MyTable(a:e, c:e?,

SQL_NAME_PATTERN = r'CREATE\s+(VIEW|TABLE)\s+(?P<name>\w+)'


DIRECTIVE_NAME = \
    r'\s*\.\.\s+(?:sql:)?(?:table|query|view)::\s*' \
    r'(?P<name>\w+)\s*'
SQL_DIRECTIVE = \
    r'(?:\n|^)(?P<indent>\s*)\.\.\s+(?:sql:)?(?P<kind>table|query|view)::\s*' \
    r'(?P<name>\w+)\s*' \
    r'(?:\((?P<signature>[\w\s,:#\?>]*)\))?\s*(?:\n|$)'
SQL_DIRECTIVE_NAME_INDEX = re.findall(r'\(\?P<(\w+)>',SQL_DIRECTIVE).index('name')

ARGUMENT = \
    r'\n(?P<indent>\s*):(?P<kind>col|column|con|constraints)\s*' \
    r'(?P<signature>[^:]+)\:' \
    r'(?P<rest>[^\n]*)(?:\n|$)'

def sqlRstToBlockSequence(sqlText):

    def __tryMatchCommentBlock(text):
        """
        :param text: the text to parse
        :return: (CommentBlock|None,str). The block matched and the rest
            of the string or None and the text.
        """
        m = re.match(BLOCK_COMMENT_BLOCK, text, re.MULTILINE | re.DOTALL)
        if m:
            return (
                structure.BlockCommentBlock(
                    m.group('comment'), m.group('before'), m.group('after')),
                m.group('rest') )
        m = re.match(LINES_COMMENT_BLOCK, text, re.MULTILINE | re.DOTALL)
        if m:
            return (
                structure.LinesCommentBlock(
                    m.group('comment'), m.group('before'), m.group('after')),
                m.group('rest') )
        return (None, text)

    def __doMatchSQLStatement(text):
        m = re.match(CREATE_TABLE_RE+'.*', text,  re.IGNORECASE)
        if m:
            return(
                structure.CreateTableStatementBlock(text, name=m.group('name'))
            )
        m = re.match(CREATE_VIEW_RE+'.*', text,  re.IGNORECASE)
        if m:
            return(
                structure.CreateViewStatementBlock(text, name=m.group('name'))
            )
        m = re.match(SELECT_RE+' *(/\*: *(?P<name>[\w\.]+) *\*/)?.*', text,  re.IGNORECASE)
        if m:
            if m.group('name') is None:
                name = None
            else:
                name = m.group('name')
            return(
                structure.SelectStatementBlock(text, name=name)
            )
        return structure.UnknownStatementBlock(text)

    blocks = []
    # Split the text in (comments* +sqlstatement restofline) segments.
    # Spaces+lines before comments are removed, spaces after blocks
    # are removed. some blank lines may disappear in the process.
    segments = sqlparse.split(sqlText)

    # Process each segment as they still may contains some comments
    # additionaly to one (or more?) sql statements
    for segment in segments:

        rest = segment

        # try to get all comments before the sql statement(s?)
        (comment_block, rest) = __tryMatchCommentBlock(rest)
        while comment_block is not None : #and not re.match('\s*',rest, re.MULTILINE):
            blocks.append(comment_block)
            (comment_block, rest) = __tryMatchCommentBlock(rest)

        # a priori there is just one remaining sql block,
        # but just to be sure...
        stmt_texts = sqlparse.split(rest)
        for stmt_text in stmt_texts:
            blocks.append(__doMatchSQLStatement(stmt_text))

    return blocks

