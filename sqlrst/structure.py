# coding=utf-8

"""
Describe the abstract syntax tree of a sql file.
The file is decomposed in a sequence of blocks.
Named blocks have name.

    Block
        CommentBlock
            BlockCommentBlock   /* ... */
            LinesCommentBlock   --
        SQLStatementBlock
            SelectStatementBlock
            CreateTableStatementBlock  < NamedBlock
            CreateViewStatementBlock   < NamedBlock
            UnknownStatementBlock
"""

import re



class Block(object):

    def __init__(self):
        pass

    def text(self):
        pass

    def content(self):
        return self.text()


class CommentBlock(Block):

    def __init__(self, comment, before='', after=''):
        super(CommentBlock, self).__init__()
        self.before = before
        self.comment = comment
        self.after = after

    def content(self):
        pass

    def text(self):
        return self.before+self.comment+self.after

class BlockCommentBlock(CommentBlock):
    def __init__(self, comment, before='', after=''):
        super(BlockCommentBlock, self).__init__(comment, before, after)

    def content(self):
        return \
            re.sub('\*/\s*','',
               re.sub('\s*/\*','',self.comment))

class LinesCommentBlock(CommentBlock):
    def __init__(self, comment, before='', after=''):
        super(LinesCommentBlock, self).__init__(comment,before,after)

    def content(self):
        lines = self.comment.split('\n')
        _ = []
        for l in lines:
            l = re.sub(r'^[\t ]*-- ?', '', l)
            _.append(l)
        return '\n'.join(_)

class SQLStatementBlock(Block):

    def __init__(self, sqlText):
        Block.__init__(self)
        self.sqlText = sqlText

    def text(self):
        return self.sqlText

class NamedBlock(Block):

    def __init__(self, name):
        Block.__init__(self)
        self.name = name

class SelectStatementBlock(SQLStatementBlock, NamedBlock):
    def __init__(self, sqlText, name=None):
        NamedBlock.__init__(self, name)
        super(SelectStatementBlock, self).__init__(sqlText)

class CreateTableStatementBlock(SQLStatementBlock, NamedBlock):
    def __init__(self, sqlText, name):
        NamedBlock.__init__(self, name)
        SQLStatementBlock.__init__(self, sqlText)

class CreateViewStatementBlock(SQLStatementBlock, NamedBlock):
    def __init__(self, sqlText, name):
        NamedBlock.__init__(self, name)
        super(CreateViewStatementBlock, self).__init__(sqlText)


class UnknownStatementBlock(SQLStatementBlock):

    def __init__(self, sqlText):
        super(UnknownStatementBlock, self).__init__(sqlText)


